# Rodada SEO/GEO/AEO — 20/10/2026, tarde

## Escopo
Fichas revisadas: ARQ-034 a ARQ-039. Cursor anterior: ARQ-034; próximo cursor: ARQ-040.

## Decisão editorial
- ARQ-034, ARQ-035 e ARQ-037 foram preservadas sem alteração: compartilham a intenção de digitalização em Belo Horizonte com a página pilar e com ARQ-033. Não houve base para criar mais conteúdo equivalente.
- ARQ-036, ARQ-038 e ARQ-039 receberam conteúdo AEO distinto, identidade institucional, atendimento único e CTA rastreável.

## Publicações verificadas
| ID | URL | Alteração | SHA publicado |
|---|---|---|---|
| ARQ-036 | https://conarq-juridico-nova-lima.arquindex.com.br/ | Matriz de preparação e aceite para contratos/anexos; Decreto 10.278; links para pilar e proposta | cb9b8b44475aa63940d5c160534f2896c053aa928209a668e3954cbb01f1ab5b |
| ARQ-038 | https://ged.arquindex.com.br/bh.html | Resposta e matriz organização × GED × ECM; links para páginas pilares e proposta; title corrigido para “Sistema GED em BH: Gestão Eletrônica de Documentos | Arquindex”; correção de overflow móvel | 640091a330760bcbaff83fdf7f7ae6965ddf6d59f605ea71ec3f2d9e4c3f8fcd (antes da correção pontual) |
| ARQ-039 | https://ocr-prontuarios-contagem.arquindex.com.br/ | Limites do OCR, revisão por risco, vínculo com imagem e CTA para amostra | 8dc4aaef33524df08e50e213051f094b8a9f36c0802e1acf7c6c7c1da5f4a4cb |

## Evidências
- Publicação/backup/HTTP: https://github.com/arxazure/arquindex/actions/runs/39467810977
- Primeira validação: https://github.com/arxazure/arquindex/actions/runs/39468162603 — falhou corretamente ao detectar overflow móvel e title repetido na ARQ-038.
- Correção ARQ-038: https://github.com/arxazure/arquindex/actions/runs/39468319417
- Revalidação final: https://github.com/arxazure/arquindex/actions/runs/39468414681 — sucesso em mobile e desktop para as três URLs.
- Commits de implementação: 7a3615aeea29cec288ea85cda0cacd29dd215f9d, ef5a87470760d3a79b477d39d7a69083e88ae02c, 49cb8dd0ea6973333a13834137dce4771f9ca32e, d379768ddbb88026d395e910e61c37676f154402, 204c4c9c17208ac9d5f2d9da709e4f345ec39058.
- Backup da publicação principal: /seo-backups/rodada-20261020-tarde-20261020T173923Z/.
- Backup adicional ARQ-038 criado pelo workflow de correção.

## Critérios finais validados
HTTP 200, canonical único, um H1, meta description, ausência de noindex, logo/menu oficiais, atendimento único com WhatsApp +55 31 97363-2725, CTA de proposta, conteúdo AEO presente e sem overflow em 390 px e 1440 px.

## Descoberta, métricas e divulgação
Nenhuma URL foi criada. Por isso nenhum sitemap foi alterado e nenhuma submissão a Google/Bing/IndexNow foi repetida. Não houve nova divulgação social nesta rodada. Os dados completos de Search Console não mudaram desde a coleta diária concluída às 12h20 de Brasília; não foi inferida indexação, posição ou lead.

## Próximas prioridades
1. Retomar ARQ-040 a ARQ-045 e separar novas intenções de parâmetros/duplicações.
2. Tratar ARQ-023 em rodada própria, com foco RH/DP e correção de dois H1/canonical duplicada.
3. Medir ARQ-036, ARQ-038 e ARQ-039 após janela consolidada, sem trocar títulos novamente sem diagnóstico.
