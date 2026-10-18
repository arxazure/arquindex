# Rodada SEO/GEO/AEO — 2026-10-18, tarde

## Escopo e deduplicação
- Cursor inicial: ARQ-007.
- ARQ-099 preservada; nenhuma republicação ou divulgação.
- Seis URLs auditadas: formulário comercial, ARQ-007, ARQ-008, ARQ-009, ARQ-010 e ARQ-011.
- Três melhorias publicadas: ARQ-007, ARQ-008 e ARQ-009.
- Nenhuma publicação social feita nesta rodada.

## Auditoria antes da alteração

| ID | URL | Evidência anterior | Decisão |
|---|---|---|---|
| FUNIL | https://www.arquindex.com.br/solicitar-proposta-contratacao.html | HTTP acessível no navegador, canonical próprio, 1 H1, index/follow, viewport, formulário renderizado e um escape direto para WhatsApp | Preservar; formulário já publicado e funcional como destino principal |
| ARQ-007 | https://consultoria-adequacao-lgpd-pequenas-empresas.arquindex.com.br/ | Title longo; H1 genérico; canonical próprio; og:url incorreto para /index-seo.html; 8 links diretos ao WhatsApp; nenhum link ao formulário | Corrigir metadados, H1, conteúdo útil e funil |
| ARQ-008 | https://faz-consultoria-adequacao-lgpd.arquindex.com.br/como-escolher.html | Canonical incorreto para caminho no domínio www; title repetia Arquindex três vezes; 3 links diretos ao WhatsApp; nenhum link ao formulário | Corrigir canonical/title/H1, adicionar checklist e funil |
| ARQ-009 | https://servicos-consultoria-adequacao-lgpd-oferece-pequenas.arquindex.com.br/diagnostico-completo.html | Canonical incorreto para caminho no domínio www; title repetia Arquindex três vezes; nenhum CTA WhatsApp ou formulário | Corrigir canonical/title/H1, adicionar matriz de entregas e funil |
| ARQ-010 | https://governanca.arquindex.com.br/bh.html?post=como-digitalizar-documentos-em-qualquer-impressora | Canonical para /bh.html sem parâmetro; og:url idem; title do artigo; dois H1 visíveis | Não promover o parâmetro; revisar arquitetura e H1 em rodada própria |
| ARQ-011 | https://7-motivos-contar-dpo-terceirizado.arquindex.com.br/?post=ocr-para-documentos | Parâmetro não gerou página OCR distinta; canonical/og:url apontam para a raiz e H1 continua LGPD/DPO | Não promover como URL OCR; manter cursor técnico |

## Alterações publicadas

| ID | Title anterior | Title novo | Canonical depois | Conteúdo/funil |
|---|---|---|---|---|
| ARQ-007 | Consultoria Adequacao Lgpd Pequenas Empresas \| consultoria LGPD e DPO as a Service em Belo Horizonte \| Arquindex | Consultoria LGPD para Pequenas Empresas \| Arquindex | https://consultoria-adequacao-lgpd-pequenas-empresas.arquindex.com.br/ | Matriz de etapas/aceite; distinção consultoria x DPO contínuo; CTA principal ao formulário com UTM; um link WhatsApp discreto |
| ARQ-008 | O que faz uma consultoria de adequação LGPD - Como escolher \| Arquindex \| Arquindex \| Arquindex | Como Escolher Consultoria LGPD \| Critérios Práticos \| Arquindex | https://faz-consultoria-adequacao-lgpd.arquindex.com.br/como-escolher.html | Checklist de comparação e perguntas comerciais; CTA principal ao formulário com UTM; um link WhatsApp discreto |
| ARQ-009 | Quais serviços uma consultoria de adequação LGPD oferece para pequenas empresas - Diagnóstico completo \| Arquindex \| Arquindex \| Arquindex | Consultoria LGPD: Diagnóstico e Entregas \| Arquindex | https://servicos-consultoria-adequacao-lgpd-oferece-pequenas.arquindex.com.br/diagnostico-completo.html | Matriz diagnóstico→plano→aceite; CTA principal ao formulário com UTM; um link WhatsApp discreto |

As três páginas também receberam descrições distintas, um único H1 coerente, og:url próprio e referências primárias para a LGPD e a ANPD. Não foram adicionadas alegações de conformidade automática, cases, preços ou resultados não comprovados.

## Backup, commit, workflow e validação
- Commit executor: https://github.com/arxazure/arquindex/commit/05a9179c18a04ee0d7359bdba4db78a5d2263c14
- Workflow: https://github.com/arxazure/arquindex/actions/runs/39150970825
- Job: 117744368017
- Resultado: success.
- Backup remoto: /seo-backups/queue-20261018-afternoon-20261018T174435Z/
- Hash anterior ARQ-007: 1f111198988ca6da6746de4d46e72dd46fbc774f7ff788ddf970dd41137d6f9b
- Hash publicado ARQ-007: 7e072c72676600dcd3f18d4bb00e82490c8148ef85c7ac4ed78898a0ccae8197
- Hash anterior ARQ-008: c0b281500a11d288bd44a6ebc27ce05a80b3aa39cc8a5c0c1537759651ba8651
- Hash publicado ARQ-008: 0238aff1173c2a35304cadca6a9e0e28b73e0bed9e2221408d489281bf571d87
- Hash anterior ARQ-009: 36053d47e78b0735b9f99fc148b368023c75486863a912bbd8122d46edf2f2a5
- Hash publicado ARQ-009: f77d2ec31cd8f1dea27a63fd44e7d3805e1aa67ff6995b5b809c4bc606e6a890
- Workflow e segunda leitura pública confirmaram HTTP 200, canonical, og:url, title, um H1, descrição, viewport, indexabilidade, conteúdo novo, formulário e fallback WhatsApp nas três URLs.
- Nenhum rollback foi acionado.

## Search Console — linha de base, períodos completos
Propriedade: sc-domain:arquindex.com.br. Período atual: 2026-09-18 a 2026-10-15. Anterior: 2026-08-21 a 2026-09-17.

| ID | Atual | Anterior | Leitura |
|---|---|---|---|
| ARQ-007 | 0 cliques, 4 impressões, CTR 0%, posição média 51,25 | 0 cliques, 1 impressão, CTR 0%, posição 11 | Amostra insuficiente; não atribuir tendência |
| ARQ-008 | 0 cliques, 3 impressões, CTR 0%, posição média 8 | Sem linha retornada | Presença inicial, amostra insuficiente |
| ARQ-009 | 0 cliques, 2 impressões, CTR 0%, posição média 11,5 | Sem linha retornada | Presença inicial, amostra insuficiente |

As alterações foram publicadas em 2026-10-18 e não podem explicar métricas consolidadas anteriores.

## Sitemap e submissões
Nenhuma URL nova foi criada nesta rodada. Os canonicals corrigidos são das próprias páginas existentes, portanto não houve atualização ou reenvio de sitemap. Nenhuma submissão ao Google, Bing ou IndexNow foi alegada.

## Próximo cursor
- Retomar em ARQ-010.
- ARQ-010: decidir a arquitetura correta do conteúdo parametrizado e eliminar o H1 duplicado sem criar URL sobreposta.
- ARQ-011: não promover o parâmetro de OCR; verificar se existe URL editorial própria antes de qualquer ação.
- ARQ-012: auditar conteúdo/canonical e concluir o trio de parâmetros.
