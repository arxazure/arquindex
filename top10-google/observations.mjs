// Offline contract for exports supplied by an authorized operator. No network or writes.
const object = v => v !== null && typeof v === 'object' && !Array.isArray(v);
const timestamp = v => typeof v === 'string' && /^\d{4}-\d{2}-\d{2}T.*(?:Z|[+-]\d{2}:\d{2})$/.test(v) && Number.isFinite(Date.parse(v));
const https = v => {try {const u=new URL(v);return u.protocol==='https:' && !u.username && !u.password;}catch{return false;}};
const domains = ['ranking','indexing','pages','articles','publications'];
export function validObservations(rows) {
  return Array.isArray(rows) && rows.every(r => object(r) && domains.includes(r.kind)
    && typeof r.key==='string' && r.key.trim().length>0
    && typeof r.source==='string' && r.source.trim().length>0
    && typeof r.account==='string' && r.account.trim().length>0
    && timestamp(r.observedAt) && typeof r.evidenceId==='string' && r.evidenceId.trim().length>0
    && ['observed','unavailable','error'].includes(r.status)
    && (r.url==null || https(r.url))
    && (r.note==null || typeof r.note==='string')
    && (r.value==null || typeof r.value==='string' || (typeof r.value==='number' && Number.isFinite(r.value)))
    && (r.status!=='observed' || (r.value!=null && https(r.url)))
    && (r.kind!=='ranking' || r.status!=='observed' || (typeof r.value==='number' && r.value>0)));
}
export function summarizeObservations(rows=[]) {
  if(!validObservations(rows)) throw Error('Invalid observations');
  // Last observation per source/account/key. Later failures invalidate older successes.
  const latest=new Map();
  for(const r of rows){const key=JSON.stringify([r.kind,r.source,r.account,r.key]);const old=latest.get(key);if(!old || Date.parse(r.observedAt)>=Date.parse(old.observedAt))latest.set(key,r);}
  return domains.map(kind=>{const entries=[...latest.values()].filter(r=>r.kind===kind);return {kind,entries,observed:entries.length?entries.filter(r=>r.status==='observed').length:null};});
}
