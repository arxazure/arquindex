# Inventário Arquindex — lote 06/10 — 12/11/2026

**Escopo:** seis hosts 31–36 do manifesto `seo-regional/56-sites/manifest.json`.  
**Execução:** [GitHub Actions #43211528304](https://github.com/arxazure/arquindex/actions/runs/43211528304).  
**Artefato:** [inventario-56-lote06 #13942330242](https://github.com/arxazure/arquindex/actions/runs/43211528304/artifacts/13942330242).  
**Digest SHA-256 do ZIP:** `c0917e0aa58455f626f4d2f75f15d7242a3eb2855527b2c57b7f54f5ef7330b7`.

## Deduplicação e limites

- A fila ARQ-001–ARQ-238 permanece concluída; nenhuma ficha foi reaberta.
- ARQ-007 e ARQ-099 foram preservadas e não receberam nova divulgação.
- Nenhuma postagem foi criada para hosts sem DNS.
- A execução foi somente leitura e respeitou o limite de seis URLs.

## Resultado por URL

| URL | DNS | TLS/HTTP/SEO | Antes/depois | Backup | Sitemap/envio | Estado |
|---|---|---|---|---|---|---|
| https://gestaodocumentalemcontagem.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |
| https://incineracaodedocumentosemcontagem.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |
| https://escaneardocumentosemcontagem.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |
| https://alfrescoemcontagem.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |
| https://consultorialgpd-contagem.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |
| https://adequacaolgpd-contagem.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |

Sem DNS, não foi possível comprovar SSL, HTTP, canonical, title, H1, meta description, responsividade, robots, sitemap, links internos, conteúdo, CTA ou formulário. O resultado do workflow `success` comprova a coleta e o artefato, não a disponibilidade dos sites.

## Publicação e indexação

- HomeHost/FTP: não acessado; document root individual não comprovado.
- Railway, Hostinger e ChatGPT Site: não utilizados.
- Backups: não iniciados porque não há destino público individual validado.
- Sitemap: sem alteração.
- Search Console, Bing e IndexNow: sem envio.
- Redes sociais/GBP: nenhuma postagem ou peça criada.
- Indexação, posição, cliques, leads e conversões: não inferidos.

## Cobertura e próxima rotação

Cobertura documentada dos lotes 01–06: **36/56**, sem equivaler a disponibilidade ou publicação.

Próximo lote, itens 37–42:

1. `dpoemcontagem.arquindex.com.br`
2. `canaldedenunciaslgpd-contagem.arquindex.com.br`
3. `ecmemcontagem.arquindex.com.br`
4. `escanearprontuariomedicoemcontagem.arquindex.com.br`
5. `escaneardossiefuncionario-contagem.arquindex.com.br`
6. `digitalizacaodepartamentopessoal-contagem.arquindex.com.br`

Qualquer publicação futura continua condicionada a DNS ativo, TLS válido, HTTP verificável, raiz individual autorizada, backup anterior com hash e validação pública posterior.
