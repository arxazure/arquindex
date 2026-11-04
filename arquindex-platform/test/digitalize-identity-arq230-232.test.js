import test from 'node:test';
import assert from 'node:assert/strict';
import { renderDigitalize } from '../digitalize-pages.js';

const origin='https://arquindex.com.br';
const targets=[
  ['santa-luzia','Digitalize em Santa Luzia: digitalização de documentos | Arquindex','Digitalize seus documentos em Santa Luzia'],
  ['ribeirao-das-neves','Digitalize em Ribeirão das Neves: digitalização de documentos | Arquindex','Digitalize seus documentos em Ribeirão das Neves'],
  ['ibirite','Digitalize em Ibirité: digitalização de documentos | Arquindex','Digitalize seus documentos em Ibirité'],
  ['sabara','Digitalize em Sabará: digitalização de documentos | Arquindex','Digitalize seus documentos em Sabará'],
  ['lagoa-santa','Digitalize em Lagoa Santa: digitalização de documentos | Arquindex','Digitalize seus documentos em Lagoa Santa'],
  ['pedro-leopoldo','Digitalize em Pedro Leopoldo: digitalização de documentos | Arquindex','Digitalize seus documentos em Pedro Leopoldo']
];

for(const [slug,title,h1] of targets){
  test('identidade e conversão preservam SEO em '+slug,()=>{
    const path='/digitalize/'+slug+'/';
    const html=renderDigitalize(path,origin).body;
    assert.ok(html.includes('class="aq-logo"'));
    assert.ok(html.includes('class="aq-logo-name"'));
    assert.ok(html.includes('EFICIÊNCIA MÁXIMA EM GESTÃO DE DOCUMENTOS'));
    assert.ok(html.includes('id="aq-nav"'));
    assert.ok(html.includes('id="arq-floating"'));
    assert.ok(html.includes('utm_source=seo_local&utm_medium=organic&utm_campaign=digitalize_'+slug));
    assert.ok(html.includes('<title>'+title+'</title>'));
    assert.ok(html.includes('<h1>'+h1+'</h1>'));
    assert.ok(html.includes('rel="canonical" href="'+origin+path+'"'));
    assert.equal((html.match(/<h1\b/g)||[]).length,1);
  });
}

test('mudança não é aplicada indiscriminadamente à família',()=>{
  const html=renderDigitalize('/digitalize/vespasiano/',origin).body;
  assert.ok(!html.includes('id="arq-floating"'));
  assert.ok(!html.includes('class="aq-logo"'));
  assert.ok(!html.includes('class="aq-logo-name"'));
});
