# Rodada SEO/GEO/AEO — digitalização, guarda e OCR

**Data:** 23/11/2026 (noite, America/Sao_Paulo)  
**Escopo:** ARQ-054 a ARQ-059  
**Modo:** auditoria somente leitura em produção; registros e automações no GitHub

## Resultado executivo

Foram auditadas seis URLs prioritárias. Todas resolveram para `177.234.150.42`, apresentaram TLS válido, HTTP 200, meta description, um H1, `index,follow`, WhatsApp e renderização desktop funcional.

Quatro páginas permanecem tecnicamente estáveis e foram preservadas: ARQ-054, ARQ-055, ARQ-057 e ARQ-059. A ARQ-056 mantém três falhas confirmadas em duas auditorias: canonical apontando para caminho incorreto no domínio principal, title com Arquindex repetido três vezes e overflow móvel de 422 px em viewport de 390 px. A ARQ-058 tem canonical e sitemap corretos, mas permanece curta, com 280 palavras, sete links internos e sem logo oficial detectado.

O teste HTTP baseado em `requests` marcou possível mojibake ao interpretar a resposta. A validação renderizada em Chromium confirmou `UTF-8` e nenhum mojibake nas seis páginas; portanto, o sinal do teste HTTP foi tratado como falso positivo de decodificação e não como defeito editorial comprovado.

## Evidências

- Auditoria HTTP/SEO: [run 45291461058](https://github.com/arxazure/arquindex/actions/runs/45291461058)
  - job: `138100995771`
  - artefato: `14874387683`
  - digest: `sha256:e9e9b129531f9f8a3e7dc8df5faaabaef74926ecda99c231945b081bde6fe2a5`
- Validação mobile/desktop: [run 45291486215](https://github.com/arxazure/arquindex/actions/runs/45291486215)
  - job: `138101077938`
  - artefato: `14873768339`
  - digest: `sha256:6d7ab23295ebbf6ee54c437f5d6bd5d49185cc32219d9d5f8fde44b466d3fbc9`
- Canonical renderizada: [run 45291491185](https://github.com/arxazure/arquindex/actions/runs/45291491185)
  - job: `138101094775`
  - artefato: `14874925705`
  - digest: `sha256:3b0f56d21a481924e8310310d295106984f425b373265cd8c278133fc9b398c3`

Workflows criados e executados com sucesso:

- `.github/workflows/auditoria-prioridades-20261123-noite.yml` — commit `4433b6307faddae4d20979db5d1ff6bf63c16714`
- `.github/workflows/validar-mobile-prioridades-20261123-noite.yml` — commit `9131586270617501f656e1268de5187c8d0ccf4f`
- `.github/workflows/validar-canonical-dinamico-20261123-noite.yml` — commit `6c61fc4220b28f4e3e4388cef6f26801ff4f1787`

## Registro e deduplicação

- Fila atualizada no commit [`28454f8`](https://github.com/arxazure/arquindex/commit/28454f8ad45d34d8443bf4c7493f308909985d58).
- As seis linhas foram normalizadas para 13 colunas e receberam a data e os três runs atuais.
- Falha compartilhada do host BH Digitalizar registrada na [issue #157](https://github.com/arxazure/arquindex/issues/157), incluindo a necessidade de validar a irmã ARQ-035 na mesma correção.
- Inventário de 56 subdomínios: [consolidado de 13/11/2026](https://github.com/arxazure/arquindex/blob/master/docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md), com 56/56 nomes auditados; não repetido sem mudança observável de DNS.

## Resultado por ficha

| Ficha | URL | Conteúdo e links | Identidade e mobile | Sitemap | Estado |
|---|---|---:|---|---|---|
| ARQ-054 | [Digitalização pelo celular](https://aplicativos-facilitam-digitalizacao-documentos-pelo-celular.arquindex.com.br/faq.html) | 3.452 palavras; 69 links; 2 JSON-LD | logo, menu e WhatsApp; 390/390 | 200, URL não listada | Preservar; não equiparar aplicativo móvel a processo de conformidade e localizar sitemap aplicável. |
| ARQ-055 | [Guarda em BH](https://arquivo.arquindex.com.br/bh.html) | 3.551 palavras; 60 links; 3 JSON-LD | logo, menu e WhatsApp; 390/390 | 200, URL não listada | Preservar; não alterar title sem nova evidência. |
| ARQ-056 | [Digitalizar empresas em BH](https://bhdigitalizardocumentos.arquindex.com.br/empresas.html) | 3.360 palavras; 36 links; 3 JSON-LD | logo, menu e WhatsApp; overflow 422/390 | 200, URL não listada | Bloqueada para promoção: canonical incorreta, title repetido e overflow; tratar pela issue #157 após backup. |
| ARQ-057 | [OCR em São Paulo](https://solucoes-ocr-sp.arquindex.com.br/vantagens.html) | 727 palavras; 57 links; 2 JSON-LD | logo, menu e WhatsApp; 390/390 | 200, URL listada | Preservar; não prometer precisão universal nem unidade local. |
| ARQ-058 | [Digitalização e proteção de dados em BH](https://digitalizacao-exin-bh.arquindex.com.br/) | 280 palavras; 7 links; 1 JSON-LD | menu e WhatsApp; logo não detectado; 390/390 | 200, URL listada | Mapear origem e backup; aplicar logo por alvo individual e enriquecer com autoria/fontes sem duplicar a pilar BH. |
| ARQ-059 | [Digitalização profissional](https://digitalizar-digitalizacao-especializada.arquindex.com.br/) | 5.954 palavras; 85 links; 1 JSON-LD | logo, menu e WhatsApp; 390/390 | 200, URL listada | Preservar; revisar sobreposição antes de nova expansão. |

## Fechamento do dia

As três rodadas de 23/11/2026 auditaram 18 URLs distintas, cada uma com evidências no GitHub e atualização individual na fila. Não houve republicação da ARQ-007 ou ARQ-099 nem execução indiscriminada do script de identidade.

Nenhuma escrita via FTP/Homehost, alteração de produção, artigo, preço, oferta, caso, formulário, sitemap, IndexNow, Search Console, Bing ou divulgação social foi executada. ARQ-056 não deve ser submetida enquanto a canonical estiver incorreta. Não se inferiram indexação, posição, tráfego, conversão ou leads.
