# Auditoria HomeHost, SEO e editorial — 13/11/2026

## Decisão de origem

- Site institucional autorizado: HomeHost.
- DNS público observado: `arquindex.com.br` em `177.234.150.42`; `www` aponta para a raiz; NS autoritativos `ns31.servidorwebsite.com` e `ns32.servidorwebsite.com`.
- A zona Cloudflare conectada está em estado `moved` e ainda contém o CNAME antigo da raiz para `tevuusva.up.railway.app`; ela não é a delegação pública observada. Nenhum registro foi alterado.
- O PR 103 já foi incorporado à `master`, apesar de o texto operacional histórico ainda descrevê-lo como pendente.
- Railway `Arquindex Plataforma` permanece separado: serviço `arquindex-web`, branch configurada `railway-production-2026`, raiz `/arquindex-platform`; o estado Railway não foi usado como evidência de publicação no domínio institucional.

## Leitura pública

| Verificação | Resultado em 13/11/2026 |
|---|---|
| Homepage | HTTP 200, canonical próprio, H1 único, `main`, viewport e dois JSON-LD |
| `guarda_de_documentos.html` | HTTP 200, canonical próprio, sem `noindex`; sem elemento `main` |
| `gestao_de_colaboradores_documentos.html` | HTTP 200, canonical próprio, sem `noindex`; título repete `Arquindex`, sem `main` e sem JSON-LD |
| `digitalizacao.html` | HTTP 200, canonical próprio, `main`, viewport e JSON-LD |
| `digitalizacao-com-ocr.html` | HTTP 200, canonical próprio, `main`, viewport e JSON-LD |
| `robots.txt` | HTTP 200 |
| `sitemap.xml` | HTTP 200; índice com 16 filhos e 579 entradas declaradas |
| `sitemap-index.xml` | HTTP 404; não é o índice vigente |
| Rotas modernas `/solucoes/...` testadas | Três HTTP 404 |
| Campanha regional 24 × 3 | 72 HTTP 404 na HomeHost; nenhuma publicação comprovada |

Tempos observados pelo ponto de teste: homepage 4,70 s total, guarda 3,69 s, gestão de colaboradores 3,74 s, digitalização 4,37 s e OCR 3,84 s. São medições pontuais, não Core Web Vitals de usuários reais.

Os quatro recursos históricos continuam com HTTP 404:

- `/arquindex-favicon.png`
- `/img/about.webp`
- `/assets/img/about.webp`
- `/css/IE-fix.css`

HTTP foi redirecionado para HTTPS, mas os hosts HTTPS com e sem `www` continuam ambos em 200. Recomenda-se escolher o host canônico já usado nas páginas e implementar redirecionamento definitivo apenas após backup e confirmação da configuração HomeHost.

## Rastreamento

- Homepage, digitalização e OCR expõem `AW-17020939105` e `AW-17029507720`.
- Guarda documental e gestão de colaboradores não apresentaram identificador `AW-`, `G-` ou `GTM-` na leitura do HTML.
- Nenhuma alteração foi feita. Antes de adicionar rastreamento, é necessário confirmar consentimento, finalidade, disparo e eventos para evitar duplicação.

## GitHub, Railway e conexões

- GitHub: leitura funcionou, sem 401/403/429/5xx.
- `master` observada antes do lote: `283fef5aed27306c6f9fa30d80f91c608223d397`.
- PR editorial anterior 144 continua aberto em rascunho e não foi tratado como publicado.
- Railway: leitura autenticada funcionou. O ambiente de produção não apresentou alteração staged efetiva; os deploys recentes listados estavam removidos e não houve redeploy.
- GSC Wizard: conta e propriedade `sc-domain:arquindex.com.br` são legíveis, mas a propriedade aparece `activated:false`. As oito leituras analíticas obrigatórias retornaram `INVALID_ARGUMENT`. Não é 401, 403, 429 ou 5xx. A ação exata é selecionar/ativar essa propriedade no conector e repetir a leitura; reconectar a conta não é indicado enquanto a leitura de identidade e propriedades funciona.
- Top10 Arquindex: leitura inofensiva funcionou, mas o retorno não confirmou um canal FTPS HomeHost atual nem backup completo restaurado.

