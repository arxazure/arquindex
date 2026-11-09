# Auditoria de canônicas 4XX — revisão Copilot e publicação HomeHost

Referência: Ahrefs, rastreamento 07/11/2026: 4.268 URLs internas; 3.139 ocorrências de erro; 556 ocorrências novas de canonical apontando para 4XX; 178 páginas com JS quebrado; 178 com imagens quebradas e 171 com links quebrados. Exportação individual **não disponível** neste PR; não confundir ocorrências com URLs únicas.

## Revisão incremental deste PR
1. Rodar somente os testes offline no PR, usando o workflow **Auditar canonicas 4XX (somente leitura)**. Sem FTP, Cloudflare, Railway, IndexNow ou modificação de produção.
2. Com exportação Ahrefs CSV contendo `URL`, `Canonical URL` e, quando houver, status explicitamente associado à canonical, executar:
   `python scripts/seo_canonical_review.py --input ahrefs-canonical.csv --out seo-report/canonical-4xx-triage.json`.
3. O parser aceita aliases de `Canonical URL` e status do destino, registra status de origem separadamente e ignora status HTTP genérico para classificar o destino. Hosts fora do site oficial, credenciais em URLs, portas não padrão e URLs malformadas ficam em revisão.
4. Agrupar causas por template somente após receber o CSV. Revisar páginas que apontam para outros hosts manualmente. Nenhum URL individual foi inferido nem corrigido sem o export.
5. Antes de cada edição, comparar GET público, redirects, canonical real, robots, sitemap publicado, indexabilidade e caminho existente na HomeHost.
6. A antiga `.github/workflows/publicar-databooks-homehost.yml` era acionada por push em `master` e por `workflow_dispatch`, escrevia em `public_html/` e fazia backup apenas dos HTML alterados. O manifesto necessário ao rollback só era criado depois de todas as gravações e readbacks; uma falha durante a escrita poderia deixar alterações sem rollback automático. O workflow foi substituído por bloqueio sem FTP.
7. `seo-recovery.yml` chamava `scripts/seo_recovery.py`, que usava FTP sem TLS, assumia `public_html/` e respaldava apenas arquivos alterados. O script agora recusa qualquer modo de escrita e exige FTPS com TLS verificado para leitura; o workflow não foi executado.
8. Auditar a divergência `og:url=/index-seo.html` versus canonical `/` observada na homepage. O `index.html` publicado não está comprovadamente presente na raiz do repositório; não gerar homepage substituta.
9. Tratar PR #118 separadamente: guias ainda em `noindex`; não declarar publicação ou liberar sitemap sem leitura pública.

## Tarefa para GitHub Copilot
Revisar com atenção o parser, os testes, os workflows de SEO e os arquivos realmente existentes. Propor PR incremental com correção **específica para cada página confirmada**, sem criação massiva de URLs, links artificiais ou sobrescrita de conteúdo existente. Validar também scripts de backup e rollback. Documentar evidências e logs; não executar deploy antes de confirmar backup restaurável, document root HomeHost, FTPS com certificado válido e aprovação explícita do lote.

## Estado e critério de publicação
Nenhum workflow foi executado contra a produção e nenhuma publicação foi feita. O workflow de publicação legado agora falha explicitamente sem FTP. Permanecem sem evidência: backup integral com teste real de restauração, raiz de produção confirmada na HomeHost, FTPS/TLS validado contra o host efetivo, lote de URLs aprovado e procedimento de rollback verificado. A origem e o conteúdo HTTP atuais também não foram confirmados neste trabalho.

Só depois de satisfazer esses gates e aprovar explicitamente um lote restrito poderá ser preparado um novo fluxo. A validação deve comparar o conteúdo antes/depois e confirmar publicamente HTTP, HTML, canonical, assets e sitemap. Push ou merge no GitHub não é publicação; Railway não é a origem do site institucional.
