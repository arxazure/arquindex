# Rede editorial regional e sitemap — 07/11/2026

## Páginas trabalhadas
- Hub: `seo-regional/gestao-documental-ecm-databooks/index.html`
- Betim, Contagem e Nova Lima: `seo-regional/gestao-documental-ecm-databooks/{cidade}/index.html`
- Guia técnico: `blog/montagem-de-databooks-de-engenharia/index.html`

## Arquitetura adotada
O hub apresenta os serviços e cidades; os guias locais fazem referência ao hub, ao guia técnico e a duas páginas relacionadas, explicando contexto documental, não uma cadeia automática de keywords. O manual de databooks aponta de volta ao hub e às três páginas locais. A marca, cores e estrutura CSS preexistentes foram preservadas. Essa rede editorial ajuda descoberta e navegação, mas não garante ganhos de ranking nem comprova a resolução das 78 páginas órfãs do Ahrefs.

## Sitemap
`seo-regional/gestao-documental-ecm-databooks/sitemap.xml` já listava as cinco URLs. Foram atualizadas apenas as cinco entradas `lastmod` para 2026-11-07. Total de 19 `loc` preservado; nenhuma URL duplicada foi adicionada.

## Validação offline
```bash
python3 scripts/validate_regional_links.py .
```
Verifica H1 único, canonical, links entre as cinco páginas e presença única no sitemap. Deve ser executado em checkout completo antes de merge/deploy.

## Bloqueio de publicação
O workflow `.github/workflows/publicar-databooks-homehost.yml` observa e seleciona **arquivos HTML** específicos; não contempla `seo-regional/gestao-documental-ecm-databooks/sitemap.xml` na seleção de arquivos. Portanto, um merge no branch principal **não comprova publicação do sitemap**. Não ampliar esse workflow automaticamente sem revisar backup, restauração, leitura pública e credenciais FTPS.

Próxima etapa autorizada de publicação deve:
1. Confirmar backup recuperável de HomeHost e os diretórios remotos reais, sem sobrescrever páginas restauradas por engano.
2. Validar o HTML publicado, todas as URLs e respectivos status HTTP/canonical.
3. Fazer upload seletivo do sitemap na rota pública correspondente **apenas após confirmar essa rota**, com backup/readback e validação XML.
4. Conferir `robots.txt`/índice de sitemaps e registro no Google Search Console/Bing Webmaster Tools. Não presumir que estar em um sitemap do repositório significa descoberta pelos buscadores.
5. Só então solicitar recrawl ou IndexNow das URLs verdadeiramente alteradas, mediante chave válida e controles existentes.

Nenhum deploy, merge, execução de Actions, alteração DNS ou submissão IndexNow foi feito nesta etapa.
