# Rodada SEO/GEO/AEO — 30/10/2026, manhã

## Escopo e limites

Foram auditadas seis fichas, ARQ-179 a ARQ-184. Uma melhoria substancial foi preparada para ARQ-172 por ser o problema técnico/editorial de maior prioridade já confirmado, mas a publicação foi interrompida antes de qualquer escrita porque o arquivo de origem não foi localizado no HomeHost autorizado. Nenhuma página, sitemap ou rede social foi alterada nesta rodada.

A referência ARQ-099 foi preservada e não foi republicada.

## Auditoria ARQ-179 a ARQ-184

Evidência: [workflow 41050386591](https://github.com/arxazure/arquindex/actions/runs/41050386591), job 124044675834, conclusão `success`.

| ID | URL | DNS | Resultado |
|---|---|---|---|
| ARQ-179 | https://dpo-terceirizado-funciona-brasil.arquindex.com.br/ | ENOTFOUND | Sem DNS público; SSL, HTTP, canonical, title/H1, conteúdo, mobile, robots e sitemap não puderam ser validados. |
| ARQ-180 | https://dpo.arquindex.com.br/ | ENOTFOUND | Mesmo bloqueio; não confundir com as páginas comerciais DPO já existentes no domínio principal. |
| ARQ-181 | https://ecm.arquindex.com.br/ | ENOTFOUND | Sem publicação verificável; precisa ser diferenciado de GED e Alfresco antes de eventual reconstrução. |
| ARQ-182 | https://empresadedigitalizacaodedocumentos.arquindex.com.br/ | ENOTFOUND | Sem publicação verificável; não criar nova página genérica sobreposta às pilares. |
| ARQ-183 | https://empresas-brasil-digitalizacao-documental-garantia-confidenciali.arquindex.com.br/ | ENOTFOUND | Sem publicação verificável; alegações de confidencialidade exigem controles comprováveis. |
| ARQ-184 | https://empresas-brasil-digitalizacao-documental-garantia-confidenciali.arquindex.com.br/comparativo.html | ENOTFOUND no host | Caminho não verificável; não publicar comparativo ou ranking sem dados documentados. |

Conclusão: são itens de inventário/ativação, não páginas publicadas. Reconstrução sem aguardar o backup integral continua autorizada quando a origem e o destino existirem, mas DNS e mapeamento do host precisam vir antes para que a publicação possa ser comprovada.

## ARQ-172 — tentativa controlada

URL: https://digitalizaca.arquindex.com.br/

Melhoria preparada:

- remoção da alegação superlativa não comprovada;
- intenção distinta: checklist para orçamento de digitalização;
- title, description e H1 textuais;
- resposta direta AEO, checklist, tabela de escopo e links para as páginas pilares;
- identidade Arquindex e CTA WhatsApp;
- criação de robots somente se ausente;
- backup individual, verificação pública e rollback previstos.

A rota FTPS pelo IP `177.234.150.42`, com certificado de `h59.servidorhh.com`, foi revalidada a partir do diagnóstico [41043086935](https://github.com/arxazure/arquindex/actions/runs/41043086935). A execução final [41050921350](https://github.com/arxazure/arquindex/actions/runs/41050921350) autenticou no FTPS, porém terminou com `TARGET_NOT_FOUND digitalizaca.arquindex.com.br/index.html`. O erro ocorreu antes do backup e antes de qualquer escrita. Não houve publicação nem rollback necessário; o estado público anterior foi preservado.

Commits principais: script preparado `02c6f9fd3927ff4ec004f1a532684caebf8d7a57`; publicador corrigido `821aacc3610be05ef909c5607f7b6997429738c3`; workflow final `bd154f782aff532aebf854113a12c79635ccef96`.

## Search Console — períodos completos

Propriedade: `sc-domain:arquindex.com.br`.

Comparação: 13–19/10/2026 versus 20–26/10/2026.

Totais agregados por consulta: 4 cliques / 785 impressões para 5 cliques / 1.168 impressões. Totais agregados por página: 30 cliques / 2.767 impressões para 36 cliques / 4.880 impressões. A diferença entre agregações por consulta e página é esperada em relatórios do Search Console e não deve ser tratada como erro de soma.

Sinais prioritários:

| Consulta/URL | 13–19/10 | 20–26/10 | Leitura |
|---|---:|---:|---|
| `digitalização de documentos` | 1 clique, 10 imp., CTR 10%, posição 2,20 | 0 clique, 68 imp., CTR 0%, posição 28,06 | Perda relevante; investigar distribuição entre URLs antes de trocar title. |
| `serviço de digitalização de documentos` | 1/26, CTR 3,85%, pos. 42,54 | 0/34, CTR 0%, pos. 31,71 | Mais visibilidade e posição melhor, ainda sem clique. |
| `guarda de documentos` | 0/19, pos. 31,00 | 0/7, pos. 53,29 | Queda de impressões e posição. |
| `consultoria lgpd` | 0/40, pos. 43,25 | 0/29, pos. 60,03 | Queda, mas amostra sem cliques. |
| `guarda de documentos belo horizonte` | 0/13, pos. 4,31 | 0/10, pos. 24,20 | Prioridade local; não atribuir causa sem análise URL+consulta. |
| /digitalizacao.html | 2 cliques/75 imp., CTR 2,67%, pos. 4,55 | 1/60, CTR 1,67%, pos. 8,70 | Perda moderada; preservar title recente até diagnóstico de canibalização. |
| /guarda_de_documentos.html | 0/136, pos. 13,47 | 0/115, pos. 8,70 | Posição melhorou, mas não houve clique; oportunidade de CTR e links internos. |
| /digitalizacao-com-ocr.html | 1/15, pos. 8,07 | 0/8, pos. 11,75 | Amostra pequena; monitorar e apoiar com links contextuais. |

Esses números são desempenho observado, não prova de indexação nova, causa ou lead.

## Descoberta, submissões e backup

- Nenhuma URL nova foi publicada; sitemaps não foram alterados.
- Não houve submissão ao Google Search Console, Bing Webmaster ou IndexNow.
- A chave IndexNow continua vazia nos workflows observados; nenhum sucesso foi alegado.
- Último checkpoint integral conhecido: `/seo-backups/resumable/20261026T115321Z-4df745d1d388/checkpoint-000087-841baf891892.json`, SHA-256 `b95074a91f1ab7eaac25d0b2c0e098e9d04a38ef34f89a6786486574cad7c282`, 21.500 arquivos e 325.946.854 bytes de origem, ainda `in_progress`. A ausência do backup terminal não foi usada para adiar reconstruções elegíveis; nesta rodada, os bloqueios foram DNS/mapeamento real.

## Registro persistente

A fila foi atualizada com ARQ-179 a ARQ-184 e com o bloqueio atual de ARQ-172 no commit `355f3cf72881c4958a9e43db87c1daa37e4e9e70`.

Não houve artigo/notícia artificial nem divulgação social. ARQ-007 e ARQ-099 permaneceram sem republicação.

## Próximas três prioridades

1. Provisionar/confirmar DNS e origem autorizada de ARQ-179 a ARQ-184; depois reconstruir somente páginas com papel editorial distinto.
2. Localizar o mapeamento real de `digitalizaca.arquindex.com.br` e reaplicar o publicador ARQ-172 com backup individual, sem gravar em raiz presumida.
3. Cruzar consulta+URL no Search Console para `digitalização de documentos` e `guarda de documentos belo horizonte`; priorizar links internos e snippet antes de nova troca de title.
