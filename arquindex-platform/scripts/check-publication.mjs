import {writeFile,mkdir} from 'node:fs/promises';
const BASES=['https://arquindex.com.br','https://arquindex-web-production.up.railway.app'];
const slugs=[
'digitalizacao-certificada-rmbh-como-contratar',
'guarda-documental-rmsp-seguranca-temporalidade',
'alfresco-ecm-gestao-documental-comparativo',
'lgpd-dpo-terceirizado-empresas-bh-sp',
'ocr-pdfa-indexacao-qualidade-empresas'
];
const paths=['/health','/robots.txt','/sitemap.xml','/llms.txt',...slugs.map(x=>'/conteudo/'+x)];
const report={executedAt:new Date().toISOString(),canonical:'https://arquindex.com.br',checks:[]};
for(const base of BASES)for(const path of paths){
const url=base+path;const item={url,status:null,ok:false,canonical:null,title:null,sitemapListed:null,errors:[]};
try{
 const res=await fetch(url,{redirect:'follow',signal:AbortSignal.timeout(15000),headers:{'user-agent':'Arquindex-SEO-Verification/1.0'}});
 item.status=res.status;item.finalUrl=res.url;item.contentType=res.headers.get('content-type');
 const text=await res.text();item.ok=res.ok;
 if(path.startsWith('/conteudo/')){
 item.title=(text.match(/<title[^>]*>([^<]*)<\/title>/i)||[])[1]||null;
 item.canonical=(text.match(/<link[^>]*rel=["']canonical["'][^>]*href=["']([^"']+)/i)||[])[1]||null;
 item.hasArticleSchema=text.includes('"@type":"Article"')||text.includes('"@type": "Article"');
 item.hasFaq=text.includes('Perguntas frequentes');
 if(!item.title)item.errors.push('missing title');
 if(!item.hasArticleSchema)item.errors.push('missing article schema');
 if(base===report.canonical&&item.canonical&&item.canonical!==report.canonical+path)item.errors.push('canonical differs from primary domain');
 if(base!==report.canonical&&item.canonical&&item.canonical!==base+path&&item.canonical!==report.canonical+path)item.errors.push('unexpected preview canonical');
 }
 if(path==='/sitemap.xml'){item.articleUrlsFound=slugs.filter(s=>text.includes('/conteudo/'+s)).length;if(item.articleUrlsFound!==5)item.errors.push('five articles not listed');}
 if(path==='/robots.txt')item.hasSitemap=text.includes('Sitemap:');
}catch(e){item.errors.push(String(e));}
report.checks.push(item);
}
await mkdir('seo-evidence',{recursive:true});
await writeFile('seo-evidence/arquindex-publication.json',JSON.stringify(report,null,2)+'\n');
const lines=['# Arquindex publication verification','','Checked: '+report.executedAt,'','| URL | HTTP | Title | Flags |','|---|---:|---|---|'];
for(const c of report.checks)lines.push('| '+c.url+' | '+(c.status??'error')+' | '+(c.title||'—').replace(/\|/g,'/')+' | '+(c.errors.join(', ')||'ok')+' |');
await writeFile('seo-evidence/arquindex-publication.md',lines.join('\n')+'\n');
const critical=report.checks.filter(x=>!x.ok||x.errors.length);
console.log(JSON.stringify({checked:report.checks.length,issues:critical.length,report:'seo-evidence/arquindex-publication.md'}));
if(critical.length)process.exitCode=1;
