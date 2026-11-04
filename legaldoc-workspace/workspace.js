const $=id=>document.getElementById(id);
let me=null,docId=null,users=[],selected=null;
function notify(text,error=false){const el=$('notice');el.style.display='block';el.style.color=error?'#ffc5a6':'#b4f0da';el.textContent=text;}
function csrf(){const part=document.cookie.split(';').map(x=>x.trim()).find(x=>x.startsWith('ldw_csrf='));return part?decodeURIComponent(part.slice(9)):'';}
async function api(url,method='GET',payload){
 const options={method,credentials:'same-origin',headers:{}};
 if(payload!==undefined){options.headers['Content-Type']='application/json';options.body=JSON.stringify(payload);}
 if(method!=='GET')options.headers['X-CSRF-Token']=csrf();
 const r=await fetch(url,options);let data={};try{data=await r.json();}catch{}
 if(!r.ok)throw Error(data.error||('HTTP '+r.status));return data;
}
async function safe(fn){try{await fn();}catch(e){notify(e.message,true);}}
const text=(tag,val,cls)=>{const el=document.createElement(tag);if(val!==undefined)el.textContent=String(val);if(cls)el.className=cls;return el;};
function button(label,onclick,cls){const el=text('button',label,cls);el.type='button';el.addEventListener('click',()=>safe(onclick));return el;}
function detail(name,val){const el=text('p');el.append(text('strong',name+': '),document.createTextNode(String(val??'—')));return el;}
function formatDate(v){return v?new Date(v).toLocaleString('pt-BR'):'—';}
function roleFor(stage){if(stage==='MINUTA')return 'author';if(stage==='REVISAO_CLIENTE')return 'client';if(stage.startsWith('REVISAO_JURIDICA_'))return 'legal';if(stage==='REVISAO_TECNICA')return 'technical';if(stage==='APROVACAO')return 'approver';if(stage==='HOMOLOGACAO')return 'homologator';return null;}
function displayStage(s){return ({SOLICITACAO:'Solicitação',MINUTA:'Elaboração da minuta',REVISAO_CLIENTE:'Conferência do cliente',REVISAO_JURIDICA_1:'Revisão jurídica 1',REVISAO_JURIDICA_2:'Revisão jurídica 2',REVISAO_TECNICA:'Revisão técnica',APROVACAO:'Aprovação',HOMOLOGACAO:'Homologação',AGUARDANDO_ASSINATURA:'Aguardando assinatura',AGUARDANDO_PUBLICACAO:'Aguardando publicação'})[s]||s;}
async function init(){
 let login=null;try{login=await api('/api/me');}catch{}
 if(!login){
  $('auth').hidden=false;$('dashboard').hidden=true;$('password-panel').hidden=true;$('logout').hidden=true;
  const s=await api('/api/setup-status');$('setup-panel').hidden=!s.needsSetup;$('login-panel').hidden=s.needsSetup;return;
 }
 me=login;$('auth').hidden=true;$('logout').hidden=false;$('password-panel').hidden=!login.mustChangePassword;$('dashboard').hidden=!!login.mustChangePassword;
 if(login.mustChangePassword){$('identity').textContent=login.email+' · Senha temporária';return;}$('identity').textContent=login.email+' ('+login.role+')';
 $('new-panel').hidden=!['admin','author'].includes(login.role);$('user-panel').hidden=login.role!=='admin';
 await refresh();if(login.role==='admin')await loadUsers();
}
async function refresh(){const r=await api('/api/docs');const list=$('doc-list');list.replaceChildren();
 if(!r.docs.length)list.append(text('p','Nenhum documento disponível.','muted'));
 for(const d of r.docs){
  const b=button(d.title+ ' | '+displayStage(d.stage),()=>openDoc(d.id),'doc-item');list.append(b);
 }
 if(docId)await openDoc(docId);
}
async function loadUsers(){const r=await api('/api/users');users=r.users;const el=$('users-list');el.replaceChildren();
 for(const u of users){const row=text('div',undefined,'user');const info=text('div');info.append(text('strong',u.email),text('div',u.role+' · '+(u.verified?'Verificado':'Não verificado'),'muted'));row.append(info);
 if(!u.verified)row.append(button('Registrar verificação',async()=>{const justification=prompt('Descreva como confirmou a identidade da pessoa (mínimo 20 caracteres):');if(!justification)return;await api('/api/users/'+u.id+'/verify','POST',{justification});notify('Usuário habilitado após conferência registrada.');await loadUsers();},'secondary'));
 el.append(row);
 }}
