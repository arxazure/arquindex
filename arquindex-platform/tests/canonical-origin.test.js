import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const source = readFileSync(new URL("../server.js", import.meta.url), "utf8");
const canonicalFn = source.match(/function canonicalOrigin\(req\)\s*\{([\s\S]*?)\n\}/)?.[1];

test("production canonical host is apex and never www", () => {
  assert.ok(canonicalFn, "canonicalOrigin exists");
  assert.match(canonicalFn, /return OFFICIAL;/);
  assert.doesNotMatch(canonicalFn, /return ["']https:\/\/www\.arquindex\.com\.br/);
  assert.match(source, /const OFFICIAL="https:\/\/arquindex\.com\.br";/);
});

test("robots and both sitemap endpoints derive URLs from canonicalOrigin", () => {
  for (const route of ["/robots.txt", "/sitemap.xml", "/sitemap-index.xml"]) {
    const anchor = source.indexOf('if(p==="' + route + '")');
    assert.ok(anchor >= 0, route + " route exists");
    assert.match(source.slice(anchor, anchor + 140), /canonicalOrigin\(req\)/);
  }
});
