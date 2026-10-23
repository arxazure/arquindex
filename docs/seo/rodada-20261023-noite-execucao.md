# Rodada SEO/GEO/AEO — 23/10/2026, noite

## Resultado executivo

Foram auditadas seis URLs (ARQ-095 a ARQ-100). Três melhorias substanciais foram publicadas e verificadas: ARQ-095, ARQ-096 e ARQ-098. ARQ-097 e ARQ-100 foram preservadas por sobreposição de intenção; ARQ-099 foi preservada por já ter sido verificada e divulgada anteriormente. Nenhuma postagem social foi repetida.

## Evidências

- Auditoria: https://github.com/arxazure/arquindex/actions/runs/40040683148
- Script: commit `94e429dddba4e0b72d94d87d5a2ccf5a50794b86`
- Publicação: https://github.com/arxazure/arquindex/actions/runs/40040867983 — sucesso
- Primeira validação: https://github.com/arxazure/arquindex/actions/runs/40041175519 — tentativa 1 detectou overflow na ARQ-098; tentativa 2 aprovada integralmente
- Diagnóstico de overflow: https://github.com/arxazure/arquindex/actions/runs/40041255779
- Correção móvel isolada: https://github.com/arxazure/arquindex/actions/runs/40041321931 — sucesso

## Publicadas

### ARQ-095 — OCR corporativo

- URL: https://digitalizar-ocr-empresas.arquindex.com.br/
- Title anterior: `OCR corporativo: digitalização e pesquisa de documentos | Arquindex`
- Title novo: `OCR Corporativo: Teste, Revisão e Critérios de Aceite | Arquindex`
- H1 novo: `OCR corporativo: como testar, revisar e aceitar a entrega`
- Melhoria: resposta direta sobre limites do OCR, amostra representativa, revisão de campos críticos, pesquisa, qualidade da imagem e aceite; fontes e CTA com UTM.
- Backup: `/seo-backups/rodada-20261023-noite-20261023T234024Z/arq-095.html`
- SHA-256 público: `9ce77622a89a55bdd0f04d60450277fa8256154d0fc3354fc78421319b82e0a4`
- Sitemap: https://digitalizar-ocr-empresas.arquindex.com.br/sitemap.xml

### ARQ-096 — comparação de fornecedores

- URL: https://empresas-digitalizacao-documentos-regiao.arquindex.com.br/como-escolher.html
- Title anterior: `Lista de empresas de digitalização de documentos na minha região - Como escolher | Arquindex | Arquindex | Arquindex`
- Title novo: `Como Comparar Empresas de Digitalização | Arquindex`
- H1 novo: `Como comparar empresas de digitalização de documentos`
- Canonical corrigido do caminho indevido no domínio principal para a própria URL.
- Melhoria: tabela de comparação por inventário, amostra, qualidade, segurança, entrega e custo total; ressalva sobre eliminação de originais; CTA com UTM.
- Backup: `/seo-backups/rodada-20261023-noite-20261023T234024Z/arq-096.html`
- SHA-256 público: `5b2a8300bf700bf87e9c4e6b62edb818699f6fbbca782dfcd401f6fd6400f9f8`
- Sitemap: https://empresas-digitalizacao-documentos-regiao.arquindex.com.br/sitemap.xml

### ARQ-098 — preparação e conferência

- URL: https://digitalizardocumentos.arquindex.com.br/o-que-e.html
- Title anterior: `O que é Digitalizar Documentos para Empresas | Arquindex | Arquindex | Arquindex`
- Title novo: `Como Preparar Documentos para Digitalização | Arquindex`
- H1 novo: `Como preparar documentos para digitalização e conferir a entrega`
- Canonical corrigido do caminho indevido no domínio principal para a própria URL.
- Melhoria: inventário, preparação, captura, indexação, conferência e entrega; fontes e CTA com UTM.
- Backup principal: `/seo-backups/rodada-20261023-noite-20261023T234024Z/arq-098.html`
- A primeira validação encontrou largura móvel de 414 px causada por link técnico longo, tabela e deslocamento do atendimento. A correção isolada foi aplicada com novo backup em `/seo-backups/correcao-arq098-20261023T234424Z.html`.
- Sitemap: https://digitalizardocumentos.arquindex.com.br/sitemap.xml

## Validação final

As três URLs passaram, em 390×844 e 1440×900:

- HTTP 200;
- title esperado;
- canonical próprio;
- um H1;
- index/follow;
- logo e menu responsivo;
- um atendimento flutuante;
- bloco AEO e CTA com UTM;
- ausência de overflow horizontal;
- sitemap público contendo a URL.

## Auditadas e preservadas

- ARQ-097 — https://digitalizacao-ocr-empresas.arquindex.com.br/: HTTP 200 e canonical próprio; conteúdo superficial e sem identidade. Preservada por sobreposição direta com ARQ-095; requer papel editorial distinto antes de alteração.
- ARQ-099 — https://empresas-digitalizacao-documentos-regiao.arquindex.com.br/custo-beneficio.html: HTTP 200, canonical próprio e conteúdo sobre orçamento já verificado. Não republicada.
- ARQ-100 — https://lista-empresas-digitalizacao-documentos-regiao.arquindex.com.br/checklist.html: HTTP 200, mas title repetido e canonical incorreto. Preservada porque repete a intenção comercial da ARQ-096; decidir consolidação ou checklist complementar antes de mudar.

## Search Console

Períodos completos comparados: 07–20/10/2026 e 23/09–06/10/2026. Todos os dados antecedem as alterações desta rodada.

| Página | Impressões recentes | Posição recente | Impressões anteriores | Posição anterior | Cliques |
|---|---:|---:|---:|---:|---:|
| ARQ-095 | 114 | 34,31 | 19 | 44,74 | 0 |
| ARQ-096 | 148 | 64,24 | 40 | 71,78 | 0 |
| ARQ-097 | 74 | 74,58 | 8 | 55,00 | 0 |
| ARQ-098 | 64 | 41,89 | 21 | 45,05 | 0 |
| ARQ-099 | 67 | 69,82 | 7 | 60,43 | 0 |
| ARQ-100 | 73 | 73,58 | 4 | 54,75 | 0 |

Houve crescimento de impressões nas seis URLs, mas nenhuma recebeu clique. As posições melhoraram em ARQ-095, ARQ-096 e ARQ-098 e pioraram nas três preservadas; isso não comprova causalidade nem impacto das mudanças feitas hoje.

O conector do Search Console é somente de leitura. Não houve confirmação autenticada de submissão ao Google, Bing ou IndexNow; sitemap validado não significa URL indexada.

## Artes e divulgação

Artes próprias publicadas e verificadas, reservadas para rotação futura:

- ARQ-095: https://www.arquindex.com.br/assets/social-arq095-100/ocr-corporativo-aceite-20261023.jpg
- ARQ-096: https://www.arquindex.com.br/assets/social-arq095-100/comparar-empresas-digitalizacao-20261023.jpg
- ARQ-098: https://www.arquindex.com.br/assets/social-arq095-100/preparar-documentos-digitalizacao-20261023.jpg

Nenhum post foi criado nesta rodada; a promoção diária já havia sido executada pela manhã.

## Continuidade

Cursor recomendado: ARQ-101. Prioridades:

1. Auditar ARQ-101 a ARQ-106.
2. Definir papel único para ARQ-097 e ARQ-100 antes de qualquer publicação.
3. Avaliar métricas das páginas alteradas somente após janela completa, sem prometer ranking, indexação ou leads.
