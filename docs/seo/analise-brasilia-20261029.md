# Brasília: análise e implementação SEO — 29/10/2026

## Conclusão
Priorizar as páginas comerciais históricas `/digitalizacao.html` e `/montagem_databook_organizar.html`, preservando as URLs. Há evidência de conteúdo público nessas duas páginas, mas o e-mail Semrush **não identifica a URL classificada de cada consulta**. Não alegar que elas já ocupam as posições 22 e 29. A dispersão entre subdomínios é uma hipótese a investigar com URL classificada/canônica escolhida e comparação do conteúdo renderizado, não canibalização comprovada.

## Linha de base confirmada no e-mail
Relatório recebido às 19h56 de 28/10, horário de Brasília; período 21–28/10/2026; Google; Brasília/DF; português do Brasil. O campo de dispositivo não informa explicitamente mobile ou desktop. Conjunto completo de palavras-chave indisponível no resumo.

| Indicador | 28/10 | Nova observação em 29/10 |
|---|---:|---|
| Visibilidade arquindex.com.br | 10,50% | Sem novo relatório localizado |
| Visibilidade stoque.com.br | 20,33% | Sem novo relatório localizado |
| Diferença | 9,83 pontos percentuais | Não mensurável novamente |
| digitalização de documentos | 22 | Não medida novamente |
| databook | 29 | Não medida novamente |

O domínio no e-mail é **stoque.com.br**, não estoque.com.br. Arquivar não aparece no quadro resumido: não há base para quantificar sua vantagem. O e-mail mostra mudanças de posição de 78 e 71, respectivamente; isso não demonstra efeito dos PRs, que seguem em rascunho. Tráfego e volume do Semrush são estimativas, não cliques medidos ou leads.

Fonte: https://mail.google.com/mail/u/?authuser=arquindex%40gmail.com#all/1a184bab2f216713

## Prioridade de URLs e intenção
| Prioridade | URL | Papel e oportunidade | Ação implementada/preparada |
|---|---|---|---|
| 1 | https://www.arquindex.com.br/digitalizacao.html | Intenção comercial empresarial; conteúdo técnico já extenso, com foco atual em BH | Preparado título, descrição e bloco curto para contratação/logística em Brasília; sem substituir o conteúdo nacional por texto local |
| 1 | https://www.arquindex.com.br/montagem_databook_organizar.html | Intenção comercial de montagem; também precisa responder “o que é”, entregáveis, revisão e aceite | Preparado título sem telefones/repetição de marca, descrição, checklist de entrega e atendimento condicionado em Brasília |
| 2 | `/digitalizacao/local/brasilia-df` na aplicação Railway | Guia regional já existente, com corpo antes compartilhado com outras cidades | Implementado conteúdo específico de logística, restrição de retirada, lote-piloto, metadados, aceite e documentos de engenharia; links para páginas históricas |
| 2 | `/solucoes/databook` na aplicação Railway | Serviço já existente, sem necessidade de criar outra landing local | Implementada matriz didática de documentos, revisões, evidências e responsabilidades; ponte para as páginas históricas |
| Investigar | `/gestao-documental/brasil/centro-oeste/df/brasilia` | Página de réplica e escopo mais amplo; issue #69 relatou canonical circular | A branch atual já contém correção e testes dessa família; preservada, sem refazer o patch ou fechar a issue sem verificação pública |
| Não ampliar | `/databooks-engenharia/`, guias e subdomínios com `?post=` | Potencial sobreposição com serviço histórico; disponibilidade pública não confirmada nesta execução | Sem criação de URL, redirecionamento, exclusão, noindex ou canonical cruzado em massa |

A pesquisa pública conseguiu extrair `/digitalizacao.html` e a página histórica de Databook. Nesta execução os demais GETs falharam ou retornaram 503 pelo caminho de acesso disponível; isso **não basta para atribuir indisponibilidade à origem**. Não declarar HTTP 200, canonical do HTML bruto, indexação ou validação visual onde não houve leitura bem-sucedida. A extração de Databook informa rastreamento de três dias antes; requer revalidação direta antes de deploy.

## Conteúdo e autoridade editorial
Digitalização já explica OCR, PDF/A, metadados e descarte não automático; adicionar outro guia genérico extenso traria pouco valor. A lacuna comercial mais clara é a contratação de projeto em Brasília sem prometer filial, coleta ou prazo disponível.

Na extração pública de Databook há título excessivo com telefones e marca repetida, referências de contato antigas e parágrafos genéricos repetidos em “Benefícios Operacionais” e “Aplicações Práticas”. A limpeza desses trechos é prioritária após exportação autenticada do arquivo original e comparação de estrutura; não remover por regex sem identificar os limites. O patch proposto não altera telefones/ofertas/endereços antigos em massa. A sede e as alegadas unidades devem ser reconciliadas separadamente com informação comercial comprovada.

Novos blocos usam autoria institucional, exemplos claramente didáticos e limites de responsabilidade documental. Não foram criados depoimentos, métricas de clientes, certificados, filiais, preços ou promessas de validade jurídica. Não atribuir revisão a Marina ou a especialista sem revisão efetiva. Para autoridade externa, publicar casos autorizados e evidências originais é uma próxima iniciativa editorial, não um resultado deste patch.

