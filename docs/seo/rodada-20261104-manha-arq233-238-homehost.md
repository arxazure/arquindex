# Rodada SEO/GEO/AEO — ARQ-233 a ARQ-238

**Data:** 2026-11-04  
**Destino oficial validado:** HomeHost, domínio `www.arquindex.com.br`  
**Escopo:** seis URLs auditadas; três melhorias publicadas; ARQ-099 preservada.

## Resultado executivo

A fila do plano foi percorrida até ARQ-238. As páginas ARQ-233, ARQ-235 e ARQ-236 receberam identidade institucional e reforço de conversão sem alteração de title, H1, meta description, canonical, FAQ, JSON-LD ou texto local já diferenciado. A publicação oficial foi feita por FTPS na HomeHost, depois de backup remoto integral, e verificada publicamente em mobile e desktop.

ARQ-234 foi auditada e preservada para respeitar o limite de três melhorias. ARQ-237 e ARQ-238 são tokens técnicos Sitechecker e foram deliberadamente excluídas de pauta, CTA e divulgação.

## Auditoria das seis URLs

| ID | URL | Resultado público | Decisão |
|---|---|---|---|
| ARQ-233 | https://www.arquindex.com.br/digitalize/sabara/ | HTTP 200; canonical próprio; title/H1 únicos; index,follow; sitemap; conteúdo local substantivo | Identidade e conversão publicadas |
| ARQ-234 | https://www.arquindex.com.br/digitalize/vespasiano/ | HTTP 200; canonical próprio; title/H1 únicos; index,follow; 969 palavras; sem overflow | Preservada; próxima candidata |
| ARQ-235 | https://www.arquindex.com.br/digitalize/lagoa-santa/ | HTTP 200; canonical próprio; title/H1 únicos; index,follow; sitemap; conteúdo de prontuários/privacidade | Identidade e conversão publicadas |
| ARQ-236 | https://www.arquindex.com.br/digitalize/pedro-leopoldo/ | HTTP 200; canonical próprio; title/H1 únicos; index,follow; sitemap; conteúdo de laudos/certificados/equipamentos | Identidade e conversão publicadas |
| ARQ-237 | https://ocr.arquindex.com.br/sitechecker5e8991ab0e9e7199188accf65b36dd02.html | HTTPS 200; token técnico; canonical própria; sem title/H1/CTA por finalidade técnica | Preservada e não divulgada |
| ARQ-238 | https://ecm.arquindex.com.br/sitechecker5e8991ab0e9e7199188accf65b36dd02.html | HTTPS 200; token técnico; canonical própria; sem title/H1/CTA por finalidade técnica | Preservada e não divulgada |

DNS resolveu para `www`, `ocr` e `ecm`; os testes HTTPS foram aceitos pelos clientes públicos. O certificado de `www.arquindex.com.br` foi observado válido até 2026-12-28 no momento da auditoria.

## Melhorias publicadas

As três páginas receberam:

- wordmark e tagline oficiais;
- cabeçalho e menu responsivos;
- rodapé institucional;
- atendimento/WhatsApp flutuante;
- CTA de proposta com UTM específica por cidade;
- preservação integral do conteúdo SEO/GEO/AEO existente.

| ID | Antes | Depois verificado |
|---|---|---|
| ARQ-233 | 968 palavras; sem wordmark, atendimento flutuante ou CTA de proposta | 994–995 palavras; identidade completa; 5 referências WhatsApp; CTA UTM `digitalize_sabara`; sem overflow |
| ARQ-235 | 982 palavras; sem identidade completa ou CTA de proposta | 1008–1009 palavras; identidade completa; CTA UTM `digitalize_lagoa-santa`; sem overflow |
| ARQ-236 | 984 palavras; sem identidade completa ou CTA de proposta | 1010–1011 palavras; identidade completa; CTA UTM `digitalize_pedro-leopoldo`; sem overflow |

## Publicação, backup e evidências

- Commit oficial de fonte/workflow: [3d7f56d8d09eb506ab91b581031b96875dc8dae8](https://github.com/arxazure/arquindex/commit/3d7f56d8d09eb506ab91b581031b96875dc8dae8)
- Workflow HomeHost: [41824068761](https://github.com/arxazure/arquindex/actions/runs/41824068761), job `126554201246`, sucesso.
- Backup remoto: `seo-backups/digitalize-20261104T114952Z`.
- O workflow calculou hash remoto/local e enviou somente três arquivos alterados: `sabara/index.html`, `lagoa-santa/index.html` e `pedro-leopoldo/index.html`.
- Verificação pública final: [41824444647](https://github.com/arxazure/arquindex/actions/runs/41824444647), sucesso.
- Testes de código: 7 testes de identidade e 2 testes de redirecionamento aprovados.
- Auditoria base: [41823352479](https://github.com/arxazure/arquindex/actions/runs/41823352479), sucesso.

Uma tentativa preliminar no Railway serviu apenas como validação de fonte legada e não foi tratada como publicação oficial. A divergência observada levou à confirmação do destino vigente no repositório e à publicação correta na HomeHost.

## Sitemap, descoberta e submissões

As três URLs já constavam em `https://www.arquindex.com.br/digitalize/sitemap.xml`. O XML e o robots foram validados após a publicação. Não houve URL nova nem nova versão necessária do sitemap; por isso não foi repetida submissão ao Search Console, Bing Webmaster ou IndexNow. Presença em sitemap não foi tratada como indexação.

## Fila persistente

A fila existente continha ARQ-001 a ARQ-232, mas o cursor havia sido retrocedido para ARQ-107 por um commit anterior. Os registros foram preservados, ARQ-233 a ARQ-238 foram acrescentados e o cursor foi mantido em ARQ-238 para compatibilidade do validador. A próxima expansão deve partir de inventário novo e verificável, sem reabrir ARQ-099 ou duplicar divulgação.

## Divulgação e métricas

Nenhuma publicação social foi repetida nesta rodada. Não houve novo material visual próprio que justificasse republicação. Não foram observados dados consolidados de Search Console, conversões rastreadas ou leads nesta execução; portanto não há afirmação de ranking, indexação ou resultado comercial.

## Próximas prioridades

1. ARQ-234 Vespasiano: aplicar identidade/CTA preservando o cenário distinto de fornecedores, obras e evidências.
2. Revalidar uma amostra da fila de subdomínios ainda sem identidade completa, respeitando o limite de seis URLs por rodada.
3. Consultar Search Console em janela completa de 7/14/28 dias quando houver dados consolidados para ARQ-233, ARQ-235 e ARQ-236.
