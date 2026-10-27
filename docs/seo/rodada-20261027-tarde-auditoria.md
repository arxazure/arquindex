# Rodada SEO/GEO/AEO — tarde de 27/10/2026

## Resultado executivo

A rodada auditou ARQ-131 a ARQ-136, atualizou a fila persistente e iniciou a continuação exata do backup HomeHost a partir do checkpoint 34. Nenhum arquivo público foi alterado.

## Backup HomeHost

O workflow [40498052939](https://github.com/arxazure/arquindex/actions/runs/40498052939) terminou com sucesso operacional, porém com o marcador `BACKUP_PARTIAL_RESUME_REQUIRED`.

Último checkpoint confirmado:

- caminho: `/seo-backups/resumable/20261026T115321Z-4df745d1d388/checkpoint-000034-4458a0fd04e6.json`
- SHA-256: `b5ab46352f0994c9af32d4b12f35ba3f805e311a451d7e0ca7a74026cb6601dc`
- arquivos acumulados: 8.250
- bytes de origem acumulados: 211.006.877
- estado: `in_progress`

A continuação exata foi iniciada no workflow [40553603756](https://github.com/arxazure/arquindex/actions/runs/40553603756), commit [eee5934](https://github.com/arxazure/arquindex/commit/eee59349cb7dcedf81ca06d5a601c4e8feaa173e). No fechamento deste registro, o job ainda estava em execução. Ainda não existe comprovação de `BACKUP_COMPLETE_VERIFIED` nem de restauração isolada; por isso, ARQ-119, ARQ-120 e ARQ-123 não foram publicadas.

## Auditoria ARQ-131 a ARQ-136

Workflow: [40553711431](https://github.com/arxazure/arquindex/actions/runs/40553711431), concluído com sucesso.

As seis URLs:

- resolveram DNS para `177.234.150.42`;
- responderam HTTPS/HTTP 200 em mobile e desktop;
- possuem canonical declarada, um H1, viewport, JSON-LD e `index,follow,max-image-preview:large`;
- responderam `/robots.txt` e `/sitemap.xml` com HTTP 200.

| ID | Diagnóstico confirmado | Decisão |
|---|---|---|
| ARQ-131 | canonical própria; conteúdo de preço/digitalização em BH; overflow 512/390; logo ausente; CTA não detectada | diferenciar do grupo de custo e da pilar antes de alterar |
| ARQ-132 | canonical própria; title/H1 genéricos de digitalização em BH; overflow; logo ausente; CTA não detectada | preservar até definir papel único |
| ARQ-133 | canonical incorreta para `www/…/ecm.arquindex.com.br/custo.html`; title com “Arquindex” triplicado; H1 específico; logo oficial e cinco CTAs; sem overflow | primeira correção técnica após o backup; preservar H1 e conteúdo distinto |
| ARQ-134 | canonical própria; hub genérico de serviços em BH; overflow; logo ausente; CTA não detectada | definir função de hub antes de ampliar |
| ARQ-135 | canonical própria; intenção genérica e sobreposta à pilar de guarda; overflow; logo ausente; CTA não detectada | diferenciar por fluxo de consulta/devolução |
| ARQ-136 | canonical própria; H1 de arquivos na educação em BH; overflow; logo ausente; CTA não detectada | validar necessidade real do setor educacional antes de ampliar |

A fila foi atualizada no commit [7ba9b12](https://github.com/arxazure/arquindex/commit/7ba9b1269635b211b3465c3c7b9339b2a363b1d0). O cursor operacional permanece em ARQ-119 até liberar as três melhorias já preparadas com backup e restauração comprovados.

## Search Console — períodos completos

Propriedade: `sc-domain:arquindex.com.br`.

Comparação 06–12/10/2026 versus 13–19/10/2026:

| URL | Impressões 06–12 | Posição média 06–12 | Impressões 13–19 | Posição média 13–19 | Cliques |
|---|---:|---:|---:|---:|---:|
| ARQ-131 | 1 | 95,0 | 5 | 68,8 | 0 / 0 |
| ARQ-132 | 3 | 37,67 | 2 | 69,5 | 0 / 0 |
| ARQ-133 | 4 | 18,5 | 0 | — | 0 / 0 |
| ARQ-134 | 5 | 33,6 | 0 | — | 0 / 0 |
| ARQ-135 | 2 | 43,5 | 1 | 72,0 | 0 / 0 |
| ARQ-136 | 1 | 4,0 | 1 | 76,0 | 0 / 0 |

As amostras são insuficientes para inferir tendência ou efeito de conteúdo. A posição de ARQ-136, por exemplo, oscilou com apenas uma impressão em cada período.

## Bing Webmaster — períodos completos

Conta: `https://arquindex.com.br/`.

- 06–12/10: 18 impressões, 0 cliques.
- 13–19/10: 29 impressões, 1 clique.
- O único clique retornou na consulta `arquindex sbc` (6 impressões; CTR 16,67%).

O conector do Bing não disponibilizou dimensão de página nem posição. Portanto, não é possível atribuir o clique a ARQ-131–136 nem comparar posição dessas URLs.

## Publicação, descoberta e divulgação

- Nenhuma página foi publicada ou alterada na HomeHost.
- Nenhum sitemap foi modificado.
- Nenhum envio a Search Console, Bing ou IndexNow foi feito.
- Nenhuma postagem social foi criada: já havia publicação editorial e divulgação separada registradas no dia, e esta rodada não criou nova URL pública.
- Nenhuma indexação, ranking, posição futura ou lead foi inferido.

## Próximas prioridades

1. Acompanhar o workflow 40553603756 e retomar somente do checkpoint que ele comprovar, até `BACKUP_COMPLETE_VERIFIED`.
2. Executar restauração isolada e confrontar inventário, partes, tamanhos e hashes.
3. Publicar ARQ-119, ARQ-120 e ARQ-123 uma a uma; depois corrigir canonical/title de ARQ-133 e validar produção, sitemap e descoberta.
