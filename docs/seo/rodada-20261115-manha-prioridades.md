# Rodada SEO/GEO/AEO — prioridades — 2026-11-15 manhã

## Escopo

Auditoria de seis URLs prioritárias com DNS, TLS, HTTP, canonical, title, H1, meta description, robots, sitemap, conteúdo, identidade, WhatsApp, links internos e renderização real em mobile/desktop.

Execução somente leitura em produção. Nenhuma gravação via FTP/HomeHost, Railway, Hostinger ou outro publicador. ARQ-007 e ARQ-099 foram preservadas sem republicação ou nova divulgação. O inventário dos 56 subdomínios permanece concluído desde 2026-11-13.

## Evidências

- Auditoria HTTP/SEO: [workflow 43709749573](https://github.com/arxazure/arquindex/actions/runs/43709749573), sucesso.
- Artefato: `auditoria-prioridades-20261115-manha`, ID `14159788753`, SHA-256 `e375563c58f64a4b612a5d2ce6e09f6996e5b2e199034624823f23f94a831641`.
- Chromium mobile 390×844 e desktop 1440×1000: [workflow 43709827294](https://github.com/arxazure/arquindex/actions/runs/43709827294), sucesso.
- Artefato mobile: `validacao-mobile-prioridades-20261115-manha`, ID `14159313783`, SHA-256 `8c491e1ab10da0c11e8ee43c048a9407f6c39b0a10db76e363f372b4cbd1cece`.
- Fila atualizada no commit [81ccfe1de50821d4b24289a5034769689484a7d1](https://github.com/arxazure/arquindex/commit/81ccfe1de50821d4b24289a5034769689484a7d1).
- Integridade da fila: [workflow 43709960617](https://github.com/arxazure/arquindex/actions/runs/43709960617), sucesso.

## Resultados

| ID | URL | Estado técnico comprovado | Pendência editorial/comercial |
|---|---|---|---|
| ARQ-125 | https://quanto-custa-servico-dpo-externo-brasil.arquindex.com.br/diagnostico.html | HTTP 200, canonical própria, title/H1 coerentes, 3.382 palavras, identidade, WhatsApp, UTF-8 e 390/390 | Fora do sitemap; preços/fatores comerciais precisam de validação antes da promoção |
| ARQ-126 | https://software-reconhecimento-texto-documentos-digitalizados.arquindex.com.br/ | HTTP 200, canonical própria, 6.172 palavras, identidade, WhatsApp e 390/390 | URL OCR usa title/H1/description genéricos de gestão da informação em BH; fora do sitemap |
| ARQ-127 | https://solucoes-digitalizacao-documentos-empresariais.arquindex.com.br/ | HTTP 200, canonical própria, 6.144 palavras, identidade, WhatsApp e 390/390 | Conteúdo genérico e sobreposto; fora do sitemap |
| ARQ-128 | https://cedoc.arquindex.com.br/ | HTTP 200, canonical própria, 6.152 palavras, identidade, WhatsApp e 390/390 | H1/conteúdo genéricos; falta protocolo próprio de consulta e devolução; fora do sitemap |
| ARQ-129 | https://consultoria-decreto10278-solucao.arquindex.com.br/ | HTTP 200, canonical própria, 6.150 palavras, identidade, WhatsApp e 390/390 | Conteúdo ainda genérico; precisa de requisitos e fontes primárias; fora do sitemap |
| ARQ-130 | https://digitalizacao-documental-curitiba-empresas-recomendadas-contrat.arquindex.com.br/ | HTTP 200, canonical própria, title/H1 Curitiba, 6.170 palavras, identidade, WhatsApp e 390/390 | Atendimento/logística em Curitiba não comprovados; fora do sitemap |

O navegador confirmou UTF-8, ausência de mojibake e ausência de overflow nas seis URLs. A ARQ-125 apresentou melhora técnica especialmente relevante em relação à auditoria anterior: canonical agora própria, title sem repetição e layout móvel corrigido. A origem da alteração não foi atribuída a esta rodada.

## Decisão de publicação

Nenhuma melhoria de produção foi publicada. As páginas já mudaram no ambiente público, mas não há commit de deploy, fonte HTML ou raiz FTP individual comprovando autoria e restauração segura. A inclusão em sitemap e a divulgação foram adiadas até a diferenciação editorial e, nos casos DPO/Curitiba, validação comercial.

Não houve envio manual a Search Console, Bing ou IndexNow nesta rodada.

## Próximas ações

1. Priorizar ARQ-126: reescrever intenção OCR com precisão, revisão humana, formatos, critérios de aceite e limites.
2. Diferenciar ARQ-128 por protocolo de localização, consulta, retirada e devolução.
3. Validar preços/fatores da ARQ-125 e atendimento em Curitiba antes de qualquer divulgação ou inclusão em sitemap.
