# Rodada SEO/GEO/AEO — 21/10/2026, noite

## Escopo e fontes

- Fila lida: ARQ-058 a ARQ-063 do plano aprovado.
- Auditoria pública mobile e desktop: [workflow 39695301391](https://github.com/arxazure/arquindex/actions/runs/39695301391).
- Search Console: propriedade `sc-domain:arquindex.com.br`, períodos completos 05–18/10/2026 e 21/09–04/10/2026.
- Publicação Homehost por FTP, com backup e rollback: [workflow 39695535120](https://github.com/arxazure/arquindex/actions/runs/39695535120).
- Validação independente posterior ao deploy: [workflow 39695829701](https://github.com/arxazure/arquindex/actions/runs/39695829701).
- Verificação de sitemaps: [workflow 39695850363](https://github.com/arxazure/arquindex/actions/runs/39695850363).
- Publicação dos dois sitemaps faltantes: [workflow 39696117697](https://github.com/arxazure/arquindex/actions/runs/39696117697).

## Search Console

| ID | Página | 05–18/10 | 21/09–04/10 | Observação |
|---|---|---:|---:|---|
| ARQ-058 | digitalizacao-exin-bh | 47 imp., 0 cliques, CTR 0%, pos. 4,06 | sem linha retornada | possível sobreposição com pilar BH |
| ARQ-059 | digitalizar-digitalizacao-especializada | 42 imp., 0 cliques, CTR 0%, pos. 2,62 | sem linha retornada | prioridade de CTR/título |
| ARQ-060 | digitalizacao-ocr-empresas/empresas.html | 17 imp., 0 cliques, CTR 0%, pos. 4,47 | sem linha retornada | erro técnico de canônica/título |
| ARQ-061 | digitalizar-arquivos-rj | 16 imp., 0 cliques, CTR 0%, pos. 7,69 | 2 imp., 0 cliques, pos. 76 | página curta; atendimento precisa confirmação |
| ARQ-062 | solucoes-ocr-sp/cidade.html | 21 imp., 0 cliques, CTR 0%, pos. 6,33 | sem linha retornada | sobreposição com ARQ-057 |
| ARQ-063 | digitalizacao-rh-sao-bernardo/o-que-e.html | 20 imp., 0 cliques, CTR 0%, pos. 18,05 | 3 imp., 0 cliques, pos. 74,67 | consulta “digitalização de documentos rh validade legal”: 7 imp., pos. 13,14 |

Ausência de linha no período anterior não foi tratada como zero confirmado. Os dados são de busca orgânica e não comprovam conversões.

## Alterações publicadas

| ID | Antes | Depois | Evidência |
|---|---|---|---|
| ARQ-059 | título “Digitalizar Digitalizacao Especializada …”; identidade ausente; overflow móvel; sem AEO/CTA | título “Digitalização Profissional: Escopo e Qualidade | Arquindex”; H1 único; resposta direta + matriz de aceite; identidade oficial; CTA UTM; um widget; canônica própria | hash `20cc8831c81138bd87c3327b97299ada5c2bdde1018732ec7e58dc30cfe1de80` |
| ARQ-060 | título repetia Arquindex; canônica apontava para caminho inválido do domínio principal; sem WhatsApp/proposta | título “OCR para Empresas: Pesquisa e Validação | Arquindex”; canônica própria; resposta sobre limites/revisão do OCR; identidade; CTA UTM; um widget | hash `4554ed9db7df41ad93dd2f35c61c8ecd1fd6fab2ed52c6afc94463e8408790c1` |
| ARQ-063 | título repetido; canônica incorreta; sem CTA | título “Digitalização de Dossiês de RH em São Bernardo | Arquindex”; canônica própria; validade contextualizada com Decreto 10.278/2020 e LGPD; identidade; CTA UTM; um widget | hash `4a43f340e6f137d0074f1252ffe8da71986a0f47b1f31c1048020491dad6669b` |

Backups da página: `/seo-backups/rodada-20261021-noite-20261021T234734Z/`. A validação confirmou HTTP 200, um canonical exato, um H1, indexabilidade, menu/logo, um widget de atendimento, AEO e ausência de overflow em 390 px e 1440 px.

## Páginas revisadas e preservadas

- ARQ-058: HTTP 200, canonical próprio, mobile estável e WhatsApp; apenas 228 palavras, sem identidade/AEO. Preservada por sobreposição com nove URLs do grupo BH.
- ARQ-061: HTTP 200, canonical próprio e mobile estável; 238 palavras, sem identidade/AEO. Reservada para confirmar logística real no Rio de Janeiro.
- ARQ-062: HTTP 200, mas título/canônica defeituosos e sem identidade/CTA. Não alterada porque pode competir com ARQ-057 no mesmo subdomínio; requer decisão de papel ou consolidação.

## Sitemaps e descoberta

- ARQ-063 já estava em `https://digitalizacao-rh-sao-bernardo-do-campo.arquindex.com.br/sitemap.xml`.
- ARQ-059 e ARQ-060 estavam ausentes e foram inseridas nos sitemaps dos próprios subdomínios. Todos os `loc` existentes foram pré-testados com HTTP 200; XML, unicidade, backup e leitura pública foram validados.
- Backup dos XMLs: `/seo-backups/sitemaps-rodada-20261021-noite-20261021T235151Z/`.
- A primeira tentativa de publicação do sitemap ([39695972852](https://github.com/arxazure/arquindex/actions/runs/39695972852)) parou antes da escrita porque um `loc` antigo era relativo; o preflight foi corrigido e a segunda tentativa teve sucesso.
- Não houve submissão ao Google Search Console, Bing Webmaster ou IndexNow: a integração Search Console disponível é somente leitura e nenhuma ação autenticada confirmou recebimento. Sitemap publicado não equivale a indexação.

## Registro operacional

- Commit do script: `8871008e1b00c1777a670f73c59f8596f4aa6252`.
- Commit do workflow de publicação: `5870e9c65ff662d1f7a535144c9fa16ab2e401eb`.
- Commit da fila: `7fa6327947fa4b0e6352e76c911aaaab9f5a2478`.
- Primeira validação [39695571761](https://github.com/arxazure/arquindex/actions/runs/39695571761) foi prematura e falhou antes do deploy terminar; a tentativa posterior 39695829701 confirmou o estado final.
- Nenhuma publicação social foi feita: a regra desta rotina é não duplicar a rotina social.
- ARQ-099 não foi alterada nem republicada.

## Próxima rodada

Cursor: ARQ-064. Auditar ARQ-064 a ARQ-069. Prioridades: diferenciar a página São Paulo, avaliar a função de segurança.arquindex.com.br e evitar ampliar URLs genéricas de digitalização sem papel próprio.
