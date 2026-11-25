# Rodada SEO/GEO/AEO — 25/11/2026 — manhã

## Escopo e limites

Foram auditadas seis fichas consecutivas da fila de 238 páginas: ARQ-078 a ARQ-083. A rodada foi somente leitura sobre os sites públicos. Não houve FTP, alteração de conteúdo em produção, envio a Search Console/Bing/IndexNow nem nova divulgação social.

ARQ-007 e ARQ-099 foram preservadas sem nova execução. O inventário consolidado dos 56 subdomínios permanece em `docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md`; esta rodada confirma apenas as seis URLs descritas abaixo.

## Evidência reproduzível

| Verificação | Run | Job | Artefato | Digest | Resultado |
|---|---:|---:|---:|---|---|
| DNS, TLS, HTTP, robots, sitemap e SEO estático | [45606198028](https://github.com/arxazure/arquindex/actions/runs/45606198028) | 139177565882 | 15017647907 | `sha256:99617d0a7e3864997a87269e1484599e8880984b6ac8804e0ee3a64b956001cf` | sucesso |
| Renderização mobile e desktop | [45606202739](https://github.com/arxazure/arquindex/actions/runs/45606202739) | 139177577824 | 15017189061 | `sha256:35d1a2127f3268262614491017c7360925e33d069db60fc14c83e52bb411adb2` | sucesso |
| Canonical e metadados renderizados | [45606205718](https://github.com/arxazure/arquindex/actions/runs/45606205718) | 139177588271 | 15016884726 | `sha256:63a26ee4b86085187db4247477ef0dfaf9dc17dc55b1d89f42c61c05d5930929` | sucesso |

Commits dos validadores: `78be606c28d605a51a9280a056ca1272f95281be`, `068e2dfcc4f6320e886fc7ea852274831a4dfdff` e `ca58b03a286c39218beabbb6e13222369b4f0a4c`.

## Resultado por ficha

| ID | Situação verificada | Pendência | Decisão |
|---|---|---|---|
| ARQ-078 | HTTP 200; canonical próprio; title/H1/meta; 503 palavras; sitemap inclui URL; logo/menu/WhatsApp; mobile 390/390 | sem formulário; GBP anterior ainda registrado como PROCESSING na fila | preservar publicação e IDs; não repetir divulgação |
| ARQ-079 | HTTP 200; canonical próprio; 6.019 palavras; logo/menu/WhatsApp | overflow 512/390; H1/meta/conteúdo genéricos de digitalização em BH; sitemap não inclui URL; sem formulário | anexada à [issue #159](https://github.com/arxazure/arquindex/issues/159); aguardar origem e backup |
| ARQ-080 | HTTP 200; um H1; 3.452 palavras; logo/menu; mobile 390/390 | canonical para caminho incorreto no domínio principal; title com Arquindex triplicado; meta truncada; sem WhatsApp/formulário; sitemap ausente; atendimento local não comprovado | criada [issue #161](https://github.com/arxazure/arquindex/issues/161); correção condicionada a origem e backup |
| ARQ-081 | HTTP 200; canonical próprio; 5.123 palavras; sitemap inclui URL; identidade/WhatsApp; mobile 390/390 | sem formulário | preservar publicação e hash; não alegar unidade local |
| ARQ-082 | HTTP 200; canonical próprio; 3.627 palavras; sitemap inclui URL; identidade/WhatsApp; mobile 390/390 | sem formulário | preservar publicação e hash; não tratar credencial como garantia |
| ARQ-083 | HTTP 200; canonical próprio; 6.055 palavras; logo/menu/WhatsApp | overflow 512/390; H1/meta/conteúdo genéricos de digitalização em BH; sitemap não inclui URL; sem formulário | anexada à [issue #159](https://github.com/arxazure/arquindex/issues/159); aguardar origem e backup |

O sinal de mojibake observado pelo cliente HTTP é falso positivo de decodificação: o navegador confirmou UTF-8 e texto correto em mobile e desktop nas seis páginas.

## Melhorias registradas

1. Três validadores independentes foram adicionados e executados, com artefatos e digests persistentes.
2. A issue #159 recebeu ARQ-079 e ARQ-083, medidas de overflow e evidências; comentário `7161334685`.
3. A issue #161 foi criada para a correção mínima e verificável de ARQ-080, sem mistura com a família de overflow.

A fila foi atualizada nas seis fichas, preservando hashes, canais, datas e IDs anteriores. Commit: [79f084a](https://github.com/arxazure/arquindex/commit/79f084a5fac41674b719073682e9a34f3e6771c1).

## Publicação e submissão

Nenhuma mudança pública foi feita. A busca no repositório não encontrou a origem HTML de ARQ-080, apenas registros de auditoria e fila. Publicar sem o arquivo/template e sem backup violaria a regra de segurança. Os sitemaps não foram alterados porque ARQ-079, ARQ-080 e ARQ-083 ainda precisam de correção e reteste. Não há comprovação nova de indexação, posição, leads ou processamento do GBP.

## Próximas ações

- localizar a origem/template compartilhada de ARQ-079 e ARQ-083 e corrigir o overflow após backup;
- localizar a origem de ARQ-080 e aplicar somente o conjunto definido na issue #161;
- confirmar atendimento em Sete Lagoas antes de manter a promessa local;
- retestar HTTP, canonical, title, H1, meta, mobile, CTA, sitemap e links;
- somente depois publicar, atualizar sitemap e submeter por integração autenticada, guardando a resposta.
