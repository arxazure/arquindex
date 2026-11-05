# Rodada da manhã — ARQ-155 a ARQ-160

Data: 2026-11-05 (BRT)

## Escopo

Foram auditadas seis URLs distintas do inventário de subdomínios. A auditoria pública verificou DNS A, TLS, HTTP, title, meta description, H1, canonical, robots, sitemap, identidade, links internos, CTA, formulários, JSON-LD e responsividade em Chromium mobile 390×844 e desktop 1440×900.

- Auditoria: [workflow 42020427746](https://github.com/arxazure/arquindex/actions/runs/42020427746)
- Commit do auditor: [89b997c346726e41d1cfd3b154b1fcad24ad760b](https://github.com/arxazure/arquindex/commit/89b997c346726e41d1cfd3b154b1fcad24ad760b)

## Resultado por URL

| ID | URL | Auditoria e ação |
|---|---|---|
| ARQ-155 | https://tabela-de-temporalidade-documental.arquindex.com.br/ | HTTP 200 e indexável, mas canonical aponta para `www/output/tabela-de-temporalidade-documental...`, title repete “Arquindex”, conteúdo tem 307 palavras e não há identidade/WhatsApp. Não publicada: fonte e raiz FTP isolada ainda não foram comprovadas. |
| ARQ-156 | https://acervos-medico-baixada-fluminense.arquindex.com.br/ | HTTP 200, canonical própria, sitemap inclui a URL e WhatsApp existente. Identidade incompleta e overflow 512/390. Não publicada: atendimento/logística na Baixada Fluminense não estão confirmados; evitada alegação local artificial. |
| ARQ-157 | https://acervos-rh-santa-luzia.arquindex.com.br/ | Identidade oficial, menu responsivo, rodapé e WhatsApp publicados com backup. HTTP 200, canonical própria, H1/title/description preservados e largura 390/390 no mobile e 1440/1440 no desktop. |
| ARQ-158 | https://adequacao-lgpd-especializada.arquindex.com.br/ | Identidade oficial, menu responsivo, rodapé e WhatsApp publicados com backup. HTTP 200, canonical própria, H1/title/description preservados e largura 390/390 no mobile e 1440/1440 no desktop. |
| ARQ-159 | https://alfresco.arquindex.com.br/ | Identidade oficial, menu responsivo, rodapé e WhatsApp publicados. O primeiro teste detectou 1 px de overflow causado por links técnicos Sitechecker; a regra de quebra de tokens foi corrigida e a validação final confirmou 390/390 mobile e 1440/1440 desktop. |
| ARQ-160 | https://armazenamento.arquindex.com.br/ | HTTP 200, canonical própria e WhatsApp existente, mas identidade incompleta, overflow 512/390 e conteúdo genérico sobreposto. Não publicada até definir papel próprio frente às páginas de guarda e digitalização. |

## Publicação e backups

Publicação isolada inicial:

- Commit: [0a4f8bdec64cb89133a8fe2548c4f560d4a52bf8](https://github.com/arxazure/arquindex/commit/0a4f8bdec64cb89133a8fe2548c4f560d4a52bf8)
- Workflow: [42020719158](https://github.com/arxazure/arquindex/actions/runs/42020719158)
- ARQ-157: `/seo-backups/identidade-20261105T113952Z/0aed1dad6017c601716d.html`
- ARQ-158: `/seo-backups/identidade-20261105T114016Z/293653e71ca3f17a84b7.html`
- ARQ-159: `/seo-backups/identidade-20261105T114037Z/c2639b2116827573968c.html`

O workflow inicial terminou com falha apenas porque ARQ-159 apresentou largura 391/390; ARQ-157 e ARQ-158 já haviam sido publicadas e verificadas dentro do mesmo job.

Correção final de ARQ-159:

- Diagnóstico: [workflow 42021357650](https://github.com/arxazure/arquindex/actions/runs/42021357650)
- Causa comprovada: dois links técnicos Sitechecker excediam a viewport em 1,421875 px.
- Correção reutilizável: [commit 89791fd58bad0b0fe878c4985fdcde978eac5355](https://github.com/arxazure/arquindex/commit/89791fd58bad0b0fe878c4985fdcde978eac5355)
- Publicação e verificação final: [workflow 42021749872](https://github.com/arxazure/arquindex/actions/runs/42021749872)
- Backup final: `/seo-backups/identidade-20261105T114732Z/c2639b2116827573968c.html`

## Descoberta e divulgação

Não foram criadas URLs novas. Os sitemaps permaneceram disponíveis, mas ARQ-157, ARQ-158, ARQ-159 e ARQ-160 não aparecem nos próprios sitemaps observados; a regularização exige mapear a origem individual dos XMLs antes de alterar. Não houve submissão a Google, Bing ou IndexNow, pois nenhuma nova versão de sitemap foi publicada e não há resposta autenticada a registrar.

Nenhuma divulgação social foi repetida nesta rodada. ARQ-099 permaneceu intocada.

## Próximas prioridades

1. Mapear fonte e raiz FTP isolada da ARQ-155 para corrigir canonical e reconstruir o guia sem inventar prazos universais.
2. Definir o papel editorial exclusivo da ARQ-160 antes de aplicar identidade e conversão.
3. Localizar a origem dos sitemaps de ARQ-157 a ARQ-160 e incluir somente as URLs canônicas existentes, com validação XML e submissão autenticada sem confundir envio com indexação.
