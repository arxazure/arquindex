# Inventário Arquindex — lote 05/10 — 11/11/2026

**Escopo:** seis hosts 25–30 do manifesto `seo-regional/56-sites/manifest.json`.  
**Execução:** [GitHub Actions #43121630294](https://github.com/arxazure/arquindex/actions/runs/43121630294).  
**Artefato:** [inventario-56-lote05 #13901556130](https://github.com/arxazure/arquindex/actions/runs/43121630294/artifacts/13901556130).  
**Digest SHA-256 do ZIP:** `db042f600fa41fa09fccad89ca3888083fd960fade8579f8cb31caeca341efb0`.

## Deduplicação e limites

- A fila ARQ-001–ARQ-238 permanece concluída; nenhuma ficha foi reaberta.
- ARQ-007 e ARQ-099 foram preservadas e não receberam nova divulgação.
- Nenhuma postagem foi criada para hosts sem DNS.
- A execução foi somente leitura e respeitou o limite de seis URLs.

## Resultado por URL

| URL | DNS | TLS/HTTP/SEO | Antes/depois | Backup | Sitemap/envio | Estado |
|---|---|---|---|---|---|---|
| https://ecmembetim.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |
| https://escanearprontuariomedicoembetim.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |
| https://escaneardossiefuncionario-betim.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |
| https://digitalizacaodepartamentopessoal-betim.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |
| https://digitalizacaodedocumentosemcontagem.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |
| https://guardadocumentalemcontagem.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |

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

Cobertura documentada dos lotes 01–05: **30/56**, sem equivaler a disponibilidade ou publicação.

Próximo lote, itens 31–36:

1. `gestaodocumentalemcontagem.arquindex.com.br`
2. `incineracaodedocumentosemcontagem.arquindex.com.br`
3. `escaneardocumentosemcontagem.arquindex.com.br`
4. `alfrescoemcontagem.arquindex.com.br`
5. `consultorialgpd-contagem.arquindex.com.br`
6. `adequacaolgpd-contagem.arquindex.com.br`

Qualquer publicação futura continua condicionada a DNS ativo, TLS válido, HTTP verificável, raiz individual autorizada, backup anterior com hash e validação pública posterior.
