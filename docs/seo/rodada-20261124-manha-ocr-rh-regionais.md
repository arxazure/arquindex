# Rodada SEO/GEO/AEO — OCR, RH e digitalização regional

**Data:** 24/11/2026 (manhã, America/Sao_Paulo)  
**Escopo:** ARQ-060 a ARQ-065  
**Modo:** auditoria somente leitura em produção; registros e automações no GitHub

## Resultado executivo

Foram auditadas seis URLs. Todas resolveram para `177.234.150.42`, apresentaram TLS válido, HTTP 200, meta description, um H1, `index,follow` e renderização desktop funcional.

ARQ-060, ARQ-063 e ARQ-064 mantêm canonical própria e foram preservadas. ARQ-061 e ARQ-064 têm conteúdo muito curto — 289 e 276 palavras — e não exibem logo oficial detectável. A ARQ-062 mantém canonical incorreta, title com quatro ocorrências de Arquindex e ausência de WhatsApp; sua intenção genérica também se sobrepõe à ARQ-057. A ARQ-065 conserva canonical e conteúdo extenso, mas continua com overflow móvel de 512 px em viewport de 390 px e posicionamento editorial genérico para Belo Horizonte.

O teste HTTP baseado em `requests` marcou possível mojibake ao interpretar as respostas. A validação renderizada em Chromium confirmou `UTF-8` e nenhum mojibake nas seis páginas; o sinal foi tratado como falso positivo de decodificação.

## Evidências

- Auditoria HTTP/SEO: [run 45386242783](https://github.com/arxazure/arquindex/actions/runs/45386242783)
  - job: `138417786559`
  - artefato: `14916691453`
  - digest: `sha256:c1d65c40332877e4eac5265005eb8ac889d99a9e0ede6ac3cdd067c7d575e255`
- Validação mobile/desktop: [run 45386244080](https://github.com/arxazure/arquindex/actions/runs/45386244080)
  - job: `138417790750`
  - artefato: `14915823542`
  - digest: `sha256:3f34589c4ab164a2ed8196fc96075628ff260807d1b75de82044250f486b84fa`
- Canonical renderizada: [run 45386247018](https://github.com/arxazure/arquindex/actions/runs/45386247018)
  - job: `138417803146`
  - artefato: `14915269361`
  - digest: `sha256:d0e1c5282936fb254284dd7e912d207180cc98a9a2db8f03cbef52e4f2e1308f`

Workflows criados e executados com sucesso:

- `.github/workflows/auditoria-prioridades-20261124-manha.yml` — commit `cb3f43dc95e894f2587eff37f542f2b23c94917b`
- `.github/workflows/validar-mobile-prioridades-20261124-manha.yml` — commit `243eee6bdabcec2ae393c1281795b80fd6e91a59`
- `.github/workflows/validar-canonical-dinamico-20261124-manha.yml` — commit `1e29b94dffbfbbe101f156210449a74ac12db031`

## Registro e deduplicação

- Fila atualizada no commit [`c2252dd`](https://github.com/arxazure/arquindex/commit/c2252dd302b280847103d5f0babc52fb0c994ea7).
- As seis linhas foram normalizadas para 13 colunas, com data e três runs atuais.
- ARQ-062 registrada na [issue #158](https://github.com/arxazure/arquindex/issues/158).
- ARQ-065 registrada na [issue #159](https://github.com/arxazure/arquindex/issues/159).
- Inventário de 56 subdomínios: [consolidado de 13/11/2026](https://github.com/arxazure/arquindex/blob/master/docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md), com 56/56 nomes auditados; não repetido sem mudança observável de DNS.

## Resultado por ficha

| Ficha | URL | Conteúdo e links | Identidade e mobile | Sitemap | Estado |
|---|---|---:|---|---|---|
| ARQ-060 | [OCR para empresas](https://digitalizacao-ocr-empresas.arquindex.com.br/empresas.html) | 3.566 palavras; 64 links; 2 JSON-LD | logo, menu e WhatsApp; 390/390 | 200, URL não listada | Preservar; não prometer precisão universal e localizar sitemap aplicável. |
| ARQ-061 | [Digitalização no Rio de Janeiro](https://digitalizar-arquivos-rj.arquindex.com.br/) | 289 palavras; 7 links; 1 JSON-LD | menu e WhatsApp; logo não detectado; 390/390 | 200, URL listada | Mapear origem/backup, aplicar logo e ampliar conteúdo com autoria e fontes sem alegar unidade local. |
| ARQ-062 | [OCR em regiões metropolitanas](https://solucoes-ocr-sp.arquindex.com.br/cidade.html) | 520 palavras; 36 links; 2 JSON-LD | logo e menu; sem WhatsApp; 390/390 | 200, URL não listada | Bloqueada: canonical incorreta, title repetido e sobreposição com ARQ-057; issue #158. |
| ARQ-063 | [Dossiês de RH em São Bernardo](https://digitalizacao-rh-sao-bernardo-do-campo.arquindex.com.br/o-que-e.html) | 3.614 palavras; 63 links; 2 JSON-LD | logo, menu e WhatsApp; 390/390 | 200, URL não listada nesta verificação | Preservar; não inferir conformidade automática e localizar sitemap aplicável. |
| ARQ-064 | [Digitalização empresarial em São Paulo](https://digitalizar-arquivos-sp.arquindex.com.br/) | 276 palavras; 7 links; 1 JSON-LD | menu e WhatsApp; logo não detectado; 390/390 | 200, URL listada | Mapear origem/backup, aplicar logo e enriquecer sem alegar unidade local. |
| ARQ-065 | [Digitalização especializada](https://digitalizar-arquivos-especializada.arquindex.com.br/) | 6.015 palavras; 101 links; 1 JSON-LD | logo, menu e WhatsApp; overflow 512/390 | 200, URL não listada | Corrigir overflow e diferenciar da pilar BH após backup; issue #159. |

## Limites

Nenhuma escrita via FTP/Homehost, alteração de produção, artigo, preço, oferta, caso, formulário, sitemap, IndexNow, Search Console, Bing ou divulgação social foi executada. ARQ-062 não deve ser submetida enquanto a canonical e a intenção editorial estiverem inconsistentes.

O script `scripts/padronizar-identidade-arquindex.py` não foi executado em lote. ARQ-007 e ARQ-099 foram preservadas sem republicação. Não se inferiram indexação, posição, tráfego, conversão ou leads.
