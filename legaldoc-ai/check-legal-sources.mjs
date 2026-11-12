// Read-only legislative source availability and fingerprint report.
// No text ingestion into approved templates; changes require legal review.
import {legalSources} from './legal-catalog.js';
import {writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const allowedHosts=new Set(['www.gov.br','www.planalto.gov.br']);
const results=[];
for(const [key,source] of Object.entries(legalSources)){
 const record={id:key,title:source.title,source:source.url,checkedAt:new Date().toISOString(),status:'unavailable'};
 try{
  const url=new URL(source.url);
  if(url.protocol!=='https:'||!allowedHosts.has(url.hostname))throw Error('Source outside allowlist');
  const signal=AbortSignal.timeout(15000);
  const response=await fetch(url,{signal,redirect:'follow',headers:{'User-Agent':'Arquindex-LegalDoc-Compliance-Monitor/0.1 (contact via arquindex.com.br)'}});
  const finalUrl=new URL(response.url);
  if(finalUrl.protocol!=='https:'||!allowedHosts.has(finalUrl.hostname))throw Error('Unexpected redirect');
  record.httpStatus=response.status;
  record.lastModified=response.headers.get('last-modified')||null;
  record.etag=response.headers.get('etag')||null;
  record.contentType=response.headers.get('content-type')||null;
  if(!response.ok)throw Error('HTTP '+response.status);
  const body=await response.text();
  if(body.length>5_000_000)throw Error('Page exceeds inspection limit');
  const normalized=body.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,'').replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi,'').replace(/<[^>]*>/g,' ').replace(/\s+/g,' ').trim();
  record.fingerprint=createHash('sha256').update(normalized).digest('hex');
  record.status='fetched_unverified';
 }catch(err){record.error=String(err?.message||err).slice(0,180);}
 results.push(record);
}
await mkdir('legal-source-report',{recursive:true});
await writeFile('legal-source-report/status.json',JSON.stringify({generatedAt:new Date().toISOString(),warning:'Fingerprints indicate possible changes, not legally validated amendments. No automatic template approvals.',sources:results},null,2));
console.log('Legal source report created: '+results.filter(r=>r.status==='fetched_unverified').length+'/'+results.length+' accessible.');
