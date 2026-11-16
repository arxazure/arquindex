# Rodada SEO/GEO/AEO — 16/11/2026 — tarde

## Escopo

Auditoria somente leitura de ARQ-187, ARQ-189, ARQ-192, ARQ-194, ARQ-198 e ARQ-199, sem repetir a rodada da manhã. O conjunto prioriza LGPD/DPO, OCR/RH e uma página técnica de indexação.

## Evidências

- Auditoria técnica: [run 43920264554](https://github.com/arxazure/arquindex/actions/runs/43920264554)
  - job `133485332901`
  - artifact `14253306620`
  - SHA-256 `0c904bc049797514d4be69fc3221cb462c5a2f6e502bc9433e13c62d0576efef`
- Mobile/desktop: [run 43920261491](https://github.com/arxazure/arquindex/actions/runs/43920261491)
  - job `133485321797`
  - artifact `14252253859`
  - SHA-256 `7dbcbf75aa938af3c05277325cdabc4d68aafbc023e8a9c69c5c7d3688d070b8`
- Fila atualizada: [commit c5a4de6](https://github.com/arxazure/arquindex/commit/c5a4de668a66240f99b0843d0ff50f5f014f2457)
- Integridade da fila: [run 43920608678](https://github.com/arxazure/arquindex/actions/runs/43920608678) — sucesso.

## Resultados

| Ficha | Resultado comprovado | Pendência |
|---|---|---|
| ARQ-187 | HTTP 200; canonical própria; title/H1 de consultoria LGPD/DPO em BH; 6.110 palavras; logo, menu, WhatsApp e URL no sitemap. | Conteúdo sobreposto a ARQ-186 e à pilar LGPD; mobile 512/390; sem formulário. |
| ARQ-189 | HTTP 200; canonical própria; 5.996 palavras; logo, menu e WhatsApp recuperados. | URL LGPD mantém title/H1/description genéricos de gestão documental; mobile 512/390; sitemap sem URL; sem formulário. |
| ARQ-192 | DNS/TLS válidos e HTTP 200; sem overflow. | Publica apenas “Index of /” com 28 palavras; sem canonical, description, robots, sitemap, identidade ou CTA. |
| ARQ-194 | HTTP 200; canonical própria; title/H1 coerentes com LGPD, São Vicente e compras; 6.115 palavras; identidade e WhatsApp. | Atendimento/logística não comprovados; mobile 512/390; sitemap sem URL; sem formulário. |
| ARQ-198 | HTTP 200; canonical própria; 6.117 palavras; identidade e WhatsApp. | Usa “melhores consultorias” sem base comparativa e mantém corpo/H1 genéricos; mobile 512/390; sitemap sem URL; sem formulário. |
| ARQ-199 | HTTP 200; 3.389 palavras; H1 coerente; logo/menu; sem overflow em 390/390 e 1440/1440. | Canonical aponta para caminho incorreto no domínio www; title triplica “Arquindex”; sem WhatsApp/formulário; sitemap sem URL; preço, precisão e atendimento em Niterói não confirmados. |

O Chromium confirmou UTF-8 e ausência de mojibake nas seis URLs.

## Publicação e submissão

- Melhorias substanciais publicadas: **0**.
- Motivo: não há mapeamento individual de origem/FTP e backup restaurável comprovados para as páginas com erro. ARQ-194 e ARQ-199 também exigem validação regional/comercial.
- Sitemap, Search Console, Bing e IndexNow: nenhuma alteração ou envio.
- Divulgação social: nenhuma; não houve publicação nova ou material distinto aprovado.
- ARQ-007 e ARQ-099: preservadas sem reprocessamento.
- Indexação, posição e leads: não inferidos.

## Próximas ações seguras

1. ARQ-192: bloquear a listagem de diretório e reconstruir somente após localizar a origem.
2. ARQ-199: corrigir canonical/title e implantar CTA apenas após validar oferta, preço e atendimento.
3. ARQ-198: substituir “melhores” por critérios documentados de contratação e diferenciar do grupo LGPD.
