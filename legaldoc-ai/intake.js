// Guided local-only workflow. Production actions must be server-authorized; this is NOT real approval.
export const questions=[
 {key:'customer',label:'Qual é a razão social ou identificação fictícia do solicitante?',max:160},
 {key:'documentType',label:'Que documento deseja elaborar (contrato, política, termo, formulário, procedimento, PGR, auditoria etc.)?',max:180},
 {key:'request',label:'Descreva a finalidade, partes envolvidas, cláusulas desejadas, contexto de negócio e os documentos de referência.',max:3000},
 {key:'legalEmails',label:'Quais e-mails do jurídico devem participar da revisão? Separe por vírgula. Use dados de teste nesta demonstração.',max:500},
 {key:'rounds',label:'Quantas revisões jurídicas deseja: 1 ou 2?',max:1},
 {key:'technical',label:'Quem fará a revisão técnica (função, departamento ou responsável)?',max:160},
 {key:'approver',label:'Quem será o responsável pela aprovação e homologação (função ou perfil)?',max:160},
 {key:'outcome',label:'Depois da homologação: PUBLICAR ou ASSINAR?',max:8}
];
export const emailPattern=/^[^\s@,;]+@[^\s@,;]+\.[^\s@,;]+$/;
export function validateAnswer(question,input){
 const answer=String(input??'').trim();
 if(!answer||answer.length>question.max)return {ok:false,message:'Resposta obrigatória ou acima do limite.'};
 if(question.key==='legalEmails'){
  const emails=answer.split(/[;,]/).map(x=>x.trim().toLowerCase());
  if(emails.length>8||emails.some(x=>!emailPattern.test(x)))return {ok:false,message:'Informe de 1 a 8 endereços válidos, separados por vírgulas.'};
  return {ok:true,value:[...new Set(emails)]};
 }
 if(question.key==='rounds'&&!['1','2'].includes(answer))return {ok:false,message:'Escolha 1 ou 2 revisões.'};
 if(question.key==='outcome'&&!['PUBLICAR','ASSINAR'].includes(answer.toUpperCase()))return {ok:false,message:'Escolha PUBLICAR ou ASSINAR.'};
 return {ok:true,value:question.key==='rounds'?Number(answer):question.key==='outcome'?answer.toUpperCase():answer};
}
export function buildStages(data){
 const n=data.rounds===2?2:1;
 return [
  'SOLICITACAO','MINUTA','REVISAO_CLIENTE',
  ...Array.from({length:n},(_,i)=>'REVISAO_JURIDICA_'+(i+1)),
  'REVISAO_TECNICA','APROVACAO','HOMOLOGACAO',
  data.outcome==='ASSINAR'?'AGUARDANDO_ASSINATURA':'AGUARDANDO_PUBLICACAO'
 ];
}
export function nextLocalStage(stages,index){
 if(!Array.isArray(stages)||!Number.isInteger(index)||index<0||index>=stages.length)return -1;
 return index+1<stages.length?index+1:index;
}
const $=id=>document.getElementById(id);
const history=$('chat-history'),input=$('answer'),form=$('chat-form');
let answerIndex=0,answers={},stages=[],stageIndex=-1,events=[];
function element(tag,text,cls){const x=document.createElement(tag);if(text!==undefined)x.textContent=String(text);if(cls)x.className=cls;return x;}
function message(text,from){const div=element('div',text,'bubble '+from);history.append(div);history.scrollTop=history.scrollHeight;}
function event(text){events.push({date:new Date().toISOString(),event:text,kind:'SIMULATION_ONLY'});render();}
function ask(){if(answerIndex<questions.length){message(questions[answerIndex].label,'assistant');input.disabled=false;$('next').disabled=false;input.focus();}else{message('Solicitação estruturada. Confira os dados, exporte para controle e simule as etapas no painel ao lado. Não houve comunicação externa.','assistant');input.disabled=true;$('next').disabled=true;stages=buildStages(answers);stageIndex=0;event('Solicitação de teste preparada (sem envio a terceiros).');}}
function begin(){answerIndex=0;answers={};stages=[];stageIndex=-1;events=[];history.replaceChildren();input.value='';$('chat-error').textContent='';render();message('Sou o assistente guiado de elaboração de documentos da Arquindex. Esta demonstração não usa IA generativa nem envia informações ao servidor.','assistant');ask();}
function label(key){return ({
SOLICITACAO:'Solicitação recebida',MINUTA:'Elaboração da minuta',REVISAO_CLIENTE:'Revisão pelo cliente',REVISAO_JURIDICA_1:'1ª revisão jurídica',REVISAO_JURIDICA_2:'2ª revisão jurídica',REVISAO_TECNICA:'Revisão técnica',APROVACAO:'Aprovação',HOMOLOGACAO:'Homologação',AGUARDANDO_ASSINATURA:'Encaminhamento para assinatura',AGUARDANDO_PUBLICACAO:'Encaminhamento para publicação'
})[key]||key;}
function render(){
 const summary=$('summary'),list=$('workflow-stages'),actions=$('workflow-actions'),log=$('event-log');list.replaceChildren();actions.replaceChildren();log.replaceChildren();
 summary.textContent=Object.keys(answers).length?('Solicitante: '+(answers.customer||'—')+' | Documento: '+(answers.documentType||'—')+' | Revisões: '+(answers.rounds||'—')+' | Jurídico: '+(Array.isArray(answers.legalEmails)?answers.legalEmails.length:0)+' destinatário(s) | Destino: '+(answers.outcome||'—')):'Complete as perguntas para estruturar o fluxo.';
 for(let i=0;i<stages.length;i++){const li=element('li',label(stages[i])+(i<stageIndex?' · Simulado':i===stageIndex?' · Etapa atual':' · Pendente'));li.className=i===stageIndex?'current':i<stageIndex?'completed':'';list.append(li);}
 if(stageIndex>=0){const current=stages[stageIndex],terminal=stageIndex===stages.length-1;const p=element('p','Etapa simulada: '+label(current));actions.append(p);if(!terminal){const advance=element('button','Registrar conclusão simulada e avançar','button');advance.type='button';advance.addEventListener('click',()=>{event('Etapa simulada concluída: '+label(current));stageIndex=nextLocalStage(stages,stageIndex);render();});actions.append(advance);}else{actions.append(element('p','Fim do fluxo demonstrativo. Em produção, esta etapa dependerá de publicação autorizada ou assinatura verificada.','note'));}}
 for(const e of events.slice(-15))log.append(element('p',new Date(e.date).toLocaleString('pt-BR')+' · '+e.event));
}
form.addEventListener('submit',e=>{e.preventDefault();if(answerIndex>=questions.length)return;const q=questions[answerIndex],v=validateAnswer(q,input.value);if(!v.ok){$('chat-error').textContent=v.message;return;}$('chat-error').textContent='';answers[q.key]=v.value;message(q.key==='legalEmails'?'[e-mails informados para roteamento futuro, sem envio]':input.value.trim(),'client');input.value='';answerIndex++;render();ask();});
$('restart').addEventListener('click',()=>{if(Object.keys(answers).length&&!confirm('Reiniciar a solicitação local? Exporte os dados antes se necessário.'))return;begin();});
$('export-request').addEventListener('click',()=>{const payload={schemaVersion:1,exportedAt:new Date().toISOString(),status:'LOCAL_DEMONSTRATION_NOT_APPROVED',request:answers,workflow:{stages,currentIndex:stageIndex,events}};const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='legaldoc-solicitacao-demo.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),3000);});
begin();