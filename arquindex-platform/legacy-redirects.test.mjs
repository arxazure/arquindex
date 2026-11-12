import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

const source = readFileSync(new URL("./server.js", import.meta.url), "utf8");
const start = source.indexOf("const legacyRedirects = new Map([");
const end = source.indexOf("]);", start);
assert.ok(start >= 0 && end > start, "legacy redirect map exists");
const map = source.slice(start, end);
const cases = [
  ["/digitalizacao.html", "/solucoes/digitalizacao-documentos"],
  ["/dpo-as-a-service-consultoria-lgpd.html", "/solucoes/dpo-terceirizado"],
  ["/gestao_documental_documentos.html", "/solucoes/gestao-documental"],
];
for (const [oldPath, target] of cases) {
  test(`legacy redirect ${oldPath} maps to ${target}`, () => {
    assert.ok(map.includes(JSON.stringify(oldPath) + "," + JSON.stringify(target)), "exact redirect mapping");
    assert.equal(map.split(JSON.stringify(oldPath) + ",").length, 2, "one mapping only");
  });
}
test("OCR intent not redirected without a dedicated decision", () => {
  assert.ok(!map.includes('"/digitalizacao-com-ocr.html"'));
});
test("legacy redirects use HTTP 301", () => {
  assert.match(source, /if\(legacyRedirects\.has\(p\)\)[\s\S]*?res\.writeHead\(301,/);
});
