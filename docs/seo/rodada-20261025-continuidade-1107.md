# Continuidade operacional SEO/GEO/AEO — 25/10/2026, 11h (Brasília)

## Estado verificado
- Auditoria ARQ-119 a ARQ-124: workflow 40189749754, sucesso.
- Melhoria preparada para ARQ-119, ARQ-120, ARQ-123: commit 811c27f610643a77f1304b5499cad9d998516682. **Não publicada**.
- Backup integral: workflow 40182813507, job `audit` em progresso, etapa `Gerar backup integral e inventário sem exclusões`. Não executar FTP simultâneo.
- Fila `seo/fila-seo-geo-aeo.csv`: cursor ARQ-119, bloqueio temporário; preservar sem avanço artificial.
- Inventário histórico 56 subdomínios: `docs/seo/auditoria-56-publicos-20261018.md`. Em 18/10, 55 NXDOMAIN e um host com conteúdo/canonical divergentes; **não extrapolar para 25/10 sem nova auditoria**.

## Condições de liberação
1. Confirmar conclusão bem-sucedida do backup integral e existência de manifesto/hashes e teste de restauração isolada.
2. Confirmar caminhos de destino Homehost, guardar cópias originais e plano de rollback.
3. Conferir que ARQ-119/120/123 usam logo e componentes atuais, imagem acessível, WhatsApp único, H1 único, CTA, canonical, title, description, mobile e links contextuais.
4. Publicar **no máximo três** URLs da rodada por fluxo FTPS autorizado, registrar commit, workflow, URL, horário e SHA antes/depois.
5. Validar GET HTTP 200 e conteúdo/canonical/robots/sitemap publicamente; somente então marcar como publicada e atualizar cursor.
6. Submissões GSC/Bing/IndexNow somente com confirmação real; divulgar peças inéditas sem repetir ARQ-007/099.

## Inventário de 56 subdomínios
Não executar workflow de upload de 56 em massa. Primeiro obter inventário DNS/SSL/HTTP atual e correspondência de document roots no cPanel. Evidência anterior: `docs/seo/auditoria-56-publicos-20261018.md`. Tratar qualquer NXDOMAIN como bloqueio, não como autorização para criar alias na raiz institucional.

## Limite desta atualização
Registro operacional apenas: nenhuma mudança de produção, nenhum sitemap enviado, nenhuma postagem social, nenhuma alegação de ganho de ranking ou lead.
