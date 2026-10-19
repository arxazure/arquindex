const KEY='arquindex-connect-v2';let data;try{data=JSON.parse(localStorage.getItem(KEY))||{actions:[],competitors:[],ranking:[],importedAt:null}}catch(e){data={actions:[],competitors:[],ranking:[],importedAt:null}};const $=id=>document.getElementById(id);const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));function save(){localStorage.setItem(KEY,JSON.stringify(data));render()}function tab(id){document.querySelectorAll('.section').forEach(x=>x.classList.toggle('active',x.id===id));document.querySelectorAll('#nav [data-tab]').forEach(x=>x.classList.toggle('active',x.dataset.tab===id))}document.querySelectorAll('#nav [data-tab]').forEach(x=>x.onclick=()=>tab(x.dataset.tab));function openAction(title='',channel='Site'){ $('actionform').reset();$('editid').value='';$('atitle').value=title;$('achannel').value=channel;$('dlgtitle').textContent='Criar ação';$('dlg').showModal()}function editAction(id){const a=data.actions.find(x=>x.id===id);if(!a)return;$('editid').value=id;$('atitle').value=a.title;$('apriority').value=a.priority;$('achannel').value=a.channel;$('astatus').value=a.status;$('aurl').value=a.url||'';$('anotes').value=a.notes||'';$('dlgtitle').textContent='Editar ação';$('dlg').showModal()}$('actionform').onsubmit=e=>{e.preventDefault();const a={id:$('editid').value||String(Date.now()),title:$('atitle').value.trim(),priority:$('apriority').value,channel:$('achannel').value,status:$('astatus').value,url:$('aurl').value.trim(),notes:$('anotes').value.trim()};if(['Publicada','Validada com mídia'].includes(a.status)&&!a.url){alert('Para marcar como publicada, informe a URL pública.');return}const i=data.actions.findIndex(x=>x.id===a.id);if(i<0)data.actions.push(a);else data.actions[i]=a;$('dlg').close();save()};function addCompetitor(){const name=$('compname').value.trim(),url=$('compurl').value.trim();if(!name)return;if(url&&!/^https?:\/\//i.test(url)){alert('Informe uma URL iniciada por https://');return}data.competitors.push({name,url,notes:''});$('compname').value='';$('compurl').value='';save()}function setCompNote(i){const c=data.competitors[i],note=prompt('Observações e evidências sobre '+c.name,c.notes||'');if(note!==null){c.notes=note;save()}}function makeAction(title,channel='SEO técnico'){openAction(title,channel);tab('actions')}function csvParse(s){const lines=s.replace(/^\uFEFF/,'').trim().split(/\r?\n/);const delimiter=(lines[0].match(/;/g)||[]).length>(lines[0].match(/,/g)||[]).length?';':',';return lines.map(line=>{let out=[],v='',q=false;for(let i=0;i<line.length;i++){const c=line[i];if(c==='"'){if(q&&line[i+1]==='"'){v+='"';i++}else q=!q}else if(c===delimiter&&!q){out.push(v);v=''}else v+=c}out.push(v);return out})}function num(s){return Number(String(s||'0').replace(/\s/g,'').replace(/%/g,'').replace(',','.'))||0}$('csv').onchange=async e=>{const f=e.target.files[0];if(!f)return;const status=$('csv-status');if(status)status.textContent='Lendo '+f.name+'...';let rows;try{rows=csvParse(await f.text())}catch(err){if(status)status.textContent='Erro ao ler o arquivo: '+err.message;return}const head=rows.shift().map(x=>x.toLowerCase().trim());const find=(...opts)=>head.findIndex(h=>opts.some(o=>h===o));const qi=find('query','consultas','consulta','top queries'),pi=find('page','página','pagina','pages'),ci=find('clicks','cliques'),ii=find('impressions','impressões','impressoes'),pos=find('position','posição','posicao');if(ci<0||ii<0||pos<0){if(status)status.textContent='CSV incompatível: faltam as colunas Cliques, Impressões ou Posição.';alert('CSV incompatível: faltam cliques, impressões ou posição.');return}data.ranking=rows.filter(x=>x.length>=head.length).map(x=>({query:qi>=0?x[qi]:'',page:pi>=0?x[pi]:'',clicks:num(x[ci]),impressions:num(x[ii]),position:num(x[pos])}));data.importedAt=new Date().toISOString();const suggestions=generateSeoActions();save();if(status)status.textContent='Importação concluída: '+data.ranking.length+' registros; '+suggestions+' ações SEO geradas automaticamente.';tab('ranking')};const csvHome=document.getElementById('csv-home');if(csvHome){csvHome.addEventListener('change',async function(){const f=this.files&&this.files[0];if(!f)return;const mainInput=document.getElementById('csv');const status=document.getElementById('csv-home-status');if(status)status.textContent='Lendo '+f.name+'...';try{const dt=new DataTransfer();dt.items.add(f);mainInput.files=dt.files;mainInput.dispatchEvent(new Event('change',{bubbles:true}));setTimeout(()=>{if(status)status.textContent=document.getElementById('csv-status').textContent},300)}catch(err){if(status)status.textContent='Erro: '+err.message}})}
function generateSeoActions(){
 const rows=Array.isArray(data.ranking)?data.ranking:[];
 const seen=new Set(data.actions.map(a=>a.sourceKey).filter(Boolean));
 let created=0;
 function add(key,title,priority,notes){
  if(seen.has(key))return;
  data.actions.push({id:String(Date.now())+'-'+created,sourceKey:key,title,priority,channel:'SEO técnico',status:'Planejada',notes,url:''});
  seen.add(key);created++;
 }
 const groups=new Map();
 rows.forEach(r=>{const q=String(r.query||'').trim().toLowerCase();if(!q)return;if(!groups.has(q))groups.set(q,[]);groups.get(q).push(r)});
 groups.forEach((list,q)=>{
  const ordered=list.filter(x=>Number(x.impressions)>0).sort((a,b)=>Number(b.impressions)-Number(a.impressions));
  if(!ordered.length)return;
  const best=ordered[0],position=Number(best.position),impressions=Number(best.impressions),pages=[...new Set(list.map(x=>x.page).filter(Boolean))];
  if(pages.length>1)add('can:'+q,'Investigar canibalização: '+q,'Alta','A consulta aparece em '+pages.length+' URLs. Comparar intenção, conteúdo e canonicals: '+pages.join(' | '));
  if(impressions>=20&&position>3&&position<=10)add('top3:'+q,'Otimizar para Top 3: '+q,'Alta','Posição '+position.toFixed(1)+'; '+impressions+' impressões. Revisar título, conteúdo e links internos. URL: '+(best.page||'não informada'));
  else if(impressions>=20&&position>10&&position<=20)add('top10:'+q,'Otimizar para Top 10: '+q,'Alta','Posição '+position.toFixed(1)+'; '+impressions+' impressões. Revisar intenção de busca, cobertura temática e indexação. URL: '+(best.page||'não informada'));
  else if(impressions>=50&&position>20)add('low:'+q,'Diagnosticar baixa visibilidade: '+q,'Média','Posição '+position.toFixed(1)+'; '+impressions+' impressões. Avaliar relevância e concorrentes.');
 });
 if(created)save();
 return created;
}
function render(){const rows=data.ranking,acts=data.actions;const clicks=rows.length?rows.reduce((s,r)=>s+r.clicks,0):null;$('clicks').textContent=clicks===null?'—':clicks.toLocaleString('pt-BR');$('top10').textContent=rows.length?new Set(rows.filter(r=>r.query&&r.position<=10).map(r=>r.query)).size:'—';$('clicksnote').textContent=data.importedAt?'CSV importado '+new Date(data.importedAt).toLocaleDateString('pt-BR'):'Importe dados do Search Console';$('date').textContent=data.importedAt?'Última importação: '+new Date(data.importedAt).toLocaleString('pt-BR'):'Sem dados de busca';$('openactions').textContent=acts.filter(a=>!['Publicada','Validada com mídia'].includes(a.status)).length;$('verified').textContent=acts.filter(a=>a.url&&['Publicada','Validada com mídia'].includes(a.status)).length;const pr=acts.filter(a=>a.priority==='Alta'&&!['Publicada','Validada com mídia'].includes(a.status));$('priority').innerHTML=pr.length?pr.slice(0,7).map(a=>'<p><span class="pill">'+esc(a.priority)+'</span> <b>'+esc(a.title)+'</b> <button class="btn secondary" onclick="editAction(\''+a.id+'\')">Abrir</button></p>').join(''):'<div class="empty">Nenhuma ação de alta prioridade cadastrada. Use “Criar ação” para iniciar.</div>';$('rankrows').innerHTML=rows.length?rows.slice(0,500).map(r=>'<tr><td>'+esc(r.query)+'</td><td>'+esc(r.page)+'</td><td>'+r.clicks+'</td><td>'+r.impressions+'</td><td>'+r.position.toFixed(1)+'</td><td><button class="btn secondary" data-q="'+esc(r.query)+'">Criar ação</button></td></tr>').join(''):'<tr><td colspan="6">Nenhum CSV importado</td></tr>';document.querySelectorAll('#rankrows button').forEach(b=>b.onclick=()=>makeAction('Analisar consulta: '+b.dataset.q));$('comprows').innerHTML=data.competitors.length?data.competitors.map((c,i)=>'<tr><td>'+esc(c.name)+'</td><td>'+ (c.url?'<a target="_blank" rel="noopener" href="'+esc(c.url)+'">Visitar site</a>':'—')+'</td><td>'+esc(c.notes||'Sem observações')+'</td><td><button class="btn secondary" onclick="setCompNote('+i+')">Anotar</button> <button class="btn dark" onclick="makeAction(\'Analisar concorrente: '+esc(c.name).replace(/'/g,'')+'\')">Criar ação</button></td></tr>').join(''):'<tr><td colspan="4">Cadastre as empresas concorrentes indicadas</td></tr>';const grouped={};rows.filter(r=>r.query&&r.page).forEach(r=>(grouped[r.query]??=[]).push(r.page));const can=Object.entries(grouped).map(([q,p])=>({q,p:[...new Set(p)]})).filter(x=>x.p.length>1);$('cannrows').innerHTML=can.length?can.slice(0,100).map(x=>'<tr><td>'+esc(x.q)+'</td><td>'+x.p.length+'</td><td>'+x.p.map(esc).join('<hr>')+'</td><td><button class="btn dark" data-q="'+esc(x.q)+'">Investigar</button></td></tr>').join(''):'<tr><td colspan="4">Nenhum conflito identificado; é necessário CSV contendo consulta e URL para essa análise</td></tr>';document.querySelectorAll('#cannrows button').forEach(b=>b.onclick=()=>makeAction('Investigar canibalização: '+b.dataset.q));const opp=rows.filter(r=>r.query&&r.impressions>0&&r.position>=4&&r.position<=20).sort((a,b)=>b.impressions-a.impressions);$('opprows').innerHTML=opp.length?opp.slice(0,100).map(r=>'<tr><td>'+esc(r.query)+'</td><td>'+r.impressions+'</td><td>'+r.position.toFixed(1)+'</td><td>'+esc(r.page)+'</td><td><button class="btn dark" data-q="'+esc(r.query)+'">Criar ação</button></td></tr>').join(''):'<tr><td colspan="5">Nenhuma oportunidade identificada com os dados disponíveis</td></tr>';document.querySelectorAll('#opprows button').forEach(b=>b.onclick=()=>makeAction('Otimizar busca: '+b.dataset.q));const filter=$('filter').value;$('actionrows').innerHTML=acts.filter(a=>!filter||a.priority===filter).map(a=>'<tr><td><span class="pill">'+esc(a.priority)+'</span></td><td><b>'+esc(a.title)+'</b><div class="hint">'+esc(a.notes||'')+'</div></td><td>'+esc(a.channel)+'</td><td>'+esc(a.status)+'</td><td>'+(a.url?'<a href="'+esc(a.url)+'" target="_blank" rel="noopener">Abrir comprovante</a>':'—')+'</td><td><button class="btn secondary" onclick="editAction(\''+a.id+'\')">Editar</button></td></tr>').join('')||'<tr><td colspan="6">Nenhuma ação cadastrada</td></tr>';$('pubrows').innerHTML=acts.filter(a=>['Site','LinkedIn','Instagram','Google Business','Blogger','Bing / IndexNow'].includes(a.channel)).map(a=>'<tr><td>'+esc(a.title)+'</td><td>'+esc(a.channel)+'</td><td><span class="pill '+(a.url?'green':'red')+'">'+esc(a.status)+'</span></td><td>'+(a.url?'<a target="_blank" rel="noopener" href="'+esc(a.url)+'">Abrir</a>':'Sem comprovante')+'</td></tr>').join('')||'<tr><td colspan="4">Sem registros de publicação</td></tr>'}function exportData(){const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='arquindex-connect-backup.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),500)}async function importBackup(e){const f=e.target.files[0];if(!f)return;try{const d=JSON.parse(await f.text());if(!Array.isArray(d.actions)||!Array.isArray(d.ranking)||!Array.isArray(d.competitors))throw Error();if(!confirm('Substituir os dados locais pelo backup selecionado?'))return;data=d;save()}catch{alert('Arquivo de backup inválido')}}render();

let publicAudit=null;
async function loadPublicAudit(force=false){
 const status=document.getElementById('audit-status'),table=document.getElementById('auditrows');
 if(!status||!table)return;
 status.textContent='Consultando auditoria pública...';
 try{
  const url='https://raw.githubusercontent.com/arxazure/arquindex/master/painel-seo/auditoria-publica.json'+(force?'?t='+Date.now():'');
  const response=await fetch(url,{cache:'no-store'});
  if(!response.ok)throw new Error('Relatório ainda não disponível (HTTP '+response.status+'). Execute o workflow no GitHub Actions.');
  const report=await response.json();
  if(!Array.isArray(report.issues))throw new Error('Formato de relatório inválido');
  publicAudit=report;
  status.textContent='Coleta: '+(report.generated_at||'sem data')+' | '+report.scanned+' páginas verificadas | '+report.issues_count+' páginas com problemas. Fonte: HTML público, não Google Search Console.';
  table.innerHTML=report.issues.length?report.issues.slice(0,150).map(x=>'<tr><td><a href="'+esc(x.url)+'" target="_blank" rel="noopener">'+esc(x.url)+'</a></td><td>'+x.issues.map(esc).join('<hr>')+'</td></tr>').join(''):'<tr><td colspan="2">Nenhum problema registrado na coleta.</td></tr>';
 }catch(err){
  status.textContent='Auditoria indisponível: '+err.message;
  table.innerHTML='<tr><td colspan="2">Nenhuma evidência carregada. Não serão criadas ações fictícias.</td></tr>';
 }
}
function createAuditActions(){
 if(!publicAudit||!Array.isArray(publicAudit.issues)){alert('Carregue primeiro um relatório real de auditoria.');return}
 const seen=new Set(data.actions.map(a=>a.sourceKey).filter(Boolean));
 let count=0;
 for(const entry of publicAudit.issues){
  if(!entry.url||!Array.isArray(entry.issues))continue;
  for(const issue of entry.issues){
   const key='audit:'+entry.url+':'+issue;
   if(seen.has(key))continue;
   const priority=/Falha ao acessar|HTTP|Noindex/i.test(issue)?'Alta':'Média';
   data.actions.push({id:'audit-'+Date.now()+'-'+count,sourceKey:key,title:'Corrigir '+issue,priority,channel:'SEO técnico',status:'Planejada',notes:'Evidência da auditoria pública '+(publicAudit.generated_at||'')+'. Página: '+entry.url,url:entry.url});
   seen.add(key);count++;
  }
 }
 if(count)save();
 const status=document.getElementById('audit-status');if(status)status.textContent+=' | '+count+' novas ações criadas.';
}
loadPublicAudit();

async function loadDirectGsc(){
 const el=document.getElementById('gsc-direct-status');
 if(el)el.textContent='Consultando relatório oficial do Google no GitHub...';
 try{
  const response=await fetch('https://raw.githubusercontent.com/arxazure/arquindex/master/painel-seo/gsc-real.json?t='+Date.now(),{cache:'no-store'});
  if(!response.ok)throw Error('Coleta oficial ainda não executada');
  const payload=await response.json();
  if(payload.source!=='Google Search Console API OAuth'||!Array.isArray(payload.rows))throw Error('Relatório inválido');
  const rows=payload.rows.filter(r=>r&&typeof r.query==='string'&&typeof r.page==='string');
  data.ranking=rows.map(r=>({query:r.query,page:r.page,clicks:Number(r.clicks)||0,impressions:Number(r.impressions)||0,position:Number(r.position)||0}));
  data.importedAt=payload.generated_at;
  save();
  const count=generateSeoActions();
  if(el)el.textContent=rows.length+' registros reais importados de '+(payload.properties||[]).length+' propriedades; '+count+' novas ações.';
 }catch(err){if(el)el.textContent='Coleta direta indisponível: '+err.message+'. Os dados existentes foram preservados.'}
}


;

/* Navegacao independente: funciona mesmo se os modulos de dados falharem. */
(function(){
  function activate(name){
    var target=document.getElementById(name);
    if(!target || !target.classList.contains('section')) return;
    document.querySelectorAll('main .section').forEach(function(el){
      var active=el.id===name;
      el.classList.toggle('active',active);
      el.hidden=!active;
      el.setAttribute('aria-hidden',String(!active));
    });
    document.querySelectorAll('#nav [data-tab]').forEach(function(btn){
      var active=btn.getAttribute('data-tab')===name;
      btn.classList.toggle('active',active);
      btn.setAttribute('aria-current',active?'page':'false');
    });
    try{history.replaceState(null,'','#'+name)}catch(e){}
  }
  document.getElementById('nav').addEventListener('click',function(e){
    var btn=e.target.closest('[data-tab]');
    if(!btn)return;
    e.preventDefault();
    e.stopImmediatePropagation();
    activate(btn.getAttribute('data-tab'));
  },true);
  var initial=location.hash.slice(1);
  activate(document.getElementById(initial)?initial:'overview');
  window.addEventListener('hashchange',function(){
    var name=location.hash.slice(1);
    if(document.getElementById(name))activate(name);
  });
})();
