import http from "node:http";
import { URL } from "node:url";
import { articles } from "./articles.js";
import { landingPages } from "./landing-pages.js";
import { authorityPages } from "./authority-pages.js";

const OFFICIAL="https://arquindex.com.br";
const PORT = Number(process.env.PORT || 3000);
const BASE = (process.env.SITE_BASE_URL || "").replace(/\/$/,"");
const WHATSAPP = "5531973632725";

const services = [
["digitalizacao-documentos","Digitalização de Documentos","Digitalização profissional com OCR, PDF/A, indexação, controle de qualidade e rastreabilidade.","A partir de R$ 0,10 por página"],
["digitalizacao-certificada","Digitalização Certificada","Projeto de digitalização alinhado aos requisitos técnicos do Decreto 10.278/2020, com integridade, metadados e controle de qualidade.","Sob orçamento"],
["prontuarios-medicos","Digitalização de Prontuários Médicos","Organização, captura, OCR e indexação de prontuários com foco em rastreabilidade, sigilo e acesso controlado.","Sob orçamento"],
["gestao-documental","Gestão Documental","Classificação, plano de classificação, temporalidade, retenção, destinação, governança e acesso seguro.","Sob orçamento"],
["organizacao-arquivos","Organização de Arquivos","Organização física e digital, inventário, endereçamento, empréstimos, temporalidade e padronização.","Sob orçamento"],
["alfresco-incloud","Alfresco inCloud","ECM/GED em nuvem com permissões, metadados, versionamento, workflows, OCR, pesquisa e auditoria.","A partir de R$ 750"],
["consultoria-lgpd","Adequação LGPD","Diagnóstico, mapeamento, ROPA, RIPD quando aplicável, políticas, contratos, cookies, direitos dos titulares e governança.","A partir de R$ 2.500"],
["dpo-terceirizado","DPO Terceirizado","Encarregado terceirizado, acompanhamento, orientação, registros, canal de titulares e governança de privacidade.","A partir de R$ 299/mês"],
["databook","Databook","Organização de documentos de engenharia por volumes, capítulos, itens, subitens, índices, conferência e entrega.","Sob orçamento"],
["digitacao","Digitação e Processamento de Formulários","Captura estruturada, validação, conferência, tratamento de dados e relatórios de produtividade.","Sob orçamento"],
["guarda-documental","Guarda Documental","Custódia, inventário, endereçamento, consultas, movimentações, temporalidade e rastreabilidade.","Sob orçamento"],
["incineracao-segura","Incineração Segura","Descarte controlado e documentado de arquivos após validação de temporalidade e autorização.","Sob orçamento"],
["storage-documental","Storage Documental / SelfStorage","Organização e operação de arquivos em unidades de self storage com inventário, estantes, endereçamento e consultas.","Sob orçamento"],
["seguranca-informacao","Segurança da Informação","Controles, processos, políticas, gestão de acessos, incidentes e boas práticas de segurança.","Sob orçamento"],
["livros-cartorios","Digitalização de Livros e Cartórios","Digitalização de livros e documentos cartorários com captura adequada ao formato, OCR e indexação.","A partir de R$ 0,25 por página"],
["juridico","Digitalização de Processos Jurídicos","Digitalização, OCR, organização e indexação de processos e documentos jurídicos.","Sob orçamento"],
["farmaceutico","Documentos Farmacêuticos","Digitalização e organização de documentação farmacêutica, administrativa e regulatória.","Sob orçamento"],
["engenharia","Documentos de Engenharia","Digitalização, organização e estruturação de desenhos, relatórios, databooks e documentação técnica.","Sob orçamento"],
["meio-ambiente","Relatórios de Meio Ambiente","Digitalização e digitação de relatórios, laudos, estudos e documentação ambiental.","Sob orçamento"],
["treinamentos","Treinamentos Corporativos","Treinamentos em gestão documental, privacidade, LGPD, segurança e operação de processos documentais.","Sob orçamento"]
];

const cities = [
"Belo Horizonte-MG","Contagem-MG","Betim-MG","Nova Lima-MG","Uberlandia-MG","Juiz de Fora-MG","Montes Claros-MG","Divinopolis-MG","Ipatinga-MG","Sete Lagoas-MG",
"Sao Paulo-SP","Campinas-SP","Guarulhos-SP","Sao Bernardo do Campo-SP","Santo Andre-SP","Osasco-SP","Sorocaba-SP","Ribeirao Preto-SP","Santos-SP","Sao Jose dos Campos-SP",
"Rio de Janeiro-RJ","Niteroi-RJ","Duque de Caxias-RJ","Nova Iguacu-RJ","Petropolis-RJ",
"Brasilia-DF","Goiania-GO","Anapolis-GO","Curitiba-PR","Londrina-PR","Maringa-PR","Porto Alegre-RS","Caxias do Sul-RS","Florianopolis-SC","Joinville-SC",
"Salvador-BA","Feira de Santana-BA","Recife-PE","Fortaleza-CE","Natal-RN","Joao Pessoa-PB","Maceio-AL","Aracaju-SE","Vitoria-ES","Serra-ES",
"Manaus-AM","Belem-PA","Cuiaba-MT","Campo Grande-MS","Palmas-TO"
];

const intents = [
["empresa","empresa especializada"],
["preco","preços e contratação"],
["terceirizacao","terceirização corporativa"],
["consultoria","consultoria e projeto"],
["solucao","solução empresarial"]
];

const cases = {
"prontuarios-medicos":"Experiências citadas pela Arquindex incluem projetos para organizações como Consete, Medicar, CST, Hospital Belvedere, Hospital de Guanhães e Santa Casa.",
"databook":"Experiências citadas incluem Boart Longyear, SanDisk, FLSmidth, Brasfels, Vallourec Oil & Gas França, Petronas e Samarco.",
"farmaceutico":"Experiências citadas incluem Hipolabor e Drogaria Araujo.",
"juridico":"Experiências citadas incluem Catta Preta Advogados, Teresa Mafra, Marcos Viana e Quaresma.",
"livros-cartorios":"Experiências citadas incluem 7º RI BH, Cartório Massote, Cartório de Notas de Matozinhos e Cartório de Notas de Ibirité.",
"engenharia":"Experiências citadas incluem Lhoist, Cimcop, Mecanorte, Terraço, Sólido Engenharia, Usimec, Soluções Usiminas, Petronas, Petrobras, Sandvik, Cemig Igarapé e RHI Magnesita.",
"treinamentos":"Experiências citadas incluem Brasfels, Federasantas, Vallourec França e Hozen Portugal."
};

