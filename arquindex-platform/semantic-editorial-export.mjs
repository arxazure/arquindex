// Offline, review-first semantic recommendations for the actual Railway article data.
// Run: node arquindex-platform/semantic-editorial-export.mjs
import { mkdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { articles } from './articles.js';
import { editorialProductionQueue } from './editorial-production-queue.js';

export const CLUSTERS = {
  lgpd: ['inventário de dados', 'ROPA', 'RIPD', 'encarregado', 'base legal', 'controle de acesso'],
  alfresco: ['Alfresco ECM', 'metadados', 'versionamento', 'workflow', 'permissões', 'auditoria'],
  digitalizacao: ['digitalização documental', 'OCR pesquisável', 'indexação', 'PDF/A', 'rastreabilidade', 'controle de qualidade'],
  guarda: ['guarda documental', 'inventário', 'temporalidade', 'consulta', 'destinação documental'],
  databook: ['Databook', 'engenharia', 'índice', 'revisões', 'certificados', 'aceite documental']
};
const norm = s => String(s || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
export function classify(article) {
  const text = norm([article.title,article.category,article.lead,article.cluster].join(' '));
  for (const [key, words] of Object.entries(CLUSTERS)) {
    if (words.some(word=>text.includes(norm(word.split(' ')[0])))) return key;
  }
  return null;
}
export function recommend(article) {
  const topic = classify(article);
  const sourceText = [article.title,article.lead,...(article.sections || []).flat()].join(' ');
  const terms = (CLUSTERS[topic] || []).filter(term => !norm(sourceText).includes(norm(term)));
  return {slug:article.slug,title:article.title,topic,missingTerms:terms.slice(0,5),
    suggestedBlock: terms.length ? {
      heading:'Critérios técnicos e dúvidas de contratação',
      editorialPrompt:'Avaliar se faz sentido explicar: '+terms.slice(0,5).join(', ')+'. Incluir exemplos próprios e fontes oficiais.',
      status:'requires_human_review'
    } : null,
    approvedForPublish:false};
}
export async function exportAll(destination) {
  await mkdir(destination,{recursive:true});
  const result={generatedAt:new Date().toISOString(),source:'Railway editorial source',articles:articles.map(recommend),
     queue:editorialProductionQueue.map(recommend)};
  await writeFile(path.join(destination,'semantic-editorial-review.json'),JSON.stringify(result,null,2),'utf8');
  return result;
}
if (process.argv[1] && path.resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
  exportAll(process.argv[2] || './seo-editorial-preview').then(r=>console.log(
    'Review proposals:',r.articles.length,'existing articles;',r.queue.length,'queued briefs'
  )).catch(e=>{console.error(e);process.exitCode=1});
}
