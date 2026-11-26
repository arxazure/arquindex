# Recuperação SEO Arquindex — 09/11/2026

## Fonte e período
GSC Wizard, propriedade sc-domain:arquindex.com.br, 11/10–07/11 versus 13/09–10/10.
- Cliques 100 vs 100; impressões 10.153 vs 5.277; CTR 0,98% vs 1,90%; posição 23,88 vs 17,96.
- 455 sitemaps cadastrados, 379 com erros, 31 com avisos (não necessariamente distintos); http://acervo.arquindex.com.br/sitemap.xml retornou 404.
- Ahrefs 07/11: 4.268 URLs rastreadas; 3.139 ocorrências; 556 novos problemas canonical 4XX. Exportação das URLs individuais ainda necessária.

## Sequência de correção — bloqueio de deploy
1. Obter CSV Ahrefs com URL, Canonical e HTTP Code; executar `python scripts/seo_canonical_review.py --input ahrefs-canonical.csv --out seo-report/canonical-4xx-triage.json`. Não inventar URLs nem redirecionar sem validar equivalência semântica.
2. Rodar `python scripts/seo_sitemap_preflight.py --help` e `python scripts/seo_robots_sitemap_live.py --help`; reconciliar URLs indexáveis com respostas HTTP, canonical, robots e sitemaps; preservar evidência por host.
3. Para canonical 4XX: identificar destino correto HTTP 200 indexável; usar 301 somente quando houver substituto equivalente; caso contrário corrigir link/canonical ou devolver 404/410 legítimo. Não criar soft 404.
4. Priorizar CTR: home (1.580 impressões, 44 cliques), /digitalizacao.html (208 impressões, 3 cliques); preservar Brasília (111, 7) e Salvador (80, 5) e avaliar as 20 oportunidades por posição, intenção e impressões.
5. Validar formulário e WhatsApp em desktop/mobile, foco, acessibilidade, abertura, envio real em ambiente seguro e eventos GA4: generate_lead, form_submit, click_whatsapp. Não registrar PII nos eventos. Verificar duplicação do botão flutuante.
6. Após publicação aprovada, comparar janelas equivalentes de 28 dias por URL/consulta/dispositivo: cliques, impressões, CTR, posição, leads e taxa de conversão. Registrar data, commit, ambiente e rollback.

## Critérios de aceite
- Nenhum canonical 4XX nas URLs comerciais auditadas; nenhum redirect loop; sitemap 200 XML válido e sem URL noindex/redirecionada.
- Formulário funcional e botão WhatsApp estável em mobile/desktop; eventos sem duplicação.
- Nenhum deploy, merge ou submissão a buscadores antes de testes e revisão.

## Estado
Branch de preparação. Este documento não comprova correção de URLs, exportação Ahrefs, teste de formulário ou publicação.
