# Conzetian Google Drive Connector

A user-owned, read-only Google Drive MCP connector starter for Conzetian manifesting. This is separate from ChatGPT's admin-controlled Google Drive connector.

## Security
- Requests only the read-only Drive scope: `https://www.googleapis.com/auth/drive.readonly`.
- OAuth credentials and tokens are local files and excluded from Git.
- Uses MCP over stdio; it does not expose a public HTTP server.
- The tools do not create, move, or delete Drive items.
- Treat file names and folder paths as private metadata. Keep manifests containing personal Drive structure out of public repositories.

## Prerequisites
- Node.js 20+
- A Google Cloud project with the Google Drive API enabled
- OAuth consent configured for the account that owns the Drive
- OAuth client credentials created for a Desktop app

## Setup
1. In Google Cloud Console, enable the Google Drive API.
2. Configure the OAuth consent screen. If the app is in Testing, add the intended Google account as a test user.
3. Create an OAuth client ID of type **Desktop app** and download its JSON.
4. Save the file as `credentials.json` in this directory. Never commit it.
5. Run `npm install`.
6. Run `npm run auth`, open the printed Google authorization URL if a browser does not open, and grant read-only Drive access. The resulting `token.json` remains local and untracked.
7. Run `npm run dev` to start the MCP server over stdio.

## MCP tools
- `drive_list_files`: paginated metadata listing with an optional Drive API query.
- `drive_get_file`: metadata for one file ID.
- `drive_read_text_file`: reads a text file or exports a Google Doc as plain text.
- `drive_manifest_page`: returns a metadata page for the private manifest.

## Current status
Source files have been committed, but this connector has not been run or authenticated against the user's Google account. It does not bypass ChatGPT's connector policy. Google Docs export and arbitrary binary file decoding may need additional handling. Verify dependencies and run `npm run typecheck` before relying on it.