# Inventário Arquindex — lote 02/10 — 10/11/2026

**Escopo:** seis hosts 7–12 do manifesto `seo-regional/56-sites/manifest.json`. **Execução:** [GitHub Actions #42923293308](https://github.com/arxazure/arquindex/actions/runs/42923293308). **Artefato:** [inventario-56-lote02 #13813041764](https://github.com/arxazure/arquindex/actions/runs/42923293308/artifacts/13813041764). Digest SHA-256 do ZIP: `84071c94e43d0618b122768755cf1060234244f273d1d8f2c30651ecbec229fb`.

| Host | DNS | TLS | HTTP, robots, sitemap | Estado |
|---|---|---|---|---|
| consultorialgpd.arquindex.com.br | não resolve | não verificável | não verificável | bloqueado |
| adequacaolgpd.arquindex.com.br | 177.234.150.42 | TLS 1.3 válido | conexão encerrada/resetada, sem status HTTP | bloqueado |
| dpoembh.arquindex.com.br | não resolve | não verificável | não verificável | bloqueado |
| canaldedenunciaslgpd.arquindex.com.br | não resolve | não verificável | não verificável | bloqueado |
| ecmembh.arquindex.com.br | não resolve | não verificável | não verificável | bloqueado |
| escanearprontuariomedicoembh.arquindex.com.br | não resolve | não verificável | não verificável | bloqueado |

Workflow `success` significa que a coleta e upload ocorreram, **não** que os seis sites passaram. Sem HTTP 200, canonical, title, H1, meta description, links, CTA, formulário, responsividade, conteúdo, robots e sitemap não foram comprovados. Sem alteração em produção; backup FTPS, sitemap, IndexNow, redes sociais e publicação: **não executados**. Antes/depois: sem alterações. ARQ-007 e ARQ-099 preservadas.

**Conteúdo técnico preparado para revisão:** [guia de digitalização certificada](../../seo/rascunhos/20261110-guia-digitalizacao-certificada-criterios-contratacao.md), commit `420fbde2790bc7dd8ee495530e696d0d5d421cb9`. Não publicado; requer validação editorial, página canônica, links contextuais, backup e destino autorizado. Não há preço ou oferta comercial confirmada.

**Próxima ação:** resolver DNS/HTTP na infraestrutura autorizada, mapear raiz individual FTP e confirmar backup com hash antes de qualquer deploy; retestar acesso público. Próximo lote do manifesto: itens 13–18, respeitando limite de seis por rodada. Cobertura desta rodada: 6/56; cobertura documentada dos lotes 01 e 02: 12/56, sem equivaler a disponibilidade.
