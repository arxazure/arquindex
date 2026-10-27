# Rodada SEO/GEO/AEO — manhã de 27/10/2026

## Resultado executivo

A rodada auditou ARQ-125 a ARQ-130 e manteve a produção HomeHost inalterada. O backup integral segue em progresso; portanto, nenhuma das três melhorias preparadas em ARQ-119, ARQ-120 e ARQ-123 foi enviada por FTP.

## Backup HomeHost

A execução [40445309906](https://github.com/arxazure/arquindex/actions/runs/40445309906) terminou com sucesso operacional e marcador `BACKUP_PARTIAL_RESUME_REQUIRED`.

Último checkpoint comprovado:

- caminho: `/seo-backups/resumable/20261026T115321Z-4df745d1d388/checkpoint-000027-6e3d9be793ba.json`
- SHA-256: `3bdf73cb8bbf81fad2865aa9fe8c772c596df2682da9f1428164d0e21c8a42d2`
- arquivos acumulados: 6.500
- bytes de origem acumulados: 192.002.636
- estado: `in_progress`

A continuação exata foi iniciada no workflow [40498052939](https://github.com/arxazure/arquindex/actions/runs/40498052939), commit [cdd1639](https://github.com/arxazure/arquindex/commit/cdd1639f67c332b91cc35d2db81963c0cc37d139). Ainda não há `BACKUP_COMPLETE_VERIFIED` nem restauração isolada comprovada.

## Auditoria ARQ-125 a ARQ-130

Workflow: [40498237347](https://github.com/arxazure/arquindex/actions/runs/40498237347)

As seis URLs:

- resolveram DNS para `177.234.150.42`;
- aceitaram HTTPS e responderam HTTP 200 em mobile e desktop;
- exibiram uma H1;
- declararam `index,follow,max-image-preview:large`;
- responderam `/robots.txt` e `/sitemap.xml` com HTTP 200;
- possuem viewport e JSON-LD observado.

### Problemas concretos

| ID | Problemas principais | Decisão |
|---|---|---|
| ARQ-125 | canonical aponta para caminho incorreto no domínio `www`; title contém “Arquindex” três vezes; overflow 554/390; logo/widget ausentes | corrigir após backup e revisão do diff |
| ARQ-126 | H1/intenção genérica de gestão da informação; overflow 512/390; logo oficial ausente; CTA não detectada | diferenciar da pilar OCR antes de alterar |
| ARQ-127 | conteúdo genérico e sobreposto ao grupo de digitalização; overflow; logo e CTA ausentes | preservar até definir papel único |
| ARQ-128 | title “Cedoc” e H1 genérico; overflow; logo e CTA ausentes | diferenciar da pilar de guarda |
| ARQ-129 | página de Decreto 10.278 com conteúdo ainda genérico; overflow; logo e CTA ausentes | focar requisitos, metadados e controle de qualidade |
| ARQ-130 | alega Curitiba; atendimento/logística não confirmados; overflow; logo e CTA ausentes | não promover nem ampliar antes da validação comercial |

Nenhuma página foi alterada, porque a auditoria confirmou que as correções exigem revisão editorial individual e o backup integral ainda está incompleto.

## Deduplicação

Foi observado um deploy separado e comprovado no Railway, commit `d6b0c465dc332c798549a2c5f4005bf4183d3353`, que adicionou apenas o elemento semântico `main` às rotas regionais. Ele não altera a HomeHost nem libera as URLs desta fila. Nenhuma ação foi repetida nesta rodada.

O radar editorial de 27/10 já possui registro próprio; não foi criado artigo ou post social duplicado.

## Descoberta e métricas

- Nenhuma submissão a Search Console, Bing ou IndexNow foi feita nesta rodada.
- Nenhuma indexação, posição ou lead foi inferido.
- A leitura GSC registrada por outra rotina em 27/10 retornou erro de argumento/código e não produziu métricas utilizáveis.

## Fila

A fila persistente foi ampliada até ARQ-130 no commit [3eb491a](https://github.com/arxazure/arquindex/commit/3eb491a389e9ca2b5c7dcb38ffc2de0359363b7f). O cursor operacional continua em ARQ-119, pois as três publicações já preparadas ainda aguardam backup completo e restauração isolada.

## Próximas prioridades

1. Concluir o backup retomável e verificar inventário, partes, tamanhos e hashes.
2. Executar restauração isolada e comparar o resultado com o inventário imutável.
3. Liberar ARQ-119, ARQ-120 e ARQ-123 uma a uma; depois priorizar ARQ-125 pela canonical incorreta e title triplicado.
