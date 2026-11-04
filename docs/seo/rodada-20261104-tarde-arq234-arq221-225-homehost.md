# Rodada SEO/GEO/AEO — tarde de 04/11/2026

## Escopo e resultado

Foram auditadas seis URLs da fila persistente. Três receberam melhorias substanciais e publicação seletiva na HomeHost por FTPS, com backup e leitura pública posterior. As outras três foram preservadas por falta de confirmação suficiente de atendimento regional e diferenciação local.

- Repositório e branch: `arxazure/arquindex`, `master`
- Commit de conteúdo: [6016ec5](https://github.com/arxazure/arquindex/commit/6016ec549ff379affdce5dcfa60edda53b1abb01)
- Auditoria inicial: [workflow 41880277658](https://github.com/arxazure/arquindex/actions/runs/41880277658)
- Verificação independente final: [workflow 41882373759](https://github.com/arxazure/arquindex/actions/runs/41882373759), sucesso
- Fila persistente: commit [8454bdd](https://github.com/arxazure/arquindex/commit/8454bdd214e6f964c181be33e5b053283fd86ca1); validação [workflow 41883032071](https://github.com/arxazure/arquindex/actions/runs/41883032071), sucesso
- ARQ-099 não foi alterada nem republicada.

## URLs auditadas

| ID | URL | Resultado da auditoria | Ação |
|---|---|---|---|
| ARQ-234 | https://www.arquindex.com.br/digitalize/vespasiano/ | HTTP 200, canonical, title/H1, meta description, index,follow, sitemap e responsividade; identidade incompleta antes da rodada | Publicada identidade oficial e CTA UTM |
| ARQ-221 | https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/boa-vista/ | HTTP 200 e SEO técnico básico válido; sem logo/menu/CTA/formulário | Preservada; requer confirmação de atendimento e diferenciação |
| ARQ-222 | https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/manaus/ | HTTP 200 e SEO técnico básico válido; sem logo/menu/CTA/formulário | Preservada; requer confirmação de atendimento e diferenciação |
| ARQ-223 | https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/cuiaba/ | HTTP 200 e SEO técnico básico válido; sem logo/menu/CTA/formulário | Preservada; requer confirmação de atendimento e diferenciação |
| ARQ-224 | https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/pedro-leopoldo/ | Conteúdo anterior genérico e identidade incompleta | Publicada identidade e conteúdo AEO de engenharia |
| ARQ-225 | https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/santa-luzia/ | Conteúdo anterior genérico para a intenção de RH e identidade incompleta | Publicada identidade e conteúdo AEO de RH/DP |

## Alterações publicadas

### ARQ-234 — Vespasiano

- Título preservado: **Digitalize em Vespasiano: digitalização de documentos | Arquindex**
- H1 preservado: **Digitalize seus documentos em Vespasiano**
- Inclusão de identidade oficial: wordmark/logo, menu responsivo, rodapé e WhatsApp flutuante.
- CTA rastreável para contato com `utm_campaign=digitalize_vespasiano`.
- Publicação: [workflow 41880946800](https://github.com/arxazure/arquindex/actions/runs/41880946800), sucesso.
- Backup remoto: `seo-backups/digitalize-20261104T175043Z`.

### ARQ-224 — Pedro Leopoldo

- Título novo: **Databooks de Engenharia em Pedro Leopoldo | Arquindex**
- H1 novo: **Databooks de engenharia e gestão documental em Pedro Leopoldo**
- Inclusão de resposta direta e conteúdo distinto sobre laudos, certificados, equipamentos, revisões, histórico e pendências.
- Identidade oficial, menu, rodapé e WhatsApp flutuante.
- CTA rastreável com `utm_campaign=arq224_databook_pedro_leopoldo_20261104`.
- Publicação: [workflow 41881061469](https://github.com/arxazure/arquindex/actions/runs/41881061469), sucesso.
- Hash público após publicação: `a49d18325c2cf25f89dc7a6dcdc1dd02f8270661f85ff441fefb1e425ff38f88`.
- Artefato de backup: `backup-databooks-41881061469`, ID `13348653757`.

### ARQ-225 — Santa Luzia

- Título novo: **Databooks de RH e Documentos Trabalhistas em Santa Luzia | Arquindex**
- H1 novo: **Databooks de RH e gestão documental em Santa Luzia**
- Inclusão de resposta direta e conteúdo distinto sobre homônimos, múltiplos vínculos, treinamentos e acesso controlado a dados sensíveis.
- Identidade oficial, menu, rodapé e WhatsApp flutuante.
- CTA rastreável com `utm_campaign=arq225_databook_rh_santa_luzia_20261104`.
- Publicação: [workflow 41881049010](https://github.com/arxazure/arquindex/actions/runs/41881049010), sucesso.
- Hash público após publicação: `53726404c513e94532aa12ee224b8cbfd75f28e85cd971020cd0b826edbc38f2`.

## Teste público final

O workflow [41882373759](https://github.com/arxazure/arquindex/actions/runs/41882373759) verificou as três URLs em 390×844 e 1440×900. Em todos os seis cenários:

- HTTP 200;
- canonical autorreferente correto;
- `index,follow`;
- title e H1 esperados, com um único H1;
- logo/wordmark, menu e atendimento flutuante presentes;
- CTA com a campanha UTM esperada;
- largura do documento igual à viewport, sem overflow horizontal;
- URL presente no sitemap correspondente.

Contagem pública observada: ARQ-234, 995–996 palavras; ARQ-224, 1.064; ARQ-225, 1.082.

## Sitemap e descoberta

As três URLs já existiam e continuaram presentes nos sitemaps correspondentes. Os XMLs foram lidos e validados nos workflows de publicação e no teste final. Não houve inclusão de URL nova, alteração de sitemap, submissão repetida ao Search Console/Bing nem envio IndexNow nesta rodada. Presença em sitemap não foi tratada como indexação.

## Ocorrências técnicas sem impacto na publicação

Workflows auxiliares de publicação criados enquanto eventos estavam atrasados falharam ou ficaram sem HTML elegível. Eles não sobrescreveram produção e foram removidos. As publicações oficiais foram concluídas pelos workflows seletivos já existentes e confirmadas pelo teste independente final.

## Métricas, divulgação e limites

- Não foram atribuídos posição, cliques, leads ou conversões sem dados consolidados e rastreados.
- Nenhuma publicação social foi repetida nesta rodada.
- A auditoria das 56 origens/subdomínios não foi refeita integralmente; esta rodada cobriu apenas as seis URLs registradas acima.
- O cursor permanece em ARQ-238 para compatibilidade da fila concluída; a expansão depende de inventário verificado.

## Próximas prioridades

1. Confirmar atendimento regional e intenção própria de ARQ-221 Boa Vista antes de aplicar identidade e conversão.
2. Fazer a mesma validação para ARQ-222 Manaus e ARQ-223 Cuiabá, evitando páginas locais equivalentes.
3. Medir ARQ-234, ARQ-224 e ARQ-225 em janelas completas de 7/14/28 dias e revisar eventos de CTA somente quando houver rastreamento confiável.
