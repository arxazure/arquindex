# Rodada SEO/GEO/AEO — pendências prioritárias

**Data:** 13/11/2026 (noite, America/Sao_Paulo)  
**Escopo:** seis URLs priorizadas após o fechamento do inventário de 56 subdomínios  
**Modo:** auditoria pública somente leitura; nenhuma escrita em produção

## Mudança material encontrada

A rota `https://www.arquindex.com.br/digitalizacao-com-ocr.html`, que retornava HTTP 404 em 31/10/2026, agora responde **HTTP 200** e apresenta:

- canonical próprio;
- title `Digitalização com OCR e PDF Pesquisável | Arquindex`;
- H1 único `Digitalização com OCR e extração de dados`;
- meta description específica;
- `index,follow,max-image-preview:large`;
- viewport responsivo;
- identidade Arquindex, navegação e WhatsApp;
- 1.457 palavras e 44 links internos detectados.

O sitemap principal responde 200, mas **não menciona a URL**. A página não foi alterada nesta rodada; a recuperação foi detectada publicamente. A origem versionada exata da página e do sitemap não foi localizada no repositório, portanto não houve tentativa de inclusão ou submissão sem backup e controle de origem.

A fila persistente foi atualizada em `seo/fila-seo-geo-aeo.csv` para registrar a recuperação e a pendência do sitemap, sem declarar autoria do deploy.

## Resultado das seis URLs

| ID | URL | Estado público em 13/11/2026 | Pendência |
|---|---|---|---|
| ARQ-192 | https://indexacao.arquindex.com.br/ | HTTP 200, mas apenas `Index of /`, 28 palavras; sem canonical, meta, identidade, robots ou sitemap | Mapear document root e reconstruir somente com backup e conteúdo próprio |
| ARQ-206 | https://tabela-de-temporalidade-arquivos.arquindex.com.br/ | HTTP 200; canonical incorreta para `/output/`; texto com caracteres corrompidos; 317 palavras; sem WhatsApp | Corrigir canonical/encoding e aprofundar com fontes aplicáveis, após backup |
| ARQ-210 | https://www.arquindex.com.br/digitalizacao-com-ocr.html | Recuperada: HTTP 200, canonical próprio, conteúdo técnico, identidade e WhatsApp | Localizar origem do sitemap e incluir URL com backup/validação |
| ARQ-215 | https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/ | HTTP 200 e canonical próprio; somente 208 palavras; sem identidade, menu, WhatsApp ou meta robots observável; consta no sitemap | Publicação preparada continua sem origem/publicador seguro comprovado |
| ARQ-217 | https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/vespasiano/ | HTTP 200, canonical próprio, 865 palavras e index,follow; sem identidade, menu, WhatsApp; fora do sitemap principal | Validar atendimento e origem antes de publicar melhoria preparada |
| ARQ-218 | https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/ibirite/ | HTTP 200, canonical próprio, 894 palavras e index,follow; sem identidade, menu, WhatsApp; fora do sitemap principal | Validar atendimento e origem antes de publicar melhoria preparada |

## Evidências

- Workflow: `.github/workflows/auditoria-pendencias-prioritarias-20261113-noite.yml`
- Commit do workflow: `0eaf4a39d9c39d29cbd4d901ae5f4d737ef2df42`
- Execução: https://github.com/arxazure/arquindex/actions/runs/43528824593
- Artefato: `auditoria-pendencias-20261113-noite` — ID `14085913010`
- Digest: `sha256:b467bc2142dbd13bd234e873e45b66f008f1aa926d73ba5287aebe212714955c`
- Atualização da fila: commit `d89c7595c3d5cbe44dbf10b42aeeebb0b2648a62`

## Controle de publicação e deduplicação

- Melhorias em produção nesta rodada: **0**.
- Melhoria documental: **1** — estado de ARQ-210 atualizado na fila com a recuperação comprovada.
- FTP/HomeHost: não acessado; origem/document root e backup não estavam comprovados para uma alteração segura.
- Sitemap/Search Console/Bing/IndexNow: não acionados.
- Divulgação: não executada; ARQ-210 não recebeu nova peça porque a origem do deploy/sitemap ainda precisa ser consolidada e não há material social novo aprovado.
- ARQ-007 e ARQ-099: preservadas.
- Indexação, posição e leads: não inferidos.

## Próxima ação segura

1. Localizar o gerador ou arquivo fonte responsável por `digitalizacao-com-ocr.html` e pelo sitemap principal.
2. Criar backup verificável antes de editar o sitemap.
3. Incluir somente a canonical ARQ-210, validar XML e resposta 200 e então considerar submissão suportada.
4. Manter ARQ-192 e ARQ-206 bloqueadas até document root, backup e correções editoriais estarem definidos.
5. Não publicar as versões preparadas de Vespasiano/Ibirité sem comprovação do atendimento e do publicador autorizado.
