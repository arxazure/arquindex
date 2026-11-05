# Rodada noturna — ARQ-167–172 — 05/11/2026

## Evidências executadas
- Auditoria inicial read-only: https://github.com/arxazure/arquindex/actions/runs/42106259703 — o runner encontrou resets transitórios.
- Repetição única e limitada: https://github.com/arxazure/arquindex/actions/runs/42131311835 — os seis hosts resolveram para 177.234.150.42, TLS foi autorizado e todas as páginas responderam HTTP 200.
- Publicação isolada ARQ-171: https://github.com/arxazure/arquindex/actions/runs/42131701619 — sucesso.
- Commit do publicador: 5503db7b606e9106cf1d5bc6f54e0c4b0abe7205.
- Artefato: https://github.com/arxazure/arquindex/actions/runs/42131701619/artifacts/13462973083.
- Backup ARQ-171: `/seo-backups/identidade-20261105T234525Z/830ed69b56f806d6bdb1.html`.
- SHA-256 publicado: `aac8c178b04561c47c478f12a07029613a31c17a0815bff875e164ea4a08de8c`.

## Resultado por ficha

| Ficha | Verificação pública | Ação | Descoberta | Estado |
|---|---|---|---|---|
| ARQ-167 | HTTP 200, canonical própria, H1 único, identidade, WhatsApp, 390/390 | Preservada; já publicada em 29/10 | robots 200 e sitemap 200 com URL | Aguardar janela e métricas |
| ARQ-168 | HTTP 200; canonical própria; title/H1 dizem Belo Horizonte em URL São Paulo; 512/390 | Nenhuma escrita | robots 200; sitemap 200 sem a URL | Bloqueada por conflito regional e atendimento |
| ARQ-169 | HTTP 200, canonical própria, H1 único e 390/390 | Preservada; title corrigido em 29/10 | robots 200; sitemap 200 sem a URL | Aguardar janela; identidade/CTA ainda incompletos |
| ARQ-170 | HTTP 200, canonical própria, H1 único; intenção saúde/São Vicente; 512/390 | Nenhuma escrita | robots 200; sitemap 200 sem a URL | Confirmar atendimento, logística e requisitos de saúde |
| ARQ-171 | HTTP 200, canonical própria, H1 único, index/follow, logo, menu, rodapé, WhatsApp e 390/390 mobile / 1440/1440 desktop | Identidade oficial publicada via FTPS com backup; title/H1 e conteúdo preservados | robots 200; sitemap 200, mas a URL não consta | Publicada e verificada; próxima etapa é revisão editorial diferenciada |
| ARQ-172 | HTTP 200, canonical própria, H1 vazio, sem meta robots, 390/390 | Nenhuma escrita; origem FTPS continua não mapeada | robots 404; sitemap 200 com URL | Corrigir somente após localizar root real e efetuar backup |

## Decisões
- O reset inicial foi tratado como transitório e não como indisponibilidade comprovada.
- ARQ-168 e ARQ-170 não foram promovidas por falta de confirmação regional/comercial.
- ARQ-167 e ARQ-169 não foram republicadas, pois já tiveram alterações recentes.
- ARQ-172 permanece intacta porque a tentativa anterior retornou `TARGET_NOT_FOUND` antes de backup/escrita.
- O sitemap de ARQ-171 não foi alterado nesta rodada: o publicador de identidade preservou o escopo, e incluir a URL exige localizar e validar o arquivo de origem correspondente.
- Não houve submissão ao Search Console, Bing ou IndexNow, nem publicação social. Envio não deve ser confundido com indexação.
- ARQ-007 e ARQ-099 foram preservadas.
