import http from 'node:http';
import fs from 'node:fs/promises';
import {randomUUID,randomBytes,scryptSync,createHash,timingSafeEqual} from 'node:crypto';
import pg from 'pg';

const PORT=Number(process.env.PORT||3000);
const pool=new pg.Pool({connectionString:process.env.DATABASE_URL,max:8,connectionTimeoutMillis:8000,idleTimeoutMillis:20000});
const sha=x=>createHash('sha256').update(String(x)).digest('hex');
const uuid=/^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const roles=new Set(['admin','author','client','legal','technical','approver','homologator']);
const roleFor=stage=>stage==='MINUTA'?'author':stage==='REVISAO_CLIENTE'?'client':stage.startsWith('REVISAO_JURIDICA_')?'legal':stage==='REVISAO_TECNICA'?'technical':stage==='APROVACAO'?'approver':stage==='HOMOLOGACAO'?'homologator':null;
const steps=(rounds,dest)=>['SOLICITACAO','MINUTA','REVISAO_CLIENTE','REVISAO_JURIDICA_1',...(rounds===2?['REVISAO_JURIDICA_2']:[]),'REVISAO_TECNICA','APROVACAO','HOMOLOGACAO',dest==='SIGN'?'AGUARDANDO_ASSINATURA':'AGUARDANDO_PUBLICACAO'];
function passwordHash(password){
 const salt=randomBytes(20).toString('hex'),derived=scryptSync(password,salt,64,{N:16384,r:8,p:1}).toString('hex');
 return salt+':'+derived;
}
function validPassword(password,stored){
 if(typeof password!=='string'||typeof stored!=='string')return false;
 const [salt,digest]=stored.split(':');if(!salt||!digest||!/^[0-9a-f]{128}$/.test(digest))return false;
 const actual=scryptSync(password,salt,64,{N:16384,r:8,p:1});
 return timingSafeEqual(actual,Buffer.from(digest,'hex'));
}
function send(res,status,data,headers={}){
 res.writeHead(status,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','X-Frame-Options':'DENY',...headers});
 res.end(JSON.stringify(data));
}
function fail(status,message){const e=new Error(message);e.status=status;throw e;}
async function bodyOf(req){
 let chunks=[],total=0;
 for await(const part of req){total+=part.length;if(total>300000)fail(413,'Solicitação acima do limite de 300 KB');chunks.push(part);}
 try{return JSON.parse(Buffer.concat(chunks).toString('utf8')||'{}');}catch{fail(400,'JSON inválido');}
}
function cookie(req,name){const match=String(req.headers.cookie||'').split(';').map(x=>x.trim()).find(x=>x.startsWith(name+'='));return match?decodeURIComponent(match.slice(name.length+1)):'';}
function isOriginAllowed(req){
 const origin=req.headers.origin;
 const base=process.env.PUBLIC_ORIGIN;
 if(!origin||!base)return false;
 return origin===base;
}
function setCookies(res,token,csrf){
 res.setHeader('Set-Cookie',[
  'ldw_session='+token+'; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=28800',
  'ldw_csrf='+csrf+'; Path=/; Secure; SameSite=Strict; Max-Age=28800'
 ]);
}
function clearCookies(res){
 res.setHeader('Set-Cookie',['ldw_session=; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=0','ldw_csrf=; Path=/; Secure; SameSite=Strict; Max-Age=0']);
}
async function session(req){
 const token=cookie(req,'ldw_session');
 if(!/^[0-9a-f]{64}$/.test(token))return null;
 const q=await pool.query("SELECT u.id,u.tenant_id,u.email,u.role,u.verified,u.active,u.must_change_password,s.csrf_hash FROM ldw_sessions s JOIN ldw_users u ON u.id=s.user_id WHERE s.token_hash=$1 AND s.expires_at>now() AND u.active=true",[sha(token)]);
 return q.rows[0]||null;
}
function requireCsrf(req,user){
 if(!isOriginAllowed(req))fail(403,'Origem não autorizada');
 const provided=req.headers['x-csrf-token'],csrf=cookie(req,'ldw_csrf');
 if(typeof provided!=='string'||!csrf||csrf!==provided||sha(provided)!==user.csrf_hash)fail(403,'Proteção CSRF inválida');
}
async function issueSession(res,user){
 const token=randomBytes(32).toString('hex'),csrf=randomBytes(24).toString('hex');
 await pool.query("INSERT INTO ldw_sessions(token_hash,csrf_hash,user_id,expires_at) VALUES($1,$2,$3,now()+interval '8 hours')",[sha(token),sha(csrf),user.id]);
 setCookies(res,token,csrf);
 send(res,200,{id:user.id,email:user.email,role:user.role,verified:user.verified,mustChangePassword:user.must_change_password,tenantId:user.tenant_id});
}
async function event(db,tenant,actor,kind,docId=null,detail={}){
 await db.query("INSERT INTO ldw_events(id,tenant_id,doc_id,actor_id,kind,detail) VALUES($1,$2,$3,$4,$5,$6)",[randomUUID(),tenant,docId,actor,kind,detail]);
}
function cleanEmail(v){return typeof v==='string'?v.trim().toLowerCase():'';}
function goodEmail(v){return v.length<=254&&/^[^\s@,;]+@[^\s@,;]+\.[^\s@,;]+$/.test(v);}
async function transact(fn){const db=await pool.connect();try{await db.query('BEGIN');const result=await fn(db);await db.query('COMMIT');return result;}catch(e){await db.query('ROLLBACK');throw e;}finally{db.release();}}
async function docRow(db,id,tenant){const q=await db.query('SELECT * FROM ldw_docs WHERE id=$1 AND tenant_id=$2 FOR UPDATE',[id,tenant]);if(!q.rowCount)fail(404,'Documento não encontrado');return q.rows[0];}
function docSummary(d){return {id:d.id,createdBy:d.created_by,title:d.title,kind:d.kind,description:d.description,rounds:d.rounds,destination:d.destination,stage:d.stages[d.stage_index],stageIndex:d.stage_index,stages:d.stages,status:d.status,version:d.version,bodyHash:d.body_hash,updatedAt:d.updated_at,createdAt:d.created_at};}
function checkRole(user,expected){return user.role===expected||(expected==='author'&&user.role==='admin');}
function extractDoc(body){
 const title=String(body.title||'').trim(),kind=String(body.kind||'').trim(),description=String(body.description||'').trim();
 const rounds=Number(body.rounds),destination=body.destination;
 const raw=Array.isArray(body.legalEmails)?body.legalEmails:[],emails=[...new Set(raw.map(cleanEmail))];
 if(title.length<3||title.length>180||kind.length<3||kind.length>180||description.length<10||description.length>12000||![1,2].includes(rounds)||!['SIGN','PUBLISH'].includes(destination)||emails.length<1||emails.length>8||emails.some(x=>!goodEmail(x)))fail(400,'Preencha título, tipo, descrição, revisores e destino válidos');
 return {title,kind,description,rounds,destination,emails};
}
async function route(req,res,url){
 const pathname=url.pathname,method=req.method;
 if(pathname==='/health'){send(res,200,{ok:true});return;}
 if(method==='GET'&&['/','/workspace.html','/workspace.js','/workspace.css'].includes(pathname)){
  const map={'/':'workspace.html','/workspace.html':'workspace.html','/workspace.js':'workspace.js','/workspace.css':'workspace.css'},file=map[pathname];
  const data=await fs.readFile(new URL('./'+file,import.meta.url));
  const type=file.endsWith('.html')?'text/html; charset=utf-8':file.endsWith('.js')?'text/javascript; charset=utf-8':'text/css; charset=utf-8';
  res.writeHead(200,{'Content-Type':type,'Cache-Control':'no-store','X-Robots-Tag':'noindex,nofollow','X-Frame-Options':'DENY','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','Content-Security-Policy':"default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"});res.end(data);return;
 }
 if(pathname==='/api/setup-status'&&method==='GET'){
  const q=await pool.query('SELECT count(*)::integer AS count FROM ldw_tenants');send(res,200,{needsSetup:q.rows[0].count===0});return;
 }
 if(pathname==='/api/setup'&&method==='POST'){
  if(!isOriginAllowed(req))fail(403,'Origem proibida');
  const body=await bodyOf(req),token=String(body.setupToken||'');
  if(!process.env.ADMIN_SETUP_TOKEN||token.length<20||!timingSafeEqual(Buffer.from(sha(token)),Buffer.from(sha(process.env.ADMIN_SETUP_TOKEN))))fail(403,'Token de instalação inválido');
  const email=cleanEmail(body.email),password=body.password,company=String(body.company||'').trim();
  if(!goodEmail(email)||typeof password!=='string'||password.length<14||password.length>200||company.length<3||company.length>180)fail(400,'Informe empresa, e-mail e senha de pelo menos 14 caracteres');
  const user=await transact(async db=>{
   await db.query('SELECT pg_advisory_xact_lock(82913764)');
   const count=await db.query('SELECT id FROM ldw_tenants FOR UPDATE');if(count.rowCount)fail(409,'Instalação já concluída');
   const tenant=randomUUID(),id=randomUUID();
   await db.query('INSERT INTO ldw_tenants(id,name) VALUES($1,$2)',[tenant,company]);
   await db.query("INSERT INTO ldw_users(id,tenant_id,email,password_hash,role,verified,must_change_password) VALUES($1,$2,$3,$4,'admin',true,false)",[id,tenant,email,passwordHash(password)]);
   await event(db,tenant,id,'INITIAL_SETUP',null,{company});
   return {id,tenant_id:tenant,email,role:'admin',verified:true,must_change_password:false};
  });await issueSession(res,user);return;
 }
 if(pathname==='/api/login'&&method==='POST'){
  if(!isOriginAllowed(req))fail(403,'Origem proibida');
  const body=await bodyOf(req),email=cleanEmail(body.email),password=body.password;
  if(!goodEmail(email)||typeof password!=='string'||password.length>200)fail(401,'Credenciais inválidas');
  const q=await pool.query('SELECT * FROM ldw_users WHERE email=$1 AND active=true ORDER BY created_at LIMIT 2',[email]);
  if(q.rowCount!==1||!validPassword(password,q.rows[0].password_hash))fail(401,'Credenciais inválidas');
  await issueSession(res,q.rows[0]);return;
 }
 const user=await session(req);
 if(!user)fail(401,'Faça login');
 if(pathname==='/api/me'&&method==='GET'){
  send(res,200,{id:user.id,email:user.email,role:user.role,verified:user.verified,mustChangePassword:user.must_change_password,tenantId:user.tenant_id});return;
 }
 if(method!=='GET'&&method!=='HEAD')requireCsrf(req,user);
 if(pathname==='/api/change-password'&&method==='POST'){
  const b=await bodyOf(req),current=b.currentPassword,next=b.newPassword;
  if(typeof current!=='string'||typeof next!=='string'||next.length<14||next.length>200||current===next)fail(400,'Informe a senha atual e uma nova senha de pelo menos 14 caracteres');
  await transact(async db=>{
   const q=await db.query('SELECT password_hash FROM ldw_users WHERE id=$1 AND tenant_id=$2 AND active=true FOR UPDATE',[user.id,user.tenant_id]);
   if(!q.rowCount||!validPassword(current,q.rows[0].password_hash))fail(403,'Senha atual inválida');
   await db.query('UPDATE ldw_users SET password_hash=$1,must_change_password=false WHERE id=$2 AND tenant_id=$3',[passwordHash(next),user.id,user.tenant_id]);
   await db.query('DELETE FROM ldw_sessions WHERE user_id=$1',[user.id]);
   await event(db,user.tenant_id,user.id,'PASSWORD_CHANGED');
  });
  await issueSession(res,{...user,must_change_password:false});return;
 }
 if(pathname==='/api/logout'&&method==='POST'){
  await pool.query('DELETE FROM ldw_sessions WHERE token_hash=$1',[sha(cookie(req,'ldw_session'))]);clearCookies(res);send(res,200,{ok:true});return;
 }
 // Deny by default after the exact authentication/password/logout handlers.
 // The flag is read from the database on every request, never trusted from a cookie.
 if(user.must_change_password)fail(403,'Substitua a senha temporária antes de continuar');
 if(pathname==='/api/users'&&method==='GET'){
  if(user.role!=='admin')fail(403,'Administrador exigido');
  const q=await pool.query('SELECT id,email,role,verified,active,created_at FROM ldw_users WHERE tenant_id=$1 ORDER BY created_at DESC LIMIT 200',[user.tenant_id]);send(res,200,{users:q.rows});return;
 }
 if(pathname==='/api/users'&&method==='POST'){
  if(user.role!=='admin')fail(403,'Administrador exigido');
  const b=await bodyOf(req),email=cleanEmail(b.email),role=b.role;
  if(!goodEmail(email)||!roles.has(role)||role==='admin')fail(400,'E-mail ou papel inválidos');
  const pwd=randomBytes(24).toString('base64url'),id=randomUUID();
  await transact(async db=>{await db.query('INSERT INTO ldw_users(id,tenant_id,email,password_hash,role) VALUES($1,$2,$3,$4,$5)',[id,user.tenant_id,email,passwordHash(pwd),role]);await event(db,user.tenant_id,user.id,'USER_CREATED',null,{newUserId:id,role});});
  send(res,201,{id,email,role,temporaryPassword:pwd,note:'Forneça a senha somente por canal seguro. A conta não está verificada até conferência do administrador.'});return;
 }
 const verify=pathname.match(/^\/api\/users\/([0-9a-f-]+)\/verify$/i);
 if(verify&&method==='POST'){
  if(user.role!=='admin'||!uuid.test(verify[1]))fail(403,'Administrador exigido');
  const b=await bodyOf(req);if(String(b.justification||'').trim().length<20)fail(400,'Justificativa mínima de 20 caracteres');
  await transact(async db=>{const q=await db.query('UPDATE ldw_users SET verified=true WHERE id=$1 AND tenant_id=$2 AND active=true RETURNING id',[verify[1],user.tenant_id]);if(!q.rowCount)fail(404,'Usuário não encontrado');await event(db,user.tenant_id,user.id,'USER_VERIFIED',null,{targetUserId:verify[1],justification:String(b.justification).trim().slice(0,500)});});
  send(res,200,{ok:true});return;
 }
 if(pathname==='/api/docs'&&method==='GET'){
  const q=await pool.query("SELECT d.* FROM ldw_docs d WHERE d.tenant_id=$1 AND (d.created_by=$2 OR $3='admin' OR EXISTS(SELECT 1 FROM ldw_assignments a WHERE a.doc_id=d.id AND a.tenant_id=$1 AND a.user_id=$2)) ORDER BY d.updated_at DESC LIMIT 100",[user.tenant_id,user.id,user.role]);
  send(res,200,{docs:q.rows.map(docSummary)});return;
 }
 if(pathname==='/api/docs'&&method==='POST'){
  if(!['admin','author'].includes(user.role))fail(403,'Autor exigido');
  const b=extractDoc(await bodyOf(req)),id=randomUUID(),stages=steps(b.rounds,b.destination),initial='MINUTA: preencher o texto e revisar todas as cláusulas antes do encaminhamento.',bodyHash=sha(initial);
  const doc=await transact(async db=>{
   const q=await db.query("INSERT INTO ldw_docs(id,tenant_id,created_by,title,kind,description,legal_emails,rounds,destination,stages,body,body_hash) VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12) RETURNING *",[id,user.tenant_id,user.id,b.title,b.kind,b.description,JSON.stringify(b.emails),b.rounds,b.destination,JSON.stringify(stages),initial,bodyHash]);
   await db.query('INSERT INTO ldw_versions(id,tenant_id,doc_id,version,body,body_hash,actor_id) VALUES($1,$2,$3,1,$4,$5,$6)',[randomUUID(),user.tenant_id,id,initial,bodyHash,user.id]);
   await event(db,user.tenant_id,user.id,'DOC_CREATED',id,{rounds:b.rounds,destination:b.destination});
   return q.rows[0];
  });
  send(res,201,{doc:docSummary(doc)});return;
 }
 const match=pathname.match(/^\/api\/docs\/([0-9a-f-]+)(?:\/(body|assign|decision))?$/i);
 if(match&&uuid.test(match[1])){
  const id=match[1],action=match[2];
  if(!action&&method==='GET'){
   const q=await pool.query('SELECT * FROM ldw_docs WHERE id=$1 AND tenant_id=$2',[id,user.tenant_id]);if(!q.rowCount)fail(404,'Documento não encontrado');
   const d=q.rows[0],allowed=user.role==='admin'||d.created_by===user.id||(await pool.query('SELECT 1 FROM ldw_assignments WHERE doc_id=$1 AND tenant_id=$2 AND user_id=$3',[id,user.tenant_id,user.id])).rowCount>0;
   if(!allowed)fail(403,'Acesso não autorizado ao documento');
   const [a,v,events]=await Promise.all([
    pool.query('SELECT stage,user_id FROM ldw_assignments WHERE doc_id=$1 AND tenant_id=$2',[id,user.tenant_id]),
    pool.query('SELECT version,body_hash,created_at FROM ldw_versions WHERE doc_id=$1 AND tenant_id=$2 ORDER BY version DESC LIMIT 30',[id,user.tenant_id]),
    pool.query('SELECT kind,detail,actor_id,created_at FROM ldw_events WHERE doc_id=$1 AND tenant_id=$2 ORDER BY created_at DESC LIMIT 50',[id,user.tenant_id])
   ]);
   send(res,200,{doc:{...docSummary(d),body:d.body,legalEmails:user.role==='admin'||d.created_by===user.id?d.legal_emails:undefined},assignments:a.rows,versions:v.rows,events:events.rows});return;
  }
  if(action==='body'&&method==='PUT'){
   const b=await bodyOf(req),content=String(b.body||'');
   if(content.length<40||content.length>180000)fail(400,'Documento entre 40 e 180.000 caracteres');
   const doc=await transact(async db=>{
    const d=await docRow(db,id,user.tenant_id);
    if(d.stage_index!==1||d.created_by!==user.id)fail(403,'Somente o autor pode alterar a minuta na etapa de elaboração');
    const version=d.version+1,hash=sha(content);
    await db.query('UPDATE ldw_docs SET body=$1,body_hash=$2,version=$3,revision_cycle=revision_cycle+1,status=$4,updated_at=now() WHERE id=$5 AND tenant_id=$6',[content,hash,version,'DRAFT',id,user.tenant_id]);
    await db.query('INSERT INTO ldw_versions(id,tenant_id,doc_id,version,body,body_hash,actor_id) VALUES($1,$2,$3,$4,$5,$6,$7)',[randomUUID(),user.tenant_id,id,version,content,hash,user.id]);
    await event(db,user.tenant_id,user.id,'DOCUMENT_VERSION_CREATED',id,{version,bodyHash:hash});return {version,hash};
   });send(res,200,doc);return;
  }
  if(action==='assign'&&method==='POST'){
   if(user.role!=='admin')fail(403,'Administrador exigido');
   const b=await bodyOf(req);
   if(!uuid.test(String(b.userId||'')))fail(400,'Usuário inválido');
   const result=await transact(async db=>{
    const d=await docRow(db,id,user.tenant_id);
    const stage=String(b.stage||''),needed=roleFor(stage);
    if(!needed||!d.stages.includes(stage)||stage==='MINUTA'||d.stages.indexOf(stage)<d.stage_index)fail(400,'Etapa não atribuível ou já concluída');
    const q=await db.query('SELECT id,email,role,verified FROM ldw_users WHERE id=$1 AND tenant_id=$2 AND active=true',[b.userId,user.tenant_id]);
    if(!q.rowCount||q.rows[0].role!==needed||!q.rows[0].verified)fail(403,'Revisor requer conta cadastrada e conferida');
    if(['APROVACAO','HOMOLOGACAO'].includes(stage)&&d.created_by===b.userId)fail(403,'Autor não pode aprovar sua própria minuta');
    if(needed==='legal'&&!d.legal_emails.includes(q.rows[0].email))fail(403,'E-mail jurídico fora da lista autorizada');
    await db.query('INSERT INTO ldw_assignments(id,tenant_id,doc_id,stage,user_id,assigned_by) VALUES($1,$2,$3,$4,$5,$6) ON CONFLICT(doc_id,stage) DO UPDATE SET user_id=excluded.user_id,assigned_by=excluded.assigned_by',[randomUUID(),user.tenant_id,id,stage,b.userId,user.id]);
    await event(db,user.tenant_id,user.id,'REVIEWER_ASSIGNED',id,{stage,reviewerId:b.userId});return {stage,userId:b.userId};
   });send(res,200,result);return;
  }
  if(action==='decision'&&method==='POST'){
   const b=await bodyOf(req),decision=b.decision,note=String(b.note||'').trim();
   if(!['APPROVE','CHANGES'].includes(decision)||note.length<10||note.length>2000)fail(400,'Decisão e justificativa de pelo menos 10 caracteres exigidas');
   const result=await transact(async db=>{
    const d=await docRow(db,id,user.tenant_id),stage=d.stages[d.stage_index],needed=roleFor(stage);
    if(!needed)fail(409,'Assinatura ou publicação exigem prestador externo e autorização');
    if(stage==='MINUTA'){if(d.created_by!==user.id)fail(403,'A etapa de minuta é exclusiva do autor');}
    else{
     if(user.role!==needed||!user.verified)fail(403,'Perfil validado exigido');
     const q=await db.query('SELECT 1 FROM ldw_assignments WHERE doc_id=$1 AND tenant_id=$2 AND stage=$3 AND user_id=$4',[id,user.tenant_id,stage,user.id]);
     if(!q.rowCount)fail(403,'Revisor não atribuído');
    }
    if(['APROVACAO','HOMOLOGACAO'].includes(stage)&&d.created_by===user.id)fail(403,'Segregação entre autor e aprovador');
    if(decision==='APPROVE'){
     if(stage==='MINUTA'&&(d.body.length<80||d.version<2))fail(409,'Minuta incompleta; salve uma versão editada antes de enviar');
     if(stage==='MINUTA'){
      const rework=await db.query("SELECT document_hash FROM ldw_decisions WHERE doc_id=$1 AND tenant_id=$2 AND action='CHANGES' ORDER BY created_at DESC LIMIT 1",[id,user.tenant_id]);
      if(rework.rowCount&&rework.rows[0].document_hash===d.body_hash)fail(409,'É necessário revisar o texto e salvar nova versão após a devolução');
     }
     if(d.stage_index>1){
      const prior=await db.query("SELECT stage,document_hash FROM ldw_decisions WHERE doc_id=$1 AND tenant_id=$2 AND revision_cycle=$3 AND action='APPROVE'",[id,user.tenant_id,d.revision_cycle]);
      for(const required of d.stages.slice(1,d.stage_index))if(!prior.rows.some(x=>x.stage===required&&x.document_hash===d.body_hash))fail(409,'Etapa anterior não revisada nesta versão');
     }
    }
    await db.query('INSERT INTO ldw_decisions(id,tenant_id,doc_id,stage,revision_cycle,actor_id,action,note,document_hash) VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9)',[randomUUID(),user.tenant_id,id,stage,d.revision_cycle,user.id,decision,note,d.body_hash]);
    const next=decision==='CHANGES'?1:d.stage_index+1;
    await db.query('UPDATE ldw_docs SET stage_index=$1,revision_cycle=revision_cycle+$2,status=$3,updated_at=now() WHERE id=$4 AND tenant_id=$5',[next,decision==='CHANGES'?1:0,decision==='CHANGES'?'REWORK':d.stages[next],id,user.tenant_id]);
    await event(db,user.tenant_id,user.id,decision==='CHANGES'?'REWORK_REQUESTED':'STAGE_APPROVED',id,{stage,note,hash:d.body_hash,revisionCycle:d.revision_cycle});
    return {nextStage:d.stages[next],version:d.version,decision};
   });send(res,200,result);return;
  }
 }
 fail(404,'Rota não encontrada');
}
let ready=false;
const server=http.createServer((req,res)=>{
 const url=new URL(req.url,'http://localhost');
 route(req,res,url).catch(e=>{console.error('request-error',e.status||500,e.message);if(!res.headersSent)send(res,e.status||500,{error:e.status?e.message:'Erro interno'});else res.end();});
});
const sql=await fs.readFile(new URL('./schema.sql',import.meta.url),'utf8');
await pool.query(sql);
ready=true;
server.listen(PORT,'0.0.0.0',()=>console.log('LegalDoc workspace listening on',PORT,'ready',ready));