const serviceFaqs = {
 "digitalizacao-documentos":[
  ["Qual a diferença entre digitalizar e apenas escanear?","Um projeto profissional inclui preparação, captura, controle de qualidade, OCR quando aplicável, indexação, organização e entrega; escanear pode significar apenas gerar uma imagem."],
  ["OCR vem incluído?","O OCR pode fazer parte do escopo para tornar PDFs pesquisáveis e apoiar extração de dados. A configuração depende do acervo e do nível de precisão exigido."],
  ["Como é calculado o prazo?","Prazo depende de volume, formatos, preparação, indexação, qualidade dos originais, logística e capacidade de produção dedicada."],
  ["É possível executar no cliente?","Sim, quando o escopo e a infraestrutura permitem. Projetos também podem prever coleta controlada e devolução."],
  ["Como pedir orçamento comparável?","Informe volume aproximado, formatos, estado físico, necessidade de OCR/indexação, cidade, prazo, coleta e forma de entrega."]
 ],
 "digitalizacao-certificada":[
  ["O Decreto 10.278/2020 vale para qualquer documento?","Não. A aplicação depende da natureza documental e das hipóteses previstas na legislação. O projeto deve avaliar requisitos técnicos e exceções."],
  ["Digitalizar permite eliminar o papel automaticamente?","Não. Temporalidade, valor histórico, legislação específica e requisitos setoriais precisam ser avaliados antes de qualquer destinação."],
  ["PDF/A é o mesmo que validade jurídica?","Não. PDF/A é um formato voltado à preservação. Integridade, metadados e demais requisitos precisam ser tratados conforme o caso."]
 ],
 "guarda-documental":[
  ["Como funciona a consulta a uma caixa?","O processo deve usar inventário, localização, protocolo de solicitação, rastreio de retirada e devolução e SLA definido."],
  ["Guarda terceirizada substitui gestão documental?","Não. Custódia física e gestão documental são complementares. Classificação, temporalidade e governança continuam necessárias."],
  ["É possível digitalizar sob demanda?","Sim, quando previsto no serviço, com controles de autorização, localização, captura e entrega."],
  ["Como calcular o espaço do acervo?","O cálculo usa quantidade e dimensões das caixas, ocupação de estantes, corredores, áreas de operação e margem de crescimento."]
 ],
 "databook":[
  ["O que é Databook?","É a organização estruturada da documentação técnica de um projeto, obra, equipamento ou contrato para entrega, consulta, auditoria e histórico."],
  ["Databook e as built são a mesma coisa?","Não. As built é um conjunto documental específico de como foi executado; o Databook pode reunir as built, certificados, relatórios, inspeções, manuais e outros registros."],
  ["Como controlar revisões?","O projeto deve distinguir versão válida, versões superadas, status de aprovação e vínculo com o índice contratual."]
 ],
 "alfresco-incloud":[
  ["Qual a diferença entre GED e ECM?","GED foca gestão eletrônica de documentos; ECM cobre um escopo mais amplo de conteúdo, processos, metadados, permissões, workflows e governança."],
  ["Alfresco pode integrar com Active Directory?","Sim, conforme versão e arquitetura adotadas, com planejamento de autenticação e sincronização."],
  ["Pode rodar em nuvem?","Sim. A arquitetura pode ser desenhada para nuvem ou infraestrutura própria, considerando segurança, disponibilidade, backup e integrações."]
 ],
 "consultoria-lgpd":[
  ["Adequação LGPD é só documentação?","Não. É um programa de governança que conecta processos, dados pessoais, sistemas, fornecedores, bases legais, segurança, retenção e responsabilidades."],
  ["ROPA precisa ser atualizado?","Sim. Mudanças em processos, sistemas, finalidades e fornecedores podem exigir revisão."],
  ["Consultoria inclui DPO?","Pode incluir como escopo separado ou integrado, conforme o plano contratado."]
 ],
 "dpo-terceirizado":[
  ["O DPO pode ser terceirizado?","A atuação do encarregado pode ser estruturada por profissional ou serviço terceirizado, observadas as regras aplicáveis e o escopo contratado."],
  ["O DPO assume a responsabilidade legal da empresa?","Não. O encarregado apoia comunicação e governança; a organização mantém suas responsabilidades legais."],
  ["O que deve constar no SLA?","Canais, disponibilidade, tipos de demanda, prazos de resposta, responsáveis internos e critérios de escalonamento."]
 ]
};

const serviceBenefits = {
 "digitalizacao-documentos":["Busca mais rápida","Redução de manuseio físico","OCR e indexação","Rastreabilidade por lote","Entrega organizada"],
 "guarda-documental":["Localização controlada","Inventário e endereçamento","SLA de consulta","Temporalidade ativa","Digitalização sob demanda"],
 "databook":["Índice confiável","Controle de revisões","Pendências rastreáveis","Entrega técnica organizada","Histórico do projeto"],
 "alfresco-incloud":["Repositório central","Permissões por função","Versionamento","Workflow","Pesquisa e auditoria"],
 "consultoria-lgpd":["Mapa de riscos","Inventário de dados","Governança","Planos de ação","Evidências de conformidade"],
 "dpo-terceirizado":["Rotina de governança","Canal de titulares","Registro de decisões","Acompanhamento de pendências","Orientação contínua"]
};

const serviceApplications = {
 "digitalizacao-documentos":["RH e Departamento Pessoal","Saúde e prontuários","Jurídico","Indústria","Engenharia e Databook"],
 "guarda-documental":["Administrativo","RH","Jurídico","Saúde","Engenharia"],
 "databook":["Construção civil","Mineração","Siderurgia","Óleo e gás","Manutenção industrial"],
 "alfresco-incloud":["RH","Engenharia","Qualidade","Jurídico","Administrativo"],
 "consultoria-lgpd":["PMEs","Saúde","Educação","Indústria","Serviços profissionais"],
 "dpo-terceirizado":["PMEs","Clínicas","Educação","Serviços profissionais","Operações com dados pessoais"]
};

