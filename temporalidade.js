import { randomUUID } from 'node:crypto';
const yyyyMmDd=x=>typeof x==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(x)&&!Number.isNaN(Date.parse(x+'T12:00:00Z'));
const normal=x=>typeof x==='string'&&x.trim().length>0&&x.length<=300;
function plusYears(iso,years){const [y,m,d]=iso.split('-').map(Number);const next=y+years;const day=Math.min(d,new Date(Date.UTC(next,m,0)).getUTCDate());return [next,String(m).padStart(2,'0'),String(day).padStart(2,'0')].join('-')}
export async function initTemporalidade(db){
 await db.query(`CREATE TABLE IF NOT EXISTS document_types(
 id uuid PRIMARY KEY,tenant_id uuid NOT NULL REFERENCES tenants(id),
 name text NOT NULL,code text,sigla text,trigger_event text NOT NULL DEFAULT 'document_date',
 current_years integer CHECK(current_years>=0),intermediate_years integer CHECK(intermediate_years>=0),
 disposition text NOT NULL DEFAULT 'review' CHECK(disposition IN ('review','permanent','eligible_for_disposal')),
 legal_basis text,source text,approved boolean NOT NULL DEFAULT false,created_at timestamptz DEFAULT now(),
 UNIQUE(tenant_id,name),UNIQUE(id,tenant_id)
 )`);
 await db.query("ALTER TABLE boxes ADD COLUMN IF NOT EXISTS description text");
 await db.query("ALTER TABLE boxes ADD COLUMN IF NOT EXISTS period_start date");
 await db.query("ALTER TABLE boxes ADD COLUMN IF NOT EXISTS period_end date");
 await db.query("ALTER TABLE boxes ADD COLUMN IF NOT EXISTS document_date date");
 await db.query("ALTER TABLE boxes ADD COLUMN IF NOT EXISTS trigger_date date");
 await db.query("ALTER TABLE boxes ADD COLUMN IF NOT EXISTS legal_hold boolean NOT NULL DEFAULT false");
 await db.query("ALTER TABLE boxes ADD COLUMN IF NOT EXISTS legal_hold_reason text");
}
export function registerTemporalidade(app,db,wrap){
 const Q=(sql,args)=>db.query(sql,args);
 app.get('/api/document-types',wrap(async(q,s)=>{
  const r=await Q('SELECT * FROM document_types WHERE tenant_id=$1 ORDER BY name',[q.user.tenant_id]);s.json(r.rows)
 }));
 app.post('/api/document-types',wrap(async(q,s)=>{
  if(q.user.role!=='admin')return s.sendStatus(403);
  const {name,code,sigla,trigger_event,current_years,intermediate_years,disposition,legal_basis,source,approved}=q.body||{};
  if(!normal(name)||!['document_date','period_end','event_date','termination','custom'].includes(trigger_event)||!['review','permanent','eligible_for_disposal'].includes(disposition)||![current_years,intermediate_years].every(n=>n===null||Number.isInteger(n)&&n>=0&&n<=200))return s.status(400).json({error:'Campos da temporalidade invalidos'});
  if(approved===true&&(!normal(legal_basis)||current_years===null||intermediate_years===null))return s.status(400).json({error:'Homologacao exige fundamentacao e prazos'});
  const r=await Q(`INSERT INTO document_types(id,tenant_id,name,code,sigla,trigger_event,current_years,intermediate_years,disposition,legal_basis,source,approved)
  VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12)
  ON CONFLICT(tenant_id,name) DO UPDATE SET code=excluded.code,sigla=excluded.sigla,trigger_event=excluded.trigger_event,current_years=excluded.current_years,intermediate_years=excluded.intermediate_years,disposition=excluded.disposition,legal_basis=excluded.legal_basis,source=excluded.source,approved=excluded.approved RETURNING *`,[randomUUID(),q.user.tenant_id,name.trim(),code||null,sigla||null,trigger_event,current_years,intermediate_years,disposition,legal_basis||null,source||null,approved===true]);
  s.json(r.rows[0])
 }));
 app.get('/api/temporalidade',wrap(async(q,s)=>{
  const [b,t]=await Promise.all([Q('SELECT id,code,doc_type,description,period_start,period_end,document_date,trigger_date,legal_hold,legal_hold_reason FROM boxes WHERE tenant_id=$1 ORDER BY created_at DESC LIMIT 1000',[q.user.tenant_id]),Q('SELECT * FROM document_types WHERE tenant_id=$1',[q.user.tenant_id])]);
  const typeMap=new Map(t.rows.map(x=>[x.name.toLocaleLowerCase('pt-BR'),x]));
  const today=new Date().toISOString().slice(0,10);
  s.json(b.rows.map(box=>{
   const rule=typeMap.get(box.doc_type.toLocaleLowerCase('pt-BR'));
   const base=rule?.trigger_event==='document_date'?box.document_date:rule?.trigger_event==='period_end'?box.period_end:box.trigger_date;
   const years=rule?.current_years!=null&&rule?.intermediate_years!=null?rule.current_years+rule.intermediate_years:null;
   const due=rule?.approved&&base&&years!==null?plusYears(String(base).slice(0,10),years):null;
   const status=box.legal_hold?'BLOQUEIO_LEGAL':!rule?'SEM_REGRA':!rule.approved?'AGUARDANDO_HOMOLOGACAO':!base?'AGUARDANDO_EVENTO':!due?'AGUARDANDO_PRAZO':rule.disposition==='permanent'?'GUARDA_PERMANENTE':today>=due?'PRAZO_ATINGIDO_REVISAO':'EM_GUARDA';
   return {...box,document_type_code:rule?.code||null,event:rule?.trigger_event||null,phase_current_years:rule?.current_years??null,phase_intermediate_years:rule?.intermediate_years??null,disposition:rule?.disposition||null,legal_basis:rule?.legal_basis||null,approved:rule?.approved||false,base_date:base||null,due_date:due,status};
  }))
 }));
}