## Cruzamento com PRs e origem de publicação
- PR #73: https://github.com/arxazure/arquindex/pull/73 — rascunho, base `master`. Contém gerador conservador de blocos e três páginas de staging; não modifica automaticamente páginas públicas. Reaproveitado o princípio de saída separada e rejeição de duplicação, sem inserir outro FAQ genérico.
- PR #79: https://github.com/arxazure/arquindex/pull/79 — rascunho, base `railway-production-2026`. O título cita quatro guias originais (TCO ECM, Decreto/metadados, BPO DP e guarda híbrida), mas a lista atual já tem **24 arquivos, incluindo 18 guias**. Isso exige nova revisão do escopo; não mesclar o pacote inteiro como se contivesse somente os quatro materiais iniciais. O guia Decreto/metadados sobrepõe conteúdo já presente em digitalização: selecionar material complementar e vincular após publicação validada, sem duplicar o texto no serviço. TCO e BPO têm intenção de apoio, não substituem a landing comercial de Databook. Posts/press-release preparados não comprovam publicação nem links externos obtidos.
- `master/index.html` é “Se-joga”, diferente da home pública. `/digitalizacao.html` e `/montagem_databook_organizar.html` não estão nessa raiz versionada. Não sobrescrever a HomeHost com o checkout inteiro.
- Railway confirmado via API: projeto `Arquindex Plataforma`, serviço `arquindex-web`, branch `railway-production-2026`, root `/arquindex-platform`, início `npm start`, último deployment consultado `c5a6696a-071c-4622-84c5-2d862382b840`, estado SUCCESS. O único domínio listado é `arquindex-web-production.up.railway.app`; não há domínio personalizado anexado. Portanto, publicar no Railway não equivale a publicar em `www.arquindex.com.br`.

## Links, canonical e dados estruturados
Preservadas as rotas, canonical e redirecionamentos existentes. O guia Brasília inclui links contextuais para digitalização e Databook históricos e para o orçamento regional existente; o bloco de serviço Databook leva ao serviço histórico de digitalização. Não se adicionou ligação em rodapé repetida em centenas de páginas.

O guia regional agora descreve `WebPage` e `Service`, com URL no mesmo origin usado pela canonical e autoria institucional. Não cria `LocalBusiness` ou endereço em Brasília, avaliações, preços, certificações ou FAQ estruturado novo. A página de serviço mantém seu schema existente. Os patches HomeHost preservam schema original até que ele possa ser inspecionado no export: não há validação sintática ou de elegibilidade real desse schema em produção nesta execução.

A orientação do Google é alinhar canonical, links e sitemap; canonical é sinal, não confirmação da versão escolhida pelo buscador. Não consolidar os subdomínios sem comparar texto efetivamente renderizado e o parâmetro `post`: ele pode selecionar um artigo real, não apenas rastreamento. Conteúdo Soro incorporado pode exigir JavaScript e rolagem conforme o registro versionado de 18/10.

Referência oficial consultada: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls

## Backup e publicação
Execução inspecionada: https://github.com/arxazure/arquindex/actions/runs/40789699871 — job `123171554225`. Embora verde, o passo real terminou com `BACKUP_PARTIAL_RESUME_REQUIRED`, estado `in_progress`, checkpoint 67, 16.500 arquivos, 282.538.669 bytes. Não há `BACKUP_COMPLETE_VERIFIED` nem evidência de restauração isolada nesse job. **HomeHost permanece sem liberação de publicação.** Não se iniciou outra cópia nem se retomou uma sessão sem conferir eventual execução concorrente/checkpoint mais recente.

Para liberar HomeHost: concluir e verificar backup integral; restaurar em área isolada e comparar inventário/tamanhos/hashes; reconciliar a origem na janela de publicação. Depois exportar os dois arquivos via FTPS autenticado, registrar SHA-256 e gerar cópias com `scripts/prepare-brasilia-homehost.py`. O gerador exige canonical própria, um H1, title/description únicos, âncora única dentro do body e ausência do bloco. Rejeita hash divergente, encoding inválido, fonte já modificada e saída sobre a origem. HTML legado sem `main` exige uma âncora editorial explícita e revisada. Não altera robots, sitemap ou scripts de medição.

Validar o diff do export real, renderizar desktop/mobile, testar navegação, formulário/WhatsApp e schemas. Publicar apenas arquivos aprovados, com conferência da versão concorrente, readback e comparação pública. Reverter aos bytes originais do backup se falhar. Não disparar workflows antigos que enviem sem a condição de backup.

Para Railway: testes locais aprovados não são comprovação pública; manter o PR em rascunho até revalidar o host real e revisar o conteúdo. Não mudar DNS nem apontar domínio para essa aplicação como parte deste trabalho.

