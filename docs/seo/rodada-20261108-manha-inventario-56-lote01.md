# Rodada da manhã — inventário de 56 subdomínios, lote 01/10

Data da verificação: 2026-11-08 (BRT)

## Escopo e deduplicação

- A fila operacional `seo/fila-seo-geo-aeo.csv` já registra ARQ-001 a ARQ-238 como concluídas, com cursor em ARQ-238.
- ARQ-099 foi preservada e não foi reaberta.
- ARQ-007 e ARQ-099 não receberam nova divulgação.
- Esta rodada avançou o inventário histórico de 56 subdomínios em um lote de seis URLs, respeitando o limite por rodada.
- Nenhuma página foi alterada ou publicada.

## Evidências

- Commit do workflow: [9977da2bff61cb0deac0a4402c9c7a8ad856ec88](https://github.com/arxazure/arquindex/commit/9977da2bff61cb0deac0a4402c9c7a8ad856ec88)
- Workflow: [execução 42476557258](https://github.com/arxazure/arquindex/actions/runs/42476557258) — `success`
- Artefato: `auditoria-inventario-56-lote01`, ID `13615836238`
- Digest do artefato: `sha256:2f889c9c2250ad76c1008872b864692f74e4ded46dca4a083572c7c3657581d1`
- Horário UTC registrado pelo workflow: `2026-11-08T11:37:29.114426+00:00`

## Resultado por URL

| URL | DNS | TLS | HTTP/SEO | Antes/depois | Estado |
|---|---|---|---|---|---|
| https://digitalizacaodedocumentosembh.arquindex.com.br/ | indisponível | não validado | não verificável | sem alteração | bloqueada por DNS |
| https://guardadocumentalembh.arquindex.com.br/ | indisponível | não validado | não verificável | sem alteração | bloqueada por DNS |
| https://gestaodocumentalembh.arquindex.com.br/ | indisponível | não validado | não verificável | sem alteração | bloqueada por DNS |
| https://incineracaodedocumentosembh.arquindex.com.br/ | indisponível | não validado | não verificável | sem alteração | bloqueada por DNS |
| https://escaneardocumentosembh.arquindex.com.br/ | indisponível | não validado | não verificável | sem alteração | bloqueada por DNS |
| https://alfrescoembh.arquindex.com.br/ | indisponível | não validado | não verificável | sem alteração | bloqueada por DNS |

Sem resolução DNS, não há base técnica para declarar SSL, HTTP 200, canonical, title, H1, meta description, responsividade, robots, sitemap, links, conteúdo, CTA ou formulário. A falha de DNS não autoriza criar subdomínio, apontamento ou alias para a raiz institucional.

## Publicação, backup e indexação

- Backup FTP: não iniciado, pois nenhuma origem pública ou destino individual foi confirmado.
- FTP/HomeHost: não acessado.
- Railway, Hostinger e ChatGPT Site: não utilizados.
- Sitemap: sem alteração.
- Search Console, Bing e IndexNow: sem envio.
- Peças sociais: nenhuma criada ou publicada.
- Posição, indexação, cliques, leads e conversões: não inferidos.

## Estado e próxima rotação

Cobertura comprovada nesta rotação: **6/56**. Isso não equivale ao inventário integral.

Próximo lote: itens 7–12 do manifesto `seo-regional/56-sites/manifest.json`:

1. `consultorialgpd.arquindex.com.br`
2. `adequacaolgpd.arquindex.com.br`
3. `dpoembh.arquindex.com.br`
4. `canaldedenunciaslgpd.arquindex.com.br`
5. `ecmembh.arquindex.com.br`
6. `escanearprontuariomedicoembh.arquindex.com.br`

Qualquer publicação futura continua condicionada a DNS ativo, TLS válido, destino individual confirmado, backup anterior e verificação pública posterior.
