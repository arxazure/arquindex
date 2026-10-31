# Rodada SEO/GEO/AEO — 31/10/2026, noite

## Escopo e evidência

- Fichas revisadas: ARQ-209 a ARQ-214.
- Auditoria pública: [workflow 41253853183](https://github.com/arxazure/arquindex/actions/runs/41253853183), job 124692747722, concluído com sucesso.
- Verificações: DNS, TLS/HTTPS, HTTP em desktop e mobile, URL final, canonical, title, H1, meta description, robots, CTA, JSON-LD, conteúdo e overflow horizontal. `robots.txt` e `sitemap.xml` raiz responderam HTTP 200.
- Referência de arquitetura: `painel-seo/auditoria-publica.json`, gerado em 31/10/2026 15:45 UTC, registra as rotas modernas de soluções com HTTP 200 e canonical próprio. Esse arquivo é auditoria pública, não dado do Search Console.

## Resultado por ficha

| ID | URL planejada | Resultado observado | Destino/decisão |
|---|---|---|---|
| ARQ-209 | `/digitalizacao.html` | HTTP 404 em desktop e mobile; template “Página não encontrada”; canonical aponta para a própria URL legada; `index,follow` | Equivalente moderno comprovado: `/solucoes/digitalizacao-documentos` (HTTP 200/canonical no inventário público). Candidata a 301. |
| ARQ-210 | `/digitalizacao-com-ocr.html` | HTTP 404 em desktop e mobile; template de erro indexável | Não há rota `/solucoes/ocr` comprovada. Definir se OCR é seção de digitalização ou intenção própria antes do redirecionamento. |
| ARQ-211 | `/guarda_de_documentos.html` | 301 para `/solucoes/guarda-documental`; final HTTP 200 | Canonical moderno correto; title/H1 coerentes; 4 CTAs, 4 JSON-LD; 912 palavras visíveis; sem overflow detectado. |
| ARQ-212 | `/lgpd-consultoria.html` | 301 para `/solucoes/consultoria-lgpd`; final HTTP 200 | Canonical moderno correto; title “Adequação LGPD | Arquindex”; H1 “Adequação LGPD”; 4 CTAs, 4 JSON-LD; 501 palavras visíveis; sem overflow. |
| ARQ-213 | `/dpo-as-a-service-consultoria-lgpd.html` | HTTP 404 em desktop e mobile; template de erro indexável | Equivalente moderno comprovado: `/solucoes/dpo-terceirizado` (HTTP 200/canonical). Candidata a 301. |
| ARQ-214 | `/gestao_documental_documentos.html` | HTTP 404 em desktop e mobile; template de erro indexável | Equivalente moderno comprovado: `/solucoes/gestao-documental` (HTTP 200/canonical). Candidata a 301. |

## Diagnóstico de migração

Registros do próprio repositório em `docs/maintenance/2026-10-26-seo-deploy.json` e `2026-10-27-seo-deploy.json` indicavam `digitalizacao.html`, `digitalizacao-com-ocr.html` e outras páginas legadas acessíveis. Em 31/10, quatro URLs deste recorte estão em 404. O código de plataforma do commit `77d357a4ae6bfbfe893030cca8b4bfa78433639f` contém um mapa `legacyRedirects`, mas não inclui ARQ-209, ARQ-210, ARQ-213 ou ARQ-214. O caminho `arquindex-platform/server.js` não está disponível na cabeça atual do branch consultado, embora esteja no commit implantado anteriormente. Portanto, a origem editável da plataforma precisa ser conciliada antes de acrescentar os 301.

## Alterações e publicação

- Nenhuma página foi reescrita ou republicada: os equivalentes modernos já existem e recriar HTML legado aumentaria sobreposição.
- Nenhum redirecionamento foi aplicado, pois o código da plataforma em produção não está presente na cabeça atual do repositório e o FTP HomeHost não foi confirmado como origem dessas rotas.
- Nenhum sitemap foi alterado: não houve URL nova publicada.
- Nenhum envio a Search Console, Bing Webmaster ou IndexNow foi feito.
- Nenhuma postagem social foi criada; ARQ-007 e ARQ-099 permaneceram preservadas.

## Próximas prioridades

1. Reconciliar o branch/deploy efetivo que contém `arquindex-platform/server.js` e aplicar 301 exatos para ARQ-209 → `/solucoes/digitalizacao-documentos`, ARQ-213 → `/solucoes/dpo-terceirizado` e ARQ-214 → `/solucoes/gestao-documental`, com teste e rollback.
2. Decidir o papel único da ARQ-210: redirecionar para digitalização se OCR for subtema, ou manter rota própria somente se houver intenção e conteúdo diferenciados.
3. Auditar e substituir links internos que ainda apontam para as quatro URLs 404; depois validar sitemap e métricas em janela consolidada, sem atribuir impacto antes dos dados.
