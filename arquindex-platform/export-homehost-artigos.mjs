// Gerador de arquivos HTML estaticos para revisar antes de subir na HomeHost/Hostinger.
import { mkdir, writeFile } from 'node:fs/promises';
import { arquindexSeoArticles } from './arquindex-seo-nov2026.js';
const root=process.argv[2]||'./dist-homehost';
const base='https://arquindex.com.br';
const esc=(v)=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const generated=[];
for(const a of arquindexSeoArticles){
 const url=base+'/conteudo/'+a.slug;
 const sections=a.sections.map(([h,p])=>'<section><h2>'+esc(h)+'</h2><p>'+esc(p)+'</p></section>').join('');
 const faqs=(a.faqs||[]).map(([q,v])=>'<details><summary>'+esc(q)+'</summary><p>'+esc(v)+'</p></details>').join('');
 const graph={'@context':'https://schema.org','@graph':[{'@type':'Article',headline:a.title,description:a.lead,inLanguage:'pt-BR',datePublished:a.reviewed,dateModified:a.reviewed,mainEntityOfPage:url,author:{'@type':'Organization',name:'Arquindex'},publisher:{'@type':'Organization',name:'Arquindex'}},{'@type':'BreadcrumbList',itemListElement:[{ '@type':'ListItem',position:1,name:'Início',item:base+'/'},{'@type':'ListItem',position:2,name:'Conteúdo',item:base+'/conteudo'},{'@type':'ListItem',position:3,name:a.title,item:url}]}]};
 const html='<!doctype html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(a.title)+' | Arquindex</title><meta name="description" content="'+esc(a.lead)+'"><link rel="canonical" href="'+url+'"><meta name="robots" content="index,follow"><script type="application/ld+json">'+JSON.stringify(graph).replace(/</g,'\\u003c')+'</script><style>body{font:18px/1.7 system-ui;margin:0;background:#f7fafb;color:#17354a}header{padding:22px 7%;background:#113c53}header a{color:white}main{max-width:880px;padding:46px 24px;margin:auto}h1{font-size:clamp(32px,5vw,50px);line-height:1.16}section{margin-top:38px}a{color:#116b80}details{padding:12px;border-bottom:1px solid #ccc}footer{padding:25px 7%;border-top:1px solid #ddd}</style></head><body><header><a href="'+base+'/">Arquindex — Gestão Documental</a></header><main><a href="'+base+'/conteudo">Todos os conteúdos</a><article><h1>'+esc(a.title)+'</h1><p>'+esc(a.lead)+'</p>'+sections+'<h2>Perguntas frequentes</h2>'+faqs+'<h2>Referência técnica</h2><p><a rel="noopener noreferrer" href="'+esc(a.source)+'">Consultar fonte</a></p></article><p><a href="'+base+'/contato">Solicitar avaliação comercial</a></p></main><footer>Arquindex — escopo e condições sujeitos à avaliação comercial.</footer></body></html>';
 const dir=root+'/conteudo/'+a.slug;
 await mkdir(dir,{recursive:true});
 await writeFile(dir+'/index.html',html,'utf8');
 generated.push({url,path:'conteudo/'+a.slug+'/index.html'});
}
await mkdir(root,{recursive:true});
await writeFile(root+'/MANIFEST.json',JSON.stringify({brand:'Arquindex',canonicalHost:base,generated,warning:'Validar origem DNS, HTML 200 e backup antes de upload por FTP.'},null,2));
console.log('Gerados '+generated.length+' artigos estaticos para revisao em '+root);
