# Rodada SEO/GEO/AEO — 20/11/2026 — manhã

## Escopo

Auditoria somente leitura de ARQ-084, ARQ-085, ARQ-091, ARQ-092, ARQ-093 e ARQ-097: adequação LGPD, CONARQ em Minas Gerais, serviços de digitalização, gestão da informação, mapeamento documental e OCR corporativo. O lote não repete as 18 URLs verificadas em 19/11 nem ARQ-099.

## Evidências

- Auditoria técnica: [run 44729928081](https://github.com/arxazure/arquindex/actions/runs/44729928081)
  - job `136266770330`
  - artifact `14625982026`
  - SHA-256 `b5c8d66de6c2157f9ca690de850fecc7ccd142b18855406eb706fbf0164a2e26`
- Mobile/desktop: [run 44729930538](https://github.com/arxazure/arquindex/actions/runs/44729930538)
  - job `136266778329`
  - artifact `14625877123`
  - SHA-256 `c2a97f16eed78b6c708b751dc9b3e97baef49225f60d6af0fada0b3c9114a2fc`
- Fila atualizada: [commit b9de88c](https://github.com/arxazure/arquindex/commit/b9de88ce0fe8121a037a65cfe77975474cde1671)
- Integridade da fila: [run 44730165732](https://github.com/arxazure/arquindex/actions/runs/44730165732) — sucesso.

## Resultado comprovado

| Ficha | Página | Resultado comprovado | Pendência |
|---|---|---|---|
| ARQ-084 | Adequação LGPD | HTTP 200; canonical própria; title/H1/meta de LGPD/DPO; 6.083 palavras; logo, menu, WhatsApp e 103 links internos. | Overflow móvel 512/390; sem formulário; sitemap próprio não menciona a URL; papel frente à pilar/ARQ-075 precisa ser definido. |
| ARQ-085 | Consultoria CONARQ MG | HTTP 200; canonical própria; 6.035 palavras; logo, menu, WhatsApp e 101 links internos. | Title/H1/meta citam BH apesar da intenção Minas Gerais; overflow 512/390; sem formulário; sitemap próprio não menciona a URL; atendimento estadual não comprovado. |
| ARQ-091 | Melhores soluções de digitalização | HTTP 200; canonical própria; 6.047 palavras; logo, menu, WhatsApp e 103 links internos. | Conteúdo genérico de digitalização BH; overflow 512/390; sem formulário; sitemap próprio não menciona a URL; sobreposição editorial. |
| ARQ-092 | Soluções para documentos | HTTP 200; canonical própria; 6.033 palavras; logo, menu, WhatsApp e 94 links internos. | Intenção ainda ampla; overflow 512/390; sem formulário; sitemap próprio não menciona a URL; sobreposição com grupo de doze URLs. |
| ARQ-093 | Mapeamento documental | HTTP 200; canonical própria; 6.038 palavras; logo, menu, WhatsApp e 94 links internos. | Papel no cluster ainda indefinido; overflow 512/390; sem formulário; sitemap próprio não menciona a URL. |
| ARQ-097 | OCR para empresas | HTTP 200; canonical própria; title/H1/meta; 280 palavras; menu, WhatsApp, 7 links internos e presença no sitemap próprio; sem overflow. | Conteúdo curto, logo não detectada e sobreposição direta com ARQ-095; sem formulário. |

As seis páginas renderizaram em UTF-8, sem mojibake. DNS e TLS estavam válidos, com resolução para `177.234.150.42`. O parser HTTP exibiu caracteres corrompidos pela falta de charset explícito em algumas respostas, mas o navegador confirmou o texto correto.

## Diagnóstico de família

ARQ-084, ARQ-085, ARQ-091, ARQ-092 e ARQ-093 ampliam a amostra de páginas com largura móvel 512 px em viewport de 390 px. O padrão coincide com o observado nos lotes de 19/11 e reforça a necessidade de localizar o template comum e testar páginas irmãs antes de qualquer correção em massa.

## Publicação e submissão

- Melhorias publicadas em produção: **0**.
- Motivo: cinco páginas compartilham provável template comum, enquanto ARQ-097 exige definição editorial para não competir com ARQ-095. Não há backup integral com restauração comprovada nem mapeamento inequívoco dos arquivos de produção.
- FTP/Homehost: nenhuma escrita.
- Script de identidade: não executado indiscriminadamente.
- Sitemap: nenhuma alteração.
- Search Console, Bing e IndexNow: nenhum envio, pois não houve alteração publicada.
- Divulgação social: nenhuma.
- Inventário dos 56 subdomínios: não repetido; permanece o [consolidado de 13/11/2026](https://github.com/arxazure/arquindex/blob/master/docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md) até mudança observável de DNS.
- ARQ-007 e ARQ-099: preservadas.
- Indexação, posição, conversão e leads: não inferidos.

## Próximas ações seguras

1. Localizar o template comum das cinco páginas com overflow e identificar o elemento de 512 px.
2. Corrigir ARQ-085 somente após confirmar atendimento estadual e diferenciar da página principal de Minas Gerais.
3. Definir papel próprio para ARQ-084, ARQ-091, ARQ-092 e ARQ-093 antes de alterar conteúdo.
4. Enriquecer ARQ-097 apenas com autoria, fontes, limites e critérios de revisão OCR, preservando a distinção da ARQ-095.
