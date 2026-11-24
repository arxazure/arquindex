# Rodada SEO/GEO/AEO — segurança, contratação, OCR e equipamentos

**Data:** 24/11/2026 (tarde, America/Sao_Paulo)  
**Escopo:** ARQ-066 a ARQ-071  
**Modo:** auditoria somente leitura em produção; registros e automações no GitHub

## Resultado executivo

Foram auditadas seis URLs. Todas resolveram para `177.234.150.42`, apresentaram TLS válido, HTTP 200, meta description, um H1, `index,follow` e renderização desktop funcional.

ARQ-066, ARQ-067 e ARQ-070 permanecem tecnicamente estáveis, com canonical própria, identidade completa, WhatsApp e URL presente no sitemap local; foram preservadas.

ARQ-068 e ARQ-069 repetem o padrão da ARQ-065: conteúdo longo e canonical própria, mas overflow móvel de 512 px em viewport de 390 px e conteúdo genérico de digitalização em Belo Horizonte. Na ARQ-069, o title menciona equipamentos, porém H1, meta description e corpo não entregam um guia técnico específico. As duas foram incorporadas à issue #159 para correção na origem comum, evitando remendos duplicados.

A ARQ-071 permanece com canonical incorreta no domínio principal, title com Arquindex repetido três vezes, ausência de WhatsApp e possível sobreposição com a ARQ-067. Foi registrada na issue #160 e não deve ser submetida.

O teste HTTP baseado em `requests` marcou possível mojibake, mas o Chromium confirmou `UTF-8` e nenhum texto corrompido. O sinal foi tratado como falso positivo de decodificação.

## Evidências

- Auditoria HTTP/SEO: [run 45451947686](https://github.com/arxazure/arquindex/actions/runs/45451947686)
  - job: `138651119670`
  - artefato: `14947623082`
  - digest: `sha256:52aa457dec875f72497701b42d351848081c999b746e9db7c63b121d20b28b2d`
- Validação mobile/desktop: [run 45451953406](https://github.com/arxazure/arquindex/actions/runs/45451953406)
  - job: `138651136962`
  - artefato: `14947428364`
  - digest: `sha256:27beb1bef2e13a5658b8a53e05f1720340207893dc3ff5e4169e512a32faf91c`
- Canonical renderizada: [run 45451962139](https://github.com/arxazure/arquindex/actions/runs/45451962139)
  - job: `138651162763`
  - artefato: `14949255666`
  - digest: `sha256:deb81486dcc051b9b086c8ca8386498df7a97f76836b57424ec0b9919622e928`

Workflows criados e executados com sucesso:

- `.github/workflows/auditoria-prioridades-20261124-tarde.yml` — commit `42a896d3ed6122e1ac24a15584ab157a40c4afee`
- `.github/workflows/validar-mobile-prioridades-20261124-tarde.yml` — commit `df3c361a37d5b16529cbc52fc1aa2a5401797f5d`
- `.github/workflows/validar-canonical-dinamico-20261124-tarde.yml` — commit `70e75dd79ccc6fa035e3c46451e3786b8e738d4a`

## Registro e deduplicação

- Fila atualizada no commit [`bd1da71`](https://github.com/arxazure/arquindex/commit/bd1da7152cf0700c52397e8cd79fcd7ba50fbc6c).
- As seis linhas receberam data e três runs atuais.
- ARQ-068 e ARQ-069 anexadas à [issue #159](https://github.com/arxazure/arquindex/issues/159), junto da ARQ-065.
- ARQ-071 registrada na [issue #160](https://github.com/arxazure/arquindex/issues/160).
- Inventário de 56 subdomínios: [consolidado de 13/11/2026](https://github.com/arxazure/arquindex/blob/master/docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md), com 56/56 nomes auditados; não repetido sem mudança observável de DNS.

## Resultado por ficha

| Ficha | URL | Conteúdo e links | Identidade e mobile | Sitemap | Estado |
|---|---|---:|---|---|---|
| ARQ-066 | [Segurança da informação](https://seguranca.arquindex.com.br/) | 5.940 palavras; 79 links; 1 JSON-LD | logo, menu e WhatsApp; sem overflow | 200, URL listada | Preservar e separar consultas de marca, segurança e guarda. |
| ARQ-067 | [Digitalização com armazenamento](https://contratar-servicos-digitalizacao-documentos-com-armazenamento.arquindex.com.br/) | 5.983 palavras; 87 links; 1 JSON-LD | logo, menu e WhatsApp; 390/390 | 200, URL listada | Preservar e diferenciar dos demais guias de contratação. |
| ARQ-068 | [Solução de digitalização](https://digitalizar-digitalizacao-solucao.arquindex.com.br/) | 6.029 palavras; 101 links; 1 JSON-LD | logo, menu e WhatsApp; overflow 512/390 | 200, URL não listada | Corrigir origem comum e definir intenção própria; issue #159. |
| ARQ-069 | [Equipamentos para digitalização](https://equipamentos-recomendados-digitalizar-documentos-alta-qualidade.arquindex.com.br/) | 6.052 palavras; 103 links; 1 JSON-LD | logo, menu e WhatsApp; overflow 512/390 | 200, URL não listada | Substituir conteúdo genérico por guia técnico original após backup; issue #159. |
| ARQ-070 | [OCR em Mauá](https://ocr-maua.arquindex.com.br/) | 5.975 palavras; 85 links; 1 JSON-LD | logo, menu e WhatsApp; 390/390 | 200, URL listada | Preservar; não alegar unidade local nem precisão universal. |
| ARQ-071 | [Erros ao contratar digitalização](https://escolher-servico-confiavel-digitalizacao-documentos-brasil.arquindex.com.br/erros-comuns.html) | 3.377 palavras; 46 links; 2 JSON-LD | logo e menu; sem WhatsApp; 390/390 | 200, URL não listada | Bloqueada: canonical e title incorretos; diferenciar da ARQ-067; issue #160. |

## Limites

Nenhuma escrita via FTP/Homehost, alteração de produção, artigo, preço, oferta, caso, formulário, sitemap, IndexNow, Search Console, Bing ou divulgação social foi executada.

O script `scripts/padronizar-identidade-arquindex.py` não foi executado em lote. ARQ-007 e ARQ-099 foram preservadas sem republicação. Não se inferiram indexação, posição, tráfego, conversão ou leads.
