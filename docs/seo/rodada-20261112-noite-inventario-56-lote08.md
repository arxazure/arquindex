# Rodada SEO/GEO/AEO — inventário de 56 subdomínios — lote 08

**Data da verificação:** 12/11/2026 (noite, America/Sao_Paulo)  
**Escopo:** itens 43–48 do inventário histórico em `seo-regional/56-sites/manifest.json`  
**Modo:** auditoria pública somente leitura; nenhuma alteração de produção

## Resultado executivo

Os seis nomes de Nova Lima retornaram **NXDOMAIN** (`[Errno -2] Name or service not known`) no runner do GitHub Actions. Sem resolução DNS não existe origem pública verificável; por isso TLS/SSL, HTTP/HTTPS, canonical, title, H1, meta description, viewport/mobile, robots, sitemap, links internos, conteúdo, CTA, WhatsApp e formulários não puderam ser validados.

O gate de segurança permaneceu fechado. Nenhum acesso FTP/HomeHost, backup, deploy, criação de página ou artigo, alteração de sitemap, envio a Google/Bing/IndexNow ou divulgação social foi executado.

## URLs auditadas

| Item | URL | Palavras no manifesto | DNS | Publicação comprovada | Estado |
|---:|---|---:|---|---|---|
| 43 | https://digitalizacaodedocumentosemnovalima.arquindex.com.br/ | 3.695 | NXDOMAIN | Não | Bloqueada por DNS |
| 44 | https://guardadocumentalemnovalima.arquindex.com.br/ | 3.606 | NXDOMAIN | Não | Bloqueada por DNS |
| 45 | https://gestaodocumentalemnovalima.arquindex.com.br/ | 3.562 | NXDOMAIN | Não | Bloqueada por DNS |
| 46 | https://incineracaodedocumentosemnovalima.arquindex.com.br/ | 3.696 | NXDOMAIN | Não | Bloqueada por DNS |
| 47 | https://escaneardocumentosemnovalima.arquindex.com.br/ | 3.651 | NXDOMAIN | Não | Bloqueada por DNS |
| 48 | https://alfrescoemnovalima.arquindex.com.br/ | 3.584 | NXDOMAIN | Não | Bloqueada por DNS |

A contagem de palavras acima é apenas o valor registrado no manifesto do repositório; não comprova que esse conteúdo esteja publicado.

## Evidências

- Manifesto verificado: `seo-regional/56-sites/manifest.json` — blob `6052e433c71f3a0e801fa1908d8a86b2d51a201c`
- Workflow: `.github/workflows/inventario-56-lote08-20261112.yml`
- Commit do workflow: `e72a89e7ebe334b01db9bdd2b3d54ca80d2af1c4`
- Execução: https://github.com/arxazure/arquindex/actions/runs/43331143650
- Resultado: `success`
- Artefato: `inventario-56-lote08` — ID `13993744182`
- Digest do artefato: `sha256:f95ed9c192d5358c06fd4efba7a549113193979315cd083307cf11a268e0e270`
- Job: `audit` — ID `131575858775`

## Controle de mudanças e deduplicação

- Melhorias publicadas nesta rodada: **0**.
- FTP/HomeHost: não acessado, pois não há DNS/origem/document root comprovados para estes hosts.
- Backup: não aplicável; nenhuma produção foi tocada.
- Sitemap e submissões: não realizados, pois não há URL publicável confirmada.
- Divulgação: não criada nem republicada; não existe página pública elegível.
- ARQ-007: preservada, sem repetição do workflow de identidade.
- ARQ-099: referência preservada, sem republicação.
- Indexação, posições e leads: não inferidos.

## Cobertura acumulada

**48/56 subdomínios inventariados e documentados.** Isto representa cobertura de auditoria, não publicação nem disponibilidade. Os lotes anteriores permanecem registrados em `docs/seo/`.

## Próximo lote registrado (49–54)

1. `consultorialgpd-novalima.arquindex.com.br`
2. `adequacaolgpd-novalima.arquindex.com.br`
3. `dpoemnovalima.arquindex.com.br`
4. `canaldedenunciaslgpd-novalima.arquindex.com.br`
5. `ecmemnovalima.arquindex.com.br`
6. `escanearprontuariomedicoemnovalima.arquindex.com.br`

Antes de qualquer publicação futura, cada host exige DNS resolvido, origem e document root confirmados, backup individual, validação pública HTTP 200/canonical/conteúdo e comprovação do atendimento local.
