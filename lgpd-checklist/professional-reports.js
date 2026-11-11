import { deflateRawSync } from 'node:zlib';

const missing = label => '[PENDENTE DE COLETA: ' + label + ']';
const value = (x,label) => String(x ?? '').trim() || missing(label);
const raw = x => String(x ?? '').trim();
const esc = x => String(x ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const list = x => raw(x).split(/\s*[,;\n]\s*/).filter(Boolean);
const row = (label,text) => ({kind:'row',label,text:String(text)});
const para = text => ({kind:'paragraph',text:String(text)});
const title = text => ({kind:'title',text:String(text)});
const section = text => ({kind:'section',text:String(text)});
const note = text => ({kind:'note',text:String(text)});
const table = (columns,rows) => ({kind:'table',columns,rows});
const fmtDate = d => {const date=new Date(d);return Number.isFinite(date.valueOf())?date.toLocaleDateString('pt-BR',{timeZone:'UTC'}):'Não informada';};

export function buildProfessionalReport(type,records,companyPayload,now=new Date()){
  if(!['privacy','ropa','risk','incident','audit','cookies','training'].includes(type)) throw Error('Tipo de documento inválido');
  const company=companyPayload||{};
  const all=records||[];
  const get=s=>all.filter(r=>r.section===s);
  const processes=get('process');
  const departments=new Map(get('department').map(r=>[r.id,r]));
  const branches=new Map(get('branch').map(r=>[r.id,r]));
  const risks=get('risk');
  const websites=get('website');
  const incidents=get('incident');
  const audits=get('audit');
  const trainings=get('training');
  const operators=get('operator');
  const systems=get('system');
  const name=value(company.company_name,'razão social');
  const dpo=raw(company.company_dpo);
  const email=raw(company.company_email);
  const blocks=[];
  const add=(...items)=>blocks.push(...items);
  const meta=[
    row('Controlador',name),
    row('CNPJ',value(company.company_cnpj,'CNPJ')),
    row('Endereço',value([company.company_address,company.company_city,company.company_state].filter(Boolean).join(' — '),'endereço')),
    row('Contato público',value(email,'e-mail de contato')),
    row('Telefone',value(company.company_phone,'telefone público')),
    row('Encarregado / DPO',value(dpo,'identificação do encarregado')),
    row('Emissão',fmtDate(now)),
    row('Versão','1.0 — minuta para revisão'),
    row('Situação','RASCUNHO — NÃO PUBLICAR SEM CONFERÊNCIA E APROVAÇÃO')
  ];
  const pending=[];
  for(const r of meta) if(r.text.includes('[PENDENTE')) pending.push(r.label);
  const field=(obj,key,label)=>{const v=value(obj?.[key],label);if(v.includes('[PENDENTE'))pending.push(label);return v;};
  const deptOf=p=>{
    const dept=departments.get(p.parent_id);
    const unit=dept&&branches.get(dept.parent_id);
    return {dept:dept?.payload?.name||missing('departamento do processo'),unit:unit?.payload?.name||missing('unidade do processo')};
  };
  add(title(({ropa:'REGISTRO DE OPERAÇÕES DE TRATAMENTO DE DADOS PESSOAIS (ROPA)',privacy:'POLÍTICA DE PRIVACIDADE E PROTEÇÃO DE DADOS',risk:'RELATÓRIO DE RISCOS E AVALIAÇÃO DE IMPACTO (RIPD)',incident:'RELATÓRIO DE INCIDENTES DE SEGURANÇA',audit:'RELATÓRIO DE AUDITORIA E PLANO DE AÇÃO',cookies:'INVENTÁRIO DE COOKIES E WEBSITES',training:'RELATÓRIO DE TREINAMENTOS E CONSCIENTIZAÇÃO'})[type]),note('Documento gerado a partir dos cadastros da empresa. A existência de texto não comprova a implementação de controles.'),section('1. Identificação e controle documental'),...meta);
  if(type==='ropa'){
    add(section('2. Objetivo e abrangência'),para('Este registro organiza as atividades de tratamento mapeadas, conforme o art. 37 da Lei nº 13.709/2018 (LGPD). Cada processo deve ter suas finalidades, hipóteses legais, titulares, dados, responsáveis, compartilhamentos, retenção e controles confirmados pelo controlador.'));
    add(section('3. Quadro geral do mapeamento'));
    if(processes.length) add(table(['Referência','Processo','Departamento','Unidade'],processes.map((p,i)=>[String(i+1),value(p.payload?.name,'nome do processo'),deptOf(p).dept,deptOf(p).unit])));
    else add(note('Nenhum processo foi cadastrado. Cadastre departamentos e processos no mapa de dados antes da aprovação.'));
    add(section('4. Quadro detalhado das operações'));
    processes.forEach((p,i)=>{
      const d=deptOf(p),v=p.payload||{};
      add(section('4.'+(i+1)+' — '+value(v.name,'nome do processo')),
        row('Referência do processo',p.id),
        row('Unidade',d.unit),row('Departamento',d.dept),
        row('Classificação dos dados',field(v,'data_type_classification','classificação de dados do processo')),
        row('Operadores vinculados',field(v,'process_operators','operadores vinculados ao processo')),
        row('Descrição / atividade',field(v,'name','descrição da atividade')),
        row('Responsável',field(v,'responsible','responsável pelo processo')),
        row('Finalidade do tratamento',field(v,'purpose','finalidade do processo')),
        row('Hipótese legal avaliada',field(v,'legal_basis','base legal do processo')),
        row('Categorias de dados pessoais',field(v,'data_categories','categorias de dados do processo')),
        row('Perfil dos titulares',field(v,'data_subjects','titulares do processo')),
        row('Origem e coleta',field(v,'origin','origem dos dados')),
        row('Sistemas, ativos e armazenamento',field(v,'storage','armazenamento do processo')),
        row('Compartilhamentos e destinatários',field(v,'sharing','compartilhamentos do processo')),
        row('Transferências internacionais e salvaguardas',field(v,'international_transfer','transferência internacional do processo')),
        row('Prazo, marco e fundamento de retenção',field(v,'retention','retenção do processo')),
        row('Medidas técnicas e organizacionais',field(v,'security','medidas de segurança do processo')));
      const related=risks.filter(r=>r.parent_id===p.id);
      if(related.length) add(table(['Risco','Probabilidade','Impacto','Mitigação'],related.map(r=>[raw(r.payload?.name),raw(r.payload?.probability),raw(r.payload?.impact),raw(r.payload?.mitigation)])));
      else add(note('Riscos vinculados a esta operação: ainda não cadastrados ou não avaliados.'));
    });
    add(section('5. Inventário de sistemas e operadores'),...(systems.length?systems.map(x=>row(raw(x.payload?.name)||'Sistema', 'Fornecedor: '+value(x.payload?.provider,'fornecedor')+'; Armazenamento: '+value(x.payload?.location,'local de armazenamento')+'; Acesso: '+value(x.payload?.access,'perfis de acesso'))):[note('Sistemas não cadastrados.')]),...(operators.length?operators.map(x=>row(raw(x.payload?.name)||'Operador', 'Função: '+value(x.payload?.role,'função do operador')+'; Contrato: '+value(x.payload?.contract,'contrato do operador'))):[note('Operadores não cadastrados.')]));
    add(section('6. Compartilhamentos, retenção e medidas de segurança'),para('As informações por processo constam no quadro detalhado. A avaliação de fornecedores, contratos, transferências internacionais e tabela de temporalidade exige conferência específica. A ausência de cadastro não significa ausência de tratamento.'));
    add(section('7. Evidências e responsabilização'),para('O responsável deve anexar entrevistas, contratos, inventários, evidências de controle e decisões sobre bases legais e retenção ao processo correspondente. Este documento não substitui o RIPD quando necessário.'));
    add(section('8. Revisão e aprovação'),para('Conferir os registros com os responsáveis de cada unidade e departamento. Validar informações, versão, data e aprovação antes de circular como documento oficial.'));
  } else if(type==='privacy') {
    add(section('2. Apresentação e definições'),para('Esta política explica como o controlador trata dados pessoais de titulares com quem se relaciona. Dados pessoais identificam ou tornam uma pessoa identificável; dados sensíveis têm proteção específica nos termos da LGPD. Tratamento inclui coleta, uso, armazenamento, compartilhamento e eliminação.'));
    add(section('3. Quais dados tratamos, em quais departamentos e para quê'));
    if(processes.length){
      add(table(['Departamento','Dados e titulares','Finalidade'],processes.map(p=>[deptOf(p).dept,value(p.payload?.data_categories,'categorias de dados')+' | '+value(p.payload?.data_subjects,'titulares'),value(p.payload?.purpose,'finalidade')])));
      processes.forEach(p=>add(row('Processo: '+value(p.payload?.name,'nome do processo'),'Origem: '+value(p.payload?.origin,'origem')+' | Fundamento: '+value(p.payload?.legal_basis,'base legal')+' | Sistemas: '+value(p.payload?.storage,'sistemas'))));
    }else add(note('Não há processos de tratamento mapeados. É necessário concluir a coleta por departamento antes de publicar.'));
    add(section('4. Finalidades e hipóteses legais'),para('As finalidades e hipóteses legais constam individualmente nos processos mapeados. A hipótese deve ser verificada para cada operação; o consentimento não é fundamento universal e dados sensíveis podem exigir hipótese específica do art. 11.'));
    add(section('5. Compartilhamento com terceiros'),...processes.map(p=>row(value(p.payload?.name,'processo'),value(p.payload?.sharing,'destinatários e motivos de compartilhamento'))));
    add(section('6. Transferências internacionais'),...processes.map(p=>row(value(p.payload?.name,'processo'),value(p.payload?.international_transfer,'países, destinatários e salvaguardas'))));
    add(section('7. Segurança e proteção de dados'),...processes.map(p=>row(value(p.payload?.name,'processo'),value(p.payload?.security,'controles implementados'))),para('As medidas descritas dependem de comprovação e revisão periódica. Nenhum sistema garante segurança absoluta.'));
    add(section('8. Retenção, descarte e término do tratamento'),...processes.map(p=>row(value(p.payload?.name,'processo'),value(p.payload?.retention,'prazo, marco inicial e forma de descarte'))),para('A eliminação depende de análise das obrigações legais, preservação de evidências e autorizações aplicáveis. Não há descarte automático por esta política.'));
    add(section('9. Direitos dos titulares'),para('Nos termos da LGPD, o titular pode solicitar confirmação de tratamento, acesso, correção, anonimização, bloqueio ou eliminação quando cabíveis, portabilidade conforme regulamentação, informação sobre compartilhamentos e consentimento, revogação do consentimento e revisão de decisões automatizadas nos termos legais. As solicitações serão analisadas com verificação de identidade proporcional ao risco.'));
    add(section('10. Cookies e coleta em websites'));
    if(websites.length) add(table(['Website','Coleta','Cookies e terceiros'],websites.map(w=>[raw(w.payload?.url)||raw(w.payload?.name),value(w.payload?.collection,'coleta no website'),value(w.payload?.cookies,'cookies do website')])));
    else add(note('Inventário de cookies e websites não cadastrado. A política de cookies exige varredura e validação antes da publicação.'));
    add(section('11. Contato e canal do encarregado'),para('Encarregado: '+value(dpo,'nome do DPO')+'. E-mail de contato: '+value(email,'e-mail do canal do titular')+'. Solicitações serão tratadas conforme a LGPD e as regras aplicáveis ao caso.'));
    add(section('12. Atualizações, responsabilidade e aprovação'),para('A empresa deve revisar esta política sempre que houver alteração relevante nos tratamentos e disponibilizar ao público somente uma versão aprovada após conferência dos fatos e revisão jurídica.'));
  }
  if(type==='risk'){
    add(section('2. Metodologia e abrangência'),para('A identificação de riscos decorre dos registros informados pelos responsáveis. Probabilidade, impacto, mitigação e avaliação devem ser confirmados e documentados. Este relatório não substitui análise jurídica e avaliação de impacto quando exigidas.'));
    for(const [i,r] of risks.entries()){
      const p=processes.find(x=>x.id===r.parent_id);
      add(section('3.'+(i+1)+' — '+value(r.payload?.name,'risco identificado')),row('Processo vinculado',value(p?.payload?.name,'processo vinculado')), ...['risk_level','probability','impact','assessment','mitigation','responsible','deadline','status'].map(k=>row(({risk_level:'Nível de risco',probability:'Probabilidade',impact:'Impacto',assessment:'Avaliação de impacto',mitigation:'Plano de mitigação',responsible:'Responsável',deadline:'Prazo',status:'Situação'})[k],field(r.payload,k,k))));
    }
    if(!risks.length)add(note('Não há riscos cadastrados. O relatório não comprova avaliação de impacto.'));
  }
  if(type==='incident'){
    add(section('2. Registro, contenção e comunicação'),para('Registros administrativos de incidentes; a decisão de comunicação à ANPD e aos titulares depende da avaliação dos requisitos legais aplicáveis.'));
    for(const [i,r] of incidents.entries())add(section('3.'+(i+1)+' — '+value(r.payload?.name,'incidente')),...Object.entries(r.payload||{}).map(([k,v])=>row(k,value(v,k))));
    if(!incidents.length)add(note('Nenhum incidente cadastrado. Isto não é evidência de inexistência de incidentes.'));
  }
  if(type==='audit'){
    add(section('2. Escopo, evidências e critérios'),para('As constatações e recomendações refletem exclusivamente os registros inseridos. Uma auditoria técnica de website exige evidências de varredura, data, escopo e metodologia, não inferidas automaticamente.'));
    for(const [i,r] of audits.entries())add(section('3.'+(i+1)+' — '+value(r.payload?.name,'controle auditado')),...Object.entries(r.payload||{}).map(([k,v])=>row(k,value(v,k))));
    if(!audits.length)add(note('Nenhuma auditoria cadastrada. Não é possível atribuir pontuação de conformidade.'));
  }
  if(type==='cookies'){
    add(section('2. Escopo e metodologia'),para('Inventário declaratório de websites, formulários e cookies. Uma varredura passiva não confirma comportamento de scripts nem prova bloqueio de cookies antes do consentimento.'));
    for(const [i,r] of websites.entries())add(section('3.'+(i+1)+' — '+value(r.payload?.name,'website')),...Object.entries(r.payload||{}).map(([k,v])=>row(k,value(v,k))));
    if(!websites.length)add(note('Nenhum website cadastrado. A política de cookies deve aguardar inventário e validação.'));
  }
  if(type==='training'){
    add(section('2. Treinamentos, responsáveis e evidências'),para('Registros de treinamentos e conscientização da equipe, com datas, responsáveis, público, status e evidências disponíveis.'));
    for(const [i,r] of trainings.entries())add(section('3.'+(i+1)+' — '+value(r.payload?.name,'treinamento')),...Object.entries(r.payload||{}).map(([k,v])=>row(k,value(v,k))));
    if(!trainings.length)add(note('Nenhum treinamento cadastrado. Não é possível atestar capacitação.'));
  }
  const issues=[...new Set(pending)];
  if(!processes.length&&['ropa','privacy','risk'].includes(type))issues.unshift('processos de tratamento não cadastrados');
  add(section('Pendências de qualidade e publicação'),para(issues.length?issues.join('; '):'Nenhuma lacuna textual automática encontrada. Ainda é necessária revisão factual, jurídica e aprovação.'));
  return {type,name,blocks,issues,status:'RASCUNHO',processCount:processes.length,createdAt:now.toISOString()};
}

export function reportHtml(report){
  const content=report.blocks.map(b=>{
    if(b.kind==='title')return '<h1>'+esc(b.text)+'</h1>';
    if(b.kind==='section')return '<h2>'+esc(b.text)+'</h2>';
    if(b.kind==='paragraph')return '<p>'+esc(b.text)+'</p>';
    if(b.kind==='note')return '<aside>'+esc(b.text)+'</aside>';
    if(b.kind==='row')return '<table class="kv"><tr><th>'+esc(b.label)+'</th><td>'+esc(b.text)+'</td></tr></table>';
    if(b.kind==='table')return '<table><thead><tr>'+b.columns.map(x=>'<th>'+esc(x)+'</th>').join('')+'</tr></thead><tbody>'+b.rows.map(r=>'<tr>'+r.map(x=>'<td>'+esc(x)+'</td>').join('')+'</tr>').join('')+'</tbody></table>';
    return '';
  }).join('\n');
  return '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(report.name)+' — '+report.type.toUpperCase()+'</title><style>@page{size:A4;margin:18mm 16mm 20mm}*{box-sizing:border-box}body{font:11pt/1.52 "Segoe UI",Arial,sans-serif;color:#172a44;background:#f0f4fa;margin:0}.paper{max-width:210mm;margin:24px auto;background:white;padding:20mm 16mm;box-shadow:0 12px 32px #14294720}.brand{font-weight:800;letter-spacing:.07em;color:#0871d7;border-bottom:3px solid #0aa3e5;padding-bottom:12px;margin-bottom:30px}.status{display:inline-block;border:1px solid #bf6a23;background:#fff7ed;color:#8b4513;border-radius:5px;padding:4px 9px;font-size:9pt}h1{font-size:21pt;line-height:1.2;color:#102d54;margin:24px 0 20px}h2{font-size:13pt;color:#0c5ea8;border-bottom:1px solid #c5d8e9;padding:5px 0;margin:26px 0 12px;break-after:avoid}p{margin:10px 0;text-align:justify;overflow-wrap:anywhere}aside{background:#eef6ff;border-left:4px solid #1379d5;padding:10px 13px;margin:15px 0}table{border-collapse:collapse;width:100%;margin:8px 0 15px;table-layout:fixed;font-size:9pt}td,th{border:1px solid #c8d6e6;padding:8px;vertical-align:top;text-align:left;overflow-wrap:anywhere}thead th{background:#e6f0fb;color:#163c65}.kv th{width:34%;background:#f1f5fa;color:#234364}.kv td{width:66%}tr{break-inside:avoid}footer{margin-top:30px;border-top:1px solid #d5e1ee;padding-top:10px;color:#64748b;font-size:8pt}@media print{body{background:white}.paper{margin:0;max-width:none;padding:0;box-shadow:none}h1{break-after:avoid}a{color:inherit}}</style></head><body><main class="paper"><div class="brand">ARQUINDEX <span style="font-weight:400;color:#506e92">| Governança e Privacidade</span></div><div class="status">RASCUNHO — SUJEITO À REVISÃO</div>'+content+'<footer>Gerado a partir dos registros cadastrados. Não comprova conformidade nem substitui aprovação jurídica. Arquindex · LGPD Checklist</footer></main></body></html>';
}

const latin = s=>Buffer.from(String(s).normalize('NFC').replace(/[‘’]/g,"'").replace(/[“”]/g,'"').replace(/[–—]/g,'-').replace(/[^\u000a\u0020-\u00ff]/g,'?'),'latin1');
const pdfEsc = s=>{let o='';for(const c of latin(s)){if(c===40||c===41||c===92)o+='\\'+String.fromCharCode(c);else if(c<32||c>126)o+='\\'+c.toString(8).padStart(3,'0');else o+=String.fromCharCode(c);}return o;};
const approx = s=>String(s).length;
function wrap(text,max=95){const out=[];for(const p of String(text).split('\n')){let line='';for(const word of p.split(/\s+/)){if(!word)continue;if(line&&approx(line+' '+word)>max){out.push(line);line='';}if(word.length>max){if(line){out.push(line);line='';}for(let i=0;i<word.length;i+=max)out.push(word.slice(i,i+max));}else line+=(line?' ':'')+word;}out.push(line);}return out;}
export function reportPdf(report){
  const pages=[],width=595,height=842,left=48,right=548;
  let commands=[],y=754;
  const newPage=()=>{if(commands.length)pages.push(commands.join('\n'));commands=[];y=754;};
  const text=(str,size=10,bold=false,color='0.11 0.20 0.33')=>{commands.push('BT /'+(bold?'F2':'F1')+' '+size+' Tf '+color+' rg 1 0 0 1 '+left+' '+y+' Tm ('+pdfEsc(str)+') Tj ET');};
  const line=()=>commands.push('0.79 0.85 0.92 RG 0.6 w '+left+' '+(y-4)+' m '+right+' '+(y-4)+' l S');
  const ensure=(heightNeeded)=>{if(y-heightNeeded<66)newPage();};
  const drawLines=(str,size=10,bold=false,limit=96)=>{const lines=wrap(str,limit);for(const l of lines){ensure(size+6);text(l,size,bold);y-=size+5;}};
  for(const b of report.blocks){
    if(b.kind==='title'){ensure(65);drawLines(b.text,17,true,48);y-=14;line();y-=15;}
    else if(b.kind==='section'){ensure(45);y-=8;drawLines(b.text,12,true,74);line();y-=12;}
    else if(b.kind==='paragraph'){drawLines(b.text,10,false,99);y-=11;}
    else if(b.kind==='note'){drawLines('ATENÇÃO: '+b.text,9,false,108);y-=12;}
    else if(b.kind==='row'){const lab=wrap(b.label,40),val=wrap(b.text,93);ensure((lab.length+val.length)*13+16);drawLines(b.label.toUpperCase(),9,true,100);drawLines(b.text,10,false,99);line();y-=9;}
    else if(b.kind==='table'){
      ensure(40);drawLines(b.columns.join('  |  '),9,true,105);line();y-=10;
      for(const r of b.rows){const cells=r.map((v,i)=>b.columns[i]+': '+v).join('   |   ');drawLines(cells,9,false,111);line();y-=7;}
    }
  }
  newPage();
  const objects=[],add=s=>{objects.push(Buffer.isBuffer(s)?s:Buffer.from(s,'latin1'));return objects.length;};
  const catalog=add(''),root=add('');
  const font=add('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>');
  const bold=add('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>');
  const pageIds=[];
  pages.forEach((content,i)=>{
    const header='0.05 0.36 0.70 rg 48 793 500 3 re f BT /F2 10 Tf 0.06 0.28 0.54 rg 1 0 0 1 48 808 Tm (ARQUINDEX  |  LGPD CHECKLIST) Tj ET';
    const footer='BT /F1 8 Tf 0.38 0.45 0.55 rg 1 0 0 1 48 38 Tm (RASCUNHO - Revisao obrigatoria  |  Pagina '+(i+1)+' de '+pages.length+') Tj ET';
    const stream=Buffer.from(header+'\n'+content+'\n'+footer,'latin1');
    const cid=add(Buffer.concat([Buffer.from('<< /Length '+stream.length+' >>\nstream\n'),stream,Buffer.from('\nendstream')]));
    pageIds.push(add('<< /Type /Page /Parent '+root+' 0 R /MediaBox [0 0 '+width+' '+height+'] /Resources << /Font << /F1 '+font+' 0 R /F2 '+bold+' 0 R >> >> /Contents '+cid+' 0 R >>'));
  });
  objects[catalog-1]=Buffer.from('<< /Type /Catalog /Pages '+root+' 0 R >>');
  objects[root-1]=Buffer.from('<< /Type /Pages /Count '+pageIds.length+' /Kids ['+pageIds.map(x=>x+' 0 R').join(' ')+'] >>');
  const chunks=[Buffer.from('%PDF-1.4\n')],offsets=[0];let position=chunks[0].length;
  objects.forEach((obj,i)=>{offsets.push(position);const buf=Buffer.concat([Buffer.from((i+1)+' 0 obj\n'),obj,Buffer.from('\nendobj\n')]);chunks.push(buf);position+=buf.length;});
  const xref=position;
  chunks.push(Buffer.from('xref\n0 '+(objects.length+1)+'\n0000000000 65535 f \n'+offsets.slice(1).map(n=>String(n).padStart(10,'0')+' 00000 n \n').join('')+'trailer\n<< /Size '+(objects.length+1)+' /Root '+catalog+' 0 R >>\nstartxref\n'+xref+'\n%%EOF'));
  return Buffer.concat(chunks);
}
