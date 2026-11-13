# Rodada SEO/GEO/AEO — inventário de 56 subdomínios — lote 09

**Data da verificação:** 13/11/2026 (manhã, America/Sao_Paulo)  
**Escopo:** itens 49–54 do inventário histórico em `seo-regional/56-sites/manifest.json`  
**Modo:** auditoria pública somente leitura; nenhuma alteração de produção

## Resultado executivo

Os seis nomes de Nova Lima retornaram **NXDOMAIN** (`[Errno -2] Name or service not known`) no runner do GitHub Actions. Sem resolução DNS não existe origem pública verificável; por isso TLS/SSL, HTTP/HTTPS, canonical, title, H1, meta description, viewport/mobile, robots, sitemap, links internos, conteúdo, CTA, WhatsApp e formulários não puderam ser validados.

O gate de segurança permaneceu fechado. Nenhum acesso FTP/HomeHost, backup, deploy, criação de página ou artigo, alteração de sitemap, envio a Google/Bing/IndexNow ou divulgação social foi executado.

## URLs auditadas

| Item | URL | DNS | Publicação comprovada | Estado |
|---:|---|---|---|---|
| 49 | https://consultorialgpd-novalima.arquindex.com.br/ | NXDOMAIN | Não | Bloqueada por DNS |
| 50 | https://adequacaolgpd-novalima.arquindex.com.br/ | NXDOMAIN | Não | Bloqueada por DNS |
| 51 | https://dpoemnovalima.arquindex.com.br/ | NXDOMAIN | Não | Bloqueada por DNS |
| 52 | https://canaldedenunciaslgpd-novalima.arquindex.com.br/ | NXDOMAIN | Não | Bloqueada por DNS |
| 53 | https://ecmemnovalima.arquindex.com.br/ | NXDOMAIN | Não | Bloqueada por DNS |
| 54 | https://escanearprontuariomedicoemnovalima.arquindex.com.br/ | NXDOMAIN | Não | Bloqueada por DNS |

## Evidências

- Workflow: `.github/workflows/inventario-56-lote09-20261113.yml`
- Commit do workflow: `62ebc95969709c791cf6991e54bf30f70e22b25d`
- Execução: https://github.com/arxazure/arquindex/actions/runs/43419077706
- Resultado: `success`
- Artefato: `inventario-56-lote09` — ID `14032238606`
- Digest do artefato: `sha256:87ff65857f791cfb13585fa151dab4ff9be81105cdcaa37450706e36e83bbfa9`
- Job: `audit` — ID `131864236298`

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

**54/56 subdomínios inventariados e documentados.** Isto representa cobertura de auditoria, não publicação nem disponibilidade. Os lotes anteriores permanecem registrados em `docs/seo/`.

## Lote final registrado (55–56)

1. `escaneardossiefuncionario-novalima.arquindex.com.br`
2. `digitalizacaodepartamentopessoal-novalima.arquindex.com.br`

Antes de qualquer publicação futura, cada host exige DNS resolvido, origem e document root confirmados, backup individual, validação pública HTTP 200/canonical/conteúdo e comprovação do atendimento local.
