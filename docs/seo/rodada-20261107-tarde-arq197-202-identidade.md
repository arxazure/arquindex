# Rodada SEO/GEO/AEO — ARQ-197 a ARQ-202 — 07/11/2026 (tarde)

## Evidências

- Auditoria: [workflow 42397477580](https://github.com/arxazure/arquindex/actions/runs/42397477580), commit `ddb3ecd2d19fe56372d5bcde263322caf7ff8892`, conclusão **success**.
- Primeira definição do publicador: commit `475f8607fe9f21c18b5642acda7067a6910d7553`. O YAML foi recusado antes de criar jobs; não houve acesso ao FTP nem alteração pública.
- Correção do publicador: commit `ce13310bfa817c975b21a09aa00b338ec37f1184`.
- Publicação final: [workflow 42397672316](https://github.com/arxazure/arquindex/actions/runs/42397672316), conclusão **success**.
- Escopo: seis URLs auditadas e duas melhorias publicadas. ARQ-099 preservada.

## Auditoria

| ID | Resultado | Decisão |
|---|---|---|
| ARQ-197 | HTTP 200, canonical próprio, indexável; identidade ausente, overflow e sitemap sem URL | sem escrita: atendimento/logística em São Vicente não confirmados |
| ARQ-198 | HTTP 200, canonical próprio; title usa “melhores”, identidade ausente, overflow e sitemap sem URL | sem escrita: alegação comparativa sem critérios documentados |
| ARQ-199 | HTTP 200 e 3.299 palavras; canonical aponta para caminho diferente no domínio www, title repete Arquindex e falta WhatsApp | sem escrita: canonical e atendimento em Niterói precisam de validação conjunta |
| ARQ-200 | HTTP 200, canonical próprio, indexável; conteúdo coerente de OCR, mas identidade ausente, overflow e sitemap sem URL | identidade publicada |
| ARQ-201 | HTTP 200, canonical próprio, indexável; conteúdo de digitalização em grande volume, identidade ausente, overflow e sitemap sem URL | identidade publicada; diferenciação editorial ainda pendente |
| ARQ-202 | HTTP 200, canonical próprio e sitemap contendo URL; conteúdo sobreposto à página já verificada para pequenas empresas | preservada para evitar doorway duplicada |

## Melhorias publicadas

### ARQ-200 — OCR e indexação
- URL: https://ocr.arquindex.com.br/
- Alteração: identidade oficial, menu responsivo, rodapé e WhatsApp flutuante; overflow corrigido sem mudar title, H1, description ou canonical.
- Verificação: HTTP 200, canonical próprio, um H1, index/follow, mobile 390/390 e desktop 1440/1440.
- Backup: `/seo-backups/identidade-20261107T174331Z/da05c15b25d0f7f656f6.html`
- SHA-256: `6031e59734e11e2aa7d86689c7f91805721732fea1e4f58fb2ea6aa5078ec543`
- Descoberta: robots.txt e sitemap.xml 200; sitemap ainda sem a URL.

### ARQ-201 — digitalização de grandes volumes
- URL: https://scanners-digitalizacao-grandes-volumes-documentos.arquindex.com.br/
- Alteração: identidade oficial e correção responsiva; conteúdo preservado.
- Verificação: HTTP 200, canonical próprio, um H1, index/follow, mobile 390/390 e desktop 1440/1440.
- Backup: `/seo-backups/identidade-20261107T174351Z/176ab54ac7e0745986bc.html`
- SHA-256: `f0bfe9cb59c33e5de0598002d097eb24a5ad0525ff78ee2b25474f302099caf1`
- Descoberta: robots.txt e sitemap.xml 200; sitemap ainda sem a URL.

## Pendências

1. Corrigir ARQ-199 somente após confirmar canonical pretendido, atendimento em Niterói e política de preços/precisão.
2. Reescrever o posicionamento de ARQ-198 como critérios de contratação, removendo qualquer ranking não comprovado.
3. Diferenciar ARQ-201 por preparação de lote, captura, conferência e entrega antes de divulgação.
4. Consolidar ou diferenciar ARQ-202 da página de LGPD para pequenas empresas já verificada.
5. Localizar a origem segura dos sitemaps antes de incluir ARQ-200 e ARQ-201. Não houve submissão a Google, Bing ou IndexNow.
6. Não houve artigo artificial, divulgação social duplicada, nem inferência de posição, indexação ou leads.
