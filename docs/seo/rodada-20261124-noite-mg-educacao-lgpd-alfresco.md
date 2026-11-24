# Rodada SEO/GEO/AEO — 24/11/2026 — noite

## Escopo e limites

Rodada de auditoria de seis URLs da fila de 238 fichas, sem escrita em produção. Foram usados três fluxos independentes para infraestrutura/SEO, renderização mobile/desktop e canonical renderizado. Não houve acesso FTP, alteração de conteúdo público, republicação social, submissão a buscadores nem alegação de indexação, posição ou leads.

As referências de ARQ-007 e ARQ-099 foram preservadas sem nova publicação. O inventário consolidado dos 56 subdomínios permanece em `docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md`; esta rodada revalidou apenas seis URLs da fila. Somadas às rodadas da manhã e da tarde, 18 URLs distintas foram auditadas em 24/11/2026.

## Evidência reproduzível

| Verificação | Run | Job | Artefato | Digest | Resultado |
|---|---:|---:|---:|---|---|
| DNS, TLS, HTTP e SEO estático | [45512447779](https://github.com/arxazure/arquindex/actions/runs/45512447779) | 138863331179 | 14976012458 | `sha256:7e2f8dbc492b338874d9e345be0024810c3578686a61874ce1a9319086a66425` | sucesso |
| Mobile/desktop renderizado | [45512450715](https://github.com/arxazure/arquindex/actions/runs/45512450715) | 138863343193 | 14975462675 | `sha256:88ac3b9788413563854db901d006020c9efa5188057e729cb3dc1a2439f3f879` | sucesso |
| Canonical e metadados renderizados | [45512452914](https://github.com/arxazure/arquindex/actions/runs/45512452914) | 138863351578 | 14976726102 | `sha256:ca78efcd004f60439b3b9cc30a37f3ee4aad9bbc03391b79b33a28f16a7f3fb4` | sucesso |

Commits dos validadores: `284b1aec047e8ed8a6ef4d14e38e301ae5dd0a66`, `a3b22c9abe993157a60cb6c68ff39e400f054b1e` e `f2626e81c1003ce1c6023c83e9465019537d49d1`.

## Resultado por URL

| ID | URL | Verificado | Pendência comprovada | Estado |
|---|---|---|---|---|
| ARQ-072 | https://digitalizar-digitalizacao-mg.arquindex.com.br/ | DNS, TLS, HTTP 200, canonical próprio, index/follow, title, H1, meta, logo, menu, WhatsApp, 101 links internos | overflow 512/390; title/H1/meta restritos a BH apesar da intenção MG; sitemap não lista URL; sem formulário | pendência ligada à [issue #159](https://github.com/arxazure/arquindex/issues/159); sem alteração |
| ARQ-073 | https://mapeamento-educacao.arquindex.com.br/ | HTTP 200, canonical próprio, 5987 palavras, sitemap lista URL, identidade e mobile 390/390 | sem formulário | publicação anterior preservada; sem republicação |
| ARQ-074 | https://corporativo.arquindex.com.br/ | DNS, TLS, HTTP 200, canonical próprio, index/follow, logo, menu, WhatsApp, 103 links internos | overflow 512/390; conteúdo genérico de BH; sitemap não lista URL; sem formulário | pendência ligada à [issue #159](https://github.com/arxazure/arquindex/issues/159); sem alteração |
| ARQ-075 | https://digitalizar-lgpd-solucao.arquindex.com.br/empresas.html | HTTP 200, canonical próprio, title/H1/meta, 3565 palavras, identidade e mobile 390/390 | sitemap raiz não mencionou a URL exata; sem formulário | publicação anterior e hash preservados |
| ARQ-076 | https://instalaralfresco.arquindex.com.br/ | HTTP 200, canonical próprio, sitemap lista URL, title/H1/meta, identidade e mobile 390/390 | sem formulário; GBP permanece sem nova verificação autenticada | divulgação anterior preservada; nenhuma repetição |
| ARQ-077 | https://mapeamento-niteroi.arquindex.com.br/ | DNS, TLS, HTTP 200, canonical próprio, title/H1/meta locais, logo, menu, WhatsApp, 101 links internos | overflow 512/390; sitemap não lista URL; sem formulário; atendimento local não comprovado | pendência ligada à [issue #159](https://github.com/arxazure/arquindex/issues/159); sem alteração |

O marcador de “mojibake” do cliente HTTP foi descartado como falso positivo: a renderização real em navegador confirmou charset UTF-8 e texto correto nas seis páginas.

## Registros efetuados

1. A fila foi atualizada nas fichas ARQ-072 a ARQ-077, preservando hashes e IDs de publicação anteriores. Commit: [da9b470](https://github.com/arxazure/arquindex/commit/da9b4707b292d87f6e0dd73e26f2d03db71409f6).
2. A issue #159 recebeu comentário com ARQ-072, ARQ-074 e ARQ-077, medidas de overflow, runs e digest do artefato. Comentário: `7147768885`.
3. Três validadores auditáveis foram adicionados e executados com sucesso; eles não fazem escrita no servidor público.

## Decisão de publicação

Nenhuma das três páginas com overflow recebeu correção automática: a origem/template e o backup específico ainda precisam ser confirmados. ARQ-073, ARQ-075 e ARQ-076 estavam saudáveis no escopo testado e não justificavam republicação. Nenhum post social foi repetido, nenhuma peça nova foi criada sem material útil e nenhum sitemap foi submetido sem canal autenticado.

## Próximas ações seguras

- localizar a origem compartilhada do overflow 512/390 e corrigir após backup, com reteste individual;
- confirmar atendimento estadual de ARQ-072 e atendimento/logística em Niterói antes de alterar promessa ou promover;
- incluir ARQ-072, ARQ-074 e ARQ-077 no sitemap somente junto de conteúdo diferenciado e publicação confirmada;
- conferir a URL exata de ARQ-075 no sitemap relativo antes de qualquer submissão;
- verificar o estado do GBP de ARQ-076 e Search Console/Bing/IndexNow apenas por integrações autenticadas, guardando a resposta.
