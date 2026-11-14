# Rodada SEO/GEO/AEO — pendências centrais — 2026-11-14 manhã

## Escopo e critérios

Rodada somente de leitura em produção, limitada a seis URLs da fila persistente. Nenhuma gravação por FTP/HomeHost, Railway ou outro publicador foi executada. ARQ-007 e ARQ-099 foram preservadas e não receberam nova publicação ou divulgação.

O inventário de 56 subdomínios já havia sido concluído em 2026-11-13 (56/56 auditados, 55 NXDOMAIN e 1 host com DNS/TLS sem HTTP utilizável) e não foi repetido sem mudança de DNS comprovada.

## Evidências

- Auditoria HTTP/SEO: [workflow 43591139784](https://github.com/arxazure/arquindex/actions/runs/43591139784), sucesso.
- Artefato da auditoria: `auditoria-pendencias-centrais-20261114`, ID `14112855172`, SHA-256 `ad3e927f689afe7272229cdcbee4e05881fef2cbbea1e635241659b66406268b`.
- Validação real em Chromium, mobile 390×844 e desktop 1440×1000: [workflow 43591239757](https://github.com/arxazure/arquindex/actions/runs/43591239757), sucesso.
- Artefato mobile: `validacao-mobile-recuperadas-20261114`, ID `14112791052`, SHA-256 `1962ed04d84a0275db672f0d794b10febd6b65b60b9cdce16afa707079794b33`.
- Fila atualizada no commit [1d37f9f0611a74d3e814607d8b5224a85011ea7a](https://github.com/arxazure/arquindex/commit/1d37f9f0611a74d3e814607d8b5224a85011ea7a).
- Integridade da fila confirmada pelo [workflow 43591356610](https://github.com/arxazure/arquindex/actions/runs/43591356610), sucesso.

## Resultado por URL

| ID | URL | Resultado verificado | Estado |
|---|---|---|---|
| ARQ-150 | https://instalacao-acervos-preco.arquindex.com.br/ | HTTP 200, canonical própria, indexável, 6.048 palavras, logo/menu/WhatsApp, UTF-8 sem mojibake, desktop sem overflow | Recuperação pública detectada; mobile ainda apresenta overflow 512/390; URL ausente do sitemap próprio |
| ARQ-151 | https://mapa-de-processos.arquindex.com.br/ | HTTP 200, 314 palavras, sitemap contém URL | Canonical incorreta para `/output`, title duplicado e ausência de identidade/WhatsApp |
| ARQ-154 | https://tabela-de-temporalidade-arquivar-documentos.arquindex.com.br/ | HTTP 200, 320 palavras, sitemap contém URL | Canonical incorreta para `/output`, title duplicado e ausência de identidade/WhatsApp |
| ARQ-160 | https://armazenamento.arquindex.com.br/ | HTTP 200, canonical própria, indexável, 6.040 palavras, logo/menu/WhatsApp, UTF-8 sem mojibake, desktop sem overflow | Recuperação pública detectada; mobile ainda apresenta overflow 512/390; URL ausente do sitemap próprio |
| ARQ-165 | https://consultorias-adequacao-lgpd-diagnostico-completo-privacidade.arquindex.com.br/ | HTTP 200, canonical própria, indexável, 6.124 palavras, logo/menu/WhatsApp, UTF-8 sem mojibake, desktop sem overflow | Recuperação pública detectada; mobile ainda apresenta overflow 512/390; URL ausente do sitemap próprio |
| ARQ-188 | https://gestao-da-informacao.arquindex.com.br/ | HTTP 200, 314 palavras, sitemap contém URL | Canonical incorreta para `/output` e ausência de identidade/WhatsApp |

## Alterações e publicação

Foram registradas três recuperações públicas substanciais detectadas (ARQ-150, ARQ-160 e ARQ-165), mas a origem dessas mudanças não foi atribuída a esta rodada. Por segurança, elas não foram declaradas concluídas porque a validação real confirmou overflow móvel.

Nenhuma melhoria de produção foi publicada nesta rodada: a fonte e a raiz FTP individual das seis páginas não estão comprovadas para escrita segura, e uma publicação sem esse preflight poderia sobrescrever conteúdo atual ou atingir o destino errado. Também não houve submissão a Search Console, Bing ou IndexNow, pois não houve URL nova ou conteúdo publicado nesta rodada.

## Pendências priorizadas

1. Mapear fonte e destino individual de ARQ-150, ARQ-160 e ARQ-165, criar backup e corrigir o overflow 512/390; depois incluir cada URL no sitemap próprio e repetir a validação mobile/desktop.
2. Corrigir canonical `/output`, title e identidade de ARQ-151, ARQ-154 e ARQ-188 somente após preflight da raiz de publicação.
3. Não divulgar nenhuma das seis URLs antes da correção e da comprovação pública; não repetir peças de ARQ-007 ou ARQ-099 sem material novo.
