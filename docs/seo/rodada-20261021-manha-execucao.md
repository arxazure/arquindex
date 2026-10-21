# Rodada SEO/GEO/AEO — 21/10/2026, manhã

## Escopo e fila

- Cursor recebido: ARQ-046.
- Fichas lidas no plano persistente: ARQ-046 a ARQ-051.
- URLs auditadas: 6.
- Melhorias substanciais publicadas: 3 (ARQ-046, ARQ-048 e ARQ-049).
- Próximo cursor: ARQ-052; próxima auditoria: ARQ-052 a ARQ-057.
- ARQ-099 preservada, sem republicação.
- Auditoria: https://github.com/arxazure/arquindex/actions/runs/39593308901

## Diagnóstico anterior à mudança

As seis URLs respondiam HTTP 200, tinham uma canonical, um H1, meta description, `index,follow` e não apresentavam overflow em 390 px ou 1440 px. As seis não tinham o cabeçalho/menu/rodapé oficiais nem o atendimento flutuante padronizado. ARQ-050 e ARQ-051 tinham somente um link interno detectado. O conteúdo renderizado mostrou que ARQ-046 a ARQ-049 tratam de databooks, intenção mais específica que o brief genérico de GED/ECM.

ARQ-047 foi preservada nesta rodada para não concentrar novas alterações em Belo Horizonte, grupo que recebeu mudanças recentes. ARQ-050 e ARQ-051 foram preservadas até definir claramente seus papéis em relação às páginas-pilar de digitalização e evitar canibalização.

## Mudanças publicadas

| ID | URL | Conteúdo útil acrescentado | Hash publicado |
| --- | --- | --- | --- |
| ARQ-046 | https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/nova-lima/ | Identidade oficial; resposta direta e tabela de aceite de databook; links para CONARQ, gestão documental e Alfresco; CTA com UTM; atendimento único | `ad849fbc0964bf02d5049be10db85f7098cfe83674d0d0be196b70b2df1f78d1` |
| ARQ-048 | https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/betim/ | Identidade oficial; matriz para certificados, inspeções e desenhos; limites de alegação local; links contextuais; CTA com UTM; atendimento único | `0afcef339b6872c2a5d7fa01d51d881a73b130fa575fdce529efeb7dabae4ff8` |
| ARQ-049 | https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/contagem/ | Identidade oficial; matriz pedido/nota/entrega/ocorrência; limites de alegação local; links contextuais; CTA com UTM; atendimento único | `8aadf84ef99a1b86e8f10a4d9e1843ad72e7b1039259104e8e69c35a748aadf3` |

Títulos, H1 e descrições anteriores foram preservados porque já distinguiam cidade e intenção de databooks. Nenhuma alegação de unidade física local foi adicionada.

## Publicação, backup e validação

- Correção reutilizável para URLs do domínio principal terminadas em barra: commit https://github.com/arxazure/arquindex/commit/2075c0b2d0d5fee80a0b4643ce513a6f902bddca
- Script da rodada: commit https://github.com/arxazure/arquindex/commit/efcd552522f33448cb0bacdfb2c6835b4eae5524
- Workflow de publicação FTP: https://github.com/arxazure/arquindex/actions/runs/39593554829 — sucesso.
- Backups verificados: `/seo-backups/rodada-20261021-manha-20261021T114012Z/`.
- Validação independente mobile/desktop: https://github.com/arxazure/arquindex/actions/runs/39593782902 — sucesso.
- Resultado validado por URL: HTTP 200, uma canonical correta, um H1, descrição presente, sem noindex, largura sem overflow, logo oficial, menu, um atendimento flutuante, resposta AEO, WhatsApp e CTA de proposta.

## Sitemap e descoberta

- Workflow: https://github.com/arxazure/arquindex/actions/runs/39593973261 — sucesso.
- Foram percorridos 26 XMLs válidos a partir dos sitemaps anunciados em `robots.txt`, incluindo índices e filhos.
- As três URLs constam em `https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/sitemap.xml`.
- Nenhuma URL nova foi criada e a mesma versão do sitemap já continha as URLs. Portanto não houve alteração, reenvio ao Search Console/Bing nem IndexNow. Isso evita repetir submissão e não implica indexação.

## Search Console — períodos completos

Filtro temático amplo: consultas contendo “gestão documental”, “ged”, “ecm” ou “digitaliza”.

| Período | Cliques | Impressões | CTR calculado | Posição média ponderada |
| --- | ---: | ---: | ---: | ---: |
| 05–18/10/2026 | 2 | 499 | 0,40% | 37,84 |
| 21/09–04/10/2026 | 5 | 273 | 1,83% | 32,98 |

Leitura: houve aumento de 226 impressões (+82,8%), mas queda de 3 cliques, CTR menor e piora de 4,86 posições no agregado temático. O conjunto mistura muitas consultas e URLs; não deve ser usado para atribuir efeito às mudanças recentes.

Para as seis URLs ARQ-046 a ARQ-051, o Search Console retornou zero linhas nos dois períodos completos. Não há amostra para afirmar posição, perda, recuperação ou ganho dessas páginas.

## Divulgação e conversão

- CTAs de proposta com UTM foram adicionados às três páginas publicadas.
- Nenhuma publicação social foi feita nesta rotina para não duplicar a rotina social nem reutilizar peças de ARQ-007/ARQ-099.
- Nenhum lead ou conversão foi atribuído sem rastreamento.

## Pendências e próximas prioridades

1. Auditar ARQ-052 a ARQ-057, dando peso a ARQ-054 a ARQ-057, que têm impressões e posição consolidadas no plano.
2. Definir o papel de ARQ-050 e ARQ-051 frente às páginas-pilar antes de ampliar links ou conteúdo.
3. Em rodada própria, tratar identidade/atendimento de ARQ-047 e a pendência anterior de ARQ-042, sem reverter títulos recentes.
