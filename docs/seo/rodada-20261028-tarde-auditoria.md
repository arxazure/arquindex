# Rodada SEO/GEO/AEO — 28/10/2026, tarde

## Escopo e evidências

- Fichas revisadas: ARQ-149 a ARQ-154.
- Workflow de auditoria: https://github.com/arxazure/arquindex/actions/runs/40738176208
- Job: 122992273600 — conclusão `success`.
- Commit do workflow: `4623995c2bcb4441064ba3eda6ba3e13d3a0bf2d`.
- Fila atualizada no commit `b06c2226ee58c5086d13f47bec94c5c8a9768955`.
- Continuação do backup HomeHost: https://github.com/arxazure/arquindex/actions/runs/40738173664
- Commit da continuação: `3cdb0e5f3efb9500cb18f64aeeb77849911a3116`.
- Estado observado durante a rodada: job em andamento, etapa `Retomar checkpoint privado verificado`.

## Resultado por URL

| ID | URL | HTTP / descoberta | Diagnóstico verificável | Decisão |
|---|---|---|---|---|
| ARQ-149 | https://incineracaodocumentos.arquindex.com.br/ | HTTP 200; robots e sitemap 200 | Canonical própria; sem logo e CTA detectáveis; overflow móvel 512/390; conteúdo amplo e sobreposto | Preservar. Diferenciar por autorização, cadeia de custódia e certificado, sem afirmar que digitalização autoriza descarte. |
| ARQ-150 | https://instalacao-acervos-preco.arquindex.com.br/ | HTTP 200; robots e sitemap 200 | Canonical própria; sem logo/CTA; overflow; sobreposição com ARQ-118 e grupo de preço | Não promover até definir papel e premissas de orçamento distintas. |
| ARQ-151 | https://mapa-de-processos.arquindex.com.br/ | HTTP 200; robots e sitemap 200 | Canonical aponta indevidamente para `www.arquindex.com.br/output/...`; title/H1 genéricos; 305 palavras; sem identidade/CTA | Correção técnica e reconstrução específica pendentes de backup completo. |
| ARQ-152 | https://negocios.arquindex.com.br/ | HTTP 200; robots e sitemap 200 | Canonical própria; sem logo/CTA; overflow; sobreposição com 12 URLs | Definir função de hub ou consolidar; não ampliar conteúdo genérico. |
| ARQ-153 | https://simagestao.arquindex.com.br/ | HTTP 200; robots e sitemap 404 | Exposição de `Index of /`; sem canonical, meta robots, descrição, identidade, CTA ou conteúdo; 21 palavras | Prioridade crítica: retirar listagem e reconstruir isoladamente após confirmar intenção e ter backup verificável. |
| ARQ-154 | https://tabela-de-temporalidade-arquivar-documentos.arquindex.com.br/ | HTTP 200; robots e sitemap 200 | Canonical aponta indevidamente para `www.arquindex.com.br/output/...`; title/H1 genéricos; 309 palavras; sem identidade/CTA | Corrigir canonical e criar guia útil sem inventar prazos universais, após backup completo. |

## Alterações aplicadas

- Produção/FTP: nenhuma.
- Sitemap: nenhuma alteração, pois nenhuma URL nova foi publicada.
- Search Console, Bing e IndexNow: nenhuma submissão; não houve versão nova publicada.
- Redes sociais: nenhuma publicação; ARQ-007 e ARQ-099 não foram repetidas.
- Railway, Hostinger e ChatGPT Site: nenhum deploy alegado.
- Dados de ranking, indexação ou leads: não inferidos.

A decisão de não publicar foi deliberada: o backup completo e restaurável ainda não tinha confirmação, e as correções exigem substituição de conteúdo/arquivos em produção. A regra de até três melhorias não é uma meta mínima; nesta rodada foram aplicadas apenas melhorias de auditoria, fila e continuidade do backup.

## Backup

A continuação parte do checkpoint privado:

- checkpoint: `/seo-backups/resumable/20261026T115321Z-4df745d1d388/checkpoint-000054-39263e729ab7.json`
- SHA-256: `7d29acfa420284df573238d876b1ba99b8b56f02af37858d15210d46811c3bfa`
- arquivos acumulados: 13.250
- bytes de origem acumulados: 265.109.473
- marcador anterior: `BACKUP_PARTIAL_RESUME_REQUIRED`

Só prosseguir com FTP depois de `BACKUP_COMPLETE_VERIFIED` e evidência de restauração isolada.

## Próximas três prioridades

1. Confirmar a conclusão do backup retomável e executar teste de restauração isolada.
2. Corrigir imediatamente a exposição de diretório da ARQ-153 por publicação isolada, com página institucional útil e identidade oficial, sem presumir serviço não validado.
3. Corrigir as canonicals da ARQ-151 e ARQ-154 e reconstruir respostas AEO específicas, evitando sobreposição e prazos universais.

## Cobertura

A fila persistente avançou até ARQ-154. Esta rodada revisou seis URLs; não representa cobertura integral das 238 fichas nem confirmação integral dos 56 subdomínios.
