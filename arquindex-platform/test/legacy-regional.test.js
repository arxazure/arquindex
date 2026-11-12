import assert from "node:assert/strict";
import {test} from "node:test";
import {regionalRecoveryPaths,regionalRecoveryPage,regionalRecoveryWords} from "../legacy-regional-pages.js";
test("rotas históricas especificas",()=>assert.deepEqual(new Set(regionalRecoveryPaths),new Set(["/digitalizacao-documentos-brasilia.html","/digitalizacao-documentos-salvador.html"])));
for(const p of regionalRecoveryPaths){test("conteudo técnico distinto: "+p,()=>{const d=regionalRecoveryPage(p);assert.ok(d.topics.length>=12);assert.ok(regionalRecoveryWords(p)>=600);assert.ok(d.city&&d.uf);assert.ok(d.topics.every(([h,v])=>h.length>10&&v.length>200));});}
test("não cria páginas regionais arbitrárias",()=>assert.equal(regionalRecoveryPage("/digitalizacao-documentos-cidade-inexistente.html"),null));
