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

## Histórico de fontes registrado antes desta revisão

Windsor: Search Console `sc-domain:arquindex.com.br`, Bing Webmaster `https://arquindex.com.br/`, GA4 `311737260`, Instagram `17841429848911605`. Metricool: marca `7366010`, organização LinkedIn `94842130`, leitura de posts e agenda. GSC Wizard recusou chamadas com `subscription_required`; não é dependência da coleta via Windsor.

Comparação de busca: 01–21/10/2026 contra 10–30/09/2026, 21 dias cada. Totais Google consultados sem dimensão página; consulta de páginas separada não é somada para formar totais. CTR = cliques / impressões, diferença em pontos percentuais. Posição menor significa melhoria. Ausentes, iguais ou sem base comparável ficam cinza; base zero não recebe percentual infinito. O provedor não retornou maturidade nem hora de preenchimento do cache: informar essa limitação. GA4 filtrado para os dois hostnames institucionais retornou nenhuma linha; não interpretar como ausência comprovada de visitas ou leads.

A coleta é um instantâneo consultado nos conectores autorizados em sessão anterior, segundo o histórico do PR, armazenado em variável privada. Não é uma integração contínua entre o runtime e o MCP do ChatGPT. Recarregar o painel recalcula cores, mas não atualiza fontes. Renovar `TOP10_SNAPSHOT_JSON` somente após nova leitura autorizada e conferência das respostas. Para sincronização autônoma ainda faltam credenciais de API de servidor ou exportação autorizada para armazenamento privado; não copiar tokens do ChatGPT nem criar outro serviço para simular integração.

## Publicação e permissões

Instagram, LinkedIn e Google Business Profile têm ações de escrita anunciadas pelo Windsor. A presença da ação não comprova um teste de publicação bem-sucedido. LinkedIn com imagem exige `create_image_post` e `image_url` ou `image_urn`; Google exige `photo_url` para campanha visual; Instagram exige `image_url`. O runner e a fila existentes não são alterados por este módulo. IDs aceitos sem permalink não são tratados como visibilidade pública; URL retornada pela API é evidência do provedor, não teste de acesso anônimo.

Facebook orgânico está ligado a outra identidade; não confundir a conta de anúncios Arquindex com permissão orgânica. TikTok tem nomes diferentes entre conectores e requer conferência. YouTube está listado, mas não houve validação de upload. Reddit, X, Threads, Blogger e WhatsApp Status não têm escrita comprovada nesta auditoria. Bing Places não equivale à API de métricas Bing Webmaster. O painel não envia publicações e não reprocessa estados desconhecidos.

## Limites e preservação

Ranking regional, inspeção atual de indexação, eventos de leitura/scroll, conversões qualificadas e citações em IA ainda não integrados. As metas 3 posts/dia/canal, 100 páginas e 15 artigos continuam planejamento. Não foram verificadas como execução.

Manter PR #36 isolado: **não fazer merge em master nem implantar na HomeHost antes da validação do backup integral da issue #28**. Qualquer implantação, inclusive nos serviços Railway existentes, exige aprovação explícita da usuária. Esta revisão altera somente o branch do PR. Manter automações, fila e demais aplicações. Rollback por revisão anterior do serviço; não restaurar o antigo backend público com dados privados. Nenhum snapshot privado ou segredo deve entrar no GitHub.



## Revisão de 27/10/2026 — entrada de evidências

O estado atual já contém backend privado e testes; não é apenas HTML estático. Esta revisão não consultou provedores de métricas nem verificou os segredos de produção. Contas e capacidades citadas acima são histórico, não confirmação de conexão atual.

`observations.mjs` acrescenta um contrato opcional, retrocompatível, para exportações autorizadas nas cinco áreas: ranking, indexing, pages, articles e publications. Cada linha exige kind, key, source, account, observedAt (ISO com fuso), evidenceId, status (observed/unavailable/error), value e URL HTTPS para um resultado observado. note é opcional. Ranking exige número positivo; a chave deve identificar consulta, país, dispositivo e, apenas quando medido pelo provedor, cidade. Não converter posição média do GSC em posição regional.

