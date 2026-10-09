import http from "node:http";
import { URL } from "node:url";
import { articles } from "./articles.js";

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

function esc(s){return String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));}
function slugCity(c){return c.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");}
function origin(req){return BASE || ("https://"+(req.headers.host||"localhost"));}
function layout(title,desc,body,req,extraHead=""){
 const o=origin(req);
 return `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)}</title><meta name="description" content="${esc(desc)}"><link rel="canonical" href="${o}${new URL(req.url,o).pathname}">${extraHead}
 <style>
 :root{--b:#0b3d91;--b2:#0b67c2;--ink:#0c1b33;--mut:#56657a;--bg:#f4f7fb;--card:#fff;--line:#d9e2ef;--g:#25d366}
 *{box-sizing:border-box}body{margin:0;font-family:Arial,Helvetica,sans-serif;color:var(--ink);background:#fff;line-height:1.55}
 header{position:sticky;top:0;z-index:30;background:#fff;border-bottom:1px solid var(--line)}.top{max-width:1200px;margin:auto;padding:14px 22px;display:flex;align-items:center;gap:24px}.brand{font-size:30px;font-weight:800;color:var(--b);letter-spacing:-1px}.tag{font-size:10px;color:#667;display:block}.nav{display:flex;gap:18px;flex:1;justify-content:center}.nav a{color:#23324a;text-decoration:none;font-size:14px}.contact{font-size:13px;text-align:right}.contact a{color:var(--b);font-weight:700;text-decoration:none}
 .hero{background:linear-gradient(110deg,#071f4d,#0b4fa7);color:#fff}.hero .wrap{max-width:1200px;margin:auto;padding:72px 22px}.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:1.3px;opacity:.85}.hero h1{font-size:48px;line-height:1.05;max-width:800px;margin:14px 0}.hero p{max-width:760px;font-size:18px;color:#d9e9ff}.cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}.btn{display:inline-block;padding:13px 18px;border-radius:10px;text-decoration:none;font-weight:700}.primary{background:#fff;color:var(--b)}.whats{background:var(--g);color:#08210f}
 .trust{max-width:1200px;margin:-24px auto 0;padding:0 22px;display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.pill{background:#fff;border:1px solid var(--line);box-shadow:0 8px 22px #08234a16;border-radius:14px;padding:18px;text-align:center}.pill strong{display:block;color:var(--b);font-size:20px}
 section{max-width:1200px;margin:auto;padding:58px 22px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px;box-shadow:0 5px 18px #142b4d0d}.card h3{margin-top:0}.price{font-weight:800;color:var(--b2)}.muted{color:var(--mut)}
 .band{background:var(--bg)}.wafloat{position:fixed;right:20px;bottom:20px;background:var(--g);color:#fff;width:58px;height:58px;border-radius:50%;display:grid;place-items:center;text-decoration:none;font-size:26px;box-shadow:0 8px 24px #0003;z-index:40}
 footer{background:#071a3a;color:#dce7f7;padding:40px 22px}.foot{max-width:1200px;margin:auto;display:grid;grid-template-columns:2fr 1fr 1fr;gap:30px}.cookie{position:fixed;left:18px;right:18px;bottom:18px;background:#fff;border:1px solid var(--line);box-shadow:0 10px 30px #0003;border-radius:14px;padding:16px;z-index:50;display:flex;gap:16px;align-items:center}.cookie p{margin:0;flex:1;font-size:13px}.cookie button{border:0;padding:10px 13px;border-radius:8px;cursor:pointer}.accept{background:var(--b);color:#fff}
 @media(max-width:800px){.nav{display:none}.hero h1{font-size:36px}.grid,.trust,.foot{grid-template-columns:1fr}.contact{font-size:12px}.cookie{flex-direction:column;align-items:stretch}}
 </style></head><body>
 <header><div class="top"><div><div class="brand">arquindex</div><span class="tag">EFICIÊNCIA MÁXIMA EM GESTÃO DE DOCUMENTOS</span></div><nav class="nav"><a href="/">Início</a><a href="/solucoes">Soluções</a><a href="/conteudo">Conteúdo</a><a href="https://arquindex.com.br/blog.html">Blog oficial</a><a href="https://arquindex.com.br/#clientes">Clientes</a><a href="/contato">Contato</a></nav><div class="contact">WhatsApp<br><a href="https://wa.me/${WHATSAPP}?text=Ol%C3%A1%20Arquindex%2C%20quero%20um%20or%C3%A7amento">31 97363-2725</a></div></div></header>
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
 <section><h2>Soluções corporativas</h2><p class="muted">Serviços desenhados para reduzir risco, acelerar acesso à informação e melhorar a governança documental.</p><div class="grid">${cards}</div></section>
 <div class="band"><section><h2>Experiência em projetos complexos</h2><p>Ao longo de duas décadas, a Arquindex acumulou experiências em setores como siderurgia, mineração, engenharia, saúde, cartórios, jurídico, educação, indústria farmacêutica, óleo & gás e serviços profissionais.</p><p><strong>Referências institucionais citadas:</strong> Usiminas, Cimcop, Lhoist, FCA/Fiat, Petrobras, Petronas, RHI Magnesita e Unimed BH. A natureza e o escopo de cada projeto devem ser confirmados antes da publicação de um case individual.</p><p><a class="btn primary" href="https://arquindex.com.br/#clientes">Consultar seção de clientes no site oficial →</a></p></section></div>`;
 return layout("Arquindex | Gestão Documental, Digitalização, LGPD e ECM","Há 20 anos em gestão documental, digitalização, LGPD, Alfresco ECM, Databook e organização de arquivos.",body,req);
}
function solutionPage(slug,req){
 const s=services.find(x=>x[0]===slug); if(!s)return null;
 const [_,name,desc,price]=s;
 const caseTxt=cases[slug]||"A Arquindex atua há 20 anos em projetos corporativos de gestão documental, digitalização, organização de arquivos, compliance e tecnologia.";
 const extra= slug==="digitalizacao-certificada" ? "<p><strong>Digitalização certificada:</strong> projetos podem ser estruturados considerando os requisitos técnicos do Decreto 10.278/2020, incluindo padrões de digitalização, metadados, integridade e controle de qualidade, conforme o contexto do acervo.</p><p><strong>Equipamentos:</strong> utilizamos scanners profissionais Fujitsu fi Series, incluindo famílias fi-6000, fi-7000 e fi-8000, além de equipamentos A3 e A4, conforme formato e volume. Recursos como alimentação automática, duplex e detecção de dupla alimentação apoiam a produtividade e a qualidade.</p>" : slug==="gestao-documental"||slug==="organizacao-arquivos" ? "<p>O trabalho pode incluir diagnóstico, inventário, classificação, plano de classificação, tabela de temporalidade, avaliação, retenção, destinação, arquivos correntes/intermediários/permanentes, empréstimos, endereçamento físico e organização digital, alinhados a boas práticas arquivísticas e referências do CONARQ.</p>" : slug==="alfresco-incloud" ? "<p>O Alfresco inCloud pode reunir repositório documental, sites por departamento, permissões, metadados, OCR/PDF-A, versionamento, workflows, pesquisa, auditoria, integrações, migração, backup, treinamento e suporte. Perfis típicos incluem Gerente, Colaborador, Contribuidor e Consumidor.</p>" : slug==="consultoria-lgpd" ? "<p>A jornada de adequação pode envolver diagnóstico, mapa de dados, bases legais, ROPA, RIPD quando aplicável, avisos de privacidade, cookies, contratos, operadores, direitos dos titulares, resposta a incidentes, retenção, treinamento, governança e DPO terceirizado.</p>" : "";
 const body=`<div class="hero"><div class="wrap"><div class="eyebrow">Solução Arquindex</div><h1>${name}</h1><p>${desc}</p><div class="cta"><a class="btn primary" href="https://wa.me/${WHATSAPP}?text=${encodeURIComponent("Olá Arquindex, quero orçamento para "+name)}">Receber orçamento</a></div></div></div>
 <section><div class="grid"><article class="card"><h3>Como funciona</h3><p>Levantamento do acervo e objetivo, definição do escopo, execução controlada, validação, entrega e acompanhamento.</p></article><article class="card"><h3>Contratação</h3><p>Por projeto, mensal/recorrente, sob demanda ou plano corporativo personalizado.</p></article><article class="card"><h3>Valor</h3><p class="price">${price}</p><p class="muted">O valor final depende de volume, complexidade, prazo, deslocamento, indexação e requisitos técnicos.</p></article></div>
 <h2>Detalhamento</h2><p>${desc}</p>${extra}<p>${caseTxt}</p>
 <h2>Referências e estudos de caso</h2><p>Conheça a apresentação institucional e a relação de clientes da Arquindex no <a href="https://arquindex.com.br/#clientes">site oficial</a>. Estudos de caso detalhados dependem de informações e autorizações específicas.</p><h2>Fale com um especialista</h2><p>Conte o volume, cidade, prazo e objetivo. O atendimento coleta as informações necessárias para preparar uma estimativa inicial e encaminhar o caso ao comercial.</p></section>`;
 return layout(name+" | Arquindex",desc,body,req);
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

function geoAudit(req){const pages=[...services.map(x=>({path:"/solucoes/"+x[0],title:x[1],type:"service"})),...articles.map(a=>({path:"/conteudo/"+a.slug,title:a.title,type:"article",source:a.source,reviewed:a.reviewed}))];return {name:"Radar GEO AEO Arquindex",date:"2026-10-08",audited:pages.length,pages:pages.map(p=>({...p,url:origin(req)+p.path,author:"Equipe editorial Arquindex",evidence:p.source||null,externalMentions:"Nao verificadas",nextAction:p.type==="article"?"Validar autoria, FAQ e exemplos autorizados":"Adicionar casos e provas publicas"})),policy:"Nao fabricar reviews, links nem mencoes. Paginas locais nao revisadas permanecem noindex."};}
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

function sitemap(req,index){
 const o=origin(req);
 const urls=[];
 for(const s of services) for(const c of cities) for(const i of intents) urls.push(`${o}/seo/${s[0]}/${slugCity(c)}/${i[0]}`);
 const start=index*1000, chunk=[]; // páginas locais aguardam revisão editorial e evidência local
 return '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+chunk.map(u=>'<url><loc>'+u+'</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>').join('')+'</urlset>';
}
const server=http.createServer(async(req,res)=>{
 const u=new URL(req.url,"http://localhost"); const p=u.pathname;
 if(p==="/radar-geo-aeo.json"){res.writeHead(200,{"content-type":"application/json; charset=utf-8"});return res.end(JSON.stringify(geoAudit(req)));}
 if(p==="/health"){res.writeHead(200,{"content-type":"application/json"});return res.end(JSON.stringify({ok:true,service:"arquindex-web"}));}
 if(p==="/favicon.ico"){res.writeHead(204);return res.end();}
 if(p==="/robots.txt"){res.writeHead(200,{"content-type":"text/plain"});return res.end(`User-agent: *\nAllow: /\nSitemap: ${origin(req)}/sitemap.xml\n`);}
 if(p==="/sitemap.xml"){res.writeHead(200,{"content-type":"application/xml"});return res.end('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+["/","/solucoes",...services.map(s=>"/solucoes/"+s[0]),"/conteudo",...articles.map(a=>"/conteudo/"+a.slug)].map(path=>"<url><loc>"+origin(req)+path+"</loc></url>").join("")+"</urlset>");}
 const sm=p.match(/^\/sitemap-(\d+)\.xml$/); if(sm){const n=Number(sm[1]);if(n>=1&&n<=5){res.writeHead(200,{"content-type":"application/xml"});return res.end(sitemap(req,n-1));}}
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
