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
 if(![1,2].includes(data?.rounds)||!['ASSINAR','PUBLICAR'].includes(data?.outcome))throw Error('Roteamento inválido');
 return ['SOLICITACAO','MINUTA','REVISAO_CLIENTE',...Array.from({length:data.rounds},(_,i)=>'REVISAO_JURIDICA_'+(i+1)),'REVISAO_TECNICA','APROVACAO','HOMOLOGACAO',data.outcome==='ASSINAR'?'AGUARDANDO_ASSINATURA':'AGUARDANDO_PUBLICACAO'];
}
export function nextLocalStage(stages,index){
 if(!Array.isArray(stages)||!Number.isInteger(index)||index<0||index>=stages.length)return -1;
 return index+1<stages.length?index+1:index;
}