# Rodada SEO/GEO/AEO — inventário de 56 subdomínios — lote 07

**Data da verificação:** 12/11/2026 (tarde, America/Sao_Paulo)  
**Escopo:** itens 37–42 do inventário histórico em `seo-regional/56-sites/manifest.json`  
**Modo:** auditoria pública somente leitura; nenhuma alteração de produção

## Resultado executivo

Os seis nomes de Contagem retornaram **NXDOMAIN** (`[Errno -2] Name or service not known`) no runner do GitHub Actions. Sem resolução DNS não existe origem pública verificável; por isso TLS/SSL, HTTP/HTTPS, canonical, title, H1, meta description, viewport/mobile, robots, sitemap, links internos, conteúdo, CTA, WhatsApp e formulários não puderam ser validados.

O gate de segurança permaneceu fechado. Nenhum acesso FTP/HomeHost, backup, deploy, criação de página ou artigo, alteração de sitemap, envio a Google/Bing/IndexNow ou divulgação social foi executado.

## URLs auditadas

| Item | URL | DNS | Publicação comprovada | Estado |
|---:|---|---|---|---|
| 37 | https://dpoemcontagem.arquindex.com.br/ | NXDOMAIN | Não | Bloqueada por DNS |
| 38 | https://canaldedenunciaslgpd-contagem.arquindex.com.br/ | NXDOMAIN | Não | Bloqueada por DNS |
| 39 | https://ecmemcontagem.arquindex.com.br/ | NXDOMAIN | Não | Bloqueada por DNS |
| 40 | https://escanearprontuariomedicoemcontagem.arquindex.com.br/ | NXDOMAIN | Não | Bloqueada por DNS |
| 41 | https://escaneardossiefuncionario-contagem.arquindex.com.br/ | NXDOMAIN | Não | Bloqueada por DNS |
| 42 | https://digitalizacaodepartamentopessoal-contagem.arquindex.com.br/ | NXDOMAIN | Não | Bloqueada por DNS |

## Evidências

- Workflow: `.github/workflows/inventario-56-lote07-20261112.yml`
- Commit do workflow: `de964e1468c56d7ace132fdf047eb0bb29fb9668`
- Execução: https://github.com/arxazure/arquindex/actions/runs/43272648388
- Resultado: `success`
- Artefato: `inventario-56-lote07` — ID `13969370979`
- Digest do artefato: `sha256:a468ae89f57b66947e7720487bf2de743f227ef026cf46cbee89e35083cdcd35`
- Job: `audit` — ID `131372866693`

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

**42/56 subdomínios inventariados e documentados.** Isto representa cobertura de auditoria, não publicação nem disponibilidade. Os lotes anteriores permanecem registrados em `docs/seo/`.

## Próximo lote registrado (43–48)

1. `digitalizacaodedocumentosemnovalima.arquindex.com.br`
2. `guardadocumentalemnovalima.arquindex.com.br`
3. `gestaodocumentalemnovalima.arquindex.com.br`
4. `incineracaodedocumentosemnovalima.arquindex.com.br`
5. `escaneardocumentosemnovalima.arquindex.com.br`
6. `alfrescoemnovalima.arquindex.com.br`

Antes de qualquer publicação futura, cada host exige DNS resolvido, origem e document root confirmados, backup individual, validação pública HTTP 200/canonical/conteúdo e comprovação do atendimento local.
