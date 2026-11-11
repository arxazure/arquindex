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
  const websiteScans=get('website_scan');
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
    if(websiteScans.length){
      add(section('4. Evidências técnicas de varredura passiva'));
      for(const [i,scan] of websiteScans.entries()){
        const result=scan.payload||{};
        const site=websites.find(x=>x.id===scan.parent_id);
        add(section('4.'+(i+1)+' — '+value(site?.payload?.url||result.finalUrl,'URL auditada')),
          row('Data da coleta',value(result.scannedAt,'data da coleta')),
          row('HTTP',value(result.httpStatus,'código HTTP')),
          row('Interpretação técnica',value(result.interpretation,'interpretação da varredura')),
          row('Limitações',Array.isArray(result.limitations)?result.limitations.join('; '):missing('limitações')));
        if(Array.isArray(result.checks))add(table(['Verificação','Observação','Evidência','Ação recomendada'],result.checks.map(c=>[raw(c.label),c.observed?'Sinal observado':'Sinal não observado',raw(c.evidence),raw(c.nextAction)])));
      }
    } else add(note('Não há varreduras técnicas anexadas a este relatório. Sem evidências técnicas não é possível atribuir conformidade de website.'));
    if(!audits.length)add(note('Nenhuma auditoria cadastrada. Não é possível atribuir pontuação de conformidade.'));
  }
  if(type==='cookies'){
    add(section('2. Escopo e metodologia'),para('Inventário declaratório de websites, formulários e cookies. Uma varredura passiva não confirma comportamento de scripts nem prova bloqueio de cookies antes do consentimento.'));
    for(const [i,r] of websites.entries())add(section('3.'+(i+1)+' — '+value(r.payload?.name,'website')),...Object.entries(r.payload||{}).map(([k,v])=>row(k,value(v,k))));
    if(websiteScans.length){
      add(section('4. Varreduras técnicas e limitações'));
      for(const scan of websiteScans){const x=scan.payload||{};add(row(value(x.finalUrl,'URL da varredura'),'Coleta: '+value(x.scannedAt,'data')+'; Cookies observados: '+(Array.isArray(x.cookies)?x.cookies.length:missing('inventário de cookies'))+'; Recursos externos: '+(Array.isArray(x.externalResourceHosts)?x.externalResourceHosts.join(', '):missing('recursos externos'))));}
    }
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
  const W=595,H=842,L=42,R=553,TOP=758,BOTTOM=65;
  const objects=[],add=b=>{objects.push(Buffer.isBuffer(b)?b:Buffer.from(b,'latin1'));return objects.length;};
  const pages=[];let cmds=[],y=TOP;
  const rgb=(r,g,b)=>r+' '+g+' '+b;
  const color=(r,g,b)=>cmds.push(rgb(r,g,b)+' rg');
  const text=(x,baseline,s,size=9,bold=false)=>{
    cmds.push('BT /'+(bold?'F2':'F1')+' '+size+' Tf 0.10 0.19 0.32 rg 1 0 0 1 '+x.toFixed(2)+' '+baseline.toFixed(2)+' Tm ('+pdfEsc(s)+') Tj ET');
  };
  const rect=(x,top,w,h,fill)=>{
    if(fill)cmds.push(rgb(...fill)+' rg '+x+' '+(top-h).toFixed(2)+' '+w+' '+h.toFixed(2)+' re f');
    cmds.push('0.78 0.84 0.90 RG 0.5 w '+x+' '+(top-h).toFixed(2)+' '+w+' '+h.toFixed(2)+' re S');
  };
  const page=()=>{if(cmds.length)pages.push(cmds.join('\n'));cmds=[];y=TOP;};
  const ensure=h=>{if(y-h<BOTTOM)page();};
  const drawText=(s,size=10,bold=false,indent=0)=>{
    const limit=Math.max(18,Math.floor((R-L-indent)/(size*0.54)));
    const lines=wrap(s,limit);
    for(const line of lines){ensure(size+6);text(L+indent,y,line,size,bold);y-=size+5;}
  };
  const drawTable=(heads,rows)=>{
    const n=heads.length;
    if(!n)return;
    const widths=n===2?[0.34,0.66]:n===3?[0.24,0.36,0.40]:n===4?[0.13,0.27,0.30,0.30]:Array(n).fill(1/n);
    const px=widths.map(x=>x*(R-L));
    const offsets=[L];for(const w of px)offsets.push(offsets.at(-1)+w);
    const renderRow=(cells,header=false)=>{
      const size=header?8.2:8.1;
      const lines=cells.map((cell,i)=>wrap(String(cell??''),Math.max(8,Math.floor((px[i]-14)/(size*0.53)))));
      const count=Math.max(1,...lines.map(x=>x.length));
      let cursor=0;
      while(cursor<count){
        if(y< BOTTOM+38)page();
        const fit=Math.max(1,Math.floor((y-BOTTOM-12)/12));
        const take=Math.min(count-cursor,fit);
        const height=take*12+13;
        for(let i=0;i<n;i++){
          rect(offsets[i],y,px[i],height,header?[0.88,0.93,0.98]:(cursor%2?[0.98,0.99,1]:null));
          for(let j=0;j<take;j++)if(lines[i][cursor+j])text(offsets[i]+6,y-15-j*12,lines[i][cursor+j],size,header);
        }
        y-=height;
        cursor+=take;
      }
    };
    ensure(60);renderRow(heads,true);
    for(const cells of rows){if(y<BOTTOM+48){page();renderRow(heads,true);}renderRow(cells);}
    y-=12;
  };
  for(const b of report.blocks){
    if(b.kind==='title'){ensure(72);drawText(b.text,17,true);y-=10;cmds.push('0.06 0.40 0.71 rg '+L+' '+(y-2)+' '+(R-L)+' 3 re f');y-=20;}
    else if(b.kind==='section'){ensure(50);y-=9;drawText(b.text,12,true);y-=7;}
    else if(b.kind==='paragraph'){drawText(b.text,9.5);y-=11;}
    else if(b.kind==='note'){ensure(30);drawText('ATENÇÃO: '+b.text,9,false,5);y-=11;}
    else if(b.kind==='row')drawTable(['Campo','Informação'],[[b.label,b.text]]);
    else if(b.kind==='table')drawTable(b.columns,b.rows);
  }
  page();
  const catalog=add(''),root=add('');
  const regular=add('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>');
  const bold=add('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>');
  const pageIds=[];
  for(let i=0;i<pages.length;i++){
    const header='0.04 0.35 0.67 rg '+L+' 792 '+(R-L)+' 3 re f BT /F2 10 Tf 0.05 0.28 0.53 rg 1 0 0 1 '+L+' 806 Tm (ARQUINDEX  |  LGPD CHECKLIST) Tj ET';
    const footer='BT /F1 8 Tf 0.35 0.42 0.52 rg 1 0 0 1 '+L+' 39 Tm (RASCUNHO - Revisao obrigatoria  |  Pagina '+(i+1)+' de '+pages.length+') Tj ET';
    const stream=Buffer.from(header+'\n'+pages[i]+'\n'+footer,'latin1');
    const cid=add(Buffer.concat([Buffer.from('<< /Length '+stream.length+' >>\nstream\n'),stream,Buffer.from('\nendstream')]));
    pageIds.push(add('<< /Type /Page /Parent '+root+' 0 R /MediaBox [0 0 '+W+' '+H+'] /Resources << /Font << /F1 '+regular+' 0 R /F2 '+bold+' 0 R >> >> /Contents '+cid+' 0 R >>'));
  }
  objects[catalog-1]=Buffer.from('<< /Type /Catalog /Pages '+root+' 0 R >>');
  objects[root-1]=Buffer.from('<< /Type /Pages /Count '+pageIds.length+' /Kids ['+pageIds.map(x=>x+' 0 R').join(' ')+'] >>');
  const chunks=[Buffer.from('%PDF-1.4\n')],offsets=[0];let pos=chunks[0].length;
  objects.forEach((o,i)=>{offsets.push(pos);const b=Buffer.concat([Buffer.from((i+1)+' 0 obj\n'),o,Buffer.from('\nendobj\n')]);chunks.push(b);pos+=b.length;});
  chunks.push(Buffer.from('xref\n0 '+(objects.length+1)+'\n0000000000 65535 f \n'+offsets.slice(1).map(x=>String(x).padStart(10,'0')+' 00000 n \n').join('')+'trailer\n<< /Size '+(objects.length+1)+' /Root '+catalog+' 0 R >>\nstartxref\n'+pos+'\n%%EOF'));
  return Buffer.concat(chunks);
}
