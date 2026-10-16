import test from "node:test";
import assert from "node:assert/strict";
import { isReadableTextMimeType } from "../src/content-type.js";

test("accepts text MIME types", () => {
  assert.equal(isReadableTextMimeType("text/plain"), true);
  assert.equal(isReadableTextMimeType("text/markdown"), true);
});

test("accepts recognized textual application MIME types", () => {
  assert.equal(isReadableTextMimeType("application/json"), true);
  assert.equal(isReadableTextMimeType("application/xml"), true);
  assert.equal(isReadableTextMimeType("application/typescript"), true);
});

test("rejects binary and unknown MIME types", () => {
  assert.equal(isReadableTextMimeType("image/png"), false);
  assert.equal(isReadableTextMimeType("application/pdf"), false);
  assert.equal(isReadableTextMimeType("application/octet-stream"), false);
  assert.equal(isReadableTextMimeType(""), false);
});
