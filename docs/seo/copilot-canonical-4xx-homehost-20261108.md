# Auditoria de canônicas 4XX — revisão Copilot e publicação HomeHost

Referência: Ahrefs, rastreamento 07/11/2026: 4.268 URLs internas; 3.139 ocorrências de erro; 556 ocorrências novas de canonical apontando para 4XX; 178 páginas com JS quebrado; 178 com imagens quebradas e 171 com links quebrados. Exportação individual **não disponível** neste PR; não confundir ocorrências com URLs únicas.

## O que executar agora
1. Rodar os testes offline no PR, usando o workflow **Auditar canonicas 4XX (somente leitura)**. Sem FTP, Cloudflare, Railway, IndexNow ou modificação de produção.
2. Com exportação Ahrefs CSV contendo `URL`, `Canonical` e, quando houver, `Canonical HTTP Code`, executar:
   `python scripts/seo_canonical_review.py --input ahrefs-canonical.csv --out seo-report/canonical-4xx-triage.json`.
3. Agrupar causas por template e domínio. Revisar páginas que apontam para outros subdomínios manualmente. A referência `httpCode` genérica pode ser status da página-fonte; não interpretá-la como status do destino.
4. Antes de cada edição, comparar GET público, redirects, canonical real, robots, sitemap publicado, indexabilidade e caminho existente na HomeHost.
5. Auditar a divergência `og:url=/index-seo.html` versus canonical `/` observada na homepage. O `index.html` publicado não está comprovadamente presente na raiz do repositório; não gerar homepage substituta.
6. Auditar `.github/workflows/publicar-databooks-homehost.yml`: atualiza somente HTML, não sitemap XML; faz backup por arquivo, **não prova backup restaurável de todo o site**. Não executar com `workflow_dispatch` nem merge sem revisar riscos de execução `on: push master`.
7. Tratar PR #118 separadamente: guias ainda em `noindex`; não declarar publicação ou liberar sitemap sem leitura pública.

## Tarefa para GitHub Copilot
Revisar com atenção o parser, os testes, os workflows de SEO e os arquivos realmente existentes. Propor PR incremental com correção **específica para cada página confirmada**, sem criação massiva de URLs, links artificiais ou sobrescrita de conteúdo existente. Validar também scripts de backup e rollback. Documentar evidências e logs; não executar deploy antes de confirmar backup restaurável, document root HomeHost, FTPS com certificado válido e aprovação explícita do lote.

## Critério de publicação
Nenhum dos presentes arquivos publica o site. A edição pública exige o confronto com arquivos restaurados, backup testado, plano de rollback e verificação HTTP 200, canonical, imagem, JS e sitemap depois do upload. Não usar Railway para o domínio institucional.
