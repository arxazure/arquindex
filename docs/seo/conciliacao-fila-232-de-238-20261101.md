# Conciliação da fila SEO/GEO/AEO — 2026-11-01

## Fonte e verificação
- Fonte: `seo/fila-seo-geo-aeo.csv` no branch `master`.
- 232 IDs únicos sequenciais de ARQ-001 a ARQ-232; nenhuma duplicidade de ID.
- ARQ-233 a ARQ-238 **não existem no CSV**. O total 238 do plano não pode ser tratado como 238 URLs cadastradas/auditadas.
- Próximo passo: recuperar a fonte original das seis fichas, confirmar URL/intenção/serviço e verificar duplicidade antes de adicioná-las. Não gerar páginas por preenchimento de contagem.

## Inventário de subdomínios
- A fila operacional referencia 157 hosts distintos sob `*.arquindex.com.br` (excluído `www`); esse conjunto **não é equivalente** ao manifesto histórico de 56 subdomínios.
- Evidência histórica: `docs/seo/auditoria-56-publicos-20261018.md`, com 55/56 NXDOMAIN naquela data; **não inferir DNS atual**.
- Workflow de auditoria existente: `.github/workflows/auditar-56-publicos.yml` (somente leitura, DNS/TLS/HTTP/SEO, artefato e issue #10). Reexecutar antes de afirmar publicação atual dos 56.

## Segurança e publicação
- Nenhuma alteração em páginas, DNS, sitemap, IndexNow, Search Console ou canais sociais nesta conciliação.
- Produção web principal confirmada anteriormente no Railway, branch `railway-production-2026`; não pressupor HomeHost como origem ativa da página principal.
- ARQ-007 e ARQ-099 preservadas, sem nova divulgação.
- Estado: **reconciliação documental, não auditoria HTTP das seis fichas ausentes nem deploy**.
