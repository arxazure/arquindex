import assert from "node:assert/strict";
import { test } from "node:test";
import { recoveryPaths, renderLegacyRecovery, legacyTechnicalWordCount } from "../legacy-recovery-pages.js";

const base="https://www.arquindex.com.br";
test("somente as rotas historicas previstas",()=>{
 assert.deepEqual(new Set(recoveryPaths),new Set([
  "/gestao_de_colaboradores_documentos.html",
  "/digitalizacao-com-ocr.html"
 ]));
 assert.equal(renderLegacyRecovery("/digitalizacao-documentos-brasilia.html",base),null);
});
for(const path of recoveryPaths){
 test("HTML de recuperação completo e canonical individual: "+path,()=>{
  const html=renderLegacyRecovery(path,base);
  assert.ok(html.startsWith("<!doctype html>"));
  assert.match(html,/<html lang="pt-BR">/);
  assert.ok(html.includes('<link rel="canonical" href="'+base+path+'">'));
  assert.ok(html.includes('<meta property="og:url" content="'+base+path+'">'));
  assert.match(html,/<meta name="robots" content="index,follow">/);
  assert.match(html,/<h1>[^<]+<\/h1>/);
  assert.match(html,/<h2>Etapas do processo<\/h2>/);
  assert.match(html,/<h2>Perguntas frequentes<\/h2>/);
  assert.match(html,/<a\b[^>]*href="https:\/\/wa\.me\/5531973632725"/);
  assert.match(html,/mailto:comercial@arquindex\.com\.br/);
  assert.doesNotMatch(html,/segurança (total|garantida)|validade jurídica automática/i);
 });
}
test("URL desconhecida não cria doorway page",()=>assert.equal(renderLegacyRecovery("/seo-local/cidade-ficticia",base),null));

for(const path of recoveryPaths){test("guia técnico acima de 2000 palavras: "+path,()=>assert.ok(legacyTechnicalWordCount(path)>=2000, "Contagem abaixo de 2000: "+legacyTechnicalWordCount(path)));}
