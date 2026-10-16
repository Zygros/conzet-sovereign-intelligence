const TEXTUAL_APPLICATION_MIME_TYPES = new Set([
  "application/json",
  "application/ld+json",
  "application/xml",
  "application/yaml",
  "application/x-yaml",
  "application/javascript",
  "application/typescript",
  "application/x-www-form-urlencoded"
]);

export function isReadableTextMimeType(mimeType: string): boolean {
  return mimeType.startsWith("text/") || TEXTUAL_APPLICATION_MIME_TYPES.has(mimeType);
}
