export const competitors = [
 {name:"Documentalize",url:"https://documentalize.com.br/",focus:["digitalização certificada","orçamento online","OCR","guarda","GED"]},
 {name:"Iron Mountain",url:"https://www.ironmountain.com/pt-br/services/document-scanning-and-digital-storage",focus:["digitalização corporativa","armazenamento","governança","automação"]},
 {name:"LogGed",url:"https://www.logged.com.br/",focus:["guarda documental","organização de arquivos","digitalização"]},
 {name:"ImageDocs",url:"https://www.imagedocs.com.br/",focus:["digitalização","gestão de acervos","arquivo digital"]},
 {name:"Arquivar",url:"https://arquivar.com.br/",focus:["gestão documental","GED","processos","automação"]},
 {name:"AccessCorp",url:"https://accesscorp.com.br/",focus:["armazenamento físico","governança","digitalização","BPO"]},
 {name:"Stoque",url:"https://stoque.com.br/",focus:["automação de processos","IA","BPO","transformação digital"]},
 {name:"Cedoc",url:"https://cedoc.net.br/",focus:["guarda","digitalização de livros","ECM","segurança física"]}
];
export const opportunities=[
 {topic:"Calculadora de digitalização por volume e formato",category:"Digitalização",priority:"alta",target:"/solucoes/digitalizacao-documentos",intent:"orçamento e contratação",differentiator:"Estimativa transparente com premissas de OCR, indexação, formatos e coleta"},
 {topic:"Checklist de cadeia de custódia e conferência de digitalização",category:"Digitalização",priority:"alta",target:"/conteudo/rastreabilidade-digitalizacao-cadeia-custodia-ocr-hash",intent:"guia técnico",differentiator:"Protocolos, controle de lote, hash e evidências de qualidade"},
 {topic:"Guarda documental em Belo Horizonte: como comparar SLA e segurança",category:"Guarda",priority:"alta",target:"/solucoes/guarda-documental",intent:"comparação comercial",differentiator:"Inventário, movimentação, consulta, temporalidade e critérios verificáveis"},
 {topic:"GED versus ECM: custos, migração e permissões",category:"Alfresco",priority:"alta",target:"/solucoes/alfresco-incloud",intent:"comparação de soluções",differentiator:"Matriz prática com arquitetura, backup, AD e workflows"},
 {topic:"Automação documental com IA: onde a revisão humana é obrigatória",category:"Automação",priority:"média",target:"/conteudo",intent:"educacional",differentiator:"OCR, classificação, erros, rastreabilidade e limites operacionais"},
 {topic:"Databook de engenharia: índice, revisões e controle de pendências",category:"Databook",priority:"alta",target:"/solucoes/databook",intent:"solução técnica",differentiator:"Capítulos, subitens, conferência por volume e aceite contratual"},
 {topic:"DPO terceirizado: entregáveis, SLA e canal do titular",category:"LGPD",priority:"alta",target:"/solucoes/dpo-terceirizado",intent:"contratação",differentiator:"Rotina documentada, responsabilidades, relatórios e critérios de atendimento"}
];
export async function competitorRadar(){
 const checkedAt=new Date().toISOString();
 const records=await Promise.all(competitors.map(async c=>{
  try{
   const response=await fetch(c.url,{redirect:"follow",headers:{"user-agent":"ArquindexEditorialRadar/1.0 (+https://arquindex.com.br)","accept":"text/html"},signal:AbortSignal.timeout(7000)});
   const ct=response.headers.get("content-type")||"";
   if(!response.ok || !ct.includes("text/html"))return {...c,status:"indisponivel",httpStatus:response.status};
   const html=(await response.text()).slice(0,300000);
   const title=html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1].replace(/<[^>]*>/g,"").replace(/\s+/g," ").trim().slice(0,160)||null;
   const description=html.match(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']{1,500})["']/i)?.[1]||null;
   return {...c,status:"acessivel",httpStatus:response.status,title,description};
  }catch(e){return {...c,status:"falha de coleta",error:String(e).slice(0,130)}}
 }));
 return {name:"Radar competitivo Arquindex",checkedAt,kind:"observacao de páginas públicas, não ranking",competitors:records,opportunities,methodology:"URLs públicas pré-aprovadas; títulos e descrições para análise editorial. Sem copiar artigos, sem alegar posições não medidas e sem indexação automática."};
}
