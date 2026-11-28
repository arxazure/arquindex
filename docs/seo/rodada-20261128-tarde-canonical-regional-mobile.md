# Rodada da tarde — ARQ-139 a ARQ-144

**Data:** 28/11/2026 (horário de Brasília)  
**Escopo:** seis URLs da fila de 238 fichas  
**Tipo:** auditoria somente leitura, revalidação móvel/canonical e governança  
**Publicações em produção:** nenhuma  
**Melhorias de página publicadas:** 0 (backup/origem, coerência editorial e validação comercial pendentes)

## Resultado executivo

As seis URLs existem e respondem HTTP 200 com DNS e TLS válidos. Cinco páginas — ARQ-139, 140, 142, 143 e 144 — mantêm overflow móvel `512/390`; o desktop mede `1440/1440`. A ARQ-141 não apresenta overflow, mas mantém canonical externa à URL pública, apontando para `/output`, title com marca duplicada, apenas 314 palavras e ausência de logo, WhatsApp e formulário.

ARQ-139 e ARQ-143 apresentam incompatibilidade grave entre URL/intenção e conteúdo publicado. Nenhuma alteração foi feita em produção.

## URLs auditadas

| ID | URL | Achado principal | Mobile | Sitemap | Estado |
|---|---|---|---|---|---|
| ARQ-139 | https://cedoc-educacao-duque-de-caxias.arquindex.com.br/ | URL Duque de Caxias; title/H1/description em Belo Horizonte | **512/390** | URL ausente | Confirmar atendimento/logística e reconstruir conteúdo |
| ARQ-140 | https://decreto10278-educacao.arquindex.com.br/ | 6.027 palavras; canonical própria; precisa revisão com fontes primárias | **512/390** | URL ausente | Não prometer validade automática |
| ARQ-141 | https://digitacao-de-documentos.arquindex.com.br/ | Canonical `/output`, title duplicado, 314 palavras, sem logo/WhatsApp/formulário | 390/390 | URL presente | Issue #172; bloquear submissão/divulgação |
| ARQ-142 | https://digitalizar-arquivos-empresas.arquindex.com.br/ | 6.019 palavras; intenção genérica/sobreposta | **512/390** | URL ausente | Definir papel próprio antes de promoção |
| ARQ-143 | https://digitalizar-lgpd-sp.arquindex.com.br/ | URL LGPD-SP; conteúdo de digitalização em Belo Horizonte | **512/390** | URL ausente | Confirmar atendimento e reconstruir conteúdo LGPD |
| ARQ-144 | https://digitalizardocumentos.arquindex.com.br/ | 6.017 palavras; canonical própria; intenção genérica | **512/390** | URL presente | Corrigir mobile preservando sitemap |

O navegador confirmou `charset=UTF-8` e texto acentuado correto; o marcador de mojibake do cliente HTTP simples é falso positivo.

## Evidências

- Auditoria SEO: https://github.com/arxazure/arquindex/actions/runs/46171543753  
  Commit: `79735121100d2695e7c5c240a385ec23d3f71807`  
  Artefato: `auditoria-prioridades-20261128-tarde`  
  SHA-256: `08a757a57ea1756a62e77f46b6904b013791e7956014c3ac838349b1864cded0`
- Mobile/desktop: https://github.com/arxazure/arquindex/actions/runs/46171544375  
  Commit: `780c733267ff6004460b2d7c4004ab5bdd9a3b5b`  
  Artefato: `validacao-mobile-prioridades-20261128-tarde`  
  SHA-256: `14ae819476d17a5aab9fa5fad7363a4ef334e41f39a68453d9bb18a3622262fd`
- Canonical renderizada: https://github.com/arxazure/arquindex/actions/runs/46171546021  
  Commit: `a277bcf0064417665116874134fb1a96e37bf01a`  
  Artefato: `canonical-dinamico-20261128-tarde`  
  SHA-256: `1af65cffd99d61cb14624beefbd7477a66bf0b1a73819ba3bdd21b306c464efa`

Todos os workflows terminaram com `success`.

## Governança e deduplicação

- Issue específica ARQ-141: https://github.com/arxazure/arquindex/issues/172
- Evidência móvel consolidada na issue existente #159: https://github.com/arxazure/arquindex/issues/159#issuecomment-7243192602
- Fila atualizada: commit `92c5087bf3bae1bf83da8db6ef7d596eae6be5ec`
- Validação: 238 IDs únicos; ARQ-139 a ARQ-144 com um registro cada.
- ARQ-007 e ARQ-099 foram preservadas; nenhuma peça social foi repetida.
- O inventário consolidado dos 56 subdomínios permanece em `docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md`; não foi alegada nova cobertura integral.

## Publicação e indexação

- FTP Homehost: não utilizado.
- Railway, Hostinger e ChatGPT Site: nenhum deploy executado ou declarado.
- Sitemap: nenhuma alteração.
- Search Console, Bing e IndexNow: nenhum envio.
- Artigo/notícia e redes sociais: nenhum material novo, pois não houve publicação substantiva.
- Indexação, posição e leads: não verificados nem alegados.

## Próximas ações seguras

1. Mapear origem/template e concluir backup recuperável antes de qualquer escrita.
2. Corrigir a canonical e identidade da ARQ-141; validar se digitação é serviço real.
3. Corrigir o elemento responsável por 512 px nas cinco URLs e reconstruir ARQ-139/143 somente após comprovação de atendimento regional.
