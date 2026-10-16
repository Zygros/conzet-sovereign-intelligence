# Android / Termux Activation Guide

This connector is designed to be runnable from an Android phone with Termux. No desktop computer is required, although Google's OAuth screens and Android file handling can vary by device.

## 1. Prepare Termux

Install Termux from its official F-Droid or GitHub distribution, then open it and run:

```sh
pkg update && pkg upgrade
pkg install nodejs git
termux-setup-storage
```

Accept Android's storage permission prompt. This lets Termux read a downloaded credentials file from shared storage.

## 2. Get the repository

```sh
git clone https://github.com/Zygros/conzet-sovereign-intelligence.git
cd conzet-sovereign-intelligence/connectors/google-drive
npm install
npm run typecheck
```

If you already cloned the repository, use `cd` to enter your existing checkout rather than cloning a second copy.

## 3. Create Google OAuth credentials in your phone browser

1. Open https://console.cloud.google.com/ in Chrome.
2. Select or create a Google Cloud project.
3. Enable the Google Drive API.
4. Configure the OAuth consent screen. If the app is in Testing, add the Google account you intend to authorize as a test user.
5. Create an OAuth client ID with application type **Desktop app**.
6. Download the JSON file. Do not paste its contents into chat or commit it to Git.

In Termux, copy the downloaded file into the connector directory. The usual Android Downloads path is:

```sh
cp ~/storage/downloads/client_secret_*.json ./credentials.json
```

If the downloaded filename differs, run `ls ~/storage/downloads` and use the exact filename. If the download is not visible there, use Android's Files app to move it into Termux's shared Downloads directory, then copy it from Termux.

Verify that the file exists without printing its secret contents:

```sh
test -s credentials.json && echo "OAuth credentials file found"
```

## 4. Authorize Drive

Run:

```sh
npm run auth
```

The command prints a Google authorization URL. Open that URL in Chrome if Termux does not open it automatically, select the intended Google account, and grant the requested read-only Drive permission.

The app listens on `127.0.0.1:53682` for Google's redirect. Because this is an Android loopback flow, keep Termux running while authorizing. If the redirect fails, do not repeatedly approve or share any authorization code. Capture the non-secret terminal error and troubleshoot the callback configuration first.

The token is saved locally to `token.json`, which is excluded from Git. Do not upload or share it.

## 5. Start the connector

```sh
npm run dev
```

This starts an MCP server over standard input/output. It is not, by itself, a user-facing Drive browser; an MCP-compatible client must connect to the process to call its tools. Do not assume ChatGPT has connected to this local process just because the server starts.

## Security and verification

- The requested scope is read-only: `https://www.googleapis.com/auth/drive.readonly`.
- Never commit `credentials.json` or `token.json`.
- Do not publish a Drive inventory, filenames, folder paths, or file contents.
- A successful OAuth callback proves authorization was saved; it does not by itself prove listing, file reading, complete inventory, or independent manifest verification.
- Confirm each stage separately: TypeScript check, OAuth callback, Drive API list request, paginated inventory, and manifest verification.
- If a command fails, share only the error message after removing email addresses, tokens, authorization codes, and private file names.