## Validação executada
- `node --check arquindex-platform/server.js`.
- 13 testes Node aprovados: duas rotas reais locais, schema JSON, URL canonical, H1 único, matriz didática, preservação de 500 rotas da réplica, sitemap e redirecionamentos existentes.
- 3 testes Python aprovados: patch mínimo, preservação de scripts/URLs/H1/canonical, rejeição de alterações concorrentes e duplicação e controle de âncora/encoding.
- As fontes da réplica nos testes são sintéticas; não confundir com teste de produção. Patches HomeHost foram testados em fixtures, não aplicados aos bytes reais. Não houve revisão visual em navegador nem teste Rich Results público.

## Comparação posterior
Estado nesta rodada: código e staging implementados/testados; publicação efetiva não realizada; indexação não confirmada; ganho de posição não medido. Nenhum desses campos deve ser preenchido automaticamente a partir de CI verde.

Depois do deploy validado, registrar data, commit, URL, hash público e cache. Em +7, +14 e +28 dias contar desde a publicação, comparar as mesmas duas consultas no mesmo projeto Semrush, localização, dispositivo e conjunto de palavras-chave. A diferença de posição é `22 − nova_posição` e `29 − nova_posição`; visibilidade é medida em pontos percentuais contra 10,50%. Se o conjunto/dispositivo mudar, iniciar uma série distinta. Isso é protocolo de acompanhamento, não automação agendada criada nesta rodada.

Confirmar indexação e canonical escolhida com URL Inspection do GSC, com data de leitura. Acompanhar impressões, cliques, CTR e leads nas URLs publicadas; GSC por país não equivale ao recorte municipal de Brasília. Aceite IndexNow e inclusão no sitemap são descoberta, não indexação. Sem nova medição, o resultado é “não medido”, não “posição mantida”. Variações após publicar não demonstram causalidade isolada: registrar concorrência, sazonalidade e alterações paralelas.

## Continuação em 30/10/2026

PR de implementação: https://github.com/arxazure/arquindex/pull/83. A atualização da branch `railway-production-2026` para `992128baf85484bf7b671b01662d03611cdf2e75` foi integrada sem conflitos; as mudanças paralelas de LGPD foram preservadas.

Backup mais recente localizado e lido nesta continuação: https://github.com/arxazure/arquindex/actions/runs/40975208048, job `123801438792`. O passo de backup real terminou às 21h28 de 29/10, horário de Brasília, com `BACKUP_PARTIAL_RESUME_REQUIRED`: checkpoint 87, 21.500 arquivos, 325.946.854 bytes, `state: in_progress`. O checkpoint de dois arquivos que aparece no início do log pertence aos testes sintéticos e não foi usado para avaliar a cópia real. Continua sem comprovação de backup integral ou restauração isolada. Nenhuma publicação foi realizada.

A busca por e-mails posteriores de acompanhamento Semrush retornou somente o relatório de 28/10; não há nova posição observada nesta continuação. A linha de base permanece histórica, sem alegação de manutenção ou ganho de ranking.


## Inspeção real de indexação — 30/10/2026, aproximadamente 01h26 BRT

Acesso GSC Wizard confirmado ativo, com escopo Google webmasters de escrita. Evidência completa em `docs/seo/indexacao-e-dns-20261030.json`; incidente registrado em https://github.com/arxazure/arquindex/issues/84.

O Google URL Inspection confirmou quatro URLs já indexadas e com canonical própria: digitalizacao.html, montagem_databook_organizar.html, guarda_de_documentos.html e digitalizacao-com-ocr.html. Isso atualiza a ausência de comprovação registrada nas rodadas anteriores; não é ganho novo atribuído a este PR. O guia blog/montagem-de-databooks-de-engenharia/ consta como descoberto e ainda não indexado. Os dois artigos técnicos de 26/27 de outubro e onde-digitalizar-documentos.html constam como desconhecidos pelo Google. Publicação efetiva dos quatro destinos ainda precisa ser verificada antes de submeter.

Falha ao vivo confirmada por Google DNS-over-HTTPS e Cloudflare DNS-over-HTTPS: SERVFAIL, servidores autoritativos inacessíveis. O Registro.br informa ns29.servidorwebsite.net e ns30.servidorwebsite.net; o Google menciona ausência de resposta de 177.234.150.42 e 177.234.150.43. A zona não foi encontrada na conta Cloudflare conectada. A correção depende do provedor autoritativo/registrador, sem trocar nameservers ou endereços às cegas. Os campos de HTML vazios na auditoria são consequência da falha de leitura, não prova de ausência de metadados.

O sitemap principal registra um erro e já havia sido reenviado em 30/10 às 00h59 BRT; a causa específica ainda não foi extraída. Não foi feita outra submissão enquanto o DNS está falhando. IndexNow e Bing Webmaster API não configurados no GSC Wizard; não se gerou chave nova, pois há uma rotina independente no GitHub e é necessário verificar a chave já publicada quando a resolução voltar.

As oito URLs foram adicionadas ao Indexing Tracker: cinco novas e três já acompanhadas. Nenhuma publicação, submissão nova, ganho de indexação ou de ranking foi afirmado nesta rodada. Próxima condição técnica: DNS NOERROR em dois resolvedores, GET público 200, robots/canonical conferidos e sitemaps válidos; depois solicitar descoberta das URLs efetivamente publicadas.
