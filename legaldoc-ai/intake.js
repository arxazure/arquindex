import {questions,validateAnswer,buildStages,nextLocalStage} from './intake-flow.js';
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
 if(stageIndex>=0){const current=stages[stageIndex],terminal=stageIndex===stages.length-1;const p=element('p','Etapa simulada: '+label(current));actions.append(p);if(!terminal){
 const labelNote=element('label','Parecer / observação da etapa (simulação)');labelNote.htmlFor='decision-note';
 const note=element('textarea');note.id='decision-note';note.rows=3;note.maxLength=2000;note.placeholder='Descreva critérios, evidências e justificativa (mínimo 10 caracteres).';
 const approve=element('button','Concluir etapa simulada','button');approve.type='button';
 const reject=element('button','Solicitar ajustes na minuta','button secondary');reject.type='button';
 const decide=(outcome)=>{const reason=note.value.trim();if(reason.length<10){alert('Registre justificativa de no mínimo 10 caracteres.');return;}
 events.push({date:new Date().toISOString(),event:label(current)+' — '+(outcome==='approve'?'simulada como concluída':'devolvida para ajustes'),note:reason,kind:'SIMULATION_ONLY'});
 if(outcome==='request_changes'){stageIndex=stages.indexOf('MINUTA');}else{stageIndex=nextLocalStage(stages,stageIndex);}render();};
 approve.addEventListener('click',()=>decide('approve'));reject.addEventListener('click',()=>decide('request_changes'));
 actions.append(labelNote,note,approve,reject);
 }else{actions.append(element('p','Fim do fluxo demonstrativo. Em produção, esta etapa dependerá de publicação autorizada ou assinatura verificada.','note'));}}
 for(const e of events.slice(-15))log.append(element('p',new Date(e.date).toLocaleString('pt-BR')+' · '+e.event+(e.note?' | Observação: '+e.note:'')));
}
form.addEventListener('submit',e=>{e.preventDefault();if(answerIndex>=questions.length)return;const q=questions[answerIndex],v=validateAnswer(q,input.value);if(!v.ok){$('chat-error').textContent=v.message;return;}$('chat-error').textContent='';answers[q.key]=v.value;message(q.key==='legalEmails'?'[e-mails informados para roteamento futuro, sem envio]':input.value.trim(),'client');input.value='';answerIndex++;render();ask();});
$('restart').addEventListener('click',()=>{if(Object.keys(answers).length&&!confirm('Reiniciar a solicitação local? Exporte os dados antes se necessário.'))return;begin();});
$('export-request').addEventListener('click',()=>{const payload={schemaVersion:1,exportedAt:new Date().toISOString(),status:'LOCAL_DEMONSTRATION_NOT_APPROVED',request:answers,workflow:{stages,currentIndex:stageIndex,events}};const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='legaldoc-solicitacao-demo.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),3000);});
begin();