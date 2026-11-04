const $=id=>document.getElementById(id);
const library={
identification:['Identificação das partes','Este documento é celebrado entre {{razao_social}}, inscrita no CNPJ {{cnpj}}, com sede em {{endereco}}, doravante denominada CONTRATANTE, e {{contratada}}, doravante denominada CONTRATADA.'],
purpose:['Objeto e finalidade','O presente instrumento tem por objeto {{objeto}}, de acordo com as condições definidas pelas partes.'],
scope:['Escopo e obrigações','As atividades compreendem {{escopo}}. As responsabilidades e os critérios de aceite serão definidos e validados pelas partes.'],
privacy:['Tratamento de dados e LGPD','As partes avaliarão os papéis de controlador e operador, finalidades, bases legais, medidas de segurança e demais obrigações de proteção de dados pessoais aplicáveis às atividades descritas.'],
security:['Confidencialidade e segurança','As partes comprometem-se a proteger informações confidenciais e a adotar medidas técnicas e administrativas proporcionais aos riscos envolvidos.'],
term:['Vigência e prazos','A vigência começa em {{data_inicio}} e termina em {{data_fim}}, observadas as condições de prorrogação aprovadas pelas partes.'],
payment:['Valores e condições','A remuneração acordada é de {{valor}}, com forma e prazo de pagamento {{condicoes_pagamento}}.'],
termination:['Rescisão','A rescisão e seus efeitos observarão as condições negociadas, a legislação aplicável e as obrigações pendentes.'],
forum:['Foro e solução de conflitos','As partes definirão o foro competente e eventuais métodos adequados de solução de conflitos conforme a legislação aplicável.'],
signature:['Assinaturas','Local e data: {{local_data}}\n\nCONTRATANTE: _____________________\n\nCONTRATADA: _____________________'],
custom:['Nova seção','Descreva o conteúdo desta seção.']
};
const presets={
blank:[],
contract:['identification','purpose','scope','term','payment','privacy','security','termination','forum','signature'],
privacy:['purpose','privacy','security','term','custom'],
confidentiality:['identification','purpose','security','term','forum','signature'],
record:['identification','purpose','custom','signature'],
delivery:['identification','scope','term','signature']
};
let data={title:'Documento corporativo',sections:[],fields:{}},selected=null;
const safeText=v=>String(v??'');
const section=(kind)=>({id:crypto.randomUUID?.()||String(Date.now()+Math.random()),title:library[kind][0],body:library[kind][1]});
function node(tag,content,cls){const e=document.createElement(tag);if(content!==undefined)e.textContent=content;if(cls)e.className=cls;return e;}
function control(text,fn,disabled=false){const b=node('button',text,'mini');b.type='button';b.disabled=disabled;b.addEventListener('click',fn);return b;}
function extractFields(){let names=new Set();for(const sec of data.sections){for(const m of sec.body.matchAll(/\{\{\s*([A-Za-z][A-Za-z0-9_]{0,63})\s*\}\}/g))names.add(m[1]);}return [...names].sort();}
function renderList(){const ol=$('section-list');ol.replaceChildren();data.sections.forEach((s,i)=>{const li=node('li',undefined,s.id===selected?'active':'');li.append(control(String(i+1)+'. '+s.title,()=>{selected=s.id;render();}));li.firstChild.className='select-section';li.append(control('↑',()=>move(i,-1),i===0));li.append(control('↓',()=>move(i,1),i===data.sections.length-1));li.append(control('×',()=>{data.sections.splice(i,1);if(selected===s.id)selected=data.sections[0]?.id||null;render();}));ol.append(li);});}
function move(i,by){const j=i+by;if(j<0||j>=data.sections.length)return;[data.sections[i],data.sections[j]]=[data.sections[j],data.sections[i]];render();}
function renderEditor(){const host=$('section-editor');host.replaceChildren();const s=data.sections.find(x=>x.id===selected);$('section-status').textContent=s?'Seção em edição':'Nenhuma seção selecionada';if(!s){host.append(node('p','Escolha ou adicione uma seção à esquerda.'));return;}
const titleLabel=node('label','Título da seção');titleLabel.htmlFor='section-title';const title=node('input');title.id='section-title';title.maxLength=160;title.value=s.title;title.addEventListener('input',()=>{s.title=title.value;renderList();renderPreview();});
const bodyLabel=node('label','Texto / cláusulas');bodyLabel.htmlFor='section-body';const textarea=node('textarea');textarea.id='section-body';textarea.rows=9;textarea.maxLength=20000;textarea.value=s.body;textarea.addEventListener('input',()=>{s.body=textarea.value;renderFields();renderPreview();});
host.append(titleLabel,title,bodyLabel,textarea);}
function renderFields(){const host=$('field-list');host.replaceChildren();for(const name of extractFields()){const wrapper=node('div',undefined,'field-row');const label=node('label',name);const id='field-'+name;label.htmlFor=id;const input=node('input');input.id=id;input.value=safeText(data.fields[name]);input.maxLength=300;input.addEventListener('input',()=>{data.fields[name]=input.value;renderPreview();});wrapper.append(label,input);host.append(wrapper);}if(!host.childElementCount)host.append(node('p','Nenhuma variável encontrada. Use {{nome_campo}} no texto de uma seção.','note'));}
function interpolate(text){return text.replace(/\{\{\s*([A-Za-z][A-Za-z0-9_]{0,63})\s*\}\}/g,(all,name)=>{const val=safeText(data.fields[name]).trim();return val||all;});}
function previewContent(){const missing=new Set();const sections=data.sections.map(s=>({title:s.title,body:s.body.replace(/\{\{\s*([A-Za-z][A-Za-z0-9_]{0,63})\s*\}\}/g,(all,key)=>{const v=safeText(data.fields[key]).trim();if(!v)missing.add(key);return v||all;})}));return {sections,missing:[...missing]};}
function appendHighlighted(parent,text){const re=/\{\{\s*[A-Za-z][A-Za-z0-9_]{0,63}\s*\}\}/g;let start=0;for(const m of text.matchAll(re)){parent.append(document.createTextNode(text.slice(start,m.index)));parent.append(node('mark',m[0],'missing'));start=m.index+m[0].length;}parent.append(document.createTextNode(text.slice(start)));}
function renderPreview(){const host=$('document-preview');host.replaceChildren();host.append(node('h1',data.title||'Documento sem título'));const {sections,missing}=previewContent();sections.forEach((s,i)=>{host.append(node('h2',(i+1)+'. '+s.title));const p=node('p');appendHighlighted(p,s.body);host.append(p);});$('missing-fields').replaceChildren(node('p',missing.length?'Campos pendentes: '+missing.join(', '):'Nenhum campo variável pendente. A conferência jurídica e documental continua obrigatória.',missing.length?'warning':'status'));}
function render(){renderList();renderEditor();renderFields();renderPreview();}
function download(filename,text,type){const url=URL.createObjectURL(new Blob([text],{type}));const link=document.createElement('a');link.href=url;link.download=filename;link.click();setTimeout(()=>URL.revokeObjectURL(url),3000);}
function fileName(){return (data.title.normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9_-]+/gi,'-').replace(/^-|-$/g,'').slice(0,55)||'documento');}
function escapeHtml(str){return safeText(str).replace(/[&<>"']/g,x=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[x]));}
function exportHtml(){const {sections}=previewContent();const html='<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>'+escapeHtml(data.title)+'</title><style>body{font:12pt/1.6 Georgia,serif;margin:55px auto;max-width:800px;padding:0 30px}h1{text-align:center}h2{margin-top:28px;font-size:15pt}p{white-space:pre-wrap}@media print{body{margin:0;max-width:none}}</style></head><body><h1>'+escapeHtml(data.title)+'</h1>'+sections.map((s,i)=>'<h2>'+(i+1)+'. '+escapeHtml(s.title)+'</h2><p>'+escapeHtml(s.body)+'</p>').join('')+'</body></html>';download(fileName()+'.html',html,'text/html;charset=utf-8');}
function validImport(x){if(!x||typeof x!=='object'||Array.isArray(x)||typeof x.title!=='string'||x.title.length>160||!Array.isArray(x.sections)||x.sections.length>100||!x.sections.every(s=>s&&typeof s.title==='string'&&s.title.length<=160&&typeof s.body==='string'&&s.body.length<=20000)||!x.fields||typeof x.fields!=='object'||Array.isArray(x.fields)||Object.keys(x.fields).length>200||!Object.values(x.fields).every(v=>typeof v==='string'&&v.length<=300))return false;return true;}
$('add-section').addEventListener('click',()=>{const s=section($('module-type').value);data.sections.push(s);selected=s.id;render();});
$('use-template').addEventListener('click',()=>{if(data.sections.length&&!confirm('Substituir todas as seções atuais pelo modelo selecionado?'))return;data.sections=presets[$('doc-type').value].map(section);selected=data.sections[0]?.id||null;render();});
$('doc-name').addEventListener('input',e=>{data.title=e.target.value;renderPreview();});
$('refresh-fields').addEventListener('click',renderFields);
$('save-project').addEventListener('click',()=>download(fileName()+'.json',JSON.stringify({schemaVersion:1,title:data.title,sections:data.sections,fields:data.fields},null,2),'application/json'));
$('save-document').addEventListener('click',exportHtml);
$('print-document').addEventListener('click',()=>window.print());
$('import-button').addEventListener('click',()=>$('import-file').click());
$('import-file').addEventListener('change',async e=>{const file=e.target.files?.[0];if(!file)return;if(file.size>250000){alert('Projeto muito grande. Limite: 250 KB.');return;}try{const x=JSON.parse(await file.text());if(!validImport(x))throw Error('Formato inválido ou excede limites.');data={title:x.title,sections:x.sections.map(s=>({id:crypto.randomUUID?.()||String(Math.random()),title:s.title,body:s.body})),fields:Object.fromEntries(Object.entries(x.fields).filter(([key])=>/^[A-Za-z][A-Za-z0-9_]{0,63}$/.test(key)))};$('doc-name').value=data.title;selected=data.sections[0]?.id||null;render();}catch(err){alert('Não foi possível importar: '+err.message);}finally{e.target.value='';}});
render();