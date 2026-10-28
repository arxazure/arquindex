# Plano de execução SEO sem bloqueio por backup — 28/10/2026

## Objetivo e linha de base
Meta: 1.000–3.000 cliques orgânicos por janela móvel de 28 dias; referência GSC exportada em 27/10/2026: 95 cliques, 6.650 impressões, CTR aproximada 1,43%. Não confundir cliques com conversões, nem afirmar meta alcançada sem dados.

## Fase A — executar sem FTP/deploy
1. Auditar e documentar redirects de http://arquindex.com.br, http://www.arquindex.com.br, https://arquindex.com.br e https://www.arquindex.com.br; selecionar canônica somente após confirmar URL final HTTP 200 e política atual. Não fazer redirect em lote sem análise de dependências.
2. Mapear links internos contextuais e válidos para as páginas pilares: digitalização certificada, guarda, OCR, GED/Alfresco e LGPD. Verificar HTTP 200 e intenção antes de inserir qualquer link. Não trocar links por rede artificial de backlinks entre propriedades próprias.
3. Preparar individualmente ARQ-119, ARQ-120, ARQ-123 já em staging; confirmar conteúdo distinto, marca oficial, canonical própria, title único, H1 único, menu responsivo, CTA WhatsApp/formulário e ausência de overflow. Não repetir peças sociais ARQ-007 e ARQ-099.
4. Preparar patch mínimo ARQ-133: canonical própria em https://ecm.arquindex.com.br/custo.html e title sem repetição de marca; preservar H1, CTAs e layout existentes. ARQ-141: canonical própria em https://digitacao-de-documentos.arquindex.com.br/ e title sem duplicação, após confirmar que digitação é serviço ofertado.
5. ARQ-139: não prometer cobertura Duque de Caxias antes de confirmação comercial. ARQ-140: revisar fontes oficiais do Decreto 10.278/2020 sem afirmar validade automática.
6. Preparar medição: GSC cliques/impressões/CTR/posição; GA4 eventos generate_lead, whatsapp_click e form_submit com deduplicação, quando implementação for possível e consentimento aplicável.
7. Registrar por URL: estado anterior, proposta, diff, testes, commit, workflow, URL pública e verificação posterior; sitemap e submissão só depois de publicação comprovada.

## Fase B — gate para alterar HomeHost
Última evidência dos logs: workflow 40603339878 terminou com BACKUP_PARTIAL_RESUME_REQUIRED; checkpoint 45: 11.000 arquivos, 254.339.475 bytes, state=in_progress. Próxima execução deve retomar /seo-backups/resumable/20261026T115321Z-4df745d1d388/checkpoint-000045-135ec032b248.json, SHA-256 3bcb44acef4d24aa88e332b27e0d5abdf5aeb178bc576ffd6b3f0c77bb45d2ca. Não reiniciar vazio. Exigir BACKUP_COMPLETE_VERIFIED, inventário sem pendências e restauração isolada antes de sobrescrever arquivos.

## Fase C — publicação individual após liberação
Ordem ARQ-119, ARQ-120, ARQ-123, depois ARQ-133 e ARQ-141. Para cada URL: confirmar destino FTPS, gravar diff e hash, publicar por integração autorizada, verificar HTTP 200, canonical, title/H1, marca, mobile, CTA e formulário. Só então atualizar sitemap e registrar respostas de GSC/Bing/IndexNow, se disponível. Nunca alegar indexação imediata.

## Métrica e priorização
Consultas GSC: empresa de digitalização (115 impressões, posição média 39,01), serviço de digitalização de documentos (95; 34,41), empresa de digitalização de documentos (95; 32,76), digitalização de documentos (83; 20,67), consultoria LGPD (73; 49,10). Priorizar ganho de relevância das páginas pilares, links contextuais e títulos úteis; não produzir páginas repetidas por cidade. Resultados futuros dependem de nova medição.
