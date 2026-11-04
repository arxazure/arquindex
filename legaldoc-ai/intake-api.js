// PRIVATE BACKEND ONLY. Requires authenticated req.user, CSRF, rate limits,
// PostgreSQL tenant controls and verified user directory. Never mount publicly.
import express from 'express';
import {randomUUID} from 'node:crypto';
import {questions,validateAnswer,buildStages} from './intake-flow.js';
import {roleFor,evaluateDecision,applyDecision} from './decision-policy.js';
const uuid=/^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const hash=/^[a-f0-9]{64}$/i;
const handler=fn=>(req,res,next)=>Promise.resolve(fn(req,res)).catch(next);
function parseAnswers(body){
 if(!body||typeof body!=='object'||Array.isArray(body))return null;
 const result={};
 for(const q of questions){
  const raw=q.key==='legalEmails'&&Array.isArray(body[q.key])?body[q.key].join(','):body[q.key];
  const v=validateAnswer(q,raw);if(!v.ok)return null;result[q.key]=v.value;
 }
 return result;
}
export function intakeApi({pool,lookupVerifiedMember,getCurrentDocumentVersion}){
 if(!pool?.connect)throw Error('PostgreSQL pool required');
 const api=express.Router();
 api.use((req,res,next)=>{
  if(!uuid.test(String(req.user?.id||''))||!uuid.test(String(req.user?.company_id||'')))
   return res.status(401).json({error:'Sessao de empresa exigida'});
  next();
 });
 api.post('/requests',handler(async(req,res)=>{
  const values=parseAnswers(req.body);
  if(!values)return res.status(400).json({error:'Solicitacao incompleta ou invalida'});
  const id=randomUUID(),company=req.user.company_id,actor=req.user.id,stages=buildStages(values);
  const db=await pool.connect();
  try{
   await db.query('BEGIN');
   await db.query("INSERT INTO legaldoc_requests(id,company_id,created_by,client_organisation_label,technical_role_label,approver_role_label,document_type,description,review_rounds,outcome,status) VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,'IN_PROGRESS')",
    [id,company,actor,values.customer,values.technical,values.approver,values.documentType,values.request,values.rounds,values.outcome==='ASSINAR'?'SIGN':'PUBLISH']);
   for(const email of values.legalEmails)
    await db.query("INSERT INTO legaldoc_request_reviewers(request_id,company_id,email,role) VALUES($1,$2,$3,'LEGAL')",[id,company,email]);
   for(const [i,stage] of stages.entries()){
    await db.query("INSERT INTO legaldoc_request_stages(id,request_id,company_id,step_number,stage,status,assigned_user_id,completed_by,completed_at) VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9)",
    [randomUUID(),id,company,i,stage,i===0?'APPROVED':i===1?'ACTIVE':'PENDING',
      ['SOLICITACAO','MINUTA','REVISAO_CLIENTE'].includes(stage)?actor:null,i===0?actor:null,i===0?new Date():null]);
   }
   await db.query("INSERT INTO legaldoc_request_events(id,request_id,company_id,actor_id,event,detail) VALUES($1,$2,$3,$4,'REQUEST_CREATED',$5)",[randomUUID(),id,company,actor,{reviewRounds:values.rounds,reviewers:values.legalEmails.length,outcome:values.outcome}]);
   await db.query('COMMIT');res.status(201).json({id,status:'IN_PROGRESS',nextStage:'MINUTA',emailInvitations:'NOT_SENT'});
  }catch(error){await db.query('ROLLBACK');throw error;}finally{db.release();}
 }));
 api.get('/requests/:id',handler(async(req,res)=>{
  if(!uuid.test(req.params.id))return res.status(400).json({error:'ID invalido'});
  const company=req.user.company_id;
  const q=await pool.query("SELECT r.id,r.document_type,r.status,r.review_rounds,r.outcome,r.created_at FROM legaldoc_requests r WHERE r.id=$1 AND r.company_id=$2 AND (r.created_by=$3 OR EXISTS(SELECT 1 FROM legaldoc_request_stages s WHERE s.request_id=r.id AND s.company_id=$2 AND s.assigned_user_id=$3) OR $4 IN ('tenant_admin','compliance_admin'))",[req.params.id,company,req.user.id,req.user.role]);
  if(!q.rowCount)return res.status(404).json({error:'Nao encontrado'});
  const stages=await pool.query("SELECT id,step_number,stage,status,assigned_user_id,completed_at FROM legaldoc_request_stages WHERE request_id=$1 AND company_id=$2 ORDER BY step_number",[req.params.id,company]);
  res.json({request:q.rows[0],stages:stages.rows});
 }));
 api.post('/requests/:id/stages/:stageId/assign',handler(async(req,res)=>{
  if(!['tenant_admin','compliance_admin'].includes(req.user.role))return res.status(403).json({error:'Administrador da empresa exigido'});
  if(!uuid.test(req.params.id)||!uuid.test(req.params.stageId)||!uuid.test(String(req.body?.userId||'')))return res.status(400).json({error:'IDs invalidos'});
  if(typeof lookupVerifiedMember!=='function')return res.status(503).json({error:'Diretorio de identidades verificado indisponivel'});
  const company=req.user.company_id,db=await pool.connect();
  try{
   await db.query('BEGIN');
   const q=await db.query("SELECT s.*,r.created_by FROM legaldoc_request_stages s JOIN legaldoc_requests r ON r.id=s.request_id AND r.company_id=s.company_id WHERE s.id=$1 AND s.request_id=$2 AND s.company_id=$3 FOR UPDATE OF s",[req.params.stageId,req.params.id,company]);
   if(!q.rowCount){await db.query('ROLLBACK');return res.status(404).json({error:'Etapa inexistente'});}
   const stage=q.rows[0],role=roleFor(stage.stage);
   if(!role||['signer','publisher'].includes(role)){await db.query('ROLLBACK');return res.status(409).json({error:'Etapa nao atribuivel aqui'});}
   const member=await lookupVerifiedMember({companyId:company,userId:req.body.userId,db});
   if(!member?.verified||member.role!==role){await db.query('ROLLBACK');return res.status(403).json({error:'Usuario verificado com perfil correspondente exigido'});}
   if(role==='legal'){
    const invited=await db.query("SELECT 1 FROM legaldoc_request_reviewers WHERE request_id=$1 AND company_id=$2 AND role='LEGAL' AND lower(email)=lower($3)",[req.params.id,company,member.email||'']);
    if(!invited.rowCount){await db.query('ROLLBACK');return res.status(403).json({error:'Revisor juridico deve ter email previamente autorizado'});}
   }
   if(['approver','homologator'].includes(role)&&String(stage.created_by)===String(req.body.userId)){await db.query('ROLLBACK');return res.status(403).json({error:'Segregacao entre autor e aprovador'});}
   if(!['PENDING','ACTIVE'].includes(stage.status)){await db.query('ROLLBACK');return res.status(409).json({error:'Etapa encerrada'});}
   await db.query("UPDATE legaldoc_request_stages SET assigned_user_id=$1 WHERE id=$2 AND company_id=$3",[req.body.userId,stage.id,company]);
   if(role==='legal')await db.query("UPDATE legaldoc_request_reviewers SET reviewer_user_id=$1,verified_at=now() WHERE request_id=$2 AND company_id=$3 AND role='LEGAL' AND lower(email)=lower($4)",[req.body.userId,req.params.id,company,member.email]);
   await db.query("INSERT INTO legaldoc_request_events(id,request_id,company_id,actor_id,event,detail) VALUES($1,$2,$3,$4,'STAGE_ASSIGNED',$5)",[randomUUID(),req.params.id,company,req.user.id,{stageId:stage.id,role}]);
   await db.query('COMMIT');res.json({stageId:stage.id,assignment:'RECORDED_NOT_NOTIFIED'});
  }catch(error){await db.query('ROLLBACK');throw error;}finally{db.release();}
 }));
 api.post('/requests/:id/decision',handler(async(req,res)=>{
  if(!uuid.test(req.params.id))return res.status(400).json({error:'ID invalido'});
  if(typeof getCurrentDocumentVersion!=='function'||typeof lookupVerifiedMember!=='function')return res.status(503).json({error:'Identidade e repositorio versionado obrigatorios'});
  const company=req.user.company_id,db=await pool.connect();
  try{
   await db.query('BEGIN');
   const q=await db.query("SELECT * FROM legaldoc_requests WHERE id=$1 AND company_id=$2 FOR UPDATE",[req.params.id,company]);
   if(!q.rowCount){await db.query('ROLLBACK');return res.status(404).json({error:'Nao encontrado'});}
   const steps=await db.query("SELECT * FROM legaldoc_request_stages WHERE request_id=$1 AND company_id=$2 ORDER BY step_number FOR UPDATE",[req.params.id,company]);
   const index=steps.rows.findIndex(s=>s.status==='ACTIVE');
   if(index<0){await db.query('ROLLBACK');return res.status(409).json({error:'Etapa ativa inexistente'});}
   const stage=steps.rows[index];
   if(String(stage.assigned_user_id)!==String(req.user.id)){await db.query('ROLLBACK');return res.status(403).json({error:'Revisor designado e autenticado exigido'});}
   const member=await lookupVerifiedMember({db,companyId:company,userId:req.user.id});
   if(!member?.verified||member.role!==roleFor(stage.stage)){await db.query('ROLLBACK');return res.status(403).json({error:'Identidade ou papel nao validos'});}
   const document=await getCurrentDocumentVersion({db,companyId:company,requestId:req.params.id});
   if(!hash.test(String(document?.sha256||''))||!document?.versionId){await db.query('ROLLBACK');return res.status(409).json({error:'Documento armazenado e versionado obrigatorio'});}
   if(index>1&&steps.rows.slice(1,index).some(s=>s.status!=='APPROVED'||s.document_version_hash!==document.sha256)){
    await db.query('ROLLBACK');return res.status(409).json({error:'Versao alterada: revisoes anteriores precisam ser repetidas'});
   }
   const result=evaluateDecision({stage:stage.stage,decision:req.body?.decision,actorRole:req.user.role,note:req.body?.note,documentHash:document.sha256,authorId:document.authorUserId||q.rows[0].created_by,actorId:req.user.id});
   if(!result.ok){await db.query('ROLLBACK');return res.status(403).json({error:result.error});}
   const next=applyDecision({stages:steps.rows.map(s=>s.stage),index,decision:req.body.decision});
   if(!next.ok){await db.query('ROLLBACK');return res.status(409).json({error:next.error});}
   if(req.body.decision==='request_changes'){
    await db.query("UPDATE legaldoc_request_stages SET status='PENDING',completed_by=NULL,completed_at=NULL,document_version_hash=NULL WHERE company_id=$1 AND request_id=$2 AND step_number>$3",[company,req.params.id,next.index]);
    await db.query("UPDATE legaldoc_request_stages SET status='ACTIVE',completed_by=NULL,completed_at=NULL,document_version_hash=NULL WHERE id=$1 AND company_id=$2",[steps.rows[next.index].id,company]);
   }else{
    await db.query("UPDATE legaldoc_request_stages SET status='APPROVED',completed_by=$1,completed_at=now(),document_version_hash=$2 WHERE id=$3 AND company_id=$4",[req.user.id,document.sha256,stage.id,company]);
    await db.query("UPDATE legaldoc_request_stages SET status='ACTIVE' WHERE id=$1 AND company_id=$2",[steps.rows[next.index].id,company]);
   }
   await db.query("INSERT INTO legaldoc_request_events(id,request_id,company_id,actor_id,event,detail) VALUES($1,$2,$3,$4,$5,$6)",
   [randomUUID(),req.params.id,company,req.user.id,req.body.decision==='approve'?'STAGE_APPROVED':'REWORK_REQUESTED',{stage:stage.stage,versionId:document.versionId,sha256:document.sha256,note:req.body.note.trim()}]);
   await db.query('COMMIT');res.json({stage:steps.rows[next.index].stage,status:next.state});
  }catch(error){await db.query('ROLLBACK');throw error;}finally{db.release();}
 }));
 return api;
}
