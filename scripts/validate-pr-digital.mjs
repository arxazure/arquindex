import {readFileSync,existsSync} from 'node:fs';
const root='pr-digital/';
const pages=['index.html','custo-oculto-transformacao-digital/index.html','ia-local-governanca-documental/index.html','databooks-digitais-engenharia/index.html','calculadora-tco/index.html'];
const base='https://www.arquindex.com.br/pr-digital/';
let failed=0;
for(const path of pages){const file=root+path;if(!existsSync(file)){console.error('AUSENTE',file);failed++;continue}
const html=readFileSync(file,'utf8');const suffix=path==='index.html'?'':path.replace(/index\.html$/,'');
const checks={'lang=pt-BR':/<html[^>]+lang="pt-BR"/i.test(html),'title':/<title>[^<]+<\/title>/i.test(html),'description':/<meta name="description" content="[^"]+"/.test(html),'canonical':html.includes('href="'+base+suffix+'"'),'headings':/<h1>[^<]+<\/h1>/i.test(html),'links internal':html.includes(base)};
for(const [name,ok] of Object.entries(checks)){if(!ok){failed++;console.error('FALHA',file,name)}}
console.log('VALIDADO',file,Object.values(checks).filter(Boolean).length+'/'+Object.keys(checks).length)}
const sitemap=readFileSync(root+'sitemap.xml','utf8');for(const path of pages){const suffix=path==='index.html'?'':path.replace(/index\.html$/,'');if(!sitemap.includes('<loc>'+base+suffix+'</loc>')){failed++;console.error('FALHA sitemap',path)}}
if(failed){console.error('Total de falhas:',failed);process.exit(1)}
console.log('Todas as validacoes PR Digital passaram');
