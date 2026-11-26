# Auditoria HomeHost e editorial — 26/11/2026

## Resultado executivo

A decisão operacional permanece: **HomeHost é a origem autorizada do site institucional**. O repositório `arxazure/arquindex` em `master` já contém `config/site-hosting.json` e `AGENTS.md` com essa orientação; o PR #103 foi incorporado em 02/11/2026. O DNS autoritativo observado usa `ns31.servidorwebsite.com` e `ns32.servidorwebsite.com`, com o apex em `177.234.150.42`.

Nenhuma escrita foi feita na HomeHost. Não houve comprovação, nesta execução, de backup restaurável, raiz FTPS ou escrita com certificado válido. Portanto, os dois artigos foram preparados em branch isolada, com `noindex,follow`, e **não são considerados publicados**.

## Auditoria/deploy técnico

- `https://arquindex.com.br/`: HTTP 200.
- `https://www.arquindex.com.br/`: HTTP 200.
- `/robots.txt`: HTTP 200.
- `/sitemap.xml`: HTTP 200.
- `/sitemap-index.xml`: HTTP 404.
- Prioridades `guarda_de_documentos.html`, `gestao_de_colaboradores_documentos.html`, `digitalizacao.html` e `digitalizacao-com-ocr.html`: HTTP 200.
- `/assets/` e `/seo/`: HTTP 200 com listagem de diretório publicamente alcançável.
- Campanha regional: 72/72 rotas testadas retornaram HTTP 404.
- Sitemap público: 17 sitemaps-filhos e 212 entradas URL/sitemap.
- GSC: último download do sitemap principal em 18/11/2026; 579 URLs submetidas e 3 avisos.
- Conclusão: o conjunto público e o conjunto conhecido pelo GSC divergem. Não houve nova submissão.

### Search Console

Propriedade `http://arquindex.com.br/`, período 27/10 a 23/11/2026, consolidado até 24/11:

| Métrica | Atual | Período anterior |
|---|---:|---:|
| Cliques | 0 | 0 |
| Impressões | 56 | 49 |
| CTR | 0% | 0% |
| Posição média | 5,86 | 7,16 |

A melhora numérica de posição não compensa a ausência de cliques nem autoriza expansão regional em massa. O volume é baixo, e as oportunidades de consulta observadas não justificam páginas de cidade sem intenção distinta e conteúdo comprovável.

### Railway separado

O projeto Arquindex Plataforma continua com raiz `/arquindex-platform` e branch `railway-production-2026`. O deployment `9904bd1e-d2e9-46bc-af55-ba0ba4f1a7f8` ficou `SUCCESS` em 24/11/2026, commit `163221cbd268323ed17d9ace415d8990c6addac7`, sem staged changes. Esse dado **não comprova publicação** no domínio institucional.

## Dois artigos originais

1. **OCR de formulários e tabelas: como controlar campos, confiança e fila de exceção**
   - 2.209 palavras úteis, excluindo JSON-LD.
   - Estado: CRIADA.
   - URL proposta: `https://www.arquindex.com.br/blog/ocr-formularios-tabelas-campos-confianca-excecao/`.
   - Leitura pública: HTTP 404; não publicada.

2. **Alfresco REST API: como fazer upload idempotente quando os nomes se repetem**
   - 2.466 palavras úteis, excluindo JSON-LD.
   - Estado: CRIADA.
   - URL proposta: `https://www.arquindex.com.br/blog/alfresco-rest-api-upload-idempotente-nomes-repetidos/`.
   - Leitura pública: HTTP 404; não publicada.

Ambos contêm resposta direta, etapas, riscos, checklist, FAQ, fontes oficiais datadas, autoria, links internos, metadados, canonical, Open Graph, schema TechArticle e CTA Arquindex. Os exemplos estão marcados como hipotéticos.

## Páginas SEO e indexação

| Estado | Quantidade |
|---|---:|
| PLANEJADA | 0 |
| CRIADA | 0 |
| TESTADA | 0 |
| PUBLICADA | 0 |
| SUBMETIDA | 0 |
| INDEXADA confirmada | 0 |

Não foram criadas páginas de cidade apenas para cumprir volume. As 72 rotas regionais seguem 404 e exigem inventário de URL, conteúdo único, demanda comprovada e origem HomeHost validada. Não houve envio ao GSC, Bing ou IndexNow.

## Blogger

A leitura pública do feed foi tentada antes de declarar bloqueio. O acesso web retornou erro de indisponibilidade e o navegador conectado retornou `Unknown tool`. A última linha de base verificável, de 22/11/2026, tinha 36 posts e nenhuma correspondência exata com os oito títulos históricos. Não existe conector Blogger v3/OAuth de escrita exposto nesta execução. Nenhum POST foi tentado e nenhuma postagem foi publicada.

## Fila privada Arquindex

A leitura inofensiva do status autorizado funcionou. Foram retornados 98 jobs: 3 `claimed`, 34 `accepted`, 12 `unknown`, 41 `published`, 7 `blocked` e 1 `draft`. Nenhum job foi criado ou repetido.

## Bloqueios e próximos passos

1. **HomeHost / publicação** — operação necessária: confirmar backup restaurável fora do diretório público, raiz correta e leitura FTPS com TLS válido; depois publicar somente os arquivos aprovados e fazer readback HTTP/canonical.
2. **Sitemap/GSC** — reconciliar 212 entradas públicas com 579 URLs registradas no último download antes de submeter.
3. **Directory listing** — corrigir `/assets/` e `/seo/` apenas após localizar a configuração HomeHost e validar que não afeta arquivos legítimos.
4. **Campanha regional** — revisar a matriz 24 × 3, mapear intenção e conteúdo existente e manter 404 enquanto não houver página substancial ou redirecionamento um a um comprovado.
5. **Blogger** — expor API Blogger v3 com OAuth do blog correto, ou Apps Script autenticado, e executar leitura de títulos antes de um único POST com readback.
6. **Merchant Center** — permanece frente separada e não foi auditado.

Nenhuma limpeza destrutiva foi executada; 26/11/2026 é quinta-feira, portanto o módulo semanal de domingo não era devido.
