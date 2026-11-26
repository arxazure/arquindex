# Auditoria HomeHost e lote editorial — 21/11/2026

## Resultado executivo

A decisão operacional continua sendo **HomeHost** para `arquindex.com.br` e `www.arquindex.com.br`. O `master` do GitHub está em `bf8dbe80ef54fc4fbb434eefe3b0cbf57599cf27` e contém `config/site-hosting.json` e `AGENTS.md` coerentes com essa decisão. A evidência pública de 21/11/2026 também aponta para HomeHost: delegação em `ns31.servidorwebsite.com` e `ns32.servidorwebsite.com`, raiz em `177.234.150.42` e `www` como CNAME do domínio raiz.

Não houve escrita na HomeHost, DNS, Railway, sitemap público, GSC, IndexNow/Bing ou Blogger. Faltam confirmação da raiz pública HomeHost, backup completo restaurável fora de `public_html` e leitura FTPS com certificado TLS válido. O acesso público HTTPS funcionou; isso não comprova acesso de publicação.

Foram preparados dois artigos originais, com 2.024 e 2.108 palavras úteis no `main`, em branch editorial e com `noindex,follow`. As URLs propostas continuam HTTP 404 e, portanto, os artigos estão **CRIADOS, não publicados**.

## 1. Auditoria e deploy técnico

### Origem e conexões

| Serviço | Leitura inofensiva | Resultado | Interpretação |
|---|---|---|---|
| GitHub `arxazure/arquindex` | commit, arquivos e PRs | OK | `master` e aviso HomeHost lidos; PR #151 continua aberto e draft |
| Site público/HomeHost | DNS, HTTPS e conteúdo | OK | HTTP 200 no domínio e páginas prioritárias; não prova FTPS, backup ou raiz |
| Railway | projeto, config e deployments | OK | `arquindex-web`, branch `railway-production-2026`, raiz `/arquindex-platform`, sem staged; cinco deployments recentes em `REMOVED` |
| Cloudflare | identidade e lista de zonas | OK | autenticação válida; consulta exata retornou zero zonas `arquindex.com.br` nesta conexão |
| GSC Wizard | propriedade `http://arquindex.com.br/` | OK | dados disponíveis até 19/11/2026 |
| Blogger | feed público JSON | OK | 36 posts; sem título exato da fila; nenhum conector OAuth de escrita disponível |
| Top10 privado | status | OK | fila lida; nenhuma reserva ou escrita executada |

### DNS, TLS e HTTP públicos

