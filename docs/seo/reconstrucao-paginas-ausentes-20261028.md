# Reconstrução conservadora de páginas ausentes — Arquindex

Data: 2026-10-28. Preparação sem bloqueio pelo backup, sem sobrescrita da produção.

## Inventário inicial de páginas já reconstruídas em staging

| ID | Host pretendido | Fonte reconstruída |
|---|---|---|
| ARQ-119 | contratar-digitalizacao-documentos-armazenamento-nuvem.arquindex.com.br | staging/seo/paginas-pilares-20261028/contratar-digitalizacao-documentos-armazenamento-nuvem/index.html |
| ARQ-120 | compliance-digitalizacao-preco.arquindex.com.br | staging/seo/paginas-pilares-20261028/compliance-digitalizacao-preco/index.html |
| ARQ-123 | mapeamento-juridico.arquindex.com.br | staging/seo/paginas-pilares-20261028/mapeamento-juridico/index.html |

## Critérios para reconstruir outras páginas

1. Obter lista real de hosts e document roots pela configuração HomeHost/GitHub; não presumir que um subdomínio é vazio porque não aparece no Google.
2. Consultar HTTP/HTTPS, redirects, canonical, robots, H1, title, conteúdo e sitemap de cada host; guardar evidências.
3. Se o destino não existe comprovadamente, criar **somente** a pasta nova com index.html, robots.txt e sitemap.xml específicos; nunca usar comando de sincronização com exclusão.
4. Se o destino existe, registrar o HTML atual e comparar com staging; não sobrescrever sem cópia recuperável daquele arquivo.
5. Usar canonicals absolutos do host final, um H1, um title, dados estruturados consistentes e links contextuais válidos.
6. Não inserir automaticamente URLs no sitemap principal antes de confirmar HTTP 200 no host final.
7. Não solicitar IndexNow nem declarar indexação sem a verificação de produção.

## Bloqueios atuais

- O inventário completo de páginas ausentes não está confirmado.
- A autenticação HomeHost por navegador ainda não foi comprovada.
- As páginas ARQ-120 e ARQ-123 contêm repetições editoriais a revisar.
- Não há evidência de que o logo e as URLs institucionais usadas nos templates respondem 200.
- A condição de backup integral continua pendente para sobrescritas e deploys destrutivos; **não impede reconstrução de arquivos novos em staging**.

## Próxima verificação

Cruzar os sitemaps efetivamente servidos e a lista de subdomínios HomeHost com os diretórios GitHub, gerar uma matriz `host / HTTP / canonical / arquivo existente / ação` e publicar apenas novos caminhos após preflight individual.
