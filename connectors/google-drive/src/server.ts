import { readFile } from "node:fs/promises";
import { google } from "googleapis";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { isReadableTextMimeType } from "./content-type.js";

const credentials = JSON.parse(await readFile(new URL("../credentials.json", import.meta.url), "utf8"));
const token = JSON.parse(await readFile(new URL("../token.json", import.meta.url), "utf8"));
const installed = credentials.installed ?? credentials.web;
// googleapis typechecks against the OAuth client it bundles. Importing
// OAuth2Client from the direct google-auth-library dependency is a second
// class (it is missing methods the bundled client has) and fails `tsc`.
const oauth = new google.auth.OAuth2(installed.client_id, installed.client_secret, "http://127.0.0.1:53682/oauth2callback");
oauth.setCredentials(token);
const drive = google.drive({ version: "v3", auth: oauth });
const server = new McpServer({ name: "conzetian-google-drive-readonly", version: "0.1.0" });

const safeFile = (f: any) => ({
  id: f.id, name: f.name, mimeType: f.mimeType, modifiedTime: f.modifiedTime,
  createdTime: f.createdTime, size: f.size, parents: f.parents,
  webViewLink: f.webViewLink, trashed: f.trashed, md5Checksum: f.md5Checksum
});

server.tool("drive_list_files", "List Drive files using a read-only query. Returns metadata only.", {
  query: z.string().optional().describe("Optional Google Drive API q expression, for example trashed = false"),
  pageSize: z.number().int().min(1).max(1000).optional(),
  pageToken: z.string().optional()
}, async ({ query, pageSize, pageToken }) => {
  const result = await drive.files.list({
    q: query ?? "trashed = false",
    pageSize: pageSize ?? 100,
    pageToken,
    orderBy: "name",
    fields: "nextPageToken,files(id,name,mimeType,modifiedTime,createdTime,size,parents,webViewLink,trashed,md5Checksum)"
  });
  return { content: [{ type: "text", text: JSON.stringify({ files: (result.data.files ?? []).map(safeFile), nextPageToken: result.data.nextPageToken ?? null }, null, 2) }] };
});

server.tool("drive_get_file", "Get metadata for one Drive file ID.", {
  fileId: z.string().min(1)
}, async ({ fileId }) => {
  const result = await drive.files.get({ fileId, fields: "id,name,mimeType,modifiedTime,createdTime,size,parents,webViewLink,trashed,md5Checksum,description" });
  return { content: [{ type: "text", text: JSON.stringify(safeFile(result.data), null, 2) }] };
});

server.tool("drive_read_text_file", "Read a text file or export a Google Doc as plain text. Large content may be truncated by the caller.", {
  fileId: z.string().min(1),
  maxCharacters: z.number().int().min(1).max(200000).optional()
}, async ({ fileId, maxCharacters }) => {
  const meta = await drive.files.get({ fileId, fields: "id,name,mimeType" });
  const mime = meta.data.mimeType ?? "";
  let text: string;
  if (mime === "application/vnd.google-apps.document") {
    const response = await drive.files.export({ fileId, mimeType: "text/plain" }, { responseType: "text" });
    text = String(response.data);
  } else {
    if (!isReadableTextMimeType(mime)) {
      throw new Error(
        `drive_read_text_file only reads text content and Google Docs; file ${fileId} has unsupported MIME type: ${mime || "unknown"}`
      );
    }
    const response = await drive.files.get({ fileId, alt: "media" }, { responseType: "text" });
    text = String(response.data);
  }
  const limit = maxCharacters ?? 50000;
  return { content: [{ type: "text", text: JSON.stringify({ id: fileId, name: meta.data.name, mimeType: mime, truncated: text.length > limit, content: text.slice(0, limit) }, null, 2) }] };
});

server.tool("drive_manifest_page", "Return one metadata page suitable for a private manifest. Does not write, move, or delete Drive items.", {
  pageSize: z.number().int().min(1).max(1000).optional(),
  pageToken: z.string().optional(),
  query: z.string().optional()
}, async ({ pageSize, pageToken, query }) => {
  const result = await drive.files.list({
    q: query ?? "trashed = false",
    pageSize: pageSize ?? 500,
    pageToken,
    orderBy: "name",
    fields: "nextPageToken,files(id,name,mimeType,modifiedTime,createdTime,size,parents,trashed,md5Checksum)"
  });
  const files = (result.data.files ?? []).map(safeFile);
  return { content: [{ type: "text", text: JSON.stringify({ generatedAt: new Date().toISOString(), count: files.length, files, nextPageToken: result.data.nextPageToken ?? null, writeOperationsPerformed: false }, null, 2) }] };
});

await server.connect(new StdioServerTransport());
