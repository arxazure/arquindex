# Inventário Arquindex — lote 03/10 — 11/11/2026

**Escopo:** seis hosts 13–18 do manifesto `seo-regional/56-sites/manifest.json`.  
**Execução:** [GitHub Actions #43013846059](https://github.com/arxazure/arquindex/actions/runs/43013846059).  
**Artefato:** [inventario-56-lote03 #13851756998](https://github.com/arxazure/arquindex/actions/runs/43013846059/artifacts/13851756998).  
**Digest SHA-256 do ZIP:** `cffc18797bbefe4ef374a86a7fab9ddbc7a0637d8299afe36c8b7b6e0ace0969`.

## Deduplicação e limites

- A fila ARQ-001–ARQ-238 permanece concluída; nenhuma ficha foi reaberta.
- ARQ-007 e ARQ-099 foram preservadas e não receberam nova divulgação.
- Nenhuma postagem foi criada para hosts sem DNS.
- A execução foi somente leitura e respeitou o limite de seis URLs.

## Resultado por URL

| URL | DNS | TLS/HTTP/SEO | Antes/depois | Backup | Sitemap/envio | Estado |
|---|---|---|---|---|---|---|
| https://escaneardossiefuncionario.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |
| https://digitalizacaodepartamentopessoal.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |
| https://digitalizacaodedocumentosembetim.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |
| https://guardadocumentalembetim.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |
| https://gestaodocumentalembetim.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |
| https://incineracaodedocumentosembetim.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |

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

Cobertura documentada dos lotes 01–03: **18/56**, sem equivaler a disponibilidade ou publicação.

Próximo lote, itens 19–24:

1. `escaneardocumentosembetim.arquindex.com.br`
2. `alfrescoembetim.arquindex.com.br`
3. `consultorialgpd-betim.arquindex.com.br`
4. `adequacaolgpd-betim.arquindex.com.br`
5. `dpoembetim.arquindex.com.br`
6. `canaldedenunciaslgpd-betim.arquindex.com.br`

Qualquer publicação futura continua condicionada a DNS ativo, TLS válido, HTTP verificável, raiz individual autorizada, backup anterior com hash e validação pública posterior.