## Segurança de publicação HomeHost

Não houve escrita, exclusão, quarentena, limpeza ou alteração de layout. Os três pré-requisitos não foram comprovados em conjunto nesta execução:

1. raiz pública HomeHost confirmada por listagem;
2. backup completo fora de `public_html` com restauração isolada validada;
3. sessão FTPS com certificado TLS válido e permissão de escrita na raiz correta.

Resultado da limpeza: zero arquivos removidos, zero itens movidos e zero bytes liberados. O módulo semanal não é devido nesta sexta-feira.

## Campanha regional e páginas SEO

As 72 URLs do padrão `/seo/{servico}/{cidade}/empresa` retornaram 404. O manifesto deste lote registra cada URL como `PLANEJADA`, não elegível para publicação, com bloqueio por ausência de demanda diferenciada e risco de doorway/canibalização. Nenhuma foi incluída em sitemap ou submetida.

Meta diária de até dez páginas SEO:

| Estado | Quantidade |
|---|---:|
| PLANEJADA para criação no lote diário | 0 |
| CRIADA | 0 |
| TESTADA | 0 |
| PUBLICADA | 0 |
| SUBMETIDA | 0 |
| INDEXADA confirmada | 0 |

Motivo: política existing-first, GSC sem propriedade ativada no conector, inventário público já com 579 entradas e 72 rotas regionais inexistentes. Criar variações sem evidência de demanda aumentaria a canibalização e o risco de doorway pages.

## Dois artigos originais preparados

| Artigo | Palavras úteis | Estado |
|---|---:|---|
| Assentamento funcional digital: estrutura, metadados, acesso e documentos de saúde ocupacional | 2.363 | TESTADA; não publicada |
| Migração para Alfresco: lote-piloto, reconciliação, hashes e rollback | 2.523 | TESTADA; não publicada |

Validações locais: H1 único, H2/H3, resposta direta, etapas, riscos, tabelas, checklist, FAQ visível, dois JSON-LD válidos, canonical próprio, autoria, CTA, links internos e `noindex,follow`. Os arquivos ficam em `editorial/2026-11-13/`, fora da raiz pública, na branch isolada `editorial/2-artigos-20261113`.

Fontes oficiais utilizadas: CONARQ/e-ARQ Brasil, Lei nº 13.709/2018, Decreto nº 10.278/2020, ANPD, documentação oficial Hyland/Alfresco e NIST FIPS 180-4. A data de consulta registrada nos artigos é 13/11/2026.

## Blogger

- Feed público: 36 posts.
- Nenhuma correspondência exata para os oito títulos históricos pendentes.
- O último trio de títulos do feed começa por “Workflow documental: como o Alfresco atende”, “Por que contratar equipe de BPO de documentação” e “Avaliação De Documentos De Conselhos De Acordo Com Conarq”.
- Nenhum canal Blogger v3, Apps Script autenticado ou conector oficial com escrita estava disponível. Nenhum POST foi tentado; fila pendente: 8.

## Submissões e limites

- GSC: 0 URLs submetidas.
- IndexNow/Bing: 0 URLs enviadas.
- Indexação confirmada: nenhuma nova alegação.
- Merchant Center: mantido separado e não auditado.
- MIO/Bem Viver: não alterado.

## Próximos passos seguros

1. Ativar `sc-domain:arquindex.com.br` no GSC Wizard e repetir as leituras de desempenho, canibalização e indexação.
2. Concluir e testar restauração do backup HomeHost fora da raiz pública.
3. Confirmar raiz e listar via FTPS com TLS válido antes de qualquer publicação.
4. Corrigir primeiro os quatro recursos 404, o título duplicado, a semântica `main` e a lacuna de rastreamento, preservando URLs e layout.
5. Revisar e incorporar os PRs editoriais; publicar uma URL por vez, ler o conteúdo público, validar canonical/robots e somente então reconciliar sitemap e submissões.
6. Transformar as 72 intenções em páginas apenas quando houver demanda e conteúdo regional realmente distinto; caso contrário, consolidá-las em páginas existentes.
