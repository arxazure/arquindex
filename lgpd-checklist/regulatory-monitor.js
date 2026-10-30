import {createHash} from 'node:crypto';
import {regulatorySources} from './regulatory-catalog.js';

const MAX_BYTES=1024*1024;
const timeoutMs=12000;
export async function checkOfficialSource(source){
 const url=new URL(source.url);
 if(url.protocol!=='https:'||url.hostname!=='www.gov.br')throw Error('Fonte fora do dominio oficial permitido');
 const response=await fetch(url,{redirect:'manual',signal:AbortSignal.timeout(timeoutMs),headers:{'Accept':'text/html,application/pdf,text/plain','User-Agent':'Arquindex-LGPD-Regulatory-Monitor/1.0'}});
 if(!response.ok)throw Error('HTTP '+response.status);
 const mime=(response.headers.get('content-type')||'').toLowerCase();
 if(!/text\/html|text\/plain|application\/pdf/.test(mime))throw Error('Formato nao suportado: '+mime.slice(0,80));
 const reader=response.body.getReader();let total=0;const chunks=[];
 try{while(true){const {done,value}=await reader.read();if(done)break;total+=value.byteLength;if(total>MAX_BYTES)throw Error('Fonte maior que 1 MB; revisao manual necessaria');chunks.push(Buffer.from(value));}}finally{await reader.cancel().catch(()=>{});}
 const raw=Buffer.concat(chunks);
 let normalized=raw;
 if(mime.includes('text/')){
  const text=raw.toString('utf8').replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,' ').replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi,' ').replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim();
  normalized=Buffer.from(text);
 }
 return {hash:createHash('sha256').update(normalized).digest('hex'),bytes:total,mime:mime.slice(0,100),http_status:response.status};
}
export async function runOfficialChecks(db){
 const results=[];
 for(const source of regulatorySources){
  const previous=await db.query("SELECT content_hash FROM lgpd_regulatory_checks WHERE source_id=$1 AND state<>'error' ORDER BY checked_at DESC,id DESC LIMIT 1",[source.id]);
  try{
   const result=await checkOfficialSource(source);
   const state=!previous.rowCount?'baseline':previous.rows[0].content_hash===result.hash?'unchanged':'changed';
   await db.query('INSERT INTO lgpd_regulatory_checks(source_id,source_url,content_hash,state,http_status,mime,bytes,error) VALUES($1,$2,$3,$4,$5,$6,$7,NULL)',[source.id,source.url,result.hash,state,result.http_status,result.mime,result.bytes]);
   results.push({source_id:source.id,state,bytes:result.bytes});
  }catch(error){
   const message=String(error?.message||'Falha de consulta').slice(0,180);
   await db.query("INSERT INTO lgpd_regulatory_checks(source_id,source_url,state,error) VALUES($1,$2,'error',$3)",[source.id,source.url,message]);
   results.push({source_id:source.id,state:'error',error:message});
  }
 }
 return results;
}
