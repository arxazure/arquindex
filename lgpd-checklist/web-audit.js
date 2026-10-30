import https from 'node:https';
import {lookup} from 'node:dns/promises';
import {isIP} from 'node:net';

const MAX_BYTES=512*1024;
export class AuditError extends Error {constructor(message){super(message);this.code='WEB_AUDIT_BLOCKED';}}
export function isPublicIPv4(ip){
 if(isIP(ip)!==4)return false;
 const [a,b,c]=ip.split('.').map(Number);
 if(a===0||a===10||a===127||a>=224||a===169&&b===254||a===172&&b>=16&&b<=31||a===192&&b===168||a===100&&b>=64&&b<=127)return false;
 if(a===192&&b===0&&(c===0||c===2)||a===192&&b===88&&c===99||a===198&&(b===18||b===19)||a===198&&b===51&&c===100||a===203&&b===0&&c===113)return false;
 return ip!=='168.63.129.16';
}
export function validateTarget(input){
 if(typeof input!=='string'||input.length>2048)throw new AuditError('Informe uma URL HTTPS pública válida.');
 let u;try{u=new URL(input);}catch{throw new AuditError('Informe uma URL HTTPS pública válida.');}
 const h=u.hostname.toLowerCase().replace(/\.$/,'');
 if(u.protocol!=='https:'||u.username||u.password||u.port&&u.port!=='443'||isIP(h)||h.includes(':')||!h.includes('.')||!/^[a-z0-9.-]+$/.test(h)||h.split('.').some(x=>!x||x.length>63||x.startsWith('-')||x.endsWith('-'))||/(^|\.)(localhost|local|internal|invalid|test|onion)$/.test(h))throw new AuditError('Use um domínio público com HTTPS, sem credenciais ou portas alternativas.');
 if([...u.searchParams.keys()].some(k=>/^(token|password|secret|authorization|api[_-]?key|session|jwt|access[_-]?token|code)$/i.test(k)))throw new AuditError('Remova credenciais e tokens da URL antes da análise.');
 u.hostname=h;u.hash='';return u;
}
async function bounded(p,ms){let timer;try{return await Promise.race([p,new Promise((_,reject)=>{timer=setTimeout(()=>reject(new AuditError('Tempo limite da análise atingido.')),ms);})]);}finally{clearTimeout(timer);}}
export async function resolveTarget(url,resolver=lookup,timeout=4000){
 const addresses=await bounded(resolver(url.hostname,{all:true,verbatim:true}),timeout);
 const ipv4=addresses.filter(x=>x.family===4);
 if(!ipv4.length||ipv4.some(x=>!isPublicIPv4(x.address)))throw new AuditError('O domínio não possui um destino IPv4 público permitido.');
 return {address:ipv4[0].address,family:4};
}
export function pinnedOptions(url,address,timeout){
 if(!isPublicIPv4(address.address)||address.family!==4)throw new AuditError('Destino de rede não permitido.');
 return {method:'GET',agent:false,family:4,autoSelectFamily:false,servername:url.hostname,rejectUnauthorized:true,maxHeaderSize:16384,signal:AbortSignal.timeout(timeout),headers:{'User-Agent':'Arquindex-LGPD-Audit/0.3 (+https://lgpd.arquindex-capture.stream/)','Accept':'text/html,application/xhtml+xml','Accept-Encoding':'identity'},lookup:(hostname,options,callback)=>{
  if(hostname!==url.hostname)return callback(new AuditError('Destino da conexão divergente.'));
  if(options?.all)return callback(null,[address]);callback(null,address.address,4);
 }};
}
function requestPinned(url,address,timeout){
 return new Promise((resolve,reject)=>{
  const req=https.request(url,pinnedOptions(url,address,timeout),res=>{
   const headers=res.headers,status=res.statusCode||0,chunks=[];let size=0;
   const result=(truncated=false)=>resolve({status,headers,html:Buffer.concat(chunks).toString('utf8'),truncated});
   if([301,302,303,307,308].includes(status)||!/(text\/html|application\/xhtml\+xml)/i.test(String(headers['content-type']||''))||headers['content-encoding']&&headers['content-encoding']!=='identity'){result();res.destroy();return;}
   res.on('data',chunk=>{const remaining=MAX_BYTES-size;chunks.push(chunk.subarray(0,Math.max(0,remaining)));size+=chunk.length;if(size>MAX_BYTES){result(true);res.destroy();}});
   res.on('end',()=>result());res.on('error',reject);
  });req.on('error',reject);req.end();
 });
}
function attrs(tag){const out={};for(const m of tag.matchAll(/\b([a-z_:][a-z0-9_:.-]*)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))/gi))out[m[1].toLowerCase()]=(m[2]??m[3]??m[4]).replace(/&amp;/gi,'&');return out;}
function pageHints(html,base){
 const external=new Set(),privacyLinks=[];let cursor=0,count=0,title='',forms=0;
 while(cursor<html.length&&count++<3000){const start=html.indexOf('<',cursor);if(start<0)break;const end=html.indexOf('>',start+1);if(end<0)break;cursor=end+1;if(end-start>8192)continue;const tag=html.slice(start,end+1),name=/^<\s*([a-z][a-z0-9]*)\b/i.exec(tag)?.[1]?.toLowerCase();if(!name)continue;
  if(name==='title'&&!title)title=html.slice(end+1,end+501).split('<')[0].trim();
  if(name==='form')forms++;
  if(!['a','script','iframe','img','link'].includes(name))continue;const a=attrs(tag);
  if(['script','iframe','img'].includes(name)&&a.src){try{const u=new URL(a.src,base);if(['https:','http:'].includes(u.protocol)&&u.hostname!==base.hostname)external.add(u.hostname);}catch{}}
  if(name==='a'&&a.href){const text=html.slice(end+1,end+401).split('</a>')[0].replace(/<[^>]*>/g,' ');if(/privacidade|privacy|prote[cç][aã]o de dados/i.test(text+' '+a.href)){try{const u=new URL(a.href,base);if(['http:','https:'].includes(u.protocol)&&!u.username&&!u.password){u.hash='';u.search='';if(privacyLinks.length<10&&!privacyLinks.includes(u.href))privacyLinks.push(u.href);}}catch{}}}
 }
 return {title,forms,externalResourceHosts:[...external].slice(0,30),privacyLinks,cookieTextObserved:/cookies|consentimento|consent manager/i.test(html)};
}
export function analyzePage(headers,html,status,url,truncated=false){
 const hints=pageHints(html,url),header=x=>String(headers[x]||'').slice(0,2500);
 const cookieHeaders=headers['set-cookie']||[];const raw=Array.isArray(cookieHeaders)?cookieHeaders:[cookieHeaders];
 const cookies=raw.slice(0,50).map(value=>{const parts=String(value).split(';'),name=parts.shift().split('=')[0].trim().slice(0,100),attributes=parts.map(x=>x.trim());return {name,secure:attributes.some(x=>/^secure$/i.test(x)),httpOnly:attributes.some(x=>/^httponly$/i.test(x)),sameSite:attributes.find(x=>/^samesite=/i.test(x))?.split('=')[1]?.slice(0,20)||null};});
 const checks=[
  {id:'http',label:'Resposta da página',observed:status>=200&&status<300,evidence:'HTTP '+status,nextAction:'Confirmar se o conteúdo esperado está disponível aos visitantes.'},
  ...[['hsts','strict-transport-security','HSTS'],['csp','content-security-policy','Content Security Policy'],['mime','x-content-type-options','Proteção contra detecção de tipo'],['referrer','referrer-policy','Política de referência']].map(([id,k,label])=>({id,label,observed:!!header(k),evidence:header(k)||'Cabeçalho não observado nesta resposta',nextAction:'Revisar a configuração conforme o contexto técnico do website.'})),
  {id:'framing',label:'Proteção contra incorporação',observed:!!header('x-frame-options')||/frame-ancestors/i.test(header('content-security-policy')),evidence:header('x-frame-options')||(/frame-ancestors/i.test(header('content-security-policy'))?'Diretiva frame-ancestors observada':'Não observada nesta resposta'),nextAction:'Avaliar se a incorporação em outros sites deve ser permitida.'},
  {id:'privacy',label:'Link de privacidade no HTML',observed:hints.privacyLinks.length>0,evidence:hints.privacyLinks.join('\n')||'Link não identificado no HTML recebido',nextAction:'Abrir o aviso, conferir conteúdo, contato e correspondência com a coleta real.'},
  {id:'cookies',label:'Referência a cookies ou consentimento',observed:hints.cookieTextObserved,evidence:hints.cookieTextObserved?'Expressão identificada no HTML':'Expressão não identificada no HTML recebido',nextAction:'Conferir no navegador o carregamento de cookies antes e depois das escolhas do visitante.'}
 ];
 return {checks,cookies,...hints,truncated,bodyAnalyzed:html.length>0,interpretation:'Observações técnicas preliminares. Presença ou ausência de um sinal não comprova conformidade ou infração à LGPD.',limitations:['Apenas uma página pública, com até três redirecionamentos HTTPS e conexão IPv4.','Sem execução de JavaScript, navegação em links, login, submissão de formulários ou testes de exploração.','Cookies mostram apenas atributos de Set-Cookie nesta resposta; valores não são armazenados.','Recursos externos são referências encontradas no HTML, não uma classificação automática de rastreadores.','Banner, bloqueio prévio, preferências e cookies criados no navegador exigem conferência adicional.']};
}
export async function scanPage(input,{resolver=lookup,transport=requestPinned}={}){
 const started=Date.now(),deadline=started+12000;let url=validateTarget(input);const initialUrl=url.origin+url.pathname,redirects=[];
 for(let hop=0;hop<=3;hop++){
  const remaining=deadline-Date.now();if(remaining<=0)throw new AuditError('Tempo limite da análise atingido.');
  const address=await resolveTarget(url,resolver,Math.min(4000,remaining));
  const timeLeft=deadline-Date.now();if(timeLeft<=0)throw new AuditError('Tempo limite da análise atingido.');
  const response=await transport(url,address,Math.max(1,Math.min(8000,timeLeft)));
  if([301,302,303,307,308].includes(response.status)){
   if(hop===3)throw new AuditError('A página excedeu o limite de redirecionamentos.');
   if(typeof response.headers.location!=='string')throw new AuditError('Redirecionamento sem destino válido.');
   const next=validateTarget(new URL(response.headers.location,url).href);redirects.push({status:response.status,from:url.origin+url.pathname,to:next.origin+next.pathname});url=next;continue;
  }
  return {scannedAt:new Date().toISOString(),method:'passive-https-v1',initialUrl,finalUrl:url.origin+url.pathname,httpStatus:response.status,redirects,durationMs:Date.now()-started,...analyzePage(response.headers,response.html,response.status,url,response.truncated)};
 }
 throw new AuditError('Não foi possível concluir a análise.');
}
