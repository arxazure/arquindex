# Top10 Google: painel privado com coleta verificável

## Implantação reutilizada

Reutiliza os serviços `capture-hub` e `top10-google-dashboard` do projeto Railway Arquindex Capture Hub. Não cria projeto, Function, banco ou agendamento. O Hub conserva Google OAuth e o cookie existente; `/admin/top10` e `/admin/top10/data` exigem a mesma sessão administrativa. O backend aceita somente leitura autenticada com segredo interno, sem CORS público, e redireciona `/` para o Hub.

- `server.mjs`: código completo do backend Bun, também executável como Function existente.
- `capture-hub.tsx`: fonte completa do Hub existente com rota de proxy privada e link de navegação; fluxo OAuth preservado.
- `index.html`: entrada neutra sem métricas nem dados privados.
- Verificação: `node --test top10-google/*.test.mjs`.

## Configuração privada

`TOP10_INTERNAL_TOKEN`: segredo aleatório de pelo menos 32 caracteres, igual somente nos dois serviços. Nunca versionar. `TOP10_SNAPSHOT_JSON`: coleta no backend, fora do repositório. Conservar `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` e `SESSION_SECRET` existentes no Hub.

Contrato do snapshot: `schemaVersion: 1`, `collectedAt` ISO UTC, `metrics` com `current`/`previous` numéricos ou null e `lowerIsBetter` quando apropriado; `sources` com conta, disponibilidade, período e hora da consulta; `pages`, `channels`, `receipts`, `queue` e `evidence`. Toda evidência vem das respostas dos conectores. Consulta vazia não confirma valor zero. Campos do provedor são escapados antes da renderização.

As datas do resumo vêm de `periods.current` e `periods.previous`, cada um com `start` e `end` no formato `YYYY-MM-DD`. Exemplo: `{"current":{"start":"2026-10-01","end":"2026-10-21"},"previous":{"start":"2026-09-10","end":"2026-09-30"}}`. Não há datas fixas no HTML. Snapshots anteriores sem `periods` continuam aceitos, com aviso explícito de períodos não informados e orientação para conferir cada fonte. Ao renovar a coleta, preencher os dois períodos após conferir as respostas; não inferi-los da data de coleta. O painel não presume que períodos fornecidos tenham duração igual.

O backend valida o objeto principal, as listas e seus campos usados na renderização, valores numéricos, datas dos períodos e contagens da fila. Estrutura inválida retorna 503 com cache privado desativado nas duas rotas, sem expor o conteúdo da coleta. Campos numéricos ausentes ou null permanecem sem dados. Unidades também são escapadas como texto.

QA: oito testes Node aprovados localmente, incluindo troca de períodos, compatibilidade com snapshot sem datas, estruturas inválidas nas duas rotas e renderização com campos ausentes. `.github/workflows/top10-google-tests.yml` executa apenas testes com Node 24 em PRs que alteram este módulo; não contém credenciais, publicação ou deploy. Os testes do Hub simulam OAuth/sessão e upstream; login Google real, configurações privadas e correspondência entre o snapshot e as fontes ainda exigem validação no ambiente autorizado. Não registrar cookies, tokens ou o snapshot privado nos logs da revisão.

## Fontes verificadas nesta execução

Windsor: Search Console `sc-domain:arquindex.com.br`, Bing Webmaster `https://arquindex.com.br/`, GA4 `311737260`, Instagram `17841429848911605`. Metricool: marca `7366010`, organização LinkedIn `94842130`, leitura de posts e agenda. GSC Wizard recusou chamadas com `subscription_required`; não é dependência da coleta via Windsor.

Comparação de busca: 01–21/10/2026 contra 10–30/09/2026, 21 dias cada. Totais Google consultados sem dimensão página; consulta de páginas separada não é somada para formar totais. CTR = cliques / impressões, diferença em pontos percentuais. Posição menor significa melhoria. Ausentes, iguais ou sem base comparável ficam cinza; base zero não recebe percentual infinito. O provedor não retornou maturidade nem hora de preenchimento do cache: informar essa limitação. GA4 filtrado para os dois hostnames institucionais retornou nenhuma linha; não interpretar como ausência comprovada de visitas ou leads.

A coleta é um instantâneo consultado nos conectores autorizados nesta sessão, armazenado em variável privada. Não é uma integração contínua entre o runtime e o MCP do ChatGPT. Recarregar o painel recalcula cores, mas não atualiza fontes. Renovar `TOP10_SNAPSHOT_JSON` somente após nova leitura autorizada e conferência das respostas. Para sincronização autônoma ainda faltam credenciais de API de servidor ou exportação autorizada para armazenamento privado; não copiar tokens do ChatGPT nem criar outro serviço para simular integração.

## Publicação e permissões

Instagram, LinkedIn e Google Business Profile têm ações de escrita anunciadas pelo Windsor. A presença da ação não comprova um teste de publicação bem-sucedido. LinkedIn com imagem exige `create_image_post` e `image_url` ou `image_urn`; Google exige `photo_url` para campanha visual; Instagram exige `image_url`. O runner e a fila existentes não são alterados por este módulo. IDs aceitos sem permalink não são tratados como visibilidade pública; URL retornada pela API é evidência do provedor, não teste de acesso anônimo.

Facebook orgânico está ligado a outra identidade; não confundir a conta de anúncios Arquindex com permissão orgânica. TikTok tem nomes diferentes entre conectores e requer conferência. YouTube está listado, mas não houve validação de upload. Reddit, X, Threads, Blogger e WhatsApp Status não têm escrita comprovada nesta auditoria. Bing Places não equivale à API de métricas Bing Webmaster. O painel não envia publicações e não reprocessa estados desconhecidos.

## Limites e preservação

Ranking regional, inspeção atual de indexação, eventos de leitura/scroll, conversões qualificadas e citações em IA ainda não integrados. As metas 3 posts/dia/canal, 100 páginas e 15 artigos continuam planejamento. Não foram verificadas como execução.

Manter PR #36 isolado: **não fazer merge em master nem implantar na HomeHost antes da validação do backup integral da issue #28**. Implantar diretamente apenas as duas fontes dos serviços Railway existentes. Manter automações, fila e demais aplicações. Rollback por revisão anterior do serviço; não restaurar o antigo backend público com dados privados. Nenhum snapshot privado ou segredo deve entrar no GitHub.
