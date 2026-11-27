# Rodada SEO/GEO/AEO — 27/11/2026 — manhã

## Escopo e limites

Auditoria de ARQ-115 a ARQ-120. ARQ-007 e ARQ-099 foram preservadas. Não houve escrita FTP, deploy, postagem social, alteração de sitemap ou submissão a mecanismos de busca.

O inventário consolidado de 56 subdomínios continua referenciado em `docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md`. As 56 URLs não foram reexecutadas nesta rodada; portanto, não há nova alegação de cobertura total.

## Evidências

| Verificação | Run | Artefato | Digest |
|---|---|---|---|
| DNS, TLS, HTTP, SEO, robots e sitemap | [45992535194](https://github.com/arxazure/arquindex/actions/runs/45992535194) | 15194297193 | `sha256:2a9c1802ca252a6ec1fac3de7d4f12dacf4117584b2af4c70f5f68917c029b5c` |
| Mobile 390 px e desktop 1440 px | [45992537623](https://github.com/arxazure/arquindex/actions/runs/45992537623) | 15194007960 | `sha256:36db7d90fbe00cd3f82afda8ca01c6c111077ad821aa44952e6d2961a04d893e` |
| Canonical renderizada | [45992540824](https://github.com/arxazure/arquindex/actions/runs/45992540824) | 15194756238 | `sha256:740cdc312f2c6de5535f1bb6eddc6d38a8755d773eb2623e6f590daeaedf7fc2` |

Todos os workflows concluíram com sucesso. O navegador confirmou UTF-8 correto; o mojibake apontado pelo cliente HTTP foi efeito de decodificação do teste.

## Resultado por ficha

| Ficha | Resultado | Estado |
|---|---|---|
| ARQ-115 | HTTP 200 e canonical própria; intenção MG ainda usa title/H1/meta de BH; overflow 512/390; sem formulário; fora do sitemap | [#159](https://github.com/arxazure/arquindex/issues/159#issuecomment-7217405589) |
| ARQ-116 | HTTP 200 e canonical própria; intenção de preço sobreposta a ARQ-099/109/112; overflow 512/390; fora do sitemap | [#159](https://github.com/arxazure/arquindex/issues/159#issuecomment-7217405589) |
| ARQ-117 | HTTP 200 e canonical própria; intenção comparativa pouco diferenciada; overflow 512/390; fora do sitemap | [#159](https://github.com/arxazure/arquindex/issues/159#issuecomment-7217405589) |
| ARQ-118 | HTTP 200, canonical própria, 3.576 palavras, identidade, WhatsApp, sem overflow e presente no sitemap | preservada |
| ARQ-119 | HTTP 200 e canonical própria; conteúdo não expressa nuvem; overflow 512/390; script preparado sem deploy | [#169](https://github.com/arxazure/arquindex/issues/169) |
| ARQ-120 | HTTP 200 e canonical própria; conteúdo não expressa governança/compliance; overflow 512/390; script preparado sem deploy | [#169](https://github.com/arxazure/arquindex/issues/169) |

## Ações substanciais

1. Cinco ocorrências do template com overflow foram agregadas à issue #159 com as diferenças editoriais de cada URL.
2. Criada a issue #169 para revisar a preparação de ARQ-119/120, esclarecer que o PR #40 não comprova backup integral e exigir diff por URL antes de deploy.
3. Fila persistente atualizada nas seis fichas, preservando o hash e a publicação comprovada de ARQ-118. Commit: [039dba0a](https://github.com/arxazure/arquindex/commit/039dba0a0f0d6d31c7526ab6e39fc0293c1b1967).

## Pendências

- Não ampliar atendimento estadual em ARQ-115 sem confirmar logística em Minas Gerais.
- Não publicar novo preço/oferta em ARQ-116 ou ARQ-120 sem confirmação vigente.
- Não criar lista artificial de fornecedores em ARQ-117.
- Não executar o script do commit 811c27f diretamente: revisar e produzir diff isolado.
- Backup integral e restauração continuam sem comprovação; nenhuma alteração em produção foi liberada.
- Sem nova comprovação de indexação, posição ou leads.
