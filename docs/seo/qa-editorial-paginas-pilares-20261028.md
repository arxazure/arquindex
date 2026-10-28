# QA editorial — páginas pilares reconstruídas

Verificação de 2026-10-28, branch `seo/eeat-pilares-20261028`.

| Página | Palavras visíveis (aprox.) | Parágrafos longos | Distintos | Decisão |
|---|---:|---:|---:|---|
| ARQ-119 | 2172 | 20 | 20 | Encaminhar a QA técnico e de links |
| ARQ-120 | 3440 | 40 | 5 | **Bloquear publicação: repetição excessiva** |
| ARQ-123 | 3414 | 41 | 6 | **Bloquear publicação: repetição excessiva** |

## Método
Contagem aproximada por extração do texto HTML sem tags `script` e `style`; detecção de duplicação por normalização de parágrafos de 35 palavras ou mais. Contagem não é substituta de avaliação humana.

## Ações exigidas
- ARQ-120: substituir blocos genéricos repetidos por procedimentos próprios de orçamento, fatores de preço, metodologia de avaliação, entregáveis, composição de custo e critérios de contratação. Evitar valores sem evidência.
- ARQ-123: substituir blocos genéricos repetidos por classificação de contratos, aditivos, procurações, processos, vínculos, metadados, sigilo, temporalidade e exemplos concretos de busca.
- Rodar `python -m unittest discover -s tests -p 'test_paginas_pilares_staging.py' -v` e `python -m unittest discover -s tests -p 'test_gerar_blocos_eeat_staging.py' -v`.
- Verificar links institucionais, logo, canonical, sitemap e HTTP 200 antes de publicação.
- Não tratar arquivo em staging como deploy na HomeHost ou indexação confirmada.

## Evidência
Inspeção dos três arquivos HTML pelo conector GitHub; nenhuma execução de CI confirmada nesta conferência.
