// SEO legacy route recovery candidate. Draft only: validate host canonical and full backup before merge.
const wa = "https://wa.me/5531973632725";
const email = "mailto:comercial@arquindex.com.br";
const escapeHtml = s => String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const pages = {
 "/gestao_de_colaboradores_documentos.html": {
  title:"Dossiês de Colaboradores: Digitalização e Gestão para RH | Arquindex",
  description:"Organize dossiês por funcionário e tipo documental, com digitalização, OCR, conferência e acesso controlado. Solicite avaliação do acervo.",
  h1:"Digitalização e gestão de dossiês de colaboradores para RH",
  answer:"A gestão de dossiês de colaboradores organiza documentos de admissão, vínculo, benefícios, saúde ocupacional e desligamento por funcionário, tipo documental e período. O processamento pode incluir separação de documentos multipágina, captura, OCR, indexação por matrícula e conferência humana. O acesso a dados sensíveis e os prazos de retenção precisam seguir as obrigações aplicáveis a cada categoria documental.",
  steps:["Inventariar séries documentais, volumes e tipos de dossiê","Definir identificação por funcionário e matrícula, sem expor dados pessoais ao público","Preservar documentos multipágina e conferir início e fim dos dossiês","Aplicar OCR e indexação conforme critérios de aceite","Revisar exceções e implantar permissões e temporalidade"],
  faqs:[
   ["OCR dispensa a conferência humana?","Não. A identificação e a separação automática exigem conferência de amostras e de ocorrências incertas."],
   ["Como tratar atestados e exames ocupacionais?","Com segregação de acesso e regras adequadas para dados pessoais sensíveis, segundo a finalidade e as normas aplicáveis."],
   ["O desligamento autoriza descartar o dossiê?","Não. Prazos trabalhistas, previdenciários, litígios e outras exigências precisam ser avaliados antes de qualquer destinação."]
  ],
  links:[["/digitalizacao-com-ocr.html","Digitalização com OCR"],["/solucoes/guarda-documental","Guarda documental"],["/solucoes/consultoria-lgpd","Consultoria LGPD"]]
 },
 "/digitalizacao-com-ocr.html": {
  title:"Digitalização com OCR e PDF Pesquisável | Arquindex",
  description:"OCR empresarial para PDFs pesquisáveis, indexação por metadados e conferência de qualidade. Avalie um piloto com critérios de aceite.",
  h1:"Digitalização empresarial com OCR e PDF pesquisável",
  answer:"OCR é o reconhecimento de caracteres em imagens digitalizadas para permitir pesquisa textual em documentos eletrônicos. Em projetos empresariais, ele pode ser combinado com captura, indexação de campos, conferência e entrega estruturada. A qualidade depende da legibilidade do original, do idioma e do layout. OCR não garante leitura perfeita nem atribui, por si só, efeitos jurídicos ao documento digitalizado.",
  steps:["Identificar tipos documentais, volume e qualidade dos originais","Definir resolução, formatos e requisitos de captura","Executar piloto de OCR em amostra representativa","Separar texto pesquisável de extração estruturada de campos","Conferir identificadores e registrar exceções antes do aceite"],
  faqs:[
   ["Um PDF pesquisável é o mesmo que PDF/A?","Não. PDF/A é uma família de formatos para preservação; o texto OCR é uma funcionalidade de pesquisa que pode coexistir com PDF/A."],
   ["OCR reconhece manuscritos e tabelas sem erro?","Não há precisão universal. Manuscritos, tabelas, sombras e originais degradados exigem testes e revisão."],
   ["Digitalizar autoriza descartar o papel?","Não automaticamente. Os requisitos legais, arquivísticos e de retenção precisam ser examinados para cada acervo."]
  ],
  links:[["/gestao_de_colaboradores_documentos.html","Dossiês de colaboradores"],["/solucoes/digitalizacao-documentos","Digitalização empresarial"],["/solucoes/guarda-documental","Guarda de documentos"]]
 }
};
export const recoveryPaths=Object.keys(pages);
export function renderLegacyRecovery(path,canonicalBase="https://www.arquindex.com.br"){
 const d=pages[path]; if(!d) return null;
 const can=canonicalBase+path;
 const faq=d.faqs.map(([q,a])=>`<details><summary>${escapeHtml(q)}</summary><p>${escapeHtml(a)}</p></details>`).join("");
 const steps=d.steps.map(s=>`<li>${escapeHtml(s)}</li>`).join("");
 const links=d.links.map(([href,text])=>`<li><a href="${escapeHtml(href)}">${escapeHtml(text)}</a></li>`).join("");
 return `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escapeHtml(d.title)}</title><meta name="description" content="${escapeHtml(d.description)}"><meta name="robots" content="index,follow"><link rel="canonical" href="${escapeHtml(can)}"><meta property="og:url" content="${escapeHtml(can)}"><style>body{font:18px/1.65 system-ui,Arial,sans-serif;color:#17263e;margin:0}header,main,footer{max-width:900px;margin:auto;padding:24px}header{border-bottom:1px solid #ddd}a{color:#155b89}h1{line-height:1.2}section{margin:36px 0}details{padding:13px 0;border-bottom:1px solid #ddd}.cta{display:inline-block;padding:12px 18px;background:#155b89;color:white;border-radius:6px;text-decoration:none;margin-right:12px}</style></head><body><header><a href="/">Arquindex</a> · Gestão Documental</header><main><h1>${escapeHtml(d.h1)}</h1><section aria-label="Resposta direta"><h2>Como funciona?</h2><p>${escapeHtml(d.answer)}</p></section><section><h2>Etapas do processo</h2><ol>${steps}</ol></section><section><h2>Perguntas frequentes</h2>${faq}</section><nav aria-label="Serviços relacionados"><h2>Serviços relacionados</h2><ul>${links}</ul></nav><section><h2>Solicite avaliação técnica</h2><p>Informe tipo de acervo, volume aproximado, cidade e requisitos de acesso. Não envie documentos pessoais completos para orçamento inicial.</p><a class="cta" href="${wa}">WhatsApp (31) 97363-2725</a><a href="${email}">comercial@arquindex.com.br</a></section></main><footer>Arquindex · O escopo, os requisitos de preservação e as condições de execução dependem de avaliação técnica e proposta.</footer></body></html>`;
}
