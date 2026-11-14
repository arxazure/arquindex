# Auditoria Arquindex — HomeHost, SEO técnico e editorial — 12/11/2026

## Resultado executivo

- A decisão operacional é HomeHost para `arquindex.com.br` e `www.arquindex.com.br`.
- A resolução DNS pública observada delega a zona a `ns31.servidorwebsite.com` e `ns32.servidorwebsite.com`; a raiz resolve para `177.234.150.42` e `www` é CNAME da raiz.
- A zona Cloudflare conectada está com status `moved`. Ela ainda contém CNAME não proxy da raiz para `tevuusva.up.railway.app`, mas essa zona não é a delegação pública observada. Nenhum registro foi alterado.
- Raiz e `www` responderam HTTPS 200; o cliente HTTP retornou `ssl_verify_result=0`. A homepage pública tem canonical próprio, `index,follow`, um H1, viewport e JSON-LD.
- As 72 URLs da campanha regional registrada (24 cidades × digitalização, guarda e consultoria LGPD) retornaram `404 Not Found` no domínio oficial. Nenhuma foi submetida ou incluída em sitemap.
- O serviço Railway `arquindex-web` permanece ligado ao repositório `arxazure/arquindex`, branch `railway-production-2026`, root `/arquindex-platform`, mas todos os serviços do ambiente de produção foram observados offline e sem deployment ativo; implantações recentes estão removidas. Isso não é evidência de publicação institucional.
- Foram preparados e testados dois artigos originais, com 2.054 e 2.189 palavras úteis. Estão em staging editorial com `noindex,follow`, sem publicação na HomeHost.

## 1. Origem e repositório

- Repositório: `arxazure/arquindex`.
- Base auditada: `master` em `326aaadb80df14e347a9811c5c52d48be84b52a9`.
- PR 103: incorporado; merge `269707b86875477d953eae3721a36b3a22f4d19a`.
- O aviso de retorno à HomeHost está, portanto, presente na linha principal atual; a nota antiga de PR pendente não representa mais o estado do GitHub.
- Último commit da base registra continuidade do inventário de 56 subdomínios e não comprova deploy no site institucional.

## 2. DNS, HTTP e TLS

| Verificação | Evidência observada | Classificação |
|---|---|---|
| Delegação pública | `ns31.servidorwebsite.com`, `ns32.servidorwebsite.com` | Compatível com retorno à hospedagem HomeHost/servidorwebsite |
| A da raiz | `177.234.150.42` | Não aponta ao host Railway informado anteriormente |
| `www` | CNAME para `arquindex.com.br` | Coerente com a raiz pública |
| Zona Cloudflare conectada | status `moved`; CNAME raiz antigo para Railway; `www` proxy para raiz | Registro stale em zona não autoritativa observada; não alterar sem decisão de DNS |
| `https://www.arquindex.com.br/` | HTTP 200, HTTP/2, 106.295 bytes, `Last-Modified: 08/11/2026 21:38:54 GMT` | Pública e legível |
| TLS | `ssl_verify_result=0` no cliente HTTP | Cadeia/nome aceitos pelo cliente desta execução |

Esta evidência sustenta que o conteúdo público atual não está sendo servido pelo deployment Railway auditado. Ela não autoriza alteração de nameservers, e-mail ou zona DNS.

## 3. Páginas prioritárias

| URL | Resultado | Canonical | Robots | H1 | Observação |
|---|---:|---|---|---:|---|
| `/` | 200 | próprio | `index,follow,max-image-preview:large` | 1 | 49 links internos únicos; sem imagem quebrada renderizada; sem overflow horizontal no viewport auditado |
| `/guarda_de_documentos.html` | 200 | próprio | indexável | 1 | Página legada preservada; JSON-LD visível no HTML |
| `/gestao_de_colaboradores_documentos.html` | 200 | próprio | indexável | 1 | Página legada preservada; título repete `Arquindex` e deve ser revisado com dados de busca antes de editar |
| `/digitalizacao.html` | 200 | próprio | indexável | 1 | Conteúdo atual e quatro blocos JSON-LD |
| `/digitalizacao-com-ocr.html` | 200 | próprio | indexável | 1 | Conteúdo atual e três blocos JSON-LD |
| `/solucoes/digitalizacao-documentos` | 404 | nenhum | nenhum | 1 da página de erro | Rota do app Railway não existe na origem HomeHost |
| `/solucoes/guarda-documental` | 404 | nenhum | nenhum | 1 da página de erro | Não usar como destino canônico no site atual |
| `/solucoes/consultoria-lgpd` | 404 | nenhum | nenhum | 1 da página de erro | Não usar como destino canônico no site atual |

Os recursos CSS e JavaScript internos observados na homepage carregaram sem imagem quebrada no DOM. O console apresentou apenas erros da extensão do navegador de auditoria, não erros atribuídos ao site. A homepage ainda mantém um link visível “Website corporativo no Railway”; a retirada ou reclassificação desse link deve ser feita na origem HomeHost após confirmação de backup e raiz, pois o Railway auditado está offline.

## 4. Robots e sitemaps

- `robots.txt`: acessível; permite rastreamento geral e bloqueia áreas privadas (`/admin`, `/painel`, `/api/`, `/portal/`, uploads e caminhos internos).
- `sitemap.xml`: acessível como índice de 16 sitemaps filhos.
- Todos os 16 sitemaps filhos renderizaram XML e somaram 579 elementos `loc`.
- `sitemap-index.xml`: 404; o índice oficial em uso é `sitemap.xml`.
- Não foi feita submissão. As páginas regionais 404 e as rotas modernas 404 não são elegíveis.

