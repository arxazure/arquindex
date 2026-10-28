# Rodada SEO/GEO/AEO — 28/10/2026, manhã

## Resultado executivo

Foram auditadas ARQ-143 a ARQ-148 e corrigido o teste de conteúdo do PR #73. Nenhuma página foi publicada ou sobrescrita na HomeHost: a retomada do backup continua em execução e ainda não existe evidência de backup integral com restauração isolada.

- Auditoria pública: [run 40682026777](https://github.com/arxazure/arquindex/actions/runs/40682026777), job 122794865659, sucesso.
- Fila persistente: commit [138509cd8235e2e58216f77d7bb99d3299f7752c](https://github.com/arxazure/arquindex/commit/138509cd8235e2e58216f77d7bb99d3299f7752c).
- Backup anterior: checkpoint 45, 11.000 arquivos, 254.339.475 bytes de origem, SHA-256 `3bcb44acef4d24aa88e332b27e0d5abdf5aeb178bc576ffd6b3f0c77bb45d2ca`, encerrado com `BACKUP_PARTIAL_RESUME_REQUIRED`.
- Nova retomada: [run 40682024140](https://github.com/arxazure/arquindex/actions/runs/40682024140), a partir do checkpoint 45; em execução no fechamento.
- PR #73: teste corrigido nos commits [ae5aa29](https://github.com/arxazure/arquindex/commit/ae5aa29f737f603ca30fb5723c01453715fd306d) e [3e57a62](https://github.com/arxazure/arquindex/commit/3e57a620810602b9d557a760e378eea6295f5058).

## Auditoria das páginas

| ID | Resultado técnico | Problema principal | Decisão |
|---|---|---|---|
| ARQ-143 | HTTP 200, canonical própria, index/follow, robots e sitemap 200 | URL/intenção LGPD-SP publica title, H1 e descrição de digitalização em BH; sem logo/CTA; overflow móvel | Não promover; reconstruir em staging somente após confirmar atendimento em São Paulo |
| ARQ-144 | HTTP 200, canonical própria, index/follow, robots e sitemap 200 | Conteúdo genérico e sobreposto à pilar e ao grupo de 25 URLs; sem logo/CTA; overflow | Definir papel único antes de alterar |
| ARQ-145 | HTTP 200, canonical própria, index/follow, robots e sitemap 200 | Intenção RH/Mauá ainda genérica; atendimento local não confirmado; sem logo/CTA; overflow | Confirmar atendimento e criar procedimento específico de RH |
| ARQ-146 | HTTP 200, canonical própria, index/follow, robots e sitemap 200 | Title aborda preço, mas H1/conteúdo permanecem genéricos; sobreposição com ARQ-118; sem logo/CTA; overflow | Diferenciar fatores de orçamento e fluxo de movimentação |
| ARQ-147 | HTTP 200, index/follow, robots e sitemap 200; identidade, CTA e mobile adequados | Canonical aponta para `https://www.arquindex.com.br/ia.arquindex.com.br/custo.html`; title repete Arquindex três vezes | Prioridade técnica de correção após o gate de backup |
| ARQ-148 | HTTP 200, canonical própria, index/follow, robots e sitemap 200 | URL MG publica title/H1 de BH; sem logo/CTA; overflow | Não promover antes de confirmar cobertura em Minas Gerais e corrigir a divergência |

O contador de palavras ficou artificialmente maior no mobile em cinco páginas devido a conteúdo responsivo/duplicado no DOM (aproximadamente 5 mil no mobile contra 1,28 mil no desktop). A ARQ-147 apresentou contagem consistente próxima de 7,2 mil. A quantidade não foi tratada como prova de qualidade.

## PR #73 — QA editorial

A falha anterior retornava zero palavras porque as regex do teste tinham escapes duplos. Após a correção, o teste passou a medir o HTML real:

- ARQ-119 passou a contagem mínima e a verificação de duplicação.
- ARQ-120 falhou: 40 parágrafos longos, apenas 5 únicos.
- ARQ-123 falhou: 41 parágrafos longos, apenas 6 únicos.
- Execução: [run 40682206987](https://github.com/arxazure/arquindex/actions/runs/40682206987), falha esperada de qualidade.

ARQ-120 e ARQ-123 permanecem bloqueadas; não basta atingir a quantidade mínima com repetição.

## Publicação e descoberta

- HomeHost/FTP: não executado nesta rodada.
- Sitemap: sem alteração, pois nenhuma nova versão foi publicada.
- Search Console, Bing e IndexNow: sem submissão.
- Redes sociais: sem nova peça, evitando duplicação.
- Railway, Hostinger e ChatGPT Site: nenhum deploy declarado.

## Próximas prioridades

1. Concluir o backup retomável e validar restauração isolada.
2. Substituir os parágrafos repetidos de ARQ-120 e ARQ-123 por conteúdo técnico específico e repetir o CI.
3. Preparar a correção mínima da ARQ-147 (canonical e title), sem publicar antes do gate.
