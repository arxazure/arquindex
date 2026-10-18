# Rodada SEO/GEO/AEO — 2026-10-18, noite

## Escopo e deduplicação
- Seis URLs auditadas: home, ARQ-007, ARQ-008, ARQ-009, ARQ-010 e ARQ-011.
- Três melhorias publicadas: ARQ-007, ARQ-008 e ARQ-009.
- ARQ-007 já tinha identidade oficial verificada; ela não foi reaplicada.
- ARQ-099 não foi alterada nem divulgada novamente.
- A notícia/análise de IA documental já publicada no mesmo dia não foi duplicada.
- Nenhuma publicação social foi criada nesta rodada.

## Auditoria antes da alteração

| URL | Identidade oficial | Atendimento renderizado | Diagnóstico |
|---|---:|---:|---|
| https://www.arquindex.com.br/ | Sim | Um botão #arq-floating | Home já possui o novo pré-atendimento; nenhuma alteração |
| https://consultoria-adequacao-lgpd-pequenas-empresas.arquindex.com.br/ | Sim | Dois controles: .aq-brand-wa e #wa-widget-send-button | Duplicidade reproduzida; substituir pelo componente único |
| https://faz-consultoria-adequacao-lgpd.arquindex.com.br/como-escolher.html | Não | Nenhum | Aplicar identidade e atendimento |
| https://servicos-consultoria-adequacao-lgpd-oferece-pequenas.arquindex.com.br/diagnostico-completo.html | Não | Nenhum | Aplicar identidade e atendimento |
| https://governanca.arquindex.com.br/bh.html?post=como-digitalizar-documentos-em-qualquer-impressora | Não | Nenhum | Mantém dois H1 e arquitetura parametrizada; não alterada nesta rodada |
| https://7-motivos-contar-dpo-terceirizado.arquindex.com.br/?post=ocr-para-documentos | Não | Um widget antigo | Parâmetro não representa conteúdo OCR distinto; não promover nem alterar sem decidir a URL correta |

## Alterações publicadas
- ARQ-007: removidos código e carregadores do widget antigo, removido .aq-brand-wa e instalado exatamente um #arq-floating.
- ARQ-008: aplicada identidade semelhante à home — logo oficial, cabeçalho/menu, cores, tipografia, rodapé e responsividade — e instalado atendimento único.
- ARQ-009: aplicada a mesma identidade e instalado atendimento único.
- O componente oferece: Conversar no chat, Ir direto ao WhatsApp e Solicitar proposta detalhada.
- Title, H1, canonical, meta description e indexabilidade foram preservados por validação antes/depois.

## GitHub, FTP, backup e evidências
- Script reutilizável: scripts/aplicar-atendimento-unico.py
- Commit do script: https://github.com/arxazure/arquindex/commit/d7439d4c10f84881ccffd5df0b8a858426d3e365
- Commit da correção de teste: https://github.com/arxazure/arquindex/commit/0d9494f52e02f21a9aeaa2bff2d6a4a208a274b5
- Workflow inicial de identidade: https://github.com/arxazure/arquindex/actions/runs/39178000228
  - ARQ-008 e ARQ-009: identidade publicada e verificada.
  - Etapa de atendimento falhou antes da escrita por falso positivo no teste do nome .aq-brand-wa citado no deduplicador.
- Workflow de atendimento: https://github.com/arxazure/arquindex/actions/runs/39178102756
- Job: 117824879752
- Resultado: success.
- Backup: /seo-backups/atendimento-unico-20261018T234933Z/
- Hash publicado ARQ-007: 9f88d7953c9353efb1b9965e7a328264879c4712a6bdd63bfbb74348d74de3b6
- Hash publicado ARQ-008: 0dc71942478bad6eeeca5417fa0cbe6df46cd0a96929849488daf362d4e6d82c
- Hash publicado ARQ-009: b7e4600cd136d95da2a29f291b6218719d2ead1df1b13f00492c49c6a995081f

## Validação renderizada
- Workflow: https://github.com/arxazure/arquindex/actions/runs/39178284717
- Job: 117825415462
- Mobile: viewport e scrollWidth 390/390 nas três URLs.
- Desktop: viewport e scrollWidth 1440/1440 nas três URLs.
- Em cada página: HTTP 200, um cabeçalho, um rodapé, logo carregado, um H1, um canonical, indexável, um #arq-floating, um toggle e zero widgets antigos.
- O painel foi aberto por teste; chat, WhatsApp e proposta detalhada ficaram visíveis.
- Capturas e checks.json: artifact visual-atendimento-arq007-arq009.

## Sitemap e descoberta
As três URLs já existiam, e seus canonicals/conteúdo SEO não foram trocados nesta rodada. Os sitemaps corrigidos na rodada anterior permaneceram válidos. Não houve reenvio ao Google, Bing ou IndexNow e nenhuma indexação foi alegada.

## Outros destinos
- Homehost: publicação confirmada.
- Railway, Hostinger e ChatGPT Site: não alterados nesta execução. Não existe neste workflow um mapeamento confirmado dessas três páginas para destinos equivalentes; não foi alegado deploy sem evidência.

## Próximo cursor
- ARQ-010: decidir a arquitetura do conteúdo parametrizado e corrigir dois H1 sem criar página sobreposta.
- ARQ-011: não promover o parâmetro OCR; localizar URL editorial correta.
- ARQ-012: concluir auditoria de parâmetro/canonical.
- Expandir identidade e atendimento em lotes pequenos somente após inventário renderizado, mantendo uma página por intenção.
