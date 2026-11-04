# Rodada noturna — inventário ARQ-149 a ARQ-154

Data de verificação: 2026-11-04 (BRT)

## Escopo e evidência

- Auditoria somente leitura: [workflow 41935973588](https://github.com/arxazure/arquindex/actions/runs/41935973588)
- Commit do workflow: [71a930ba4cb17ceb48d80f68aa557bf9320171a9](https://github.com/arxazure/arquindex/commit/71a930ba4cb17ceb48d80f68aa557bf9320171a9)
- Fila atualizada no commit [7c51f24874fb6c303031571e77f6aa5a4af22b9c](https://github.com/arxazure/arquindex/commit/7c51f24874fb6c303031571e77f6aa5a4af22b9c)
- Validação da fila concluída com sucesso: [workflow 41936419689](https://github.com/arxazure/arquindex/actions/runs/41936419689)
- Testes: DNS A, TLS autorizado, HTTP/final URL, title, description, H1, canonical, meta robots, identidade, menu, WhatsApp, formulários, UTM, links internos, JSON-LD, largura mobile/desktop, robots.txt, sitemap.xml e presença da URL no sitemap.
- Navegadores: Chromium mobile 390×844 e desktop 1440×900.

## Resultado por URL

| ID | URL | Resultado comprovado | Estado/decisão |
|---|---|---|---|
| ARQ-149 | https://incineracaodocumentos.arquindex.com.br/ | DNS e TLS válidos; HTTP 200; canonical própria; index,follow; robots e sitemap HTTP 200; WhatsApp presente. Sem logo oficial ou atendimento flutuante; sem formulário/UTM; overflow mobile 512/390; URL ausente do sitemap próprio. | Não alterada. Diferenciar a intenção de descarte e confirmar cadeia de custódia/certificado antes de reconstruir. |
| ARQ-150 | https://instalacao-acervos-preco.arquindex.com.br/ | DNS e TLS válidos; HTTP 200; canonical própria; index,follow; robots e sitemap HTTP 200; WhatsApp presente. Sem logo oficial ou atendimento flutuante; sem formulário/UTM; overflow mobile 512/390; URL ausente do sitemap próprio. | Não alterada. Definir unidade de cobrança e papel frente às páginas de preço antes de ampliar. |
| ARQ-151 | https://mapa-de-processos.arquindex.com.br/ | DNS e TLS válidos; HTTP 200; index,follow; robots e sitemap HTTP 200; responsiva sem overflow. Canonical incorreta para https://www.arquindex.com.br/output/mapa-de-processos.arquindex.com.br/index.html; title duplicando “Arquindex”; 305 palavras; sem logo, atendimento flutuante, WhatsApp, formulário ou UTM. | Correção necessária, mas não publicada: o arquivo-fonte e a raiz FTP isolada não foram comprovados. |
| ARQ-152 | https://negocios.arquindex.com.br/ | DNS e TLS válidos; HTTP 200; canonical própria; index,follow; robots e sitemap HTTP 200; WhatsApp presente. Sem logo oficial ou atendimento flutuante; sem formulário/UTM; overflow mobile 512/390; URL ausente do sitemap próprio. | Não alterada. Definir função própria de hub e remover sobreposição antes de ampliar. |
| ARQ-153 | https://simagestao.arquindex.com.br/ | DNS e TLS válidos; HTTP 200; canonical própria; index,follow; title/H1/description coerentes; logo, menu, atendimento flutuante, WhatsApp, UTM e JSON-LD presentes; 752 palavras; sem overflow; URL no sitemap. | Preservada, sem republicação. Marco anterior continua válido. |
| ARQ-154 | https://tabela-de-temporalidade-arquivar-documentos.arquindex.com.br/ | DNS e TLS válidos; HTTP 200; index,follow; robots e sitemap HTTP 200; responsiva sem overflow. Canonical incorreta para https://www.arquindex.com.br/output/tabela-de-temporalidade-arquivar-documentos.arquindex.com.br/index.html; title duplicando “Arquindex”; 309 palavras; sem logo, atendimento flutuante, WhatsApp, formulário ou UTM. | Correção necessária, mas não publicada: o arquivo-fonte e a raiz FTP isolada não foram comprovados. |

## Publicação, sitemap e descoberta

Nenhuma página foi alterada ou publicada nesta rodada. O workflow amplo dos 56 subdomínios não foi executado porque o destino individual e o backup das ARQ-151/154 não estavam demonstrados. Portanto:

- nenhum backup remoto novo foi necessário;
- nenhum sitemap foi modificado;
- nenhuma submissão foi feita ao Search Console, Bing Webmaster ou IndexNow;
- nenhuma indexação, posição ou lead foi inferido;
- nenhuma peça social foi criada ou republicada;
- ARQ-099 permaneceu intocada.

## Próximas ações

1. Localizar no repositório o gerador/arquivo-fonte e mapear a raiz FTP individual de ARQ-151 e ARQ-154; só então fazer backup e corrigir canonical, title, identidade e CTA.
2. Corrigir o overflow de ARQ-149, ARQ-150 e ARQ-152 em publicação isolada, após definir a intenção única de cada página.
3. Validar os sitemaps próprios de ARQ-149, ARQ-150 e ARQ-152 e incluir apenas URLs canônicas publicadas; submeter somente por sessão ou integração autenticada com resposta registrada.
