import {runOfficialChecks} from './regulatory-monitor.js';
import {regulatorySources} from './regulatory-catalog.js';

// One shared session lock for both scheduled and manual checks, across replicas.
const LOCK=987643203;
export async function runRegulatoryCheck(pool,{userId=null,trigger='scheduled',check=runOfficialChecks}={}){
 const db=await pool.connect();let locked=false,destroy=false;
 try{
  locked=(await db.query('SELECT pg_try_advisory_lock($1) AS locked',[LOCK])).rows[0].locked;
  if(!locked)return {status:'busy',results:[]};
  const done=await db.query("SELECT DISTINCT source_id FROM lgpd_regulatory_checks WHERE checked_at >= date_trunc('day', now() AT TIME ZONE 'UTC') AT TIME ZONE 'UTC' AND state <> 'error'");
  const completed=new Set(done.rows.map(x=>x.source_id));
  const sources=regulatorySources.filter(x=>!completed.has(x.id));
  if(!sources.length)return {status:'already_checked',results:[]};
  // A failed source remains eligible on the next hourly/manual attempt.
  // Results and the audit event commit together; no client records are touched.
  await db.query('BEGIN');
  try{
   const results=await check(db,sources);
   await db.query('INSERT INTO lgpd_audit(user_id,company_id,action,record_id) VALUES($1,NULL,$2,$3)',[userId,'regulatory_check_'+trigger,JSON.stringify(results.map(x=>({source_id:x.source_id,state:x.state}))).slice(0,4000)]);
   await db.query('COMMIT');
   return {status:results.some(x=>x.state==='error')?'partial_failure':'completed',results};
  }catch(error){await db.query('ROLLBACK');throw error;}
 }finally{
  if(locked){try{await db.query('SELECT pg_advisory_unlock($1)',[LOCK]);}catch{destroy=true;}}
  db.release(destroy);
 }
}
