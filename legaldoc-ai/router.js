import express from 'express';
import {randomUUID} from 'node:crypto';
import {sha256,nextState,fillTemplate} from './workflow.js';
import {analyzeDocumentText} from './analysis.js';

// Montar somente atras do middleware de autenticacao e CSRF do sistema anfitriao.
// Contrato: req.user={id,role,company_id}; pool=pg.Pool.
// Nenhuma chamada de assinatura e' realizada nesta fase.
export function legalDocRouter({pool}){
 const router=express.Router();
 const guard=(req,res,next)=>{
  if(!req.user?.id)return res.status(401).json({error:'Autenticacao exigida'});
  if(!req.user.company_id&&req.user.role!=='admin')return res.status(403).json({error:'Empresa nao autorizada'});
  next();
 };
 router.use(guard);
 const allowedCompany=(req,res)=>{
  const companyId=req.user.role==='admin'?req.body?.company_id||req.query.company_id:req.user.company_id;
  if(!/^[a-f0-9-]{36}$/i.test(String(companyId||''))){res.status(400).json({error:'Empresa obrigatoria'});return null;}
  if(req.user.role!=='admin'&&companyId!==req.user.company_id){res.status(403).json({error:'Acesso negado'});return null;}
  return companyId;
 };
 const handler=fn=>(req,res,next)=>Promise.resolve(fn(req,res)).catch(next);
 const log=(db,companyId,actor,event,documentId=null,templateId=null,detail={})=>db.query(
 'INSERT INTO legaldoc_audit(id,company_id,actor_id,event,document_id,template_id,detail) VALUES($1,$2,$3,$4,$5,$6,$7)',
 [randomUUID(),companyId,actor,event,documentId,templateId,detail]);
 router.post('/analyze-text',handler(async(req,res)=>{
  const companyId=allowedCompany(req,res);if(!companyId)return;
  if(typeof req.body?.text!=='string'||req.body.text.length>200000)return res.status(400).json({error:'Texto invalido ou excede limite'});
  res.json(analyzeDocumentText(req.body.text));
 }));
 router.get('/templates',handler(async(req,res)=>{
  const companyId=allowedCompany(req,res);if(!companyId)return;
  const q=await pool.query('SELECT id,title,version,status,body_sha256,created_at,approved_at FROM legaldoc_templates WHERE company_id=$1 ORDER BY created_at DESC LIMIT 200',[companyId]);res.json(q.rows);
 }));
 router.post('/templates',handler(async(req,res)=>{
  const companyId=allowedCompany(req,res);if(!companyId)return;
  const {title,body}=req.body||{};
  if(typeof title!=='string'||!title.trim()||title.length>180||typeof body!=='string'||body.length>200000||!body.trim())return res.status(400).json({error:'Titulo ou conteudo invalido'});
  const id=randomUUID(),db=await pool.connect();
  try{await db.query('BEGIN');await db.query('INSERT INTO legaldoc_templates(id,company_id,title,body,body_sha256,created_by) VALUES($1,$2,$3,$4,$5,$6)',[id,companyId,title.trim(),body,sha256(body),req.user.id]);await log(db,companyId,req.user.id,'template_created',null,id);await db.query('COMMIT');res.status(201).json({id,status:'DRAFT'});}
  catch(e){await db.query('ROLLBACK');throw e;}finally{db.release();}
 }));
 router.post('/templates/:id/approve',handler(async(req,res)=>{
  if(!['admin','manager'].includes(req.user.role))return res.status(403).json({error:'Perfil aprovador exigido'});
  const companyId=allowedCompany(req,res);if(!companyId)return;
  const db=await pool.connect();
  try{await db.query('BEGIN');const q=await db.query('SELECT * FROM legaldoc_templates WHERE id=$1 AND company_id=$2 FOR UPDATE',[req.params.id,companyId]);
   if(!q.rowCount){await db.query('ROLLBACK');return res.status(404).json({error:'Modelo nao encontrado'});}
   const model=q.rows[0];if(model.status!=='DRAFT'){await db.query('ROLLBACK');return res.status(409).json({error:'Modelo nao e rascunho'});}
   if(String(model.created_by)===String(req.user.id)){await db.query('ROLLBACK');return res.status(403).json({error:'Aprovacao independente obrigatoria'});}
   await db.query("UPDATE legaldoc_templates SET status='APPROVED',approved_by=$1,approved_at=now(),updated_at=now() WHERE id=$2",[req.user.id,model.id]);
   await log(db,companyId,req.user.id,'template_approved',null,model.id,{sha256:model.body_sha256});await db.query('COMMIT');res.json({id:model.id,status:'APPROVED'});
  }catch(e){await db.query('ROLLBACK');throw e;}finally{db.release();}
 }));
 router.post('/documents',handler(async(req,res)=>{
  const companyId=allowedCompany(req,res);if(!companyId)return;
  const {template_id,fields}=req.body||{};
  if(!fields||typeof fields!=='object'||Array.isArray(fields)||Object.keys(fields).length>100)return res.status(400).json({error:'Campos invalidos'});
  const db=await pool.connect();
  try{await db.query('BEGIN');const q=await db.query("SELECT * FROM legaldoc_templates WHERE id=$1 AND company_id=$2 AND status='APPROVED'",[template_id,companyId]);
   if(!q.rowCount){await db.query('ROLLBACK');return res.status(404).json({error:'Modelo aprovado nao encontrado'});}
   const {rendered,missing}=fillTemplate(q.rows[0].body,fields);
   if(missing.length){await db.query('ROLLBACK');return res.status(422).json({error:'Campos obrigatorios ausentes',missing});}
   const id=randomUUID();await db.query('INSERT INTO legaldoc_documents(id,company_id,template_id,title,content,content_sha256,created_by) VALUES($1,$2,$3,$4,$5,$6,$7)',[id,companyId,template_id,q.rows[0].title,rendered,sha256(rendered),req.user.id]);
   await log(db,companyId,req.user.id,'document_created',id,template_id);
   await db.query('COMMIT');res.status(201).json({id,state:'DRAFT',sha256:sha256(rendered)});
  }catch(e){await db.query('ROLLBACK');throw e;}finally{db.release();}
 }));
 router.post('/documents/:id/transition',handler(async(req,res)=>{
  const companyId=allowedCompany(req,res);if(!companyId)return;
  const action=req.body?.action;
  // Signature execution remains unavailable until an authenticated provider webhook is implemented.
  if(action==='record_verified_signature')return res.status(501).json({error:'Provedor e validacao de assinatura ainda nao integrados'});
  const db=await pool.connect();
  try{await db.query('BEGIN');const q=await db.query('SELECT * FROM legaldoc_documents WHERE id=$1 AND company_id=$2 FOR UPDATE',[req.params.id,companyId]);
   if(!q.rowCount){await db.query('ROLLBACK');return res.status(404).json({error:'Documento nao encontrado'});}
   const doc=q.rows[0];const state=nextState(doc.state,action);
   if(['approve','prepare_signature','archive'].includes(action)&&!['admin','manager'].includes(req.user.role)){await db.query('ROLLBACK');return res.status(403).json({error:'Perfil aprovador exigido'});}
   if(action==='approve'&&String(doc.created_by)===String(req.user.id)){await db.query('ROLLBACK');return res.status(403).json({error:'Revisao independente exigida'});}
   if(action==='prepare_signature'){await db.query('ROLLBACK');return res.status(501).json({error:'Integracao de assinatura ainda nao habilitada'});}
   await db.query('UPDATE legaldoc_documents SET state=$1,approved_by=CASE WHEN $2=\'approve\' THEN $3 ELSE approved_by END,updated_at=now() WHERE id=$4',[state,action,req.user.id,doc.id]);
   await log(db,companyId,req.user.id,'document_'+action,doc.id,doc.template_id,{from:doc.state,to:state});await db.query('COMMIT');res.json({id:doc.id,state});
  }catch(e){await db.query('ROLLBACK');throw e;}finally{db.release();}
 }));
 return router;
}
