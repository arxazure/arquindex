// Shared policy for documented decisions. Intended for an authenticated backend.
// Current public UI only simulates these decisions; no signature/publication happens here.
export const stageRoles=Object.freeze({
 SOLICITACOES:['requester'], SOLICITACAO:['requester'], MINUTA:['author'],
 REVISAO_CLIENTE:['requester'], REVISAO_JURIDICA_1:['legal'],
 REVISAO_JURIDICA_2:['legal'], REVISAO_TECNICA:['technical'],
 APROVACAO:['approver'], HOMOLOGACAO:['homologator'],
 AGUARDANDO_ASSINATURA:['signer'], AGUARDANDO_PUBLICACAO:['publisher']
});
export function roleFor(stage){return stageRoles[stage]?.[0]||null;}
export function evaluateDecision({stage,decision,actorRole,note,documentHash,authorId,actorId}){
 const expected=roleFor(stage);
 if(!expected)return {ok:false,error:'Etapa desconhecida'};
 if(actorRole!==expected)return {ok:false,error:'Papel nao autorizado para etapa'};
 if(!['approve','request_changes'].includes(decision))return {ok:false,error:'Decisao invalida'};
 if(typeof note!=='string'||note.trim().length<10||note.length>2000)return {ok:false,error:'Justificativa de ao menos 10 caracteres obrigatoria'};
 if(!/^[a-f0-9]{64}$/i.test(String(documentHash||'')))return {ok:false,error:'Versao do documento sem hash verificavel'};
 if(['APROVACAO','HOMOLOGACAO'].includes(stage)&&authorId&&actorId&&authorId===actorId)return {ok:false,error:'Segregacao: autor nao pode aprovar ou homologar'};
 if(stage.startsWith('AGUARDANDO_'))return {ok:false,error:'Publicacao e assinatura exigem integracao e evidencia externa'};
 return {ok:true,event:{stage,decision,actorRole,note:note.trim(),documentHash,requiresRework:decision==='request_changes'}};
}
export function applyDecision({stages,index,decision}){
 if(!Array.isArray(stages)||!Number.isInteger(index)||index<0||index>=stages.length)return {ok:false,error:'Etapa invalida'};
 if(!['approve','request_changes'].includes(decision))return {ok:false,error:'Decisao invalida'};
 if(decision==='request_changes')return {ok:true,index:Math.max(0,stages.indexOf('MINUTA')),state:'REWORK_REQUIRED'};
 if(index===stages.length-1)return {ok:false,error:'Etapa final exige provedor externo'};
 return {ok:true,index:index+1,state:'IN_REVIEW'};
}

export function hasVerifiedRole(member,expected){
 return member?.verified===true &&
  (member.role===expected || (Array.isArray(member.roles) && member.roles.includes(expected)));
}
export function hasConsistentApprovals(stages,index,currentHash){
 if(!Array.isArray(stages)||!Number.isInteger(index)||index<1||index>=stages.length||!/^[a-f0-9]{64}$/i.test(String(currentHash||'')))return false;
 return stages.slice(1,index).every(item=>item.status==='APPROVED'&&item.document_version_hash===currentHash);
}
