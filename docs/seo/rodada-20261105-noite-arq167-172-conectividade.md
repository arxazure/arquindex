# Rodada noturna — ARQ-167–172 — 05/11/2026

## Evidência executada
- Workflow read-only: https://github.com/arxazure/arquindex/actions/runs/42106259703
- Artefato JSON: https://github.com/arxazure/arquindex/actions/runs/42106259703/artifacts/13452556308
- Commit do auditor: c538b3ba2f727f27ad8d67ca461d5b933dde5052
- Resultado do job: success (execução da auditoria, **não** sucesso dos sites).
- Seis hosts resolvem para 177.234.150.42.
- ARQ-167: handshake TLSv1.3 válido, HTTP página/robots/sitemap encerrou conexão.
- ARQ-168, 169, 170, 171, 172: TLS não validado por reset; página/robots/sitemap sem resposta HTTP.
- Status 200, canonical, H1, mobile, conteúdo, CTAs, formulários e sitemap: **não verificáveis nesta rodada**. Não confundir falha de conexão do runner com prova de indisponibilidade global.

## Decisão e ações pendentes
1. Investigar no provedor a origem de resets TCP/TLS para 177.234.150.42 e logs de vhost/firewall; comparar outro ponto de rede e validar DNS, certificado/SNI e resposta HTTP por host.
2. Confirmar root FTPS de cada host e backup íntegro individual antes de qualquer escrita; ARQ-172 já teve TARGET_NOT_FOUND em tentativa anterior.
3. Após restabelecer respostas, reexecutar auditoria por host, revisar canonical/title/H1/description/viewport/robots/sitemap/links e validar mobile visualmente (o auditor atual **não** mede overflow nem layout).
4. Não atualizar sitemap ou IndexNow sem URLs canônicas acessíveis e comprovadas; preservar ARQ-167 e ARQ-169 publicadas anteriormente até confirmar estado.
5. Inventário de 56 hosts **não** foi reexecutado nesta rodada; status histórico não deve ser tratado como estado atual.

## Log por ficha
| Ficha | Antes (fila) | Depois da auditoria | Commit de conteúdo | Publicação | Sitemap/envio | Estado |
|---|---|---|---|---|---|---|
| ARQ-167 | Publicada anteriormente, aguarda métricas | DNS/TLS ok; HTTP sem resposta | Nenhum | Não | Não | bloqueada por conectividade |
| ARQ-168 | Divergência São Paulo/BH, identidade ausente | DNS ok; TLS/HTTP reset | Nenhum | Não | Não | bloqueada por conectividade e atendimento |
| ARQ-169 | Publicada anteriormente, revisão de preços/fontes | DNS ok; TLS/HTTP reset | Nenhum | Não | Não | bloqueada por conectividade |
| ARQ-170 | Revisar logística e saúde | DNS ok; TLS/HTTP reset | Nenhum | Não | Não | bloqueada por conectividade e atendimento |
| ARQ-171 | Diferenciar conteúdo Decreto 10.278/2020 | DNS ok; TLS/HTTP reset | Nenhum | Não | Não | bloqueada por conectividade |
| ARQ-172 | FTPS TARGET_NOT_FOUND anteriormente | DNS ok; TLS/HTTP reset | Nenhum | Não | Não | bloqueada por conectividade e origem |
 
ARQ-007 e ARQ-099 preservadas. Nenhum deploy, post social ou submissão. Zero melhorias publicadas nesta rodada por falta de pré-condições técnicas.
