# Manuais Alfresco — 28/10/2026

## Publicação confirmada

Quatro artigos originais publicados no portal público Arquindex Capture, em uma central própria:
https://arquindex-capture-doc-ocr-scan.arquindex-capture.stream/manuais/alfresco/

- planejamento-implantacao-alfresco-community/ — planejamento, arquitetura, capacidade, responsabilidades e aceite;
- instalacao-alfresco-debian-docker-compose/ — laboratório novo, configuração, autenticação, persistência, busca e HTTPS;
- erros-alfresco-diagnostico-solucoes/ — diagnóstico 404, JDBC, keystore, LDAPS, imagens, indexação, preview e workflows;
- migracao-alfresco-windows-railway-validacao/ — inventário, runtimes, extensões, persistência, corte e rollback.

Os slugs são relativos à central acima. Não há dados de clientes, endereços internos ou credenciais nos textos. As instruções são exemplos para homologação, sem execução nos ambientes Alfresco. Autoria institucional Arquindex; sem alegação de teste real, certificação ou suporte oficial ao Railway.

Fonte editorial editável: conteudos/alfresco-manuais-20261028.json. HTML publicado contém title/description/canonical próprios, TechArticle JSON-LD, FAQ visível, fontes oficiais, data de revisão, sumário e CTA. A central e os quatro artigos foram incluídos no sitemap do portal e ligados a sua home e página de serviço Alfresco.

## Evidência de implantação

Site: appgprj_6ad7f0ebe0bc8191a31e44a80819a0bf, público.
Commit de fonte: 062fdd400ac70484134a440bffd356f57c357685.
Versão publicada: 6.
Deployment: appgdep_6ae26e3d8518819184c37323db0cc4a6, succeeded.
Central no domínio próprio confirmada em navegação pública após o deploy.
Preflight local: H1 único, canonical, descrição, JSON-LD, links internos/âncoras e inclusão no sitemap. Artigos com 1.009, 1.064, 1.276 e 1.097 palavras no elemento article, incluindo FAQ/fontes/sumário. Conferência visual desktop da central e do artigo de erros. Layout móvel preparado por CSS, sem alegação de teste em aparelho real.
Nenhum envio ao Google/IndexNow ou resultado de indexação/ranking é alegado.

## HomeHost: pendência de publicação

O run 40738173664 terminou com sucesso técnico, mas o job 122992265229 registrou BACKUP_PARTIAL_RESUME_REQUIRED. O último checkpoint tinha 14.750 arquivos, 276.140.682 bytes e estado in_progress. Isso não comprova backup completo ou restauração. O requisito registrado em docs/seo/rodada-20261028-tarde-auditoria.md permanece pendente.

Este PR não altera workflows de deploy, arquivos servidos pela HomeHost ou sitemaps do domínio www. Não deve ser contado como publicação em www.arquindex.com.br. Após backup completo e restauração isolada, a integração preferida é um bloco de links para a central em páginas existentes de Alfresco, sem duplicar os artigos indexáveis. Qualquer migração dos textos para o domínio principal deverá coordenar canonical e redirecionamentos para evitar duas cópias concorrentes.

Não alterar ambientes Windows, Debian/Docker ou Railway de Alfresco para publicar estes artigos.
