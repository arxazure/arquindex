# Rodada executora SEO/GEO/AEO — 19/10/2026, manhã (Brasília)

## Escopo e acesso
- Repositório efetivo: `arxazure/arquindex`, branch `master`.
- Permissão confirmada: administração e escrita.
- Destino de publicação: Homehost por FTP TLS, com backup e rollback no workflow.
- Fichas lidas no plano versão 2: ARQ-010 a ARQ-015.
- URLs auditadas: 6. URLs alteradas: 2. Nenhuma URL nova foi criada.

## Auditoria das seis URLs

| ID | URL | Resultado renderizado | Decisão |
|---|---|---|---|
| ARQ-010 | https://governanca.arquindex.com.br/bh.html?post=como-digitalizar-documentos-em-qualquer-impressora | Artigo distinto; canonical próprio; antes havia dois H1, sem identidade oficial e sem atendimento moderno | Corrigida e publicada |
| ARQ-011 | https://7-motivos-contar-dpo-terceirizado.arquindex.com.br/?post=ocr-para-documentos | Parâmetro não altera conteúdo; canonical, title e H1 continuam LGPD/DPO da raiz | Não promover |
| ARQ-012 | https://7-motivos-contar-dpo-terceirizado.arquindex.com.br/?post=maneiras-de-fazer-a-digitalizacao-de-documentos | Mesmo HTML e intenção da raiz LGPD/DPO | Não promover |
| ARQ-013 | https://7-motivos-contar-dpo-terceirizado.arquindex.com.br/?post=digitalizacao-de-documentos-valor-real | Mesmo HTML e intenção da raiz LGPD/DPO | Não promover |
| ARQ-014 | https://empresas.arquindex.com.br/?MD | Parâmetro ignorado; canonical permanece na raiz | Não promover |
| ARQ-015 | https://escolher-servico-confiavel-digitalizacao-documentos-brasil.arquindex.com.br/erros-comuns.html?post=conarq-novas-normas-para-digitalizacao-de-documentos | Artigo distinto, mas dois H1, identidade incompleta e canonical incorreto para caminho no domínio principal | Não promover o parâmetro; revisar arquitetura em rodada própria |

## Alterações publicadas

### ARQ-010
- Identidade visual oficial aplicada ao arquivo físico `bh.html`.
- Atendimento moderno único publicado: chat, WhatsApp +55 31 97363-2725 e proposta.
- Widgets antigos removidos.
- H1 contextual da página-base é rebaixado somente quando o artigo parametrizado confirmado está renderizado; o artigo fica com exatamente um H1.
- Title, description e canonical do artigo preservados.
- Hash público: `sha256:2f8802800bf175f20f80ab43649dcefd36b13f7c30c1d56591de6213d7dd1f48`.

### Guia CONARQ canônico
URL: https://www.arquindex.com.br/blog-original/conarq-novas-normas-para-digitalizacao-de-documentos/

Antes:
- Title: `CONARQ: novas normas para digitalização | Arquindex`.
- H1: `CONARQ: novas normas para digitalização`.
- Texto sugeria mudança recente sem identificar ato novo.

Depois:
- Title: `CONARQ na Digitalização: Requisitos e Proposta | Arquindex`.
- H1: `CONARQ na digitalização: o que conferir antes de contratar`.
- Description voltada a referências, entregáveis e critérios de conferência.
- Cronologia corrigida: Resolução CONARQ nº 48, de 10/11/2021, e Decreto nº 10.278, de 18/03/2020; conteúdo classificado como revisão técnica perene, não notícia.
- Inserida matriz para comparar propostas por item do acervo, requisito, entrega, evidência e inclusão comercial.
- Inseridas fontes primárias, limites jurídicos, revisão em 19/10/2026 e CTAs contextuais para serviço, guia de custo e proposta com UTM.
- Canonical próprio preservado.
- Hash público: `sha256:f35f05daa77fcd528e0256407cb11c7aa7404d0177922b76ec256dc64ea85600`.

Fontes primárias:
- https://www.gov.br/conarq/pt-br/legislacao-arquivistica/resolucoes-do-conarq/resolucao-no-48-de-10-de-novembro-de-2021
- https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10278.htm

## Backup, commits e workflows
- Backup da identidade ARQ-010: registrado no artefato `rodada-seo-20261019-manha` do workflow; o caminho não foi reproduzido no resumo de logs e não é presumido aqui.
- Backup do atendimento ARQ-010: `/seo-backups/atendimento-unico-20261019T114338Z/bcd9558195880cc056be.html`.
- Backup final conjunto: `/seo-backups/rodada-20261019-manha-20261019T114356Z/`.
- Commit da publicação: https://github.com/arxazure/arquindex/commit/5ebe41798123b59fd7adcea23afdc8444b756ba1
- Workflow de publicação: https://github.com/arxazure/arquindex/actions/runs/39246668443 — sucesso.
- Commit da validação: https://github.com/arxazure/arquindex/commit/f0a633b16ad820e2f55e8de83ee7490fc80110b3
- Workflow de validação: https://github.com/arxazure/arquindex/actions/runs/39246941584 — job `visual` concluído com sucesso.

A primeira tentativa, https://github.com/arxazure/arquindex/actions/runs/39246568790, falhou antes de escrever porque o seletor recebeu URL parametrizada. Foi corrigida para o arquivo físico; não houve publicação parcial nessa tentativa.

## Validação pública
Nos viewports 390×844 e 1440×900:
- HTTP 200 nas duas URLs.
- Exatamente uma canonical e um H1.
- `scrollWidth == clientWidth`: 390/390 e 1440/1440.
- Ausência de `noindex`.
- ARQ-010: logo oficial, menu responsivo, um `#arq-floating`, zero widgets antigos.
- Guia CONARQ: novo title/H1/description e matriz presentes.

## Search Console e Bing Webmaster
Período completo mais recente usado: 19/09–16/10/2026. Comparação: 22/08–18/09/2026.

Google Search Console, consulta+URL:
- ARQ-010 parametrizada: 6 impressões, 0 cliques, CTR 0%, posição média 97, consulta “extração de dados digitalizados”.
- Período anterior trouxe a URL-base `/bh.html`, não a parametrizada: 8 impressões, 0 cliques, posição média 14,625 para “governança de dados belo horizonte”.
- Não há amostra comparável suficiente para atribuir tendência; os dados antecedem as alterações.
- O guia CONARQ canônico não retornou linha no recorte filtrado; isso não prova ausência de indexação.

Bing Webmaster, mesmos períodos:
- Recorte atual de consultas contendo digitaliza/CONARQ/OCR: 12 linhas, 20 impressões e 2 cliques no total; os 2 cliques vieram de uma consulta sobre digitalização de pastas condominiais em Santos.
- Recorte anterior: 13 linhas, 25 impressões e 6 cliques.
- A composição de consultas mudou e as amostras são pequenas; não há causalidade demonstrada.

## Sitemap, submissões e redes
- Nenhuma URL nova foi criada e as duas canônicas já existiam; sitemap não foi alterado.
- Não houve reenvio ao Google, Bing ou IndexNow. Nenhuma indexação foi alegada.
- Nenhuma publicação social foi criada nesta rotina, evitando duplicação com a fila social.

## Próximo cursor
ARQ-016. Na próxima rodada, auditar ARQ-016 a ARQ-021, reservando pelo menos uma ficha ainda não trabalhada e sem promover parâmetros que não produzam conteúdo próprio.
