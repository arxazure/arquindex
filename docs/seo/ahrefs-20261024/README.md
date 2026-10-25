# Ahrefs de 24/10/2026 — investigação e correções preparadas

Verificações em 25/10/2026 (horários UTC em cada linha de evidência). Amostra dirigida por páginas comerciais, frequência dos links internos, páginas secundárias e sitemaps; não é um novo rastreamento integral do Ahrefs.

## Resultado e limites

- 182 URLs distintas consultadas por GET: na primeira sequência consolidada, 153 responderam 200 e 29 responderam 404. Foram analisados 109 HTMLs, o índice principal, 20 sitemaps de URLs e sete robots.txt. Os resultados e a associação com links/sitemaps estão em `http-evidence.json`.
- Nove páginas 200 com canonical malformada para destino 404 confirmadas. Quatro HTMLs corrigidos em área de preparação no repositório; cinco regras exatas de correção documentadas. Nenhuma publicação nova na HomeHost.
- Treze destinos de links internos responderam 404: 12 páginas secundárias em três subdomínios e `/LGPDEDOC-POD/` (este último recebe links de 11 páginas da amostra). Não há evidência suficiente para extinguir essas URLs ou escolher substitutos equivalentes.
- Quatro assets históricos continuam 404. A leitura adicional de `/digitalizacao-com-ocr.html` encontrou referências a `arquindex-favicon.png` e `img/about.webp`; `/gestao_de_colaboradores_documentos.html` não referenciou os quatro caminhos antigos. Três outras leituras de referência retornaram 503 e ficaram inconclusivas.
- As três correções antigas ARQ-107/110/111 foram revalidadas: 200 e canonical própria. São correções anteriores; não contar como novas resoluções desta tarefa.
- Em releituras posteriores, cinco páginas com canonical defeituosa e três páginas prioritárias retornaram 503. O cliente de verificação não identificou se o 503 veio da origem ou de uma camada intermediária. Não converter essas falhas em diagnóstico de exclusão permanente.
- Sete robots.txt e todos os sitemaps consultados responderam 200 na sequência inicial. Isso não explica nem refuta as sete ocorrências históricas do Ahrefs, que podem envolver outros hosts/horários.
- O e-mail fornece totais e links para o projeto 8395918, crawl `24-10-2026T202249`, mas não a lista das 542 URLs. O acesso ao Ahrefs encontrou uma verificação de segurança. A correspondência exata com as 542 ocorrências requer acesso ao relatório ou exportação CSV.
- Os 29 resultados 404 da amostra se decompõem em nove destinos de canonicals atuais, três destinos de canonicals históricas já corrigidas, 13 destinos de links internos e quatro assets. Não somar essas categorias aos totais do Ahrefs como se fossem novos itens independentes.

## Canônicas confirmadamente incorretas

A causa observada é a composição de uma URL com `https://www.arquindex.com.br/` seguida pelo nome de outro host como pasta. Isso é compatível com confusão entre caminho de publicação e URL pública. O gerador original desse padrão não foi localizado na branch master; não atribuir o defeito a um script específico sem evidência.

