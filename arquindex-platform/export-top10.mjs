import {top10Guides,top10Articles} from './top10-content.js';
import fs from 'node:fs/promises';
import {spawn} from 'node:child_process';
const child=spawn(process.execPath,['server.js'],{env:{...process.env,PORT:'3417'}});
await new Promise((resolve,reject)=>{child.stdout.once('data',resolve);child.once('exit',c=>reject(Error('Server exited: '+c)));setTimeout(()=>reject(Error('Server timeout')),10000).unref();});
try{
 const out='top10-public';await fs.mkdir(out,{recursive:true});
 const items=[...top10Guides.map(x=>({...x,type:'guide',route:'/guias/'+x.slug,path:'guias/'+x.slug+'.html'})),...top10Articles.map(x=>({...x,type:'article',route:'/conteudo/'+x.slug,path:'artigos/'+x.slug+'.html'}))];
 const targets=new Map(items.map(x=>[x.route,'/top10/'+x.path]));
 let failed=[];
 for(const item of items){
  const r=await fetch('http://127.0.0.1:3417'+item.route);let html=await r.text();
  if(r.status!==200||html.includes('undefined')||!html.includes(item.title))failed.push(item.slug);
  html=html.replaceAll('https://arquindex-web-production.up.railway.app','https://www.arquindex.com.br').replaceAll('https://arquindex.com.br','https://www.arquindex.com.br');
  for(const [oldpath,newpath] of targets)html=html.replaceAll('href="'+oldpath+'"','href="'+newpath+'"').replaceAll('https://www.arquindex.com.br'+oldpath+'"','https://www.arquindex.com.br'+newpath+'"');
  html=html.replaceAll('href="/guias"','href="/top10/index.html"').replaceAll('href="/conteudo"','href="/top10/index.html#artigos"').replaceAll('href="/solucoes"','href="https://www.arquindex.com.br/servicos.html"').replaceAll('href="/contato"','href="https://wa.me/5531973632725"');
  await fs.mkdir(out+'/'+item.path.split('/')[0],{recursive:true});await fs.writeFile(out+'/'+item.path,html);
 }
 const links=items.map(x=>'<li><a href="/top10/'+x.path+'">'+x.title+'</a></li>').join('');
 const hub='<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Guias empresariais e artigos | Arquindex</title><link rel="canonical" href="https://www.arquindex.com.br/top10/index.html"><style>body{max-width:1000px;margin:40px auto;padding:20px;font-family:system-ui;line-height:1.7;color:#163057}a{color:#0b5bc7}li{margin:10px 0}</style><h1>Guias empresariais da Arquindex</h1><p>100 guias por tipo documental e tarefa e 15 artigos operacionais. Exemplos ilustrativos. Base em Belo Horizonte; escopo e logística são dimensionados para cada projeto.</p><p><a href="https://www.arquindex.com.br/">Site oficial</a> · <a href="https://wa.me/5531973632725">WhatsApp comercial</a></p><h2 id="artigos">Conteúdos e orientações</h2><ul>'+links+'</ul></html>';
 await fs.writeFile(out+'/index.html',hub);
 const key='top10'+crypto.randomUUID().replaceAll('-','');await fs.writeFile(out+'/'+key+'.txt',key);
 const paths=['index.html',...items.map(x=>x.path)];
 const sitemap='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+paths.map(p=>'<url><loc>https://www.arquindex.com.br/top10/'+p+'</loc><lastmod>2026-10-12</lastmod></url>').join('')+'</urlset>';
 await fs.writeFile(out+'/sitemap.xml',sitemap);
 const files=['index.html','sitemap.xml',key+'.txt',...items.map(x=>x.path)];
 const manifest={version:'2026-10-12-top10',domain:'https://www.arquindex.com.br',basePath:'/top10',key,files:await Promise.all(files.map(async path=>{const content=await fs.readFile(out+'/'+path);const sha256=Buffer.from(await crypto.subtle.digest('SHA-256',content)).toString('hex');return {path,sha256,bytes:content.length};})),pages:items.map(x=>({path:x.path,title:x.title,type:x.type}))};
 await fs.writeFile(out+'/manifest.json',JSON.stringify(manifest,null,2));
 console.log(JSON.stringify({guides:top10Guides.length,articles:top10Articles.length,files:files.length,failed,bytes:manifest.files.reduce((a,b)=>a+b.bytes,0)}));
 if(failed.length)process.exitCode=1;
}finally{child.kill();}
