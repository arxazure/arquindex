# Rodada SEO/GEO/AEO — 24/10/2026, tarde

## Resultado

Foram auditadas ARQ-107 a ARQ-112. Três melhorias substanciais e de intenções distintas foram publicadas: ARQ-107 (OCR), ARQ-110 (diagnóstico LGPD) e ARQ-111 (arquivos físicos). ARQ-108, ARQ-109 e ARQ-112 foram preservadas por sobreposição; não houve publicação social adicional porque a promoção diária já ocorreu pela manhã.

## Evidências

- Auditoria concluída: https://github.com/arxazure/arquindex/actions/runs/40117311596
- Publicação FTP, identidade, backups, sitemaps e artes: https://github.com/arxazure/arquindex/actions/runs/40117507928
- Validação independente: https://github.com/arxazure/arquindex/actions/runs/40117728870
- Script de publicação: commit `f01d211a85a0f38730cc5667ff2f9f825541be9e`
- Backup adicional: `/seo-backups/rodada-20261024-tarde-20261024T174538Z/`

A primeira tentativa de auditoria (40117249638) falhou por resolução local do módulo Node; o workflow foi corrigido e a execução 40117311596 concluiu com sucesso. A falha não alterou o site.

## Publicadas

### ARQ-107 — OCR pesquisável

- URL: https://consultoria-ocr-vantagens.arquindex.com.br/empresas.html
- Title anterior: `Processamento De Documentos Com Ocr para empresas | Arquindex | Arquindex | Arquindex`
- Title novo: `OCR: Pesquisa, Revisão e Critérios de Aceite | Arquindex`
- Canonical corrigida para a própria URL.
- Conteúdo: amostra, captura, pesquisa, campos críticos, exceções e aceite, sem prometer precisão universal.
- SHA-256 público: `29c3997294dcf06a1afdb68d51cf86e5713917c1d3e606751c2650e20e52af0e`

### ARQ-110 — diagnóstico LGPD

- URL: https://empresas-adequacao-lgpd-paulo.arquindex.com.br/diagnostico.html
- Title anterior: `Melhores empresas para adequação à LGPD em São Paulo - Diagnóstico | Arquindex | Arquindex | Arquindex`
- Title novo: `Diagnóstico LGPD: Escopo, Entregáveis e Responsáveis | Arquindex`
- Canonical corrigida para a própria URL.
- Removida a alegação comparativa de “melhores empresas”; adicionada matriz de tratamentos, bases, riscos, terceiros, governança e acompanhamento.
- SHA-256 público: `03dfc7598ec32a936df74915452f21603e8e6ae973041fc4dcc063478fc95d23`

### ARQ-111 — arquivos físicos

- URL: https://gestao-de-arquivos-fisicos.arquindex.com.br/
- Title anterior: `Gestao De Arquivos Fisicos | Arquindex | Arquindex`
- Title novo: `Gestão de Arquivos Físicos: Consulta e Rastreabilidade | Arquindex`
- Canonical corrigida de caminho em `/output/` para a própria URL.
- Conteúdo ampliado para inventário, localização, autorização, retirada, devolução e destinação.
- SHA-256 público: `7e51a25761a8c43896fa56e67102ebcb5393646688f19f864db78189ba998d26`

## Validação

As três páginas passaram em 390×844 e 1440×900: HTTP 200, canonical própria, um H1, index/follow, identidade oficial, menu, atendimento único, resposta AEO, CTA com UTM, ausência de overflow e URL presente no sitemap XML público. Três artes próprias foram publicadas em `/assets/social-arq107-112/` para rotação futura.

## Preservadas

- ARQ-108: intenção genérica e sobreposição com ARQ-098/pilar; também apresenta overflow móvel.
- ARQ-109: intenção de preço sobreposta à ARQ-099 já trabalhada e à ARQ-112.
- ARQ-112: mesma intenção de preço de ARQ-099/109 e overflow móvel.

## Search Console

Períodos completos: 08–21/10/2026 versus 24/09–07/10/2026. Dados anteriores às mudanças.

| ID | Impressões recentes | Posição recente | Impressões anteriores | Posição anterior | Cliques |
|---|---:|---:|---:|---:|---:|
| ARQ-107 | 7 | 17,14 | 1 | 7,00 | 0 |
| ARQ-108 | 12 | 81,33 | 4 | 56,50 | 0 |
| ARQ-109 | 11 | 52,27 | 8 | 52,63 | 0 |
| ARQ-110 | 13 | 14,31 | sem linha | — | 0 |
| ARQ-111 | 12 | 56,92 | 4 | 75,75 | 0 |
| ARQ-112 | 17 | 73,29 | 13 | 62,46 | 0 |

As amostras são pequenas e anteriores à publicação. Não comprovam ganho de ranking, indexação ou conversão.

## Descoberta e divulgação

Os três sitemaps foram atualizados e validados publicamente. Não houve submissão ao Google, Bing ou IndexNow porque a integração Search Console disponível é somente leitura e não houve ação autenticada de envio com confirmação. Sitemap publicado não significa URL indexada.

Cursor seguinte: ARQ-113.