- NS: `ns31.servidorwebsite.com`, `ns32.servidorwebsite.com`.
- A da raiz: `177.234.150.42`.
- CNAME `www`: `arquindex.com.br`.
- `https://arquindex.com.br/` e `https://www.arquindex.com.br/`: HTTP 200.
- O `curl` validou HTTPS sem opção insegura; não foi usado bypass de certificado.
- `robots.txt`: HTTP 200, permite rastreamento público e bloqueia áreas administrativas/privadas.
- `sitemap.xml`: HTTP 200, índice com 16 filhos e 579 URLs no total.
- `sitemap-index.xml`: HTTP 404.
- `/assets/` e `/seo/`: HTTP 200 com **Index of /**.
- Recursos ainda HTTP 404: `/arquindex-favicon.png`, `/img/about.webp`, `/assets/img/about.webp`, `/css/IE-fix.css`.

### Páginas prioritárias

| URL | HTTP | Canonical | Robots | H1 | JSON-LD |
|---|---:|---|---|---:|---:|
| `/guarda_de_documentos.html` | 200 | autorreferente | index,follow | 1 | 1 |
| `/gestao_de_colaboradores_documentos.html` | 200 | autorreferente | index,follow | 1 | 0 |
| `/digitalizacao.html` | 200 | autorreferente | index,follow | 1 | 4 |
| `/digitalizacao-com-ocr.html` | 200 | autorreferente | index,follow | 1 | 3 |

A homepage declarou canonical `https://www.arquindex.com.br/`, robots `index,follow,max-image-preview:large`, um H1, viewport móvel e dois blocos JSON-LD. Nenhuma alteração de layout foi feita.

O teste renderizado em viewport de 390 px não foi concluído: o Chromium local encerrou com `socket() failed: Operation not permitted (1)` antes de abrir a página. O erro é do ambiente de execução, não HTTP, autenticação ou código do site. Assim, a presença do viewport foi confirmada no HTML, mas overflow, alvos de toque e layout visual móvel não foram afirmados nesta rodada.

### Campanha regional 24 × 3

As 72 URLs foram testadas individualmente em 21/11/2026: **72 retornaram HTTP 404**. Permanecem `PLANEJADA`. Foram criadas zero páginas regionais, pois não há evidência suficiente de demanda e atendimento para diferenciar 72 conteúdos sem doorway/canibalização. O manifesto registra cada URL.

### Search Console

Fonte: `get_site_summary`, `get_position_distribution`, `get_ranking_changes`, `detect_anomalies`, `get_decay_overview`, `analyze_cannibalization`, `score_opportunities`, `get_core_web_vitals` e `list_sitemaps`.

- Período atual: 22/10 a 18/11/2026; dados estabilizados até 19/11/2026.
- 0 cliques, 46 impressões, CTR 0%, posição média 4,57.
- Período anterior: 56 impressões, posição média 7,23; queda de 10 impressões e melhora numérica de 2,67 posições.
- Distribuição das consultas disponíveis: 15 impressões em posições 1–3, 8 em 4–10 e 2 em 11–20.
- Oportunidade de maior pontuação: `slice`, 8 impressões, posição 7,875, sem aderência comercial clara à Arquindex.
- A consulta comercial `empresa de digitalização de documentos` tinha 2 impressões no período anterior e nenhuma no atual; volume insuficiente para justificar páginas regionais em massa.
- Canibalização: nenhum caso detectado até o piso automático de 1 impressão; a amostra é pequena e não prova ausência estrutural.
- Core Web Vitals: conexão CrUX não configurada; nenhum valor foi inferido.
- `sitemap.xml` principal no GSC: 579 URLs, 3 warnings, 0 errors. Submissão não foi repetida.
- Existem 18 entradas históricas de sitemap, inclusive arquivos obsoletos/com erros; nenhuma exclusão foi feita.

Veredito SEO: **AT RISK — baixo volume**. O risco central é haver impressões sem cliques e consultas alheias ao negócio, enquanto a oportunidade é corrigir estrutura existente, exposição de diretórios e páginas prioritárias antes de ampliar URLs.

### Railway

O conector retornou:

- projeto `Arquindex Plataforma`;
- ambiente `production`;
- serviço `arquindex-web`;
- origem `arxazure/arquindex`, branch `railway-production-2026`;
- `rootDirectory: /arquindex-platform`;
- `staged: null`;
- deployments mais recentes: `REMOVED`.

A configuração ainda contém um custom domain histórico, mas o DNS autoritativo observado aponta para HomeHost. Railway não foi usado como prova de publicação.

### Correções e deploy

- Alterações em produção: **0**.
- Commit em produção: **nenhum**.
- Deploy HomeHost: **não executado**.
- Sitemap público atualizado: **não**.
- GSC/IndexNow/Bing enviados: **0**.
- Indexação confirmada: **0**.
- Limpeza HomeHost: não devida neste sábado; movidos 0, excluídos 0, espaço liberado 0.

Bloqueio exato: não há conector HomeHost/FTPS disponível nesta execução para confirmar a raiz, listar arquivos e validar certificado; também não existe evidência nova de backup completo restaurável e teste de restauração. A leitura pública HTTPS funciona. Próximo passo humano: disponibilizar a conexão HomeHost/FTPS já configurada com escopo de leitura e apontar a evidência do backup restaurável; não enviar senha por chat.

## 2. Dois artigos originais

| Título | Palavras úteis | Estado | URL proposta |
|---|---:|---|---|
| Digitalização de grandes formatos: plantas, mapas e desenhos técnicos | 2.024 | CRIADA | `/blog/digitalizacao-grandes-formatos-plantas-desenhos/` |
| Modelo de conteúdo no Alfresco: tipos, aspectos e metadados sem dívida técnica | 2.108 | CRIADA | `/blog/modelo-conteudo-alfresco-tipos-aspectos-metadados/` |

Os dois HTMLs têm H1 único, H2/H3, resposta direta, etapas, riscos, checklist, FAQ, fontes oficiais datadas, autoria, links internos, CTA, canonical proposto, Open Graph, `TechArticle` e `noindex,follow`. O artigo de grandes formatos responde a uma demanda observada no histórico Bing autorizado sobre digitalização de documento de 1,20 m × 1 m; não afirma atendimento ou case sem prova.

As fontes oficiais incluem Presidência/Decreto nº 10.278, CONARQ, FADGI, U.S. National Archives e documentação Hyland/Alfresco. Nenhum texto foi copiado para o Blogger ou convertido em página SEO regional.

URLs públicas propostas em 21/11/2026: HTTP 404 esperado. Portanto, publicação comprovada: **0**.

## 3. Gestão da fila Blogger

- Blog conferido: `documentosdigitaislegislaoesistemas.blogspot.com`.
- Blog ID público: `2545952967912533152`.
- Feed: 36 posts; atualizado em 18/10/2026.
- Post público mais recente: “Workflow documental: como o Alfresco atende”, publicado em 01/05/2026.
- Correspondências exatas com as oito pautas históricas: 0.
- Publicações nesta execução: 0.
- Motivo: não há API Blogger v3 OAuth, Apps Script autenticado ou conector oficial de escrita disponível. O feed público confirmou leitura, mas não autoriza POST.
- Não foi feita tentativa de POST e não existe resultado incerto a repetir.

## Estados consolidados

- Páginas SEO regionais: 72 PLANEJADAS; 0 CRIADAS; 0 TESTADAS como conteúdo novo; 0 PUBLICADAS; 0 SUBMETIDAS; 0 INDEXADAS confirmadas.
- Artigos do dia: 2 CRIADOS em branch; 0 PUBLICADOS; 0 SUBMETIDOS; 0 INDEXADOS confirmados.
- Blogger: 0 publicado.
- Meta de até 10 páginas: 0/10; déficit de 10, mantido explicitamente para evitar páginas doorway.
- Meta editorial: 2/2 artigos preparados.