async function openDoc(id){
 const r=await api('/api/docs/'+id);docId=id;selected=r;const d=r.doc,host=$('doc-detail');host.replaceChildren();
 const head=text('div',undefined,'doc-header'),left=text('div');left.append(text('h2',d.title),text('div','Versão '+d.version+' · '+d.kind,'muted'));head.append(left,text('span',displayStage(d.stage),'pill'));host.append(head);
 host.append(detail('Destino',d.destination==='SIGN'?'Assinatura':'Publicação'),detail('Revisões jurídicas',d.rounds),detail('Hash SHA-256',d.bodyHash));
 const stages=text('ol');d.stages.forEach((s,i)=>{const li=text('li',displayStage(s)+(i===d.stageIndex?' — atual':i<d.stageIndex?' — concluída nesta sequência':' — futura'));if(i===d.stageIndex)li.style.color='#87edf4';stages.append(li);});host.append(stages);
 const label=text('label','Texto integral da minuta'),area=text('textarea');area.id='doc-body';area.value=d.body;const canEdit=d.stage==='MINUTA'&&d.createdBy===me.id;
 area.readOnly=!canEdit;host.append(label,area);
 if(canEdit){
  host.append(button('Salvar nova versão',async()=>{await api('/api/docs/'+id+'/body','PUT',{body:area.value});notify('Nova versão salva.');await openDoc(id);},'secondary'));
  const upload=document.createElement('input');upload.type='file';upload.accept='.json,application/json';upload.id='project-import';upload.style.display='none';host.append(upload);
  host.append(button('Importar projeto do construtor (.json)',async()=>upload.click(),'secondary'));
  upload.addEventListener('change',()=>safe(async()=>{
   const file=upload.files?.[0];if(!file)return;if(file.size>250000)throw Error('Projeto excede 250 KB.');
   const parsed=JSON.parse(await file.text());
   if(!Array.isArray(parsed.sections)||parsed.sections.length>100||!parsed.sections.every(s=>typeof s.title==='string'&&typeof s.body==='string'&&s.title.length<=180&&s.body.length<=20000))throw Error('Formato de projeto inválido.');
   if(!parsed.fields||typeof parsed.fields!=='object'||Array.isArray(parsed.fields))throw Error('Campos inválidos.');
   const raw=parsed.sections.map((section,i)=>{
    const value=section.body.replace(/\\{\\{\\s*([A-Za-z][A-Za-z0-9_]{0,63})\\s*\\}\\}/g,(all,key)=>typeof parsed.fields[key]==='string'?parsed.fields[key].slice(0,300):all);
    return (i+1)+'. '+section.title+'\\n'+value;
   }).join('\\n\\n');
   if(raw.length<40||raw.length>180000)throw Error('Documento montado fora dos limites.');
   area.value=raw;notify('Projeto carregado no editor. Revise e clique em Salvar nova versão.');
   upload.value='';
  }));
 }
 host.append(button('Baixar texto da minuta',async()=>{const file=new Blob([area.value],{type:'text/plain;charset=utf-8'}),url=URL.createObjectURL(file),a=document.createElement('a');a.href=url;a.download='legaldoc-minuta-'+id+'.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),5000);},'secondary'));
 const role=roleFor(d.stage);if(role){host.append(text('h3','Parecer da etapa: '+displayStage(d.stage)));const note=text('textarea');note.placeholder='Justificativa e evidências (mínimo 10 caracteres)';note.rows=3;host.append(note);
 host.append(button('Aprovar etapa',async()=>{const r=await api('/api/docs/'+id+'/decision','POST',{decision:'APPROVE',note:note.value});notify('Etapa registrada. Próxima: '+displayStage(r.nextStage));await refresh();}));
 if(d.stage!=='MINUTA')host.append(button('Solicitar correções',async()=>{const r=await api('/api/docs/'+id+'/decision','POST',{decision:'CHANGES',note:note.value});notify('Devolvido para correções.');await refresh();},'secondary'));
 }else{host.append(text('p','Assinatura ou publicação bloqueada até integrar o prestador e validar o documento.','muted'));}
 if(me.role==='admin'&&role&&d.stage!=='MINUTA'){
  host.append(text('h3','Designar participante'));const select=text('select');const eligible=users.filter(u=>u.verified&&u.role===role&&(role!=='legal'||(d.legalEmails||[]).includes(u.email)));
  const first=text('option','Selecione um participante verificado');first.value='';select.append(first);
  for(const u of eligible){const o=text('option',u.email);o.value=u.id;select.append(o);}host.append(select);
  host.append(button('Atribuir à etapa',async()=>{if(!select.value)throw Error('Selecione um participante');await api('/api/docs/'+id+'/assign','POST',{stage:d.stage,userId:select.value});notify('Responsável atribuído.');await openDoc(id);},'secondary'));
 }
 if(r.assignments.length){const box=text('div');box.append(text('h3','Responsáveis designados'));for(const a of r.assignments){const user=users.find(x=>x.id===a.user_id);box.append(detail(displayStage(a.stage),user?.email||a.user_id));}host.append(box);}
 const events=text('div');events.append(text('h3','Trilha de eventos'));for(const ev of r.events.slice(0,20)){const row=text('div',undefined,'event');row.append(text('strong',ev.kind+' · '+formatDate(ev.created_at)));if(ev.detail)row.append(text('p',JSON.stringify(ev.detail)));events.append(row);}host.append(events);
}
$('setup-submit').addEventListener('click',()=>safe(async()=>{const r=await api('/api/setup','POST',{setupToken:$('setup-token').value,email:$('setup-email').value,password:$('setup-password').value,company:$('company').value});notify('Administrador criado.');await init();}));
$('login-submit').addEventListener('click',()=>safe(async()=>{await api('/api/login','POST',{email:$('login-email').value,password:$('login-password').value});notify('Acesso autorizado.');await init();}));
$('logout').addEventListener('click',()=>safe(async()=>{await api('/api/logout','POST',{});me=null;docId=null;selected=null;notify('Sessão encerrada.');await init();}));
$('refresh').addEventListener('click',()=>safe(refresh));
$('create-doc').addEventListener('click',()=>safe(async()=>{const b={title:$('new-title').value,kind:$('new-kind').value,description:$('new-description').value,legalEmails:$('new-emails').value.split(/[;,]/).map(x=>x.trim()).filter(Boolean),rounds:Number($('new-rounds').value),destination:$('new-dest').value};const result=await api('/api/docs','POST',b);notify('Documento criado.');await refresh();await openDoc(result.doc.id);}));
$('create-user').addEventListener('click',()=>safe(async()=>{const u=await api('/api/users','POST',{email:$('user-email').value,role:$('user-role').value});const box=$('one-time-password');box.hidden=false;box.textContent='Senha temporária do participante '+u.email+': '+u.temporaryPassword+' — copie e envie somente por canal seguro. Não será exibida novamente.';await loadUsers();notify('Participante criado, aguardando confirmação de identidade.');}));
safe(init);

$('password-submit').addEventListener('click',()=>safe(async()=>{
 await api('/api/change-password','POST',{currentPassword:$('old-password').value,newPassword:$('new-password').value});
 $('old-password').value='';$('new-password').value='';notify('Senha pessoal atualizada.');await init();
}));
