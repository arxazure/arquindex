# Rodada noturna — ARQ-127 a ARQ-132

**Data:** 27/11/2026 (horário de Brasília)  
**Escopo:** seis URLs da fila de 238 fichas  
**Tipo:** auditoria somente leitura, revalidação e governança editorial  
**Publicações em produção:** nenhuma  
**Melhorias de página publicadas:** 0 (bloqueadas por sobreposição editorial e validações comerciais)

## Resultado executivo

As seis URLs existem e estão publicadas: DNS resolveu para `177.234.150.42`, TLS foi validado, todas responderam HTTP 200, conservaram canonical própria, `index,follow`, meta description, H1, identidade oficial (logo, menu e WhatsApp), UTF-8 correto e layout sem overflow em 390 px e 1440 px.

Nenhuma das seis URLs possui formulário e nenhuma é mencionada pelo sitemap local. Não houve alteração segura de produção nesta rodada porque o grupo exige diferenciação editorial, comprovação comercial/local ou consolidação antes de promoção e submissão.

## URLs auditadas

| ID | URL | HTTP / canonical | Mobile | Conteúdo e conversão | Sitemap | Estado |
|---|---|---|---|---|---|---|
| ARQ-127 | https://solucoes-digitalizacao-documentos-empresariais.arquindex.com.br/ | 200 / própria | 390/390, sem overflow | 6.144 palavras; identidade/WhatsApp; sem formulário; intenção genérica | 200, URL ausente | Não promover; diferenciar da pilar e ARQ-132 |
| ARQ-128 | https://cedoc.arquindex.com.br/ | 200 / própria | 390/390, sem overflow | 6.152 palavras; identidade/WhatsApp; sem formulário; conteúdo amplo | 200, URL ausente | Definir protocolo CEDOC próprio |
| ARQ-129 | https://consultoria-decreto10278-solucao.arquindex.com.br/ | 200 / própria | 390/390, sem overflow | 6.150 palavras; title/H1 coerentes; corpo genérico; sem formulário | 200, URL ausente | Aprofundar com fontes primárias; sem promessa de validade automática |
| ARQ-130 | https://digitalizacao-documental-curitiba-empresas-recomendadas-contrat.arquindex.com.br/ | 200 / própria | 390/390, sem overflow | 6.170 palavras; title/H1 Curitiba; sem formulário | 200, URL ausente | Confirmar atendimento/logística; não alegar unidade local |
| ARQ-131 | https://digitalizacao-documental-paulo-empresas-melhor-custo-beneficio.arquindex.com.br/ | 200 / própria | 390/390, sem overflow | 6.173 palavras; title de preço; sem formulário; sobreposição potencial | 200, URL ausente | Validar preços/ofertas e diferenciar de ARQ-099/109/112/116 |
| ARQ-132 | https://digitalizar-arquivos-solucao.arquindex.com.br/ | 200 / própria | 390/390, sem overflow | 6.130 palavras; identidade/WhatsApp; sem formulário; intenção genérica | 200, URL ausente | Diferenciar da pilar e ARQ-127 ou consolidar |

O marcador de mojibake do cliente HTTP simples é falso positivo nesta família; o navegador confirmou `charset=UTF-8` e texto acentuado correto nas seis páginas.

## Evidências verificáveis

### Workflows

- Auditoria SEO: https://github.com/arxazure/arquindex/actions/runs/46084264811  
  Commit: `b502db13d10805110bcadc0a231206a7202216ff`  
  Artefato: `auditoria-prioridades-20261127-noite`  
  SHA-256: `7f3fde015061bb63d1d8e8bcc8bd3f3b167a8be1b865a7d33c3c6e33a73e9b6d`
- Mobile/desktop: https://github.com/arxazure/arquindex/actions/runs/46084266543  
  Commit: `698046e24ad0a7abece7fd505385d8690f59c74c`  
  Artefato: `validacao-mobile-prioridades-20261127-noite`  
  SHA-256: `1d1c1faaae32cccb2eee977df4fe044706ba9072cb52d2d2c9ad91a33717c34f`
- Canonical renderizada: https://github.com/arxazure/arquindex/actions/runs/46084268377  
  Commit: `2fa2761f60d6c602cad249adcb7627c63fed279d`  
  Artefato: `canonical-dinamico-20261127-noite`  
  SHA-256: `9b63091284dbe003ced7d7852244806a072c65956eee6e63c6cecd7a1c4f99ee`

Todos os três workflows terminaram com `success`.

### Governança e deduplicação

- Pendência editorial consolidada: https://github.com/arxazure/arquindex/issues/171
- Fila atualizada: commit `bbff2d69a3583cd6a076b4f773f11f5e5422538f`
- Validação da fila após edição: 238 IDs únicos; ARQ-127 a ARQ-132 com um registro de ficha cada.
- ARQ-007 e ARQ-099 foram preservadas; nenhuma republicação ou nova peça social foi criada.
- O inventário consolidado dos 56 subdomínios permanece referenciado em `docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md`; não foi alegada nova cobertura integral nesta rodada.

## Publicação, sitemap e indexação

- FTP Homehost: não utilizado.
- Railway, Hostinger e ChatGPT Site: nenhum deploy executado ou declarado.
- Sitemap: nenhuma alteração, pois as URLs ainda não têm papel editorial validado.
- Search Console, Bing e IndexNow: nenhum envio realizado.
- Artigo/notícia e divulgação social: não criados, por ausência de novo material útil e publicação substantiva.
- Indexação, posição e leads: não verificados nem alegados.

## Próximas ações seguras

1. Decidir consolidação ou papel editorial único de ARQ-127 e ARQ-132.
2. Validar protocolo CEDOC (ARQ-128), requisitos do Decreto com fontes primárias (ARQ-129), atendimento em Curitiba (ARQ-130) e preços/ofertas atuais (ARQ-131).
3. Somente após backup recuperável e revisão, publicar via integração autorizada, revalidar produção, atualizar sitemap e registrar eventual submissão.