| Página 200 | Canonical atual com destino 404 | Correção proposta | Preparação |
|---|---|---|---|
| https://consultoria-ocr-vantagens.arquindex.com.br/cidade.html | https://www.arquindex.com.br/consultoria-ocr-vantagens.arquindex.com.br/cidade.html | https://consultoria-ocr-vantagens.arquindex.com.br/cidade.html | HTML corrigido |
| https://consultoria-ocr-vantagens.arquindex.com.br/custo.html | https://www.arquindex.com.br/consultoria-ocr-vantagens.arquindex.com.br/custo.html | https://consultoria-ocr-vantagens.arquindex.com.br/custo.html | HTML corrigido |
| https://empresas-adequacao-lgpd-paulo.arquindex.com.br/artigo-principal.html | https://www.arquindex.com.br/empresas-adequacao-lgpd-paulo.arquindex.com.br/artigo-principal.html | https://empresas-adequacao-lgpd-paulo.arquindex.com.br/artigo-principal.html | HTML corrigido |
| https://empresas-adequacao-lgpd-paulo.arquindex.com.br/auditoria.html | https://www.arquindex.com.br/empresas-adequacao-lgpd-paulo.arquindex.com.br/auditoria.html | https://empresas-adequacao-lgpd-paulo.arquindex.com.br/auditoria.html | HTML corrigido |
| https://empresas-adequacao-lgpd-paulo.arquindex.com.br/como-escolher.html | https://www.arquindex.com.br/empresas-adequacao-lgpd-paulo.arquindex.com.br/como-escolher.html | https://empresas-adequacao-lgpd-paulo.arquindex.com.br/como-escolher.html | Regra pronta; releitura 503 |
| https://empresas-adequacao-lgpd-paulo.arquindex.com.br/comparativo.html | https://www.arquindex.com.br/empresas-adequacao-lgpd-paulo.arquindex.com.br/comparativo.html | https://empresas-adequacao-lgpd-paulo.arquindex.com.br/comparativo.html | Regra pronta; releitura 503 |
| https://digitalizar-arquivos-corporativo.arquindex.com.br/cidade.html | https://www.arquindex.com.br/digitalizar-arquivos-corporativo.arquindex.com.br/cidade.html | https://digitalizar-arquivos-corporativo.arquindex.com.br/cidade.html | Regra pronta; releitura 503 |
| https://digitalizar-arquivos-custo.arquindex.com.br/cidade.html | https://www.arquindex.com.br/digitalizar-arquivos-custo.arquindex.com.br/cidade.html | https://digitalizar-arquivos-custo.arquindex.com.br/cidade.html | Regra pronta; releitura 503 |
| https://gestao-digitalizacao-preco.arquindex.com.br/cidade.html | https://www.arquindex.com.br/gestao-digitalizacao-preco.arquindex.com.br/cidade.html | https://gestao-digitalizacao-preco.arquindex.com.br/cidade.html | Regra pronta; releitura 503 |

## Links internos com destino 404

| Destino | Páginas de origem na amostra |
|---|---|
| https://arquindex.com.br/LGPDEDOC-POD/ | https://digitalizar-arquivos-corporativo.arquindex.com.br/<br>https://digitalizar-arquivos-custo.arquindex.com.br/<br>https://gestao-digitalizacao-preco.arquindex.com.br/<br>https://digitalizar-acervos-empresas.arquindex.com.br/<br>https://digitalizar-arquivos-empresas.arquindex.com.br/<br>https://digitalizar-arquivos-especializada.arquindex.com.br/<br>https://digitalizar-arquivos-mg.arquindex.com.br/<br>https://digitalizar-arquivos-preco.arquindex.com.br/<br>https://consultoria-ocr-vantagens.arquindex.com.br/<br>https://consultoria-ocr-vantagens.arquindex.com.br/index.html<br>https://empresas-adequacao-lgpd-paulo.arquindex.com.br/ |
| https://digitalizar-arquivos-corporativo.arquindex.com.br/adequacao-lgpd-para-empresas.html | https://digitalizar-arquivos-corporativo.arquindex.com.br/ |
| https://digitalizar-arquivos-corporativo.arquindex.com.br/avaliacao-de-arquivos-para-digitalizacao.html | https://digitalizar-arquivos-corporativo.arquindex.com.br/ |
| https://digitalizar-arquivos-corporativo.arquindex.com.br/blog.html | https://digitalizar-arquivos-corporativo.arquindex.com.br/ |
| https://digitalizar-arquivos-corporativo.arquindex.com.br/controles-da-informacao-adequacao-lgpd.html | https://digitalizar-arquivos-corporativo.arquindex.com.br/ |
| https://digitalizar-arquivos-custo.arquindex.com.br/adequacao-lgpd-para-empresas.html | https://digitalizar-arquivos-custo.arquindex.com.br/ |
| https://digitalizar-arquivos-custo.arquindex.com.br/avaliacao-de-arquivos-para-digitalizacao.html | https://digitalizar-arquivos-custo.arquindex.com.br/ |
| https://digitalizar-arquivos-custo.arquindex.com.br/blog.html | https://digitalizar-arquivos-custo.arquindex.com.br/ |
| https://digitalizar-arquivos-custo.arquindex.com.br/controles-da-informacao-adequacao-lgpd.html | https://digitalizar-arquivos-custo.arquindex.com.br/ |
| https://gestao-digitalizacao-preco.arquindex.com.br/adequacao-lgpd-para-empresas.html | https://gestao-digitalizacao-preco.arquindex.com.br/ |
| https://gestao-digitalizacao-preco.arquindex.com.br/avaliacao-de-arquivos-para-digitalizacao.html | https://gestao-digitalizacao-preco.arquindex.com.br/ |
| https://gestao-digitalizacao-preco.arquindex.com.br/blog.html | https://gestao-digitalizacao-preco.arquindex.com.br/ |
| https://gestao-digitalizacao-preco.arquindex.com.br/controles-da-informacao-adequacao-lgpd.html | https://gestao-digitalizacao-preco.arquindex.com.br/ |

