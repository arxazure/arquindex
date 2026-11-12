import {safeCorrections} from './quality.js';
export async function reconcileExistingCompanies(pool){
 const db=await pool.connect();
 try{
  await db.query('BEGIN');
  await db.query('CREATE TABLE IF NOT EXISTS lgpd_record_revisions (id BIGSERIAL PRIMARY KEY, record_id UUID NOT NULL, company_id UUID NOT NULL, previous_payload JSONB NOT NULL, change_reason TEXT NOT NULL, changed_at TIMESTAMPTZ NOT NULL DEFAULT now())');
  const rows=(await db.query('SELECT id,section,company_id,parent_id,payload FROM lgpd_records ORDER BY company_id,section,created_at FOR UPDATE')).rows;
  const grouped=new Map();
  for(const r of rows){if(!grouped.has(r.company_id))grouped.set(r.company_id,[]);grouped.get(r.company_id).push(r);}
  let changed=0,companies=0;
  for(const [companyId,records] of grouped){
   const corrections=safeCorrections(records);
   if(!corrections.length)continue;
   companies++;
   for(const change of corrections){
    const record=records.find(x=>x.id===change.id);
    if(!record||record.section!==change.section)continue;
    if(String(record.payload?.[change.field]??'')!==change.before)continue;
    await db.query('INSERT INTO lgpd_record_revisions(record_id,company_id,previous_payload,change_reason) VALUES($1,$2,$3,$4)',[record.id,companyId,JSON.stringify(record.payload),change.reason]);
    const newPayload={...record.payload,[change.field]:change.after};
    const update=await db.query('UPDATE lgpd_records SET payload=$1,updated_at=now() WHERE id=$2 AND payload=$3::jsonb',[JSON.stringify(newPayload),record.id,JSON.stringify(record.payload)]);
    if(update.rowCount!==1)throw Error('Concurrent record modification: '+record.id);
    await db.query('INSERT INTO lgpd_audit(user_id,company_id,action,record_id) VALUES(NULL,$1,$2,$3)',[companyId,'safe_data_quality_reconciliation:'+change.field,record.id]);
    record.payload=newPayload;changed++;
   }
  }
  await db.query('COMMIT');
  return {companies_scanned:grouped.size,companies_changed:companies,fields_corrected:changed};
 }catch(e){await db.query('ROLLBACK');throw e;}finally{db.release();}
}
