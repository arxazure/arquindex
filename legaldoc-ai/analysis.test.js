import test from 'node:test';import assert from 'node:assert/strict';import {analyzeDocumentText} from './analysis.js';
test('identifica pendencias e documento sem alegar parecer juridico',()=>{const a=analyzeDocumentText('Empresa {{razao_social}}. Data 10/10/2026. PENDENTE.');assert.equal(a.warnings,2);assert.ok(a.findings.some(x=>x.type==='date'));assert.match(a.disclaimer,/revisar/);});
test('mascara CPF na saida da triagem',()=>{const a=analyzeDocumentText('CPF 123.456.789-00');assert.equal(a.findings[0].excerpt,'[dado pessoal oculto]');});
test('rejeita carga excessiva',()=>assert.throws(()=>analyzeDocumentText('x'.repeat(200001))));