## Sitemaps, arquivos e publicação

A branch master examinada foi `0627515e707af4a7387c34693f1109edb89219c6`. Dos 146 HTMLs versionados, 125 tinham canonical e nenhum apresentava múltiplas canonicals ou o padrão de host inserido em pasta. As nove fontes afetadas não estavam versionadas nessa branch: as quatro cópias corrigidas foram obtidas por HTTP e preservam os demais bytes, inclusive finais de linha. O manifesto contém SHA-256 do original, URL, canonical anterior/nova e caminho FTP candidato. O caminho FTP ainda exige confirmação por igualdade de hash antes de qualquer escrita.

O índice principal publicou 14 sitemaps filhos válidos, com 538 entradas de páginas. A amostra também consultou seis sitemaps de subdomínios. Cinco dos seis sitemaps de subdomínios contêm 40 entradas `<loc>` relativas (como `/cidade.html`), incluindo as nove páginas com canonical defeituosa. Essas entradas precisam ser absolutas. As duas rodadas anteriores apenas acrescentaram uma URL absoluta e preservaram as entradas relativas antigas; por isso a checagem de presença de uma URL não detectou o problema completo. As cinco regras de normalização estão em `sitemap-rules.json`; precisam de fonte fresca e validação dos destinos antes da publicação. Fonte oficial: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap?hl=pt-BR

`scripts/prepare_ahrefs_canonical_patch.py` prepara arquivos somente em diretório local separado, exige igualdade do SHA-256 original e exatamente uma canonical correspondente, e não faz FTP nem publicação. Os testes verificam preservação de conteúdo e CRLF, recusa de fonte alterada e recusa de canonicals múltiplas. As quatro cópias de HTML preparadas têm a mesma transformação verificada.

## Backup e reversão

A issue #28 exige backup integral fora de `public_html`, com leitura completa e SHA-256 verificado. As execuções identificadas `40084543361` e `40053631810` foram canceladas. O log da primeira terminou durante a leitura dos arquivos; não apresentou o resultado final de backup validado. Backups pontuais das rodadas SEO não substituem essa condição. Não há comprovação suficiente para liberar a escrita na hospedagem nesta tarefa.

Antes de publicar: concluir e validar o backup integral; obter snapshot fresco de cada fonte; confirmar virtual host e caminho FTP por hash; reaplicar somente a troca de canonical; guardar originais por arquivo fora da raiz pública; publicar um pequeno lote; verificar GET 200, canonical única e destino 200; restaurar os originais se houver divergência. Não mover URLs nem descartar conteúdo. A presença desta pasta no GitHub não publica os arquivos na hospedagem.

## Redirecionamentos e alertas não confirmados

`http://www.arquindex.com.br/loja/` chegou a `https://www.arquindex.com.br/servicos/` com 200; a falha de transporte relatada anteriormente não foi reproduzida. Variantes `/index.html`, host sem www e barra final foram registradas como divergências de normalização, não como canonicals quebradas, pois os destinos consultados responderam 200. O status de cada salto não foi capturado nesta amostra, portanto não se afirma a correção de todas as cadeias.

## Contagem de resolução

- Novos defeitos publicados e comprovadamente resolvidos nesta tarefa: **0**.
- Correções anteriores revalidadas: **3** (ARQ-107, ARQ-110 e ARQ-111).
- Novas correções preparadas: **9 regras**, sendo **4 HTMLs completos** e **5 dependentes de nova captura após 503**.
- Recuperação de indexação: **não avaliada/comprovada**. Não foi iniciado novo rastreamento no Ahrefs nem submetida URL à indexação.

## Evidências anteriores

- E-mail: https://mail.google.com/mail/u/?authuser=arquindex%40gmail.com#all/1a16f94a9526ecdc
- Auditoria ARQ: https://github.com/arxazure/arquindex/actions/runs/40117311596
- Publicação anterior: https://github.com/arxazure/arquindex/actions/runs/40117507928
- Validação anterior: https://github.com/arxazure/arquindex/actions/runs/40117728870
- Backup cancelado: https://github.com/arxazure/arquindex/actions/runs/40084543361
- Condição do backup: https://github.com/arxazure/arquindex/issues/28
