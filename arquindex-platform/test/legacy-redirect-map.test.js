import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";

const source=readFileSync(new URL("../server.js",import.meta.url),"utf8");
const body=source.match(/const legacyRedirects = new Map\(\[([\s\S]*?)\]\);/)?.[1]||"";
const pairs=[...body.matchAll(/\["([^"]+)","([^"]+)"\]/g)].map(([,from,to])=>[from,to]);
const redirects=new Map(pairs);

const expected=new Map([
 ["/digitalizacao.html","/solucoes/digitalizacao-documentos"],
 ["/dpo-as-a-service-consultoria-lgpd.html","/solucoes/dpo-terceirizado"],
 ["/gestao_documental_documentos.html","/solucoes/gestao-documental"]
]);

test("rotas legadas comerciais apontam para soluções canônicas",()=>{
 for(const [from,to] of expected){
  assert.equal(redirects.get(from),to);
  assert.ok(!redirects.has(to),"destino não deve iniciar cadeia de redirect: "+to);
 }
});

test("rotas legadas usam destino interno absoluto e sem parâmetros",()=>{
 for(const to of expected.values()){
  assert.match(to,/^\/solucoes\/[a-z0-9-]+$/);
  assert.ok(!to.includes("?"));
 }
});
