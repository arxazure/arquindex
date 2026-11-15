# Rodada SEO/GEO/AEO — 15/11/2026 — tarde

## Escopo e critérios

Rodada limitada a seis URLs da fila, ARQ-131 a ARQ-136. Foram verificados HTTP/HTTPS, canonical, title, H1, meta description, viewport e largura renderizada em 390 px e 1440 px, identidade visual pública, CTA/WhatsApp, formulários e presença no sitemap. A fila foi atualizada com evidências rastreáveis e validada automaticamente.

Esta rodada não publicou alterações em produção: o mapeamento individual entre cada URL e sua origem/FTP ainda não está comprovado. Também não houve submissão ao Search Console, Bing ou IndexNow, pois nenhuma URL nova foi publicada nesta execução.

## Evidências automatizadas

- Auditoria HTTP/SEO: [workflow 43742221853](https://github.com/arxazure/arquindex/actions/runs/43742221853)
  - job: `132897665584`
  - artifact: `14172488917`
  - SHA-256: `ac7fd0b0bfb7ab1aa2a44644fcae902fb0feb55e80c34988c9d31d74950cb736`
- Validação mobile/desktop: [workflow 43742310977](https://github.com/arxazure/arquindex/actions/runs/43742310977)
  - job: `132897944985`
  - artifact: `14173540034`
  - SHA-256: `02f03f8289cf03d1abbcd7055ed03a242387b22a449470086d49c87f05412351`
- Atualização da fila: [commit cbb62cc](https://github.com/arxazure/arquindex/commit/cbb62cc9e97c26cfd805b421e2f10e9b0832f19d)
- Integridade da fila: [workflow 43742479832](https://github.com/arxazure/arquindex/actions/runs/43742479832) — concluído com sucesso.

## Resultado por URL

| Ficha | URL | Verificação comprovada | Pendência/próxima ação |
|---|---|---|---|
| ARQ-131 | https://digitalizacao-documental-paulo-empresas-melhor-custo-beneficio.arquindex.com.br/ | HTTP 200; canonical próprio; title e H1 orientados a preço/digitalização em BH; 6.173 palavras; logo, menu e WhatsApp; UTF-8; viewport sem overflow em 390 px e 1440 px. | Não consta no sitemap. Há risco de sobreposição com outras páginas de preço; validar oferta, preço e diferenciação comercial antes de alterar. Não foi encontrado formulário. |
| ARQ-132 | https://digitalizar-arquivos-solucao.arquindex.com.br/ | HTTP 200; canonical próprio; 6.130 palavras; identidade, menu e WhatsApp; viewport sem overflow em 390 px e 1440 px. | Conteúdo ainda genérico para BH e URL ausente do sitemap. Mapear origem antes de uma revisão substancial. Não foi encontrado formulário. |
| ARQ-133 | https://ecm.arquindex.com.br/custo.html | HTTP 200; canonical agora aponta para a própria URL; title público agora é “Custo de ECM para Empresas \| Arquindex”; H1 coerente; 3.533 palavras; identidade, menu e WhatsApp; viewport sem overflow em 390 px e 1440 px. | Recuperação técnica pública observada em relação à evidência anterior, mas não publicada por esta rodada e com origem ainda não atribuída. URL ausente do sitemap; não foi encontrado formulário. Validar preço/oferta antes de qualquer ampliação comercial. |
| ARQ-134 | https://servicos.arquindex.com.br/ | HTTP 200; canonical próprio; 6.141 palavras; identidade, menu e WhatsApp; viewport sem overflow em 390 px e 1440 px. | Hub genérico e ausente do sitemap. Definir papel na arquitetura e links internos antes de editar. Não foi encontrado formulário. |
| ARQ-135 | https://arquivardocumento.arquindex.com.br/ | HTTP 200; canonical próprio; 6.153 palavras; identidade, menu e WhatsApp; viewport sem overflow em 390 px e 1440 px. | Conteúdo genérico de guarda e URL ausente do sitemap. Diferenciar de páginas equivalentes e comprovar o mapeamento de publicação. Não foi encontrado formulário. |
| ARQ-136 | https://arquivos-educacao.arquindex.com.br/ | HTTP 200; canonical próprio; title e H1 relacionados a educação em BH; 6.160 palavras; identidade, menu e WhatsApp; viewport sem overflow em 390 px e 1440 px. | O corpo permanece genérico para a vertical educação e a URL não consta no sitemap. Requer conteúdo próprio e fontes antes de publicação. Não foi encontrado formulário. |

## Implementações e publicação

- Melhorias substanciais publicadas por esta rodada: **0**.
- Motivo: ausência de comprovação da origem/FTP individual das seis páginas; publicar nessas condições violaria o controle de backup e rastreabilidade.
- Recuperação pública observada: **ARQ-133**, com canonical e title corrigidos; não atribuída a esta execução.
- Sitemap: as seis URLs estavam ausentes; nenhum sitemap foi alterado sem origem comprovada.
- Submissões: nenhuma, pois não houve publicação nova.
- Divulgação social: nenhuma; não houve peça nova validada nem autorização/conexão confirmada nesta rodada.
- Indexação, posição e leads: não inferidos nem declarados.

## Deduplicação e preservação

- ARQ-007 não foi reprocessada; a evidência anterior do workflow de identidade foi preservada.
- ARQ-099 não foi republicada nem divulgada novamente.
- O inventário consolidado dos 56 subdomínios não foi repetido sem mudança de DNS comprovada.

## Próximas prioridades seguras

1. Confirmar o mapeamento de origem/FTP de ARQ-133 e, depois, incluir a URL correta no sitemap.
2. Validar preço, oferta e diferenciação entre ARQ-131 e ARQ-133 para evitar canibalização.
3. Produzir conteúdo realmente específico para educação em ARQ-136 somente após confirmar fonte, autoria e origem de publicação.
