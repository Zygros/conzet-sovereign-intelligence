import { createServer } from "node:http";
import { readFile, writeFile } from "node:fs/promises";
import { OAuth2Client } from "google-auth-library";
import open from "open";

const credentials = JSON.parse(await readFile(new URL("../credentials.json", import.meta.url), "utf8"));
const installed = credentials.installed ?? credentials.web;
if (!installed?.client_id || !installed?.client_secret) {
  throw new Error("credentials.json must contain an OAuth client_id and client_secret.");
}
const redirectUri = "http://127.0.0.1:53682/oauth2callback";
const oauth = new OAuth2Client(installed.client_id, installed.client_secret, redirectUri);
const scopes = ["https://www.googleapis.com/auth/drive.readonly"];
const authUrl = oauth.generateAuthUrl({ access_type: "offline", prompt: "consent", scope: scopes });

const server = createServer(async (req, res) => {
  const url = new URL(req.url ?? "/", redirectUri);
  if (url.pathname !== "/oauth2callback") {
    res.writeHead(404).end("Not found");
    return;
  }
  const code = url.searchParams.get("code");
  if (!code) {
    res.writeHead(400).end("Missing authorization code. Return to the terminal and retry.");
    return;
  }
  try {
    const { tokens } = await oauth.getToken(code);
    await writeFile(new URL("../token.json", import.meta.url), JSON.stringify(tokens, null, 2), { mode: 0o600 });
    res.writeHead(200, { "content-type": "text/plain; charset=utf-8" }).end("Authorization saved locally. You may close this tab.");
    console.log("OAuth token saved to token.json. Keep it private and untracked.");
  } catch (error) {
    console.error(error);
    res.writeHead(500).end("OAuth exchange failed. Check the terminal output.");
  } finally {
    setTimeout(() => server.close(), 1000);
  }
});
server.listen(53682, "127.0.0.1", async () => {
  console.log("Opening Google authorization page. If it does not open, visit this URL:\n" + authUrl);
  try { await open(authUrl); } catch { /* URL is printed above for manual opening. */ }
});
