# Rodada SEO/GEO/AEO — 16/11/2026 — noite

## Escopo

Auditoria somente leitura de ARQ-202, ARQ-203, ARQ-204, ARQ-205, ARQ-206 e ARQ-208. Foram verificadas seis URLs sem repetir as rodadas anteriores do dia.

## Evidências

- Auditoria técnica: [run 43981790291](https://github.com/arxazure/arquindex/actions/runs/43981790291)
  - job `133699834151`
  - artifact `14283228528`
  - SHA-256 `ec3069aca27c5b0224b215571df06404247a9cf594309815e76d9b07d85bf212`
- Mobile/desktop: [run 43981788676](https://github.com/arxazure/arquindex/actions/runs/43981788676)
  - job `133699829245`
  - artifact `14283004284`
  - SHA-256 `d9792ed33a1190c44aa3696d37d341a941acb74f6809f48ea8429e0964792ffb`
- Fila atualizada: [commit 0ba1b16](https://github.com/arxazure/arquindex/commit/0ba1b162fe64902b9e614162a17c37cc8fc9a6b5)
- Integridade da fila: [run 43982096017](https://github.com/arxazure/arquindex/actions/runs/43982096017) — sucesso.

## Resultado

| Ficha | Resultado comprovado | Pendência |
|---|---|---|
| ARQ-202 | HTTP 200; canonical própria; 6.110 palavras; logo, menu, WhatsApp; URL no sitemap. | Title/H1 genéricos de LGPD em BH e sem diferenciação para pequenas empresas; sobreposição com ARQ-007; mobile 512/390; sem formulário. |
| ARQ-203 | HTTP 200; canonical própria; 6.110 palavras; identidade e WhatsApp recuperados. | Conteúdo genérico e sobreposto a ARQ-186/187; mobile 512/390; sitemap sem URL; sem formulário. |
| ARQ-204 | HTTP 200; canonical própria; 6.027 palavras; identidade e WhatsApp recuperados. | Intenção genérica de gestão da informação; sobreposição com gestão, GED, OCR e digitalização; mobile 512/390; sitemap sem URL; sem formulário. |
| ARQ-205 | DNS/TLS válidos e HTTP 200; sem overflow. | Publica apenas “Index of /” com 20 palavras; sem canonical, description, robots, sitemap, identidade ou CTA. |
| ARQ-206 | HTTP 200; H1 único; 317 palavras; URL no sitemap; sem overflow. | Canonical aponta para `/output/` no domínio www; title duplica “Arquindex”; sem logo, WhatsApp ou formulário; conteúdo insuficiente e sem fontes para prazos. |
| ARQ-208 | HTTP 200; 3.319 palavras; H1 único; logo/menu; sem overflow. | Canonical incorreta no domínio www; title repete “Arquindex” quatro vezes e inclui “Arquindex 2”; alegação de “melhores consultorias” sem critérios; sem WhatsApp/formulário; sitemap sem URL. |

O Chromium confirmou UTF-8 e ausência de mojibake nas seis páginas.

## Publicação e submissão

- Melhorias publicadas: **0**.
- Motivo: não há mapeamento individual de origem/FTP e backup restaurável comprovados para as páginas com falha. ARQ-202/203/208 também exigem consolidação editorial para evitar doorway e canibalização.
- Sitemap, Search Console, Bing e IndexNow: nenhuma alteração ou envio.
- Divulgação social: nenhuma.
- ARQ-007 e ARQ-099: preservadas.
- Indexação, posição e leads: não inferidos.

## Prioridades

1. ARQ-205: bloquear listagem de diretório e confirmar a finalidade do subdomínio em espanhol.
2. ARQ-208: corrigir canonical/title e retirar alegação comparativa sem evidência.
3. ARQ-206: corrigir canonical/identidade e reconstruir conteúdo apenas com fontes aplicáveis, sem prazos universais.