function esc(s){return String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));}
function jsonLd(data){return '<script type="application/ld+json">'+JSON.stringify(data).replace(/<\/script/gi,'<\\/script')+'</script>';}
function organizationSchema(){
 return {"@context":"https://schema.org","@type":"Organization","name":"Arquindex","url":OFFICIAL,"email":"comercial@arquindex.com.br","telephone":"+55 31 97363-2725","areaServed":{"@type":"Country","name":"Brasil"},"knowsAbout":["gestão documental","digitalização de documentos","OCR","PDF/A","LGPD","DPO","Alfresco ECM","Databook","guarda documental"]};
}
function breadcrumbSchema(items,req){
 const o=origin(req);
 return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items.map((x,i)=>({"@type":"ListItem","position":i+1,"name":x[0],"item":x[1].startsWith("http")?x[1]:o+x[1]}))};
}
function answerBox(title,text){return '<div class="answer"><strong>'+esc(title)+'</strong><p>'+esc(text)+'</p></div>';}
function faqHtml(items){return items.map(([q,a])=>'<details class="faq"><summary>'+esc(q)+'</summary><p>'+esc(a)+'</p></details>').join("");}
function slugCity(c){return c.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");}
function origin(req){return "https://arquindex-web-production.up.railway.app";}
function isRailwayPreview(req){
 const host=(req.headers.host||"").toLowerCase();
 return host.endsWith(".railway.app");
}
function analyticsSnippet(){
 const id=process.env.GA4_MEASUREMENT_ID||"";
 if(!/^G-[A-Z0-9]{6,20}$/.test(id))return "";
 return `<script>
 window.dataLayer=window.dataLayer||[];
 function gtag(){dataLayer.push(arguments)}
 gtag('consent','default',{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});
 function startAnalytics(){
  if(window.__arqAnalyticsStarted)return;window.__arqAnalyticsStarted=true;
  var script=document.createElement('script');script.async=true;script.src='https://www.googletagmanager.com/gtag/js?id=${id}';document.head.appendChild(script);
  gtag('js',new Date());gtag('consent','update',{analytics_storage:'granted'});gtag('config','${id}',{anonymize_ip:true});
  var recorded=new Set();
  if('IntersectionObserver' in window){
   var obs=new IntersectionObserver(function(entries){entries.forEach(function(e){if(!e.isIntersecting)return;
   var el=e.target,heading=el.querySelector('h1,h2,h3');
   var section=(el.id||el.getAttribute('aria-label')||(heading&&heading.textContent.trim())||'secao').slice(0,95);
   if(recorded.has(section))return;recorded.add(section);
   gtag('event','section_view',{section_name:section,page_path:location.pathname});});},{threshold:0.4});
   document.querySelectorAll('main section,main article,section').forEach(function(el){obs.observe(el)});
  }
  document.addEventListener('click',function(e){var a=e.target.closest('a');if(!a)return;
   var label=(a.textContent||a.getAttribute('aria-label')||'link').trim().slice(0,95);
   var type=/wa.me|whatsapp/i.test(a.href)?'whatsapp_click':/contato|mailto:|tel:/i.test(a.href)?'contact_click':'link_click';
   gtag('event',type,{link_label:label,link_url:a.href,page_path:location.pathname});
  });
 }
 document.addEventListener('DOMContentLoaded',function(){
  var consent='';try{consent=localStorage.getItem('arquindex_analytics_consent')||''}catch(e){}
  if(consent==='granted'){startAnalytics();return}if(consent==='denied')return;
  var bar=document.createElement('div');bar.setAttribute('role','dialog');bar.setAttribute('aria-label','Preferencias de analise');
  bar.style.cssText='position:fixed;bottom:12px;left:12px;right:12px;z-index:9999;max-width:720px;margin:auto;padding:16px;border-radius:12px;background:#fff;color:#14253e;border:1px solid #ddd;box-shadow:0 8px 30px #0003;font:14px Arial';
  bar.innerHTML='<span>Utilizamos estatisticas opcionais para melhorar paginas e conteudos. Voce pode aceitar ou recusar a medicao de visitas.</span> <button type="button" data-choice="granted">Aceitar</button> <button type="button" data-choice="denied">Recusar</button>';
  bar.addEventListener('click',function(e){var v=e.target.getAttribute('data-choice');if(!v)return;
   try{localStorage.setItem('arquindex_analytics_consent',v)}catch(err){}
   bar.remove();if(v==='granted')startAnalytics();
  });document.body.appendChild(bar);
 });
 </script>`;
}
function layout(title,desc,body,req,extraHead=""){
 const o=origin(req);
 const robotsMeta=isRailwayPreview(req)?'<meta name="robots" content="noindex,nofollow,noarchive">':'<meta name="robots" content="index,follow">';
 return `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)}</title><meta name="description" content="${esc(desc)}">${robotsMeta}<link rel="canonical" href="${o}${new URL(req.url,o).pathname}">${jsonLd(organizationSchema())}${extraHead}${analyticsSnippet()}
 <style>
 :root{--b:#0b3d91;--b2:#0b67c2;--ink:#0c1b33;--mut:#56657a;--bg:#f4f7fb;--card:#fff;--line:#d9e2ef;--g:#25d366}
 *{box-sizing:border-box}body{margin:0;font-family:Arial,Helvetica,sans-serif;color:var(--ink);background:#fff;line-height:1.55}
 header{position:sticky;top:0;z-index:30;background:#fff;border-bottom:1px solid var(--line)}.top{max-width:1200px;margin:auto;padding:14px 22px;display:flex;align-items:center;gap:24px}.brand{font-size:30px;font-weight:800;color:var(--b);letter-spacing:-1px}.tag{font-size:10px;color:#667;display:block}.nav{display:flex;gap:18px;flex:1;justify-content:center}.nav a{color:#23324a;text-decoration:none;font-size:14px}.contact{font-size:13px;text-align:right}.contact a{color:var(--b);font-weight:700;text-decoration:none}
 .hero{background:linear-gradient(110deg,#071f4d,#0b4fa7);color:#fff}.hero .wrap{max-width:1200px;margin:auto;padding:72px 22px}.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:1.3px;opacity:.85}.hero h1{font-size:48px;line-height:1.05;max-width:800px;margin:14px 0}.hero p{max-width:760px;font-size:18px;color:#d9e9ff}.cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}.btn{display:inline-block;padding:13px 18px;border-radius:10px;text-decoration:none;font-weight:700}.primary{background:#fff;color:var(--b)}.whats{background:var(--g);color:#08210f}
 .trust{max-width:1200px;margin:-24px auto 0;padding:0 22px;display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.pill{background:#fff;border:1px solid var(--line);box-shadow:0 8px 22px #08234a16;border-radius:14px;padding:18px;text-align:center}.pill strong{display:block;color:var(--b);font-size:20px}
 section{max-width:1200px;margin:auto;padding:58px 22px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px;box-shadow:0 5px 18px #142b4d0d}.card h3{margin-top:0}.price{font-weight:800;color:var(--b2)}.muted{color:var(--mut)}
 .band{background:var(--bg)}.answer{background:#eef6ff;border-left:5px solid var(--b2);border-radius:12px;padding:18px 20px;margin:20px 0}.answer p{margin:7px 0 0}.toc{display:flex;gap:10px;flex-wrap:wrap;padding:14px 0}.toc a{background:#edf3fb;border:1px solid var(--line);border-radius:999px;padding:8px 12px;text-decoration:none;color:var(--b)}.steps{counter-reset:step;display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.step{border:1px solid var(--line);border-radius:14px;padding:18px}.step:before{counter-increment:step;content:counter(step,decimal-leading-zero);display:block;color:var(--b2);font-weight:800;font-size:20px;margin-bottom:8px}.faq{border-top:1px solid var(--line);padding:14px 0}.faq summary{cursor:pointer;font-weight:700}.tablewrap{overflow:auto}.compare{width:100%;border-collapse:collapse}.compare th,.compare td{border:1px solid var(--line);padding:12px;text-align:left}.calc{background:var(--bg);padding:22px;border-radius:16px}.calc input{width:100%;max-width:240px;padding:10px;border:1px solid var(--line);border-radius:8px}.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.kpi{padding:18px;border:1px solid var(--line);border-radius:14px}.wafloat{position:fixed;right:20px;bottom:20px;background:var(--g);color:#fff;width:58px;height:58px;border-radius:50%;display:grid;place-items:center;text-decoration:none;font-size:26px;box-shadow:0 8px 24px #0003;z-index:40}
 footer{background:#071a3a;color:#dce7f7;padding:40px 22px}.foot{max-width:1200px;margin:auto;display:grid;grid-template-columns:2fr 1fr 1fr;gap:30px}.cookie{position:fixed;left:18px;right:18px;bottom:18px;background:#fff;border:1px solid var(--line);box-shadow:0 10px 30px #0003;border-radius:14px;padding:16px;z-index:50;display:flex;gap:16px;align-items:center}.cookie p{margin:0;flex:1;font-size:13px}.cookie button{border:0;padding:10px 13px;border-radius:8px;cursor:pointer}.accept{background:var(--b);color:#fff}
 @media(max-width:800px){.nav{display:none}.hero h1{font-size:36px}.grid,.trust,.foot,.steps,.kpis{grid-template-columns:1fr}.contact{font-size:12px}.cookie{flex-direction:column;align-items:stretch}}
 </style></head><body>
 <header><div class="top"><div><div class="brand">arquindex</div><span class="tag">EFICIÊNCIA MÁXIMA EM GESTÃO DE DOCUMENTOS</span></div><nav class="nav"><a href="/">Início</a><a href="/solucoes">Soluções</a><a href="/conteudo">Conteúdo</a><a href="/autoridade">Guias</a><a href="/setores">Setores</a><a href="https://arquindex.com.br/blog.html">Blog oficial</a><a href="https://arquindex.com.br/#clientes">Clientes</a><a href="/contato">Contato</a></nav><div class="contact">WhatsApp<br><a href="https://wa.me/${WHATSAPP}?text=Ol%C3%A1%20Arquindex%2C%20quero%20um%20or%C3%A7amento">31 97363-2725</a></div></div></header>
 ${body}
 <a class="wafloat" aria-label="Fale com a Arquindex no WhatsApp" href="https://wa.me/${WHATSAPP}?text=Ol%C3%A1%20Arquindex%2C%20quero%20saber%20mais%20sobre%20os%20servi%C3%A7os">✆</a>
 <div class="cookie" id="cookie"><p>Usamos cookies essenciais e, com sua autorização, cookies opcionais para melhorar sua experiência e mensurar o desempenho. Consulte nossa Política de Privacidade e Cookies.</p><button onclick="localStorage.setItem('aq_cookie','essential');this.parentElement.remove()">Rejeitar opcionais</button><button class="accept" onclick="localStorage.setItem('aq_cookie','all');this.parentElement.remove()">Aceitar todos</button></div>
 <script>if(localStorage.getItem('aq_cookie'))document.getElementById('cookie')?.remove()</script>
 <footer><div class="foot"><div><strong>Arquindex</strong><p>Há 20 anos apoiando empresas na transformação de arquivos em informação estratégica.</p></div><div><strong>Atendimento</strong><p>WhatsApp: 31 97363-2725<br>comercial@arquindex.com.br<br>Belo Horizonte / MG</p></div><div><strong>Ecossistema Arquindex</strong><p><a style="color:#fff" href="https://arquindex.com.br/">Site oficial</a> · <a style="color:#fff" href="https://arquindex.com.br/blog.html">Blog e acervo</a> · <a style="color:#fff" href="/conteudo">Artigos técnicos</a></p></div></div></footer></body></html>`;
}
function home(req){
 const cards=services.slice(0,12).map(([s,n,d,p])=>`<article class="card"><h3>${n}</h3><p class="muted">${d}</p><div class="price">${p}</div><p><a href="/solucoes/${s}">Conhecer solução →</a></p></article>`).join("");
 const body=`<div class="hero"><div class="wrap"><div class="eyebrow">Gestão documental · Digitalização · LGPD · ECM · Todo o Brasil</div><h1>Transformamos arquivos em informação estratégica.</h1><p>Digitalização, gestão documental, LGPD, Alfresco inCloud, guarda, organização de arquivos, Databook e soluções corporativas com atendimento especializado.</p><div class="cta"><a class="btn primary" href="/solucoes">Conhecer soluções</a><a class="btn whats" href="https://wa.me/${WHATSAPP}?text=Ol%C3%A1%20Arquindex%2C%20quero%20um%20or%C3%A7amento">Falar no WhatsApp</a></div></div></div>
 <div class="trust"><div class="pill"><strong>20 anos</strong>de experiência</div><div class="pill"><strong>OCR + PDF/A</strong>processamento documental</div><div class="pill"><strong>Brasil</strong>projetos corporativos</div><div class="pill"><strong>LGPD</strong>privacidade e governança</div></div>
 <section>${answerBox("Resposta direta","A Arquindex atende empresas que precisam digitalizar, organizar, proteger, localizar e governar documentos físicos e digitais. O trabalho combina operação documental, OCR e indexação, gestão de arquivos, LGPD, ECM Alfresco, Databook, guarda e descarte controlado conforme o escopo.")}<h2>Núcleos de conhecimento e serviços</h2><p class="muted">A estratégia de autoridade concentra cada tema em uma página pilar, apoiada por guias, artigos, FAQs, páginas setoriais e conteúdos locais realmente diferenciados.</p><div class="grid">${cards}</div></section>
 <div class="band"><section><h2>Autoridade por especialidade</h2><div class="grid">
 <article class="card"><h3>Digitalização e OCR</h3><p>Processo técnico, qualidade, OCR, PDF/A, indexação, Decreto 10.278/2020 e grandes volumes.</p><a href="/solucoes/digitalizacao-documentos">Página pilar →</a></article>
 <article class="card"><h3>Guarda e gestão documental</h3><p>Inventário, endereçamento, SLA de consulta, temporalidade, digitalização sob demanda e descarte.</p><a href="/solucoes/guarda-documental">Página pilar →</a></article>
 <article class="card"><h3>LGPD e DPO</h3><p>Diagnóstico, ROPA, governança, contratos, titulares, incidentes e rotina do encarregado.</p><a href="/solucoes/consultoria-lgpd">Página pilar →</a></article>
 <article class="card"><h3>Alfresco ECM</h3><p>Repositório, permissões, metadados, versionamento, workflows, busca, auditoria e integração.</p><a href="/solucoes/alfresco-incloud">Página pilar →</a></article>
 <article class="card"><h3>Databook e engenharia</h3><p>Índice, capítulos, revisões, pendências, fornecedores, as built, certificados e aceite.</p><a href="/solucoes/databook">Página pilar →</a></article>
 <article class="card"><h3>Biblioteca normativa</h3><p>Leituras oficiais e comentários técnicos sobre LGPD, Decreto 10.278/2020 e CONARQ.</p><a href="/biblioteca-normativa">Consultar biblioteca →</a></article>
 </div></section></div>
 <section><h2>Páginas que já concentram sinais de busca</h2><p>O fortalecimento editorial prioriza URLs com histórico antes de criar páginas novas.</p><div class="grid">
 <article class="card"><h3>Guarda de documentos</h3><p>Custódia, inventário, consulta e temporalidade.</p><a href="https://www.arquindex.com.br/guarda_de_documentos.html">Conteúdo histórico →</a></article>
 <article class="card"><h3>Databook</h3><p>Organização e montagem de documentação técnica.</p><a href="https://www.arquindex.com.br/montagem_databook_organizar.html">Conteúdo histórico →</a></article>
 <article class="card"><h3>Consultoria LGPD</h3><p>Adequação, governança e proteção de dados.</p><a href="https://www.arquindex.com.br/lgpd-consultoria.html">Conteúdo histórico →</a></article>
 </div></section>
 <div class="band"><section><h2>Experiência em projetos complexos</h2><p>Ao longo de duas décadas, a Arquindex acumulou experiências em setores como siderurgia, mineração, engenharia, saúde, cartórios, jurídico, educação, indústria farmacêutica, óleo & gás e serviços profissionais.</p><p><strong>Referências institucionais citadas:</strong> Usiminas, Cimcop, Lhoist, FCA/Fiat, Petrobras, Petronas, RHI Magnesita e Unimed BH. A natureza e o escopo de cada projeto devem ser confirmados antes da publicação de um case individual.</p><p><a class="btn primary" href="https://arquindex.com.br/#clientes">Consultar seção de clientes no site oficial →</a></p></section></div>`;
 const extra=jsonLd(breadcrumbSchema([["Início","/"]],req));
 return layout("Arquindex | Gestão Documental, Digitalização, LGPD e ECM","Há 20 anos em gestão documental, digitalização, LGPD, Alfresco ECM, Databook e organização de arquivos.",body,req,extra);
}
function solutionPage(slug,req){
 const s=services.find(x=>x[0]===slug); if(!s)return null;
 const [_,name,desc,price]=s;
 const caseTxt=cases[slug]||"A Arquindex atua há 20 anos em projetos corporativos de gestão documental, digitalização, organização de arquivos, compliance e tecnologia.";
 const benefits=(serviceBenefits[slug]||["Diagnóstico","Execução controlada","Rastreabilidade","Qualidade","Entrega organizada"]).map(x=>'<div class="kpi"><strong>'+esc(x)+'</strong></div>').join("");
 const apps=(serviceApplications[slug]||["Indústria","Serviços","Jurídico","Administrativo","Operações corporativas"]).map(x=>'<li>'+esc(x)+'</li>').join("");
 const faqs=serviceFaqs[slug]||[
  ["Como funciona a contratação?","O projeto começa pelo levantamento do objetivo, volume, prazo, requisitos técnicos, local de execução e forma de entrega."],
  ["O serviço pode ser executado por etapas?","Sim. O escopo pode ser dividido por lotes, áreas, unidades, períodos ou prioridades."],
  ["Como é definido o preço?","O valor depende de volume, complexidade, preparação, indexação, prazo, logística e requisitos técnicos."]
 ];
 const faqSchema={"@context":"https://schema.org","@type":"FAQPage","mainEntity":faqs.map(([q,a])=>({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}))};
 const serviceSchema={"@context":"https://schema.org","@type":"Service","name":name,"description":desc,"provider":{"@type":"Organization","name":"Arquindex","url":OFFICIAL},"areaServed":{"@type":"Country","name":"Brasil"}};
 const bread=breadcrumbSchema([["Início","/"],["Soluções","/solucoes"],[name,"/solucoes/"+slug]],req);
 const extra= slug==="digitalizacao-certificada" ? "<p><strong>Digitalização certificada:</strong> projetos podem ser estruturados considerando os requisitos técnicos do Decreto 10.278/2020, incluindo padrões de digitalização, metadados, integridade e controle de qualidade, conforme o contexto do acervo.</p><p><strong>Equipamentos:</strong> utilizamos scanners profissionais Fujitsu fi Series, incluindo famílias fi-6000, fi-7000 e fi-8000, além de equipamentos A3 e A4, conforme formato e volume.</p>" : slug==="gestao-documental"||slug==="organizacao-arquivos" ? "<p>O trabalho pode incluir diagnóstico, inventário, classificação, plano de classificação, tabela de temporalidade, avaliação, retenção, destinação, arquivos correntes/intermediários/permanentes, empréstimos, endereçamento físico e organização digital, alinhados a boas práticas arquivísticas e referências do CONARQ.</p>" : slug==="alfresco-incloud" ? "<p>O Alfresco inCloud pode reunir repositório documental, sites por departamento, permissões, metadados, OCR/PDF-A, versionamento, workflows, pesquisa, auditoria, integrações, migração, backup, treinamento e suporte. Perfis típicos incluem Gerente, Colaborador, Contribuidor e Consumidor.</p>" : slug==="consultoria-lgpd" ? "<p>A jornada de adequação pode envolver diagnóstico, mapa de dados, bases legais, ROPA, RIPD quando aplicável, avisos de privacidade, cookies, contratos, operadores, direitos dos titulares, resposta a incidentes, retenção, treinamento, governança e DPO terceirizado.</p>" : "";
 const calculator=slug==="guarda-documental"?`<div class="calc"><h2>Estimador inicial de volume para guarda</h2><p>Informe a quantidade de caixas para organizar o levantamento comercial. O resultado não é orçamento.</p><label>Quantidade de caixas<br><input id="boxes" type="number" min="1" placeholder="Ex.: 1000"></label><p><button class="btn primary" style="background:#0b3d91;color:white;border:0" onclick="var n=Number(document.getElementById('boxes').value||0);document.getElementById('boxout').textContent=n?('Acervo informado: '+n.toLocaleString('pt-BR')+' caixas. Próximo passo: confirmar dimensões, frequência de consulta, temporalidade e logística.'):'Informe uma quantidade válida.'">Calcular levantamento</button></p><p id="boxout"></p></div>`:"";
 const body=`<div class="hero"><div class="wrap"><div class="eyebrow">Solução Arquindex</div><h1>${name}</h1><p>${desc}</p><div class="cta"><a class="btn primary" href="https://wa.me/${WHATSAPP}?text=${encodeURIComponent("Olá Arquindex, quero orçamento para "+name)}">Solicitar orçamento</a><a class="btn whats" href="#processo">Conhecer o processo</a></div></div></div>
 <section>${answerBox("Resposta direta",desc+" O projeto é dimensionado por volume, complexidade, prazo, segurança, indexação, logística e resultado esperado.")}
 <nav class="toc"><a href="#beneficios">Benefícios</a><a href="#processo">Processo</a><a href="#preco">Preços</a><a href="#conformidade">Conformidade</a><a href="#aplicacoes">Aplicações</a><a href="#experiencia">Experiência</a><a href="#faq">FAQ</a></nav>
 <h2 id="beneficios">Benefícios</h2><div class="kpis">${benefits}</div>
 <h2 id="processo">Processo técnico</h2><div class="steps"><div class="step"><strong>Diagnóstico</strong><p>Objetivo, volume, riscos, formatos, usuários e prazo.</p></div><div class="step"><strong>Preparação</strong><p>Regras, classificação, metadados, logística e critérios de aceite.</p></div><div class="step"><strong>Execução</strong><p>Produção em lotes com registros, controles e tratamento de exceções.</p></div><div class="step"><strong>Validação e entrega</strong><p>Qualidade, conferência, relatórios, entrega e continuidade.</p></div></div>
 <h2 id="preco">Preços e fatores de custo</h2><div class="card"><p class="price">${price}</p><p>O valor final depende de volume, formatos, preparação, prazo, deslocamento, indexação, requisitos técnicos, integrações e forma de entrega. Compare propostas pelo escopo completo, não apenas pelo valor unitário.</p></div>
 ${calculator}
 <h2 id="conformidade">Conformidade, segurança e rastreabilidade</h2><p>O projeto pode envolver controles de acesso, registro de movimentações, confidencialidade, temporalidade, integridade e documentação de decisões. Requisitos legais e regulatórios devem ser avaliados conforme o tipo documental e o setor.</p>${extra}
 <h2 id="aplicacoes">Aplicações</h2><ul>${apps}</ul>
 <h2 id="experiencia">Experiência e evidências</h2><p>${caseTxt}</p><p>Estudos de caso detalhados, volumes, resultados e nomes de clientes só devem ser publicados quando houver informação verificável e autorização adequada.</p>
 <h2 id="faq">Perguntas frequentes</h2>${faqHtml(faqs)}
 <div class="card"><h2>Solicite uma avaliação do volume</h2><p>Informe cidade, quantidade aproximada, tipo de documento, prazo e objetivo. A equipe comercial usa essas informações para preparar o próximo passo.</p><a class="btn whats" href="https://wa.me/${WHATSAPP}?text=${encodeURIComponent("Olá Arquindex, quero avaliar um projeto de "+name)}">Falar com a Arquindex</a></div>
 </section>`;
 return layout(name+" | Arquindex",desc,body,req,jsonLd(serviceSchema)+jsonLd(faqSchema)+jsonLd(bread));
}
function seoPage(serviceSlug,citySlug,intentSlug,req){
 const s=services.find(x=>x[0]===serviceSlug); const c=cities.find(x=>slugCity(x)===citySlug); const i=intents.find(x=>x[0]===intentSlug);
 if(!s||!c||!i)return null;
 const [_,name,desc,price]=s; const [__,intent]=i; const city=c.replace("-",", ");
 const title=`${name} em ${city} | ${intent} | Arquindex`;
 const description=`${name} para empresas em ${city}. ${desc} Atendimento corporativo, orçamento e implantação com a experiência de 20 anos da Arquindex.`;
 const blocks=[
 `Empresas em ${city} que precisam organizar, digitalizar ou governar documentos podem contratar a Arquindex para projetos dimensionados conforme volume, tipo documental, prazo e nível de indexação. O atendimento pode ser remoto, presencial quando necessário e estruturado por etapas.`,
 `A proposta é construída a partir do diagnóstico do acervo. Em vez de aplicar um pacote genérico, o projeto considera contexto operacional, confidencialidade, requisitos de busca, temporalidade, integração com sistemas e forma de entrega.`,
 `A Arquindex atua há 20 anos com gestão documental e transformação de acervos físicos e digitais. O objetivo é reduzir tempo de localização, melhorar rastreabilidade, apoiar auditorias e criar uma base documental mais segura e organizada.`
 ];
 const schema=JSON.stringify({"@context":"https://schema.org","@type":"Service","name":name,"provider":{"@type":"Organization","name":"Arquindex"},"areaServed":city,"description":description});
 const body=`<div class="hero"><div class="wrap"><div class="eyebrow">${city}</div><h1>${name} em ${city}</h1><p>${desc}</p><div class="cta"><a class="btn primary" href="https://wa.me/${WHATSAPP}?text=${encodeURIComponent("Olá Arquindex, quero orçamento de "+name+" para "+city)}">Solicitar orçamento</a></div></div></div><section><h2>${intent.charAt(0).toUpperCase()+intent.slice(1)} em ${city}</h2>${blocks.map(x=>"<p>"+x+"</p>").join("")}<div class="grid"><div class="card"><h3>Preço inicial</h3><div class="price">${price}</div></div><div class="card"><h3>Planos</h3><p>Projeto · Recorrente · Sob demanda · Corporativo</p></div><div class="card"><h3>Atendimento</h3><p>WhatsApp 31 97363-2725</p></div></div><h2>Perguntas frequentes</h2><h3>Como pedir orçamento?</h3><p>Informe cidade, tipo de documento, volume aproximado, prazo e necessidade de coleta ou visita.</p><h3>O atendimento é apenas em Minas Gerais?</h3><p>Não. A Arquindex desenvolve projetos para empresas em diferentes estados, conforme escopo e logística.</p></section>`;
 return layout(title,description,body,req,`<script type="application/ld+json">${schema}</script>`);
}

function geoAudit(req){const pages=[...services.map(x=>({path:"/solucoes/"+x[0],title:x[1],type:"service"})),...articles.map(a=>({path:"/conteudo/"+a.slug,title:a.title,type:"article",source:a.source,reviewed:a.reviewed})),...authorityPages.map(a=>({path:"/autoridade/"+a.slug,title:a.title,type:"authority"})),...landingPages.map(a=>({path:"/setores/"+a.slug,title:a.title,type:"sector"}))];return {name:"Radar GEO AEO Arquindex",date:"2026-10-08",audited:pages.length,pages:pages.map(p=>({...p,url:origin(req)+p.path,author:"Equipe editorial Arquindex",evidence:p.source||null,externalMentions:"Nao verificadas",nextAction:p.type==="article"?"Validar autoria, FAQ e exemplos autorizados":"Adicionar casos e provas publicas"})),policy:"Nao fabricar reviews, links nem mencoes. Paginas locais nao revisadas permanecem noindex."};}
function authorityListing(req){
 const cards=authorityPages.map(a=>'<article class="card"><div class="eyebrow" style="color:#0b3d91">'+esc(a.pillar)+'</div><h3><a href="/autoridade/'+a.slug+'">'+esc(a.title)+'</a></h3><p>'+esc(a.lead)+'</p><p><a href="/autoridade/'+a.slug+'">Ver guia →</a></p></article>').join("");
 return layout("Guias de autoridade | Arquindex","Guias técnicos aprofundados sobre Databook, digitalização certificada, gestão documental, Alfresco ECM e LGPD.",'<section><h1>Guias de autoridade Arquindex</h1><p>Conteúdo técnico aprofundado para decisões B2B, industriais e de engenharia.</p><div class="grid">'+cards+'</div></section>',req);
}
function authorityPage(slug,req){
 const a=authorityPages.find(x=>x.slug===slug); if(!a)return null;
 const sections=a.sections.map(([h,p])=>'<h2>'+esc(h)+'</h2><p>'+esc(p)+'</p>').join("");
 const faq=a.faqs.map(([q,ans])=>'<h3>'+esc(q)+'</h3><p>'+esc(ans)+'</p>').join("");
 const rel=a.related.map(x=>'<li><a href="'+x+'">'+esc(x.replace(/^\//,""))+'</a></li>').join("");
 const faqSchema={"@context":"https://schema.org","@type":"FAQPage","mainEntity":a.faqs.map(([q,ans])=>({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":ans}}))};
 const articleSchema={"@context":"https://schema.org","@type":"Article","headline":a.title,"about":a.pillar,"author":{"@type":"Organization","name":"Arquindex"},"publisher":{"@type":"Organization","name":"Arquindex"}};
 const body='<div class="hero"><div class="wrap"><div class="eyebrow">'+esc(a.pillar)+' · Guia técnico</div><h1>'+esc(a.title)+'</h1><p>'+esc(a.lead)+'</p></div></div><section style="max-width:900px"><div class="card"><strong>Resposta direta</strong><p>'+esc(a.answer)+'</p></div>'+sections+'<h2>Perguntas frequentes</h2>'+faq+'<h2>Conteúdos relacionados</h2><ul>'+rel+'</ul><div class="card"><h2>Fale com a Arquindex</h2><p>Envie volume, cidade, prazo e objetivo para dimensionarmos o projeto.</p><a class="btn whats" href="https://wa.me/'+WHATSAPP+'">Solicitar diagnóstico</a></div></section>';
 return layout(a.title+" | Arquindex",a.lead,body,req,'<script type="application/ld+json">'+JSON.stringify(articleSchema)+'</script><script type="application/ld+json">'+JSON.stringify(faqSchema)+'</script>');
}
function sectorListing(req){
 const cards=landingPages.map(a=>'<article class="card"><div class="eyebrow" style="color:#0b3d91">'+esc(a.sector)+'</div><h3><a href="/setores/'+a.slug+'">'+esc(a.title)+'</a></h3><p>'+esc(a.lead)+'</p></article>').join("");
 return layout("Soluções por setor | Arquindex","Guias de digitalização, gestão documental, LGPD, Alfresco, Databook e guarda por setor.",'<section><h1>Soluções por setor</h1><p>100 guias setoriais organizados por necessidade documental e contexto de negócio.</p><div class="grid">'+cards+'</div></section>',req);
}
function sectorPage(slug,req){
 const a=landingPages.find(x=>x.slug===slug); if(!a)return null;
 const sections=a.sections.map(([h,p])=>'<h2>'+esc(h)+'</h2><p>'+esc(p)+'</p>').join("");
 const checklist=a.checklist.map(x=>'<li>'+esc(x)+'</li>').join("");
 const faq=a.faqs.map(([q,ans])=>'<h3>'+esc(q)+'</h3><p>'+esc(ans)+'</p>').join("");
 const faqSchema={"@context":"https://schema.org","@type":"FAQPage","mainEntity":a.faqs.map(([q,ans])=>({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":ans}}))};
 const schema={"@context":"https://schema.org","@type":"Service","name":a.title,"provider":{"@type":"Organization","name":"Arquindex"},"audience":{"@type":"BusinessAudience","name":a.sector},"description":a.description};
 const body='<div class="hero"><div class="wrap"><div class="eyebrow">'+esc(a.sector)+'</div><h1>'+esc(a.title)+'</h1><p>'+esc(a.lead)+'</p><div class="cta"><a class="btn primary" href="https://wa.me/'+WHATSAPP+'">Solicitar orçamento</a></div></div></div><section style="max-width:950px"><div class="card"><strong>Aplicação no setor</strong><p>'+esc(a.description)+'</p></div>'+sections+'<h2>Checklist do projeto</h2><ul>'+checklist+'</ul><h2>Perguntas frequentes</h2>'+faq+'<p><a href="/solucoes/'+a.serviceSlug+'">Conheça a solução principal →</a></p></section>';
 return layout(a.title+" | Arquindex",a.description,body,req,'<script type="application/ld+json">'+JSON.stringify(schema)+'</script><script type="application/ld+json">'+JSON.stringify(faqSchema)+'</script>');
}
function contentListing(req){
 const cards=articles.map(a=>'<article class="card"><div class="eyebrow" style="color:#0b3d91">'+esc(a.category)+'</div><h3><a href="/conteudo/'+a.slug+'">'+esc(a.title)+'</a></h3><p>'+esc(a.lead)+'</p><p><a href="/conteudo/'+a.slug+'">Ler artigo →</a></p></article>').join("");
 return layout("Artigos sobre digitalização, Alfresco e LGPD | Arquindex","Guias técnicos de digitalização, Alfresco ECM, proteção de dados e LGPD.",'<section><h1>Conteúdos e artigos</h1><p>Guias técnicos para apoiar decisões documentais e de privacidade.</p><div class="grid">'+cards+'</div></section>',req);
}
function articlePage(slug,req){
 const a=articles.find(a=>a.slug===slug);if(!a)return null;
 const sections=a.sections.map(([h,p])=>'<h2>'+esc(h)+'</h2><p>'+esc(p)+'</p>').join("");
 const service=a.category==="Digitalização"?"/solucoes/digitalizacao-documentos":a.category==="Alfresco"?"/solucoes/alfresco-incloud":"/solucoes/consultoria-lgpd";
 const schema=JSON.stringify({"@context":"https://schema.org","@type":"Article",headline:a.title,dateModified:a.reviewed,author:{"@type":"Organization",name:"Arquindex"},publisher:{"@type":"Organization",name:"Arquindex"}});
 const body='<section style="max-width:860px"><p><a href="/conteudo">← Voltar aos artigos</a> · <a href="https://arquindex.com.br/blog.html">Blog oficial e acervo histórico</a></p><p class="muted">'+esc(a.category)+' · Revisado em '+esc(a.reviewed)+'</p><h1>'+esc(a.title)+'</h1><p style="font-size:19px">'+esc(a.lead)+'</p>'+sections+'<h2>Referência e leitura adicional</h2><p><a href="'+esc(a.source)+'" rel="noopener noreferrer">Consultar fonte técnica ou normativa</a></p><div class="card"><h2>Planeje seu projeto com a Arquindex</h2><p>Conheça as soluções relacionadas ao tema e solicite um orçamento conforme o escopo de sua organização.</p><a href="'+service+'">Conhecer solução</a> · <a href="/contato">Pedir orçamento</a></div></section>';
 return layout(a.title+" | Blog Arquindex",a.lead,body,req,'<script type="application/ld+json">'+schema+'</script>');
}

function normativeLibrary(req){
 const body='<div class="hero"><div class="wrap"><div class="eyebrow">Biblioteca normativa</div><h1>Legislação e referências para gestão documental e privacidade</h1><p>Fontes oficiais para apoiar decisões sobre digitalização, proteção de dados, classificação, temporalidade e preservação.</p></div></div><section>'+answerBox("Como usar esta biblioteca","Use as referências oficiais para validar requisitos jurídicos e técnicos. Conteúdos da Arquindex devem distinguir obrigação legal, orientação normativa e boa prática.")+'<div class="grid"><article class="card"><h2>Decreto 10.278/2020</h2><p>Requisitos técnicos relacionados à digitalização de documentos públicos ou privados nos casos abrangidos pela norma.</p><a href="https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10278.htm" rel="noopener noreferrer">Fonte oficial →</a></article><article class="card"><h2>Lei Geral de Proteção de Dados</h2><p>Lei nº 13.709/2018, com princípios, bases legais, direitos, agentes de tratamento e governança.</p><a href="https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm" rel="noopener noreferrer">Fonte oficial →</a></article><article class="card"><h2>CONARQ</h2><p>Referências arquivísticas, orientações e instrumentos para gestão, classificação e preservação documental.</p><a href="https://www.gov.br/conarq/pt-br" rel="noopener noreferrer">Portal oficial →</a></article></div></section>';
 return layout("Biblioteca normativa | Arquindex","Fontes oficiais sobre Decreto 10.278/2020, LGPD e CONARQ.",body,req,jsonLd(breadcrumbSchema([["Início","/"],["Biblioteca normativa","/biblioteca-normativa"]],req)));
}
function methodologyPage(req){
 const body='<section style="max-width:900px"><h1>Metodologia editorial e técnica Arquindex</h1>'+answerBox("Princípio editorial","A Arquindex prioriza páginas que já apresentam sinais no Google antes de criar novas URLs. Conteúdo novo deve cobrir uma intenção realmente diferente, trazer informação útil e evitar páginas doorway.")+'<h2>Como os conteúdos são produzidos</h2><p>As pautas combinam dúvidas de clientes, experiência operacional, dados de desempenho, pesquisa pública de mercado e referências oficiais. Concorrentes podem ser analisados para identificar temas e lacunas, sem copiar textos ou alegações.</p><h2>Revisão e evidências</h2><p>Legislação, normas, números, certificações, clientes e resultados devem ser verificados antes da publicação. Conteúdos técnicos recebem data de revisão e links para fontes quando necessário.</p><h2>SEO, GEO e AEO</h2><p>Cada página deve responder diretamente à intenção, usar estrutura clara, links internos, dados estruturados elegíveis e conteúdo local apenas quando existir diferença real de atendimento, logística ou contexto.</p><h2>Política de atualização</h2><p>Páginas com impressões e cliques são preservadas e fortalecidas. Resultados são reavaliados em janelas de 7, 14 e 28 dias.</p></section>';
 return layout("Metodologia editorial e técnica | Arquindex","Como a Arquindex produz, revisa e atualiza conteúdos técnicos.",body,req,jsonLd(breadcrumbSchema([["Início","/"],["Metodologia","/metodologia"]],req)));
}
function sitemap(req,index){
 const o=origin(req);
 const urls=[];
 for(const s of services) for(const c of cities) for(const i of intents) urls.push(`${o}/seo/${s[0]}/${slugCity(c)}/${i[0]}`);
 const start=index*1000, chunk=[]; // páginas locais aguardam revisão editorial e evidência local
 return '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+chunk.map(u=>'<url><loc>'+u+'</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>').join('')+'</urlset>';
}
const server=http.createServer(async(req,res)=>{
 const u=new URL(req.url,"http://localhost"); const p=u.pathname;
 if(isRailwayPreview(req))res.setHeader("x-robots-tag","noindex, nofollow, noarchive");
 if(p==="/radar-geo-aeo.json"){res.writeHead(200,{"content-type":"application/json; charset=utf-8"});return res.end(JSON.stringify(geoAudit(req)));}
 if(p==="/health"){res.writeHead(200,{"content-type":"application/json"});return res.end(JSON.stringify({ok:true,service:"arquindex-web"}));}
 if(p==="/favicon.ico"){res.writeHead(204);return res.end();}
 if(p==="/robots.txt"){res.writeHead(200,{"content-type":"text/plain"});if(isRailwayPreview(req))return res.end("User-agent: *\nDisallow: /\n");return res.end(`User-agent: *\nAllow: /\nSitemap: ${origin(req)}/sitemap.xml\n`);}
 if(p==="/sitemap.xml"){res.writeHead(200,{"content-type":"application/xml"});return res.end('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+["/","/solucoes","/conteudo","/autoridade","/setores","/biblioteca-normativa","/metodologia","/contato",...services.map(s=>"/solucoes/"+s[0]),...articles.map(a=>"/conteudo/"+a.slug),...authorityPages.map(a=>"/autoridade/"+a.slug),...landingPages.map(a=>"/setores/"+a.slug)].map(path=>"<url><loc>"+origin(req)+path+"</loc></url>").join("")+"</urlset>");}
 const sm=p.match(/^\/sitemap-(\d+)\.xml$/); if(sm){res.writeHead(410,{"content-type":"text/plain","x-robots-tag":"noindex"});return res.end("Sitemap antigo desativado. Consulte /sitemap.xml");}
 if(p==="/biblioteca-normativa"){res.writeHead(200,{"content-type":"text/html; charset=utf-8"});return res.end(normativeLibrary(req));}
 if(p==="/metodologia"){res.writeHead(200,{"content-type":"text/html; charset=utf-8"});return res.end(methodologyPage(req));}
 if(p==="/autoridade"){res.writeHead(200,{"content-type":"text/html; charset=utf-8"});return res.end(authorityListing(req));}
 const auth=p.match(/^\/autoridade\/([a-z0-9-]+)$/);if(auth){const h=authorityPage(auth[1],req);if(h){res.writeHead(200,{"content-type":"text/html; charset=utf-8"});return res.end(h);}}
 if(p==="/setores"){res.writeHead(200,{"content-type":"text/html; charset=utf-8"});return res.end(sectorListing(req));}
 const sec=p.match(/^\/setores\/([a-z0-9-]+)$/);if(sec){const h=sectorPage(sec[1],req);if(h){res.writeHead(200,{"content-type":"text/html; charset=utf-8"});return res.end(h);}}
 const art=p.match(/^\/conteudo\/([a-z0-9-]+)$/);if(art){const h=articlePage(art[1],req);if(h){res.writeHead(200,{"content-type":"text/html; charset=utf-8"});return res.end(h);}}
 if(p==="/conteudo"){res.writeHead(200,{"content-type":"text/html; charset=utf-8"});return res.end(contentListing(req));}
 if(p==="/contato"){const isContact=p==="/contato";res.writeHead(200,{"content-type":"text/html; charset=utf-8"});return res.end(layout(isContact?"Contato | Arquindex":"Conteúdos | Arquindex",isContact?"Solicite um orçamento para soluções documentais.":"Artigos e guias de gestão documental, LGPD e ECM.",isContact?'<section><h1>Fale com a Arquindex</h1><p>Peça um orçamento pelo WhatsApp: <a href="https://wa.me/'+WHATSAPP+'">31 97363-2725</a></p><p>Email: comercial@arquindex.com.br</p></section>':'<section><h1>Conteúdo técnico Arquindex</h1><p>Publicações em preparação editorial. Veja nossas <a href="/solucoes">soluções</a>.</p></section>',req));}
 if(p==="/"){res.writeHead(200,{"content-type":"text/html; charset=utf-8"});return res.end(home(req));}
 if(p==="/solucoes"){const cards=services.map(([s,n,d,pr])=>`<article class="card"><h3>${n}</h3><p>${d}</p><div class="price">${pr}</div><a href="/solucoes/${s}">Detalhes →</a></article>`).join("");res.writeHead(200,{"content-type":"text/html; charset=utf-8"});return res.end(layout("Soluções | Arquindex","Soluções de gestão documental, digitalização, LGPD, Alfresco ECM, Databook e arquivos.",`<section><h1>Soluções Arquindex</h1><div class="grid">${cards}</div></section>`,req));}
 const sol=p.match(/^\/solucoes\/([^/]+)$/); if(sol){const h=solutionPage(sol[1],req);if(h){res.writeHead(200,{"content-type":"text/html; charset=utf-8"});return res.end(h);}}
 const m=p.match(/^\/seo\/([^/]+)\/([^/]+)\/([^/]+)$/); if(m){const h=seoPage(m[1],m[2],m[3],req);if(h){res.writeHead(200,{"content-type":"text/html; charset=utf-8","x-robots-tag":"noindex, follow"});return res.end(h);}}
 if(p==="/api/indexnow"&&req.method==="POST"){res.writeHead(403,{"content-type":"application/json"});return res.end(JSON.stringify({ok:false,error:"Envio desabilitado ate aprovacao editorial e autenticacao"}));
 /*
   const key=process.env.INDEXNOW_KEY; if(!key){res.writeHead(503,{"content-type":"application/json"});return res.end(JSON.stringify({ok:false,error:"INDEXNOW_KEY not configured"}));}
   const urls=[]; for(const s of services) for(const c of cities) for(const i of intents) urls.push(`${origin(req)}/seo/${s[0]}/${slugCity(c)}/${i[0]}`);
   const payload={host:new URL(origin(req)).host,key,keyLocation:origin(req)+"/"+key+".txt",urlList:urls};
   try{const rr=await fetch("https://api.indexnow.org/indexnow",{method:"POST",headers:{"content-type":"application/json; charset=utf-8"},body:JSON.stringify(payload)});res.writeHead(rr.status,{"content-type":"application/json"});return res.end(JSON.stringify({ok:rr.ok,status:rr.status,count:urls.length}));}catch(e){res.writeHead(500,{"content-type":"application/json"});return res.end(JSON.stringify({ok:false,error:String(e)}));}
 }
 */
 }
 if(process.env.INDEXNOW_KEY&&p==="/"+process.env.INDEXNOW_KEY+".txt"){res.writeHead(200,{"content-type":"text/plain"});return res.end(process.env.INDEXNOW_KEY);}
 res.writeHead(404,{"content-type":"text/html; charset=utf-8"});res.end(layout("Página não encontrada | Arquindex","Página não encontrada.","<section><h1>Página não encontrada</h1><p><a href='/'>Voltar ao início</a></p></section>",req));
});
server.listen(PORT,"0.0.0.0",()=>console.log("Arquindex running on",PORT));
async function notifyIndexNowForPublishedPages(){
 const key=process.env.INDEXNOW_KEY;
 if(!key || !/^[A-Za-z0-9-]{8,128}$/.test(key)){console.log("IndexNow skipped: key missing or invalid");return;}
 const paths=["/","/solucoes","/conteudo","/autoridade","/setores","/biblioteca-normativa","/metodologia","/contato",...services.map(x=>"/solucoes/"+x[0]),...articles.map(a=>"/conteudo/"+a.slug),...authorityPages.map(a=>"/autoridade/"+a.slug),...landingPages.map(a=>"/setores/"+a.slug)];
 const host="arquindex-web-production.up.railway.app";
 const payload={host,key,keyLocation:"https://"+host+"/"+key+".txt",urlList:[...new Set(paths)].map(path=>"https://"+host+path)};
 try{
  const response=await fetch("https://api.indexnow.org/indexnow",{method:"POST",headers:{"content-type":"application/json; charset=utf-8"},body:JSON.stringify(payload),signal:AbortSignal.timeout(12000)});
  console.log("IndexNow notification",response.status,"urls",payload.urlList.length);
 }catch(err){console.warn("IndexNow notification error",String(err));}
}
if(process.env.NODE_ENV==="production"&&process.env.INDEXNOW_AUTO_SUBMIT==="true"){
 setTimeout(()=>{notifyIndexNowForPublishedPages().catch(err=>console.warn("IndexNow error",String(err)));},12000);
}

