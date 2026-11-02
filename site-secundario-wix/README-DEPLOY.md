# Arquindex.com — frontend externo e Wix Blog

Este projeto é o frontend separado para o domínio secundário Arquindex.
O domínio Wix atual NÃO deve ser alterado antes da prévia e auditoria de URLs.

## Arquitetura
- Frontend estático Vite em Cloudflare Pages
- Wix Blog (site ID: 3e0b1117-8205-4b3d-a162-b368d088e765)
- OAuth de visitantes Wix via Client ID público
- Não usar WIX_CLIENT_SECRET no código do navegador

## Deploy Cloudflare Pages
- Repositório: arxazure/arquindex
- Branch: master
- Root directory: site-secundario-wix
- Build command: npm install && npm run build
- Output directory: dist

A conta Cloudflare reportou erro 8000011 de integração GitHub.
Reautorize a instalação GitHub no Cloudflare antes de automatizar deploy.

## Segurança e validação
1. Confirmar que o blog público carrega, e que não exige segredo no navegador.
2. Testar responsividade, navegação, links internos e URLs atuais.
3. Preservar redirecionamentos 301 e canonicals.
4. Manter Wix Blog apenas para conteúdos editoriais; não prometer que URL Wix nativa ficará acessível após a mudança DNS.
5. Testar em URL *.pages.dev antes de apontar o domínio.
6. Segredos de administração permanecem no GitHub Actions, nunca no bundle.

## Publicações
O script scripts/wix_semantic_seo.py gera pesquisa e rascunhos quando
WIX_CREATE_DRAFT=true e credenciais estão presentes. Publicação direta
em produção depende de revisão editorial.
