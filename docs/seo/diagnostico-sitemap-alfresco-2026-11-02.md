# Recuperacao do sitemap Alfresco (2026-11-02)

## Evidencias
- Search Console: sitemap `https://www.arquindex.com.br/sitemap-alfresco-cloud-20261021.xml` registrado com 16 URLs e um erro.
- Leitura direta do sitemap pelo GSC Wizard retornou HTTP 404.
- `https://www.arquindex.com.br/sitemap.xml` foi processado com 371 URLs, sem erros nem avisos.
- A rotina `seo-rotinas/publicar-sitemap-alfresco-llm-20261024.py` pressupoe que o sitemap Alfresco ja exista no servidor (`get(ftp,FILE)`) e falha quando ausente.
- `seo/alfresco-cloud-manifest.json` contem 14 paginas locais candidatas, mas nao prova que estejam publicadas ou indexaveis.

## Plano seguro
1. Confirmar a raiz publica efetiva no HomeHost, apos a migracao de hospedagem.
2. Fazer inventario das URLs do manifesto e dos tres artigos citados na rotina, testando HTTP, canonical, robots e noindex.
3. Reconstruir o XML somente com URLs canonicas, publicas e HTTP 200; nao presumir que todas as 16 URLs antigas ainda existem.
4. Publicar em `public_html/sitemap-alfresco-cloud-20261021.xml` com backup e verificacao por HTTPS.
5. Reenviar sitemap ao Search Console apenas apos confirmar HTTP 200 e XML valido.
6. Inspecionar URLs prioritarias e acompanhar erros, sem confundir submissao com indexacao.

## Restricoes
Nao remover sitemaps historicos em massa, nao alterar DNS e nao publicar paginas nao verificadas. O arquivo OAuth nao contem refresh token e nao deve ser commitado no repositorio.
