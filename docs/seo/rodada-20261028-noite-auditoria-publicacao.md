# Rodada SEO/GEO/AEO — 28/10/2026, noite

## Resultado

A rodada auditou ARQ-155 a ARQ-160 e corrigiu o achado crítico da rodada anterior: a ARQ-153 deixou de expor uma listagem de diretório e passou a publicar uma página institucional útil, com identidade Arquindex, canonical própria, CTA, robots e sitemap.

## Evidências

- Auditoria ARQ-155–160: https://github.com/arxazure/arquindex/actions/runs/40789177108
- Job de auditoria: `123169823310` — `success`
- Commit do workflow: `cbf689e1bc5c9f93fef95479e3c17dadc189c345`
- Publicação ARQ-153: https://github.com/arxazure/arquindex/actions/runs/40789530425
- Job de publicação: `123170988386` — `success`
- Fonte HTML: `11ba1e1f3d90f26a03bc10fc146c886f07570540`
- Script de publicação: `4dc5e49e9ff98823d2ca0a22bf8df9763b2b2c57`
- Workflow de publicação: `e0d742d3e1ca0af1515ab9fde45bd1e6b2ecf676`
- Fila atualizada: `c3690e3da0ba0ca04a0df928493aa8bc72aafac5`
- Continuação de backup a partir do checkpoint 60: https://github.com/arxazure/arquindex/actions/runs/40789699871

## Auditoria por URL

| ID | URL | Estado verificado | Próxima ação |
|---|---|---|---|
| ARQ-155 | https://tabela-de-temporalidade-documental.arquindex.com.br/ | DNS/SSL e HTTP 200; robots/sitemap 200; canonical incorreta para `www/output/...`; title com marca repetida; 307 palavras; sem logo/CTA | Corrigir canonical e reconstruir método útil sem inventar prazos universais. |
| ARQ-156 | https://acervos-medico-baixada-fluminense.arquindex.com.br/ | HTTP 200 e canonical própria; intenção saúde/local; logo/CTA ausentes; overflow 512/390 | Confirmar atendimento/logística; diferenciar por sigilo e protocolo de prontuários. |
| ARQ-157 | https://acervos-rh-santa-luzia.arquindex.com.br/ | HTTP 200 e canonical própria; intenção RH/Santa Luzia; logo/CTA ausentes; overflow 512/390 | Confirmar atendimento; aprofundar homônimos, vínculos e acesso restrito. |
| ARQ-158 | https://adequacao-lgpd-especializada.arquindex.com.br/ | HTTP 200 e canonical própria; LGPD/DPO BH; logo/CTA ausentes; overflow 512/390 | Diferenciar da pilar por entregáveis e escopo verificáveis. |
| ARQ-159 | https://alfresco.arquindex.com.br/ | HTTP 200 e canonical própria; Alfresco BH; logo/CTA ausentes; overflow 512/390 | Diferenciar por versão, arquitetura, migração, piloto e recuperação. |
| ARQ-160 | https://armazenamento.arquindex.com.br/ | HTTP 200 e canonical própria; conteúdo genérico; logo/CTA ausentes; overflow 512/390 | Definir papel único frente às páginas de guarda e digitalização. |

Todos os seis hosts resolveram para `177.234.150.42`, responderam HTTPS/HTTP 200 e apresentaram robots e sitemap HTTP 200.

## Melhoria substancial publicada — ARQ-153

URL: https://simagestao.arquindex.com.br/

Antes:

- HTTP 200 com `Index of /`
- 21 palavras
- robots e sitemap 404
- sem canonical, meta robots, descrição, identidade, CTA ou conteúdo

Depois:

- HTTP 200 e canonical própria
- title: `Gestão documental: diagnóstico e próximos passos | Arquindex`
- um H1
- meta robots `index,follow,max-image-preview:large`
- logo oficial, menu responsivo e atendimento flutuante
- resposta AEO visível e conteúdo original sobre diagnóstico, inventário, temporalidade, piloto, aceite e controles
- quatro CTAs para WhatsApp/proposta
- `robots.txt` e `sitemap.xml` HTTP 200
- mobile 390/390 e desktop 1440/1440, sem overflow
- nenhuma ocorrência de `Index of /`

A publicação criou arquivos ausentes; não substituiu `index.html`, `robots.txt` ou `sitemap.xml` existentes. O inventário anterior foi salvo em:

`/seo-backups/reconstrucoes/arq153-20261028T234530Z`

SHA-256 do inventário: `20d695db1c47b9ae256859ce8b9ce08126166e2de31c5f59f291822a784830e5`

SHA-256 publicado do HTML: `ebb928c185d1a86b523dbb42f0198ab1aa39eba2a66abe8c48ea461f06f742e6`

## Descoberta e submissões

- Sitemap criado e validado: https://simagestao.arquindex.com.br/sitemap.xml
- IndexNow: não enviado; `INDEXNOW_KEY` estava vazio.
- Search Console/Bing Webmaster: não houve sessão ou integração autenticada nesta rodada que confirmasse recebimento.
- Sitemap publicado não equivale a indexação.

## Backup HomeHost

O run anterior concluiu tecnicamente, mas terminou com `BACKUP_PARTIAL_RESUME_REQUIRED`, portanto não é backup integral.

Checkpoint mais recente:

- caminho: `/seo-backups/resumable/20261026T115321Z-4df745d1d388/checkpoint-000060-150137135985.json`
- SHA-256: `81692c331ad618cc1cf86a301a8d98ec55b055e37f059053441777e482734ed8`
- arquivos: 14.750
- bytes de origem: 276.140.682

Nova continuação iniciada no workflow 40789699871. A reconstrução da ARQ-153 não aguardou o backup integral porque a página estava ausente e o procedimento foi isolado, sem sobrescrita e com rollback dos arquivos criados em caso de falha.

## Publicações e métricas

- Redes sociais: nenhuma publicação; não houve repetição de ARQ-007 ou ARQ-099.
- Railway, Hostinger e ChatGPT Site: nenhum deploy alegado.
- Ranking, indexação, posição e leads: nenhum resultado inferido.

## Próximas prioridades

1. Corrigir a canonical e aprofundar a ARQ-155, sem prazos universais.
2. Aplicar identidade/CTA e resolver overflow da ARQ-159, preservando papel distinto da página Alfresco BH.
3. Confirmar atendimento em Santa Luzia antes de revisar a ARQ-157.

Cobertura acumulada da fila: ARQ-001 a ARQ-160. Isso não significa cobertura integral das 238 fichas nem confirmação integral dos 56 subdomínios.
