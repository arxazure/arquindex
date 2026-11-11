# Inventário Arquindex — lote 04/10 — 11/11/2026

**Escopo:** seis hosts 19–24 do manifesto `seo-regional/56-sites/manifest.json`.  
**Execução:** [GitHub Actions #43070864091](https://github.com/arxazure/arquindex/actions/runs/43070864091).  
**Artefato:** [inventario-56-lote04 #13878446401](https://github.com/arxazure/arquindex/actions/runs/43070864091/artifacts/13878446401).  
**Digest SHA-256 do ZIP:** `9b0752b4895d780f5e12f1ae81a60590cd305ef0d4e4d4b1a627a2678dd7116f`.

## Deduplicação e limites

- A fila ARQ-001–ARQ-238 permanece concluída; nenhuma ficha foi reaberta.
- ARQ-007 e ARQ-099 foram preservadas e não receberam nova divulgação.
- Nenhuma postagem foi criada para hosts sem DNS.
- A execução foi somente leitura e respeitou o limite de seis URLs.

## Resultado por URL

| URL | DNS | TLS/HTTP/SEO | Antes/depois | Backup | Sitemap/envio | Estado |
|---|---|---|---|---|---|---|
| https://escaneardocumentosembetim.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |
| https://alfrescoembetim.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |
| https://consultorialgpd-betim.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |
| https://adequacaolgpd-betim.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |
| https://dpoembetim.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |
| https://canaldedenunciaslgpd-betim.arquindex.com.br/ | NXDOMAIN | não verificável | sem alteração | não iniciado | não executado | bloqueada |

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

Cobertura documentada dos lotes 01–04: **24/56**, sem equivaler a disponibilidade ou publicação.

Próximo lote, itens 25–30:

1. `ecmembetim.arquindex.com.br`
2. `escanearprontuariomedicoembetim.arquindex.com.br`
3. `escaneardossiefuncionario-betim.arquindex.com.br`
4. `digitalizacaodepartamentopessoal-betim.arquindex.com.br`
5. `digitalizacaodedocumentosemcontagem.arquindex.com.br`
6. `guardadocumentalemcontagem.arquindex.com.br`

Qualquer publicação futura continua condicionada a DNS ativo, TLS válido, HTTP verificável, raiz individual autorizada, backup anterior com hash e validação pública posterior.
