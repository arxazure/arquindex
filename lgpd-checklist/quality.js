import {definitions} from './model.js';
const val=x=>String(x??'').trim();
const draft=x=>/\b(rascunho|minuta|em (fase de )?revis[aã]o|sujeit[ao] a revis[aã]o)\b/i.test(val(x));
const cleanTitle=s=>val(s).toLocaleLowerCase('pt-BR').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/\b(minuta|politica|de|da|do|para|dos|das|dossie|gerais|geral|versao|lgpd)\b/g,'').replace(/\b\d+([.,/]\d+)*\b/g,'').replace(/[^a-z]+/g,' ').trim();
const validUf=new Set('AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO'.split(' '));
const item=(severity,section,id,field,message)=>({severity,section,record_id:id,field,message});
export function qualityForCompany(records){
 const company=records.find(x=>x.section==='company');
 if(!company)return {company_id:null,company_name:'Empresa não encontrada',counts:{},issues:[item('critical','company',null,'company_name','Cadastro da empresa não encontrado')],fixes:[]};
 const cp=company.payload||{},issues=[],fixes=[],bySec=s=>records.filter(x=>x.section===s);
 const counts=Object.fromEntries(Object.keys(definitions).map(s=>[s,bySec(s).length]));
 const add=(severity,r,field,message)=>issues.push(item(severity,r.section,r.id,field,message));
 for(const field of ['company_cnpj','company_email','company_dpo','company_address','company_city','company_state']){
   if(!val(cp[field]))add('high',company,field,'Empresa sem '+(definitions.company.fields[field]||field));
 }
 if(val(cp.company_email)&&(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(cp.company_email)||/\b(exemplo|example|teste)\b/i.test(cp.company_email)))add('high',company,'company_email','Contato institucional inválido ou de exemplo');
 if(val(cp.company_state)&&!validUf.has(val(cp.company_state).toUpperCase()))add('high',company,'company_state','UF inválida: '+val(cp.company_state));
 if(val(cp.company_state)==='MF'&&/\bbelo horizonte\b/i.test(val(cp.company_city)))fixes.push({id:company.id,section:'company',field:'company_state',before:'MF',after:'MG',reason:'UF inválida e município cadastrado como Belo Horizonte'});
 const branchIds=new Set(bySec('branch').map(x=>x.id));
 const deptIds=new Set(bySec('department').map(x=>x.id));
 const procIds=new Set(bySec('process').map(x=>x.id));
 for(const b of bySec('branch')){
   if(!val(b.payload?.branch_cnpj)){
     const match=val(b.payload?.name).match(/\b\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}\b/);
     if(match)fixes.push({id:b.id,section:'branch',field:'branch_cnpj',before:'',after:match[0],reason:'CNPJ transcrito do nome já cadastrado; sujeito a validação cadastral'});
     else add('medium',b,'branch_cnpj','Unidade sem CNPJ identificado');
   }
   if(!val(b.payload?.branch_type)&&/\bMATRIZ\b/i.test(val(b.payload?.name)))fixes.push({id:b.id,section:'branch',field:'branch_type',before:'',after:'Matriz',reason:'Tipo declarado no nome cadastrado'});
   if(!val(b.payload?.address))add('medium',b,'address','Unidade sem endereço');
 }
 for(const d of bySec('department'))if(!branchIds.has(d.parent_id))add('high',d,'parent_id','Departamento sem vínculo válido com unidade');
 for(const p of bySec('process')){
   if(!deptIds.has(p.parent_id))add('high',p,'parent_id','Processo sem departamento vinculado');
   for(const f of ['purpose','legal_basis','data_categories','data_subjects','origin','storage','sharing','retention','security','responsible'])if(!val(p.payload?.[f]))add('high',p,f,'Processo sem '+(definitions.process.fields[f]||f));
   if(/\b(a confirmar|provis[oó]ri[ao]|pendente|a definir|a validar)\b/i.test(val(p.payload?.legal_basis)))add('high',p,'legal_basis','Hipótese legal declarada como provisória: exige validação');
 }
 for(const r of bySec('risk'))if(!procIds.has(r.parent_id))add('high',r,'parent_id','Risco sem processo vinculado');
 const policies=bySec('policy'),names=new Map();
 for(const p of policies){
   const pl=p.payload||{},title=val(pl.name),text=val(pl.text);
   if(val(pl.status).toLocaleLowerCase('pt-BR')==='publicado'&&(draft(title)||draft(text.slice(0,600)))) {
     add('critical',p,'status','Documento marcado Publicado, mas contém declaração de minuta/rascunho');
     fixes.push({id:p.id,section:'policy',field:'status',before:pl.status,after:'Rascunho',reason:'Publicação incompatível com declaração explícita de minuta'});
   }
   if(!text||text.length<180)add('medium',p,'text','Texto documental muito curto ou vazio; necessita revisão');
   if(/@[^ ]*\b(exemplo|example)\b|\(exemplo\)|\bcontato fict[ií]cio\b/i.test(text))add('high',p,'text','Documento contém contato ou dado de exemplo; não publicar');
   const key=cleanTitle(title);
   if(key.length>=7){const previous=names.get(key);if(previous)add('medium',p,'name','Possível duplicidade temática com documento '+previous+'; preservar versões e revisar consolidação');else names.set(key,p.id);}
 }
 if(!bySec('process').length)issues.push(item('critical','process',null,'name','Nenhum processo mapeado'));
 if(!bySec('risk').length)issues.push(item('high','risk',null,'name','Não há riscos registrados; avaliação ainda não demonstrada'));
 if(!bySec('website').length)issues.push(item('medium','website',null,'url','Nenhum website inventariado'));
 if(!bySec('training').length)issues.push(item('medium','training',null,'evidence','Nenhum treinamento com evidência registrado'));
 const priorities={critical:0,high:1,medium:2,low:3};
 issues.sort((a,b)=>priorities[a.severity]-priorities[b.severity]);
 return {company_id:company.id,company_name:val(cp.company_name),counts,issues,fixes,issue_counts:{critical:issues.filter(x=>x.severity==='critical').length,high:issues.filter(x=>x.severity==='high').length,medium:issues.filter(x=>x.severity==='medium').length},status:issues.length?'REVISÃO NECESSÁRIA':'SEM LACUNAS AUTOMÁTICAS — EXIGE VALIDAÇÃO HUMANA'};
}
export function dossierForCompany(records,now=new Date()){
 const q=qualityForCompany(records),company=records.find(x=>x.section==='company')?.payload||{};
 const blocks=[],title=t=>blocks.push({kind:'title',text:t}),section=t=>blocks.push({kind:'section',text:t}),para=t=>blocks.push({kind:'paragraph',text:t}),row=(label,text)=>blocks.push({kind:'row',label,text:String(text??'Não informado')}),table=(columns,rows)=>blocks.push({kind:'table',columns,rows}),note=t=>blocks.push({kind:'note',text:t});
 title('DOSSIÊ DE GOVERNANÇA E CONFORMIDADE LGPD');
 note('DOCUMENTO DE TRABALHO — dados cadastrais não constituem prova de conformidade ou de aprovação de políticas.');
 section('1. Identificação do controlador e abrangência');
 for(const [k,v] of Object.entries(company))row(definitions.company.fields[k]||k,v);
 row('Data de geração',new Date(now).toLocaleDateString('pt-BR',{timeZone:'UTC'}));
 row('Estado de revisão',q.status);
 section('2. Resumo do inventário');
 table(['Módulo','Quantidade de registros'],Object.entries(q.counts).map(([k,v])=>[definitions[k]?.label||k,String(v)]));
 section('3. Diagnóstico de qualidade cadastral e documental');
 table(['Gravidade','Módulo','Registro','Pendência'],q.issues.length?q.issues.map(x=>[x.severity,x.section,x.record_id||'Empresa',x.message]):[['—','—','—','Nenhuma lacuna automática; validação humana obrigatória']]);
 section('4. Ações prioritárias e validações');
 para('Priorizar documentos declarados como minuta porém marcados publicados; corrigir dados cadastrais; validar hipóteses legais, responsáveis, vínculos entre unidades e departamentos, inventário de sistemas, evidências de segurança, riscos e treinamentos.');
 for(const [sec,d] of Object.entries(definitions)){
  const rows=records.filter(r=>r.section===sec&&sec!=='company');
  section('5. '+d.label+' — '+rows.length+' registro(s)');
  if(!rows.length){note('Nenhum registro deste módulo. Cadastro e evidências devem ser levantados.');continue;}
  for(const [i,r] of rows.entries()){
   section('5.'+(i+1)+' '+val(r.payload?.[d.name]));
   row('ID / rastreabilidade',r.id);
   if(r.parent_id)row('Vínculo / registro pai',r.parent_id);
   for(const [key,value] of Object.entries(r.payload||{})){
    const label=d.fields[key]||key;
    if(key==='text'){section('Conteúdo integral da versão cadastrada');for(const paragraph of String(value??'').split(/\n+/).filter(Boolean))para(paragraph);}
    else row(label,value);
   }
  }
 }
 section('6. Aprovação e trilha de auditoria');
 para('Esta exportação reproduz os registros cadastrados e sinaliza inconsistências. A aprovação, os testes técnicos e as evidências externas devem ser registrados pelo controlador e pelo DPO. Não altera documentos históricos.');
 return {type:'dossier',name:q.company_name,blocks,issues:q.issues,status:'RASCUNHO',createdAt:now.toISOString()};
}
export function safeCorrections(records){
 const q=qualityForCompany(records);
 return q.fixes.filter(x=>x.before!==x.after);
}