O importador valida formato e rastreabilidade declarada; não autentica a origem de um arquivo fornecido, não consulta sua URL nem confirma visibilidade pública. O operador deve conferir a resposta original, a autorização da conta e a semântica de value. Para indexing, registrar o veredito original da inspeção e sua data; para pages/articles, registrar exatamente a verificação feita (HTTP, publicação ou revisão editorial); para publications, preservar o estado original (inclusive processamento), sem chamar aceite de publicação visível. Recibos não medem a meta diária.

O painel mostra a última observação por kind/source/account/key. Falha mais recente invalida sucesso anterior nessa mesma chave; em empate vence a última linha do arquivo. Contagens são registros observados da amostra, sem somar canais nem declará-los produção total. Uma amostra vazia permanece sem dados. Evidências de escopos diferentes exigem chaves diferentes.

Preparação local, sem acesso à rede:

```sh
node top10-google/import-snapshot.mjs /caminho/privado/exportacao.json /caminho/privado/snapshot-validado.json
node --test top10-google/*.test.mjs
```

O destino é criado com permissão 0600, sem sobrescrever arquivos e sem imprimir dados. Nunca versionar os arquivos privados. Configurar o resultado em TOP10_SNAPSHOT_JSON é uma etapa externa posterior que exige aprovação; não há rota de escrita, upload público, tarefa agendada ou publicação no importador.

### Bloqueios para alimentação autônoma

| Área | O que já existe | O que falta e como liberar |
|---|---|---|
| Ranking | Métricas agregadas e observações importáveis | API/exportação de servidor autorizada do GSC/Bing, propriedade e períodos conferidos; ranking municipal exige provedor com localidade e método documentados |
| Indexação | Contrato por URL, sem inferência por cliques ou HTTP 200 | Credencial autorizada de inspeção por URL, propriedade validada, quota, data da inspeção e cobertura; IndexNow não prova indexação |
| Páginas | Planejamento de 100 URLs e tabela de busca | Inventário do CMS/repositório com URL publicada, ID, revisão e evidência HTTP/canonical; não contar o plano como entregue |
| Artigos | 15 pautas no arquivo de planejamento | Inventário editorial, revisão humana e URL comprovada; GA4 autorizado e eventos para leitura/scroll e conversões |
| Publicações | Recibos e capacidade por canal, mais observações importáveis | Identidade orgânica confirmada, exportação/API de leitura de servidor, IDs, estados e URLs por canal e data; publicar exige aprovação separada |
| Atualização | Importação offline e endpoint privado somente leitura | Escolher armazenamento privado, credenciais com menor privilégio, retenção, renovação/revogação e executor; MCP conectado no ChatGPT não é credencial do runtime |

GSC Wizard constava como subscription_required no histórico; não foi retestado. Não é possível afirmar que credenciais estejam ausentes de toda a infraestrutura: elas não foram acessadas nesta revisão. Não copiar tokens de sessões ou conectores. Falta autorização separada para qualquer provisionamento, alteração de variáveis, merge, deploy ou postagem. O bloqueio de backup da issue #28 continua registrado, sem nova comprovação nesta revisão.

Validação desta revisão: 11 testes locais aprovados com Node 24; incluindo rejeição de evidências sem origem/conta, rank inválido e URLs inseguras, ausência distinta de zero, última falha, escape HTML, importação e autenticação. A revisão não atesta funcionamento de APIs remotas ou implantação da nova versão.

### Empacotamento para futura implantação aprovada

O backend agora importa observations.mjs: distribuir ambos os arquivos no mesmo diretório. A Function atual usa código embutido em startCommand; não colar server.mjs isoladamente nesse comando. Uma implantação futura deverá empacotar os módulos (ou usar bundle revisado), preservar os segredos privados e validar em ambiente isolado. Não substituir capture-hub.tsx pela cópia deste PR sem reconciliar alterações posteriores do Hub: a configuração consultada em 27/10 já inclui outras rotas que não fazem parte desta revisão. Os dois serviços usam imagem Function Bun, sem source repo seguindo este branch; nenhuma configuração foi modificada.
