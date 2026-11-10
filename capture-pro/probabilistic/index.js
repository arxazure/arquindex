"use strict";
// Local, deterministic probabilistic indexing POC. No external calls or persistence.
const {createHash}=require("node:crypto");
function fail(code){const e=new Error(code);e.code=code;throw e;}
function norm(s){return String(s).normalize("NFKC").toLocaleLowerCase("pt-BR").trim();}
function validateToken(t){if(!t||!Array.isArray(t.hypotheses)||!t.hypotheses.length)fail("INVALID_HYPOTHESES");let sum=0;for(const h of t.hypotheses){if(typeof h.text!=="string"||!h.text.trim()||!Number.isFinite(h.probability)||h.probability<0||h.probability>1)fail("INVALID_PROBABILITY");sum+=h.probability;}if(Math.abs(sum-1)>0.001)fail("PROBABILITIES_NOT_NORMALIZED");if(t.box&&(!Array.isArray(t.box)||t.box.length!==4||t.box.some(n=>!Number.isFinite(n)||n<0)))fail("INVALID_BOX");}
function createIndex({tenantId,documentId,imageSha256,tokens,synthetic=false,embedding=null}){
 if(!synthetic)fail("SYNTHETIC_ONLY");
 if(!tenantId||!documentId||! /^[a-f0-9]{64}$/i.test(imageSha256)||!Array.isArray(tokens))fail("INVALID_DOCUMENT");
 tokens.forEach(validateToken);
 if(embedding!==null&&(!Array.isArray(embedding)||!embedding.length||embedding.some(n=>!Number.isFinite(n))))fail("INVALID_EMBEDDING");
 return Object.freeze({schemaVersion:1,tenantId,documentId,imageSha256: imageSha256.toLowerCase(),synthetic:true,
 tokens:structuredClone(tokens),embedding:embedding&&[...embedding],revision:0});
}
function lexicalSearch(index,query,{limit=20}={}){
 const q=norm(query);if(!q||!Number.isInteger(limit)||limit<1||limit>1000)fail("INVALID_QUERY");
 return index.tokens.map((t,i)=>({tokenIndex:i,score:t.hypotheses.filter(h=>norm(h.text)===q).reduce((s,h)=>s+h.probability,0),box:t.box||null,imageSha256:index.imageSha256,documentId:index.documentId}))
 .filter(x=>x.score>0).sort((a,b)=>b.score-a.score||a.tokenIndex-b.tokenIndex).slice(0,limit);
}
function cosine(a,b){if(!Array.isArray(a)||!Array.isArray(b)||a.length!==b.length||!a.length||[...a,...b].some(n=>!Number.isFinite(n)))fail("INVALID_EMBEDDING");let dot=0,aa=0,bb=0;for(let i=0;i<a.length;i++){dot+=a[i]*b[i];aa+=a[i]*a[i];bb+=b[i]*b[i];}return aa&&bb?dot/Math.sqrt(aa*bb):0;}
function semanticSearch(indexes,vector,{tenantId,limit=20}={}){
 if(!tenantId||!Number.isInteger(limit)||limit<1||limit>1000)fail("INVALID_QUERY");
 return indexes.filter(x=>x.tenantId===tenantId&&x.embedding).map(x=>({documentId:x.documentId,imageSha256:x.imageSha256,score:cosine(x.embedding,vector)})).sort((a,b)=>b.score-a.score||a.documentId.localeCompare(b.documentId)).slice(0,limit);
}
function extractFields(index,rules){
 if(!Array.isArray(rules))fail("INVALID_RULES");
 const text=index.tokens.map(t=>t.hypotheses.reduce((a,b)=>b.probability>a.probability?b:a).text).join(" ");
 return rules.map(r=>{if(!r||typeof r.name!=="string"||typeof r.pattern!=="string"||r.pattern.length>200)fail("INVALID_RULE");const m=new RegExp(r.pattern,"iu").exec(text);return {name:r.name,value:m?m[0]:null,source:"top1_transcription",requiresHumanReview:true};});
}
function validateCorrection(index,tokenIndex,text,reviewer){
 if(!Number.isInteger(tokenIndex)||tokenIndex<0||tokenIndex>=index.tokens.length||!text?.trim()||!reviewer?.trim())fail("INVALID_CORRECTION");
 const next=structuredClone(index);next.tokens[tokenIndex].validated={text,reviewer};next.revision++;return Object.freeze(next);
}
function toAlfrescoMetadata(index){return {documentId:index.documentId,properties:{"arq:sourceSha256":index.imageSha256,"arq:probabilisticSchema":String(index.schemaVersion),"arq:reviewRevision":String(index.revision)},transport:"not_implemented",requiresServerSideTenantAuthorization:true};}
function digestIndex(index){return createHash("sha256").update(JSON.stringify(index)).digest("hex");}
module.exports={createIndex,lexicalSearch,semanticSearch,extractFields,validateCorrection,toAlfrescoMetadata,digestIndex};