## 5. Campanha regional 24 × 3

Padrão auditado: `https://www.arquindex.com.br/seo/{servico}/{cidade}/empresa`.

| Serviço | URLs testadas | 200 | 404 | canonical |
|---|---:|---:|---:|---:|
| `digitalizacao-documentos` | 24 | 0 | 24 | 0 |
| `guarda-documental` | 24 | 0 | 24 | 0 |
| `consultoria-lgpd` | 24 | 0 | 24 | 0 |
| **Total** | **72** | **0** | **72** | **0** |

No Railway histórico, essas páginas tinham cerca de 392–428 palavras visíveis e alto grau de template. Mesmo que fossem copiadas, não deveriam ser publicadas como páginas locais sem diferenciação e evidência geográfica reais. Estado atual das 72 intenções: `PLANEJADA/PENDENTE_DE_RECONCILIACAO`, não publicada na origem oficial.

## 6. Railway — Arquindex Plataforma

- Projeto `f652d9de-5f85-404f-baec-a48d552d9163`, ambiente production `5ba32ff7-5386-4867-8250-2a87def0d9d4`.
- Serviço `arquindex-web` `57fb4cbc-213b-462c-9c66-920b4d620137`.
- Fonte configurada: `arxazure/arquindex`, branch `railway-production-2026`, root `/arquindex-platform`, health `/health`.
- Staged changes: nenhum conteúdo; existe patch antigo com `changes: []` desde 21/10/2026.
- Estado observado: `arquindex-web`, Postgres e `arquindex-ftp-maintenance` offline; nenhum deployment ativo.
- O deployment de sucesso anterior `b3c2ac34...` foi removido em 07/11/2026. Não houve redeploy.

## 7. Search Console, IndexNow e métricas

- Autenticação do GSC Wizard: funcional; conta `arquindex@gmail.com`, escopo `webmasters`, assinatura ativa até 30/11/2026.
- Propriedade `sc-domain:arquindex.com.br`: legível, mas não ativada no painel autorizado. Consultas por resumo e canibalização retornaram `INVALID_ARGUMENT` porque a propriedade não está selecionada.
- Classificação: não é 401, 403, 429 ou 5xx. Não pedir reconexão; o passo exato é ativar/selecionar `sc-domain:arquindex.com.br` no GSC Wizard, preservando a propriedade atualmente ativa.
- A central privada Top10 respondeu à leitura, mas o snapshot técnico/métrico exibido é histórico e não deve ser tratado como dado de 12/11/2026.
- Nenhum sitemap ou URL foi enviado ao GSC; nenhum IndexNow foi disparado; nenhuma indexação foi declarada.

## 8. Módulo de até 10 páginas SEO

- Planejadas: 0.
- Criadas: 0.
- Testadas: 0.
- Publicadas: 0.
- Submetidas: 0.
- Indexadas confirmadas: 0.

Motivo: existing-first e segurança editorial. Antes de criar novas URLs, é necessário reconciliar a origem HomeHost, as rotas 404, o inventário de 579 URLs de sitemap, a propriedade GSC e as páginas legadas que continuam 200. Publicar variações regionais agora aumentaria o risco de doorway pages, canibalização e referências a destinos inexistentes.

## 9. Dois artigos originais

| Artigo | Palavras úteis | Estado | Publicação |
|---|---:|---|---|
| PDF/A em Databooks de engenharia: perfis, validação e anexos | 2.054 | TESTADA | Não publicada |
| Matriz de acesso no Alfresco: grupos, herança e menor privilégio | 2.189 | TESTADA | Não publicada |

Ambos incluem resposta direta, etapas, requisitos, riscos, checklist, FAQ, autoria, fontes datadas, links internos, CTA, canonical planejado, Open Graph e JSON-LD coerente. Permanecem com `noindex,follow` em staging.

## 10. Blogger

- Blog público: `https://documentosdigitaislegislaoesistemas.blogspot.com/`.
- Feed público: 36 posts.
- Nenhum dos oito títulos exatos da fila histórica foi encontrado no feed.
- Não existe canal autorizado de escrita Blogger v3, Apps Script autenticado ou conector Blogger oficial nesta execução.
- Resultado: 0 publicações, nenhuma tentativa POST, fila preservada sem duplicação.

## 11. HomeHost e rotina semanal

Hoje não é o dia do módulo semanal. Além disso, não foi comprovado nesta execução um backup completo restaurável, raiz pública nem FTPS com certificado válido. Portanto:

- limpeza executada: não;
- arquivos removidos: 0;
- arquivos em quarentena: 0;
- espaço liberado: 0 bytes;
- escrita no HomeHost: não.

## Próximos passos exatos

1. Confirmar no HomeHost a raiz do domínio e obter evidência de backup completo com teste de restauração fora de `public_html`.
2. Fazer uma leitura FTPS inofensiva com validação TLS; somente depois mapear a fonte dos HTMLs, robots e sitemaps atuais.
3. Corrigir primeiro referências internas para rotas `/solucoes/...` 404 e reclassificar o link “Website corporativo no Railway”, preservando páginas legadas 200.
4. Selecionar `sc-domain:arquindex.com.br` no GSC Wizard e ler páginas/consultas antes de qualquer consolidação canônica.
5. Definir arquitetura das 72 intenções com evidência regional real; não copiar os templates curtos do Railway.
6. Publicar os artigos somente após backup, FTPS e leitura posterior de HTTP 200, canonical, robots, conteúdo e sitemap.

