import test from 'node:test';
import assert from 'node:assert/strict';
import { fork } from 'node:child_process';
import { once } from 'node:events';
import http from 'node:http';
function get(port,path,host){return new Promise((resolve,reject)=>{http.get({hostname:'127.0.0.1',port,path,headers:{host}},res=>{let body='';res.setEncoding('utf8');res.on('data',x=>body+=x);res.on('end',()=>resolve({status:res.statusCode,body}));}).on('error',reject);});}
import { regionalPage, regionalGuides } from '../regional-guides.js';
import { databookChecklist } from '../brasilia-seo.js';

test('existing Brasília route has substantive content and matching schema', () => {
 const origin = 'https://www.arquindex.com.br';
 const page = regionalPage('brasilia-df', 'local', origin);
 assert.match(page.title, /Digitalização de documentos em Brasília/);
 for(const term of ['lote-piloto','cadeia de custódia','metadados','pendências','Belo Horizonte','CONARQ']) assert.ok(page.body.includes(term),term);
 assert.equal((page.body.match(/<h1>/g)||[]).length,1);
 const schema = JSON.parse(page.head.match(/<script[^>]*>(.*?)<\/script>/s)[1]);
 assert.equal(schema['@graph'][0].url,origin+'/digitalizacao/local/brasilia-df');
 assert.doesNotMatch(page.head,/LocalBusiness|AggregateRating|FAQPage/);
 assert.equal(regionalGuides.length,20);
 assert.match(regionalPage('brasilia-df','preco').title,/Quanto custa/);
 assert.match(regionalPage('contagem-mg','local').title,/Contagem/);
 assert.equal(regionalPage('inexistente','local'),null);
});

test('Databook example has scope boundaries and links to established commercial URLs', () => {
 assert.match(databookChecklist,/Exemplo didático/);
 assert.match(databookChecklist,/responsáveis habilitados/);
 assert.match(databookChecklist,/montagem_databook_organizar\.html/);
 assert.match(databookChecklist,/digitalizacao\.html/);
 assert.doesNotMatch(databookChecklist,/<h1|R\$|garanti[ad]/);
});

test('real router serves the enhanced existing routes without canonical or redirect regressions', async t => {
 const child = fork(new URL('../server.js',import.meta.url),[],{
  execArgv:['--import',new URL('./fixtures/replica-upstream.mjs',import.meta.url).href],
  env:{...process.env,PORT:'0',NODE_ENV:'test',INDEXNOW_KEY:'',INDEXNOW_AUTO_SUBMIT:'false'},stdio:['ignore','ignore','pipe','ipc']});
 t.after(async()=>{child.kill();await once(child,'exit');});
 const [msg] = await once(child,'message');
 for(const [path,marker] of [['/digitalizacao/local/brasilia-df','digitalizacao-brasilia-escopo'],['/digitalizacao/local/brasilia-df/','digitalizacao-brasilia-escopo'],['/solucoes/databook','databook-aceite-documental']]) {
  const res=await get(msg.port,path,'www.arquindex.com.br');
  assert.equal(res.status,200);const html=res.body;
  assert.equal((html.match(/<h1\b/g)||[]).length,1);
  assert.equal((html.match(new RegExp('id="'+marker+'"','g'))||[]).length,1);
  assert.deepEqual([...html.matchAll(/<link rel="canonical" href="([^"]+)"/g)].map(x=>x[1]),['https://www.arquindex.com.br'+path]);
  for(const m of html.matchAll(/<script type="application\/ld\+json">(.*?)<\/script>/gs)){ const data=JSON.parse(m[1]); if(data['@graph']) assert.equal(data['@graph'][0].url,'https://www.arquindex.com.br'+path); }
 }
});
