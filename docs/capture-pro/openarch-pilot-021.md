# Piloto OpenArch CLI 0.2.1 no Capture Pro

Referência: issue #123. Avaliação de 06/11/2026; sem implantação.

## Resultado

Este PR acrescenta um adaptador de preparação de metadados. A flag `CAPTURE_OPENARCH_PILOT_ENABLED` é desligada por padrão e somente a string `true` permite preparação. `executar()` sempre recusa execução com `OPENARCH_RUNTIME_NOT_VALIDATED`. Não há subprocesso, envio remoto, cópia binária, migration ou integração na API Railway.

Arquivos: [adaptador](../../capture-pro/openarch/adapter.js), [testes unitários](../../capture-pro/openarch/adapter.test.js), [testes de runtime](../../capture-pro/openarch/runtime.test.js), [configuração de exemplo](../../capture-pro/openarch/.env.example).

## Interfaces verificadas na tag fixada

Fonte: [OpenArch CLI v0.2.1](https://github.com/AlfrescoLabs/openarch-cli/tree/v0.2.1), árvore Git `11340cc374ad99fa0aafe596f4f754f4ea834036`. Capture Pro avaliado no commit `208fa36c46f37c802f4e801fbb18e6c2dc24e61c`.

| Interface | Contrato |
| --- | --- |
| `openarch version --output json` | Informação de versão |
| `openarch doctor` | Verifica Docker, Compose, memória, portas e registry |
| `openarch documents create --parent /projects --file report.json` | Cria documento JSON com `sys_primaryType`; exemplo oficial usa `SysFolder` |
| `openarch documents get <id-or-path>` | Recupera documento JSON |
| `openarch query <query> --output json` | Consulta HxQL/expressão por POST `/api/query` |
| `--output json`, `--non-interactive` | Formato estruturado e execução sem prompts |
| `--url`, `--user`, `--password-stdin`, `OPENARCH_PASSWORD` | Credenciais da CLI; cliente utiliza Basic Auth |
| Códigos de saída | 0 OK; 1 erro; 2 entrada; 3 requisito; 4 saúde; 5 API; 6 autenticação |

`documents upload`, `documents list` e `documents content` não constam nesta tag. O OpenAPI embarcado contém `/api/upload` e rotas de download; esse transporte não foi implementado ou validado aqui. Não usar a documentação de versões posteriores como contrato da 0.2.1.

O OpenAPI confirma `sys_description` como string. O envelope usa somente `sys_primaryType=SysFolder`, `sys_name`, `sys_title` e `sys_description`; os metadados Capture Pro são serializados na descrição. Trata-se de registro de metadados, não armazenamento de PDF. A aceitação pelo servidor e a existência das pastas pais continuam sem validação.

## Dependências

[README da tag](https://github.com/AlfrescoLabs/openarch-cli/blob/v0.2.1/README.md): Docker com Compose v2, cerca de 4 GB de memória e, no Linux, `vm.max_map_count >= 262144`. A stack utiliza OpenArch JVM, MongoDB em replica set e OpenSearch; Caddy/TLS e Dashboards são opcionais. Nenhum requisito foi instalado ou alterado.

[go.mod](https://github.com/AlfrescoLabs/openarch-cli/blob/v0.2.1/go.mod): Go 1.26.0 para compilar; dependências diretas incluem Cobra/pflag, oapi-codegen/runtime, Sigstore, go-keyring, YAML, x/crypto, x/mod, x/term, huh e go-internal.

## Comparação e controles

| Capture Pro | Decisão do adaptador |
| --- | --- |
| `transacaoTenant`, PostgreSQL e RLS | Reutiliza a transação e SELECT parametrizado por tenant, projeto e UUID; rejeita linhas divergentes mesmo se devolvidas por dependência defeituosa |
| Storage imutável e SHA-256 | Mantém matriz no storage existente e verifica seus bytes antes de preparar o envelope |
| Sessão externa ao módulo de persistência | Exige callback servidor `resolverSessao` e permissão `openarch:pilot`; não implementa login, SSO ou federação |
| Metadados e aprovação existentes | Usa valores recuperados do banco, catálogo e perfil público configurados no servidor; exige documento validado, revisado e versionado |
| Separação por empresa | Binding servidor com instância OpenArch exclusiva por tenant; caminhos e metadados não substituem ACL |
| Restrição a sintéticos | Allowlist de SHA-256 de fixtures conhecidas; booleano enviado pelo cliente não autoriza processamento |
| Reprocessamento | Nome determinístico e chave de job estável; nenhuma garantia de idempotência remota ou ledger persistente |

API local: `criarAdaptador({env,pool,storage,resolverSessao,bindings})`, seguido de `preparar({sessao,identificadorDigital})`. A sessão é um identificador opaco validado pelo callback. Nunca usar identidade ou bindings fornecidos pelo navegador.

Cada binding exige `tenantId`, `projetoId`, `instanceId`, `syntheticSha256`, `tiposPermitidos` e `setorPublico`. A instância deve ser provisionada separadamente e sua exclusividade verificada antes de liberar transporte; o binding local sozinho não prova isolamento no servidor.

## Validação registrada

Execução local em Node v24.22.1: **26 testes, 24 aprovados, 0 falhas, 2 ignorados**. São 11 testes existentes e 13 novos testes unitários. Os testes usam dados sintéticos e doubles explícitos de PostgreSQL, storage e sessão.

Os dois testes ignorados são a consulta da versão real da CLI (binário ausente) e integração da stack (Docker/servidor ausentes e não autorizados). Go e PostgreSQL/psql também não estão disponíveis no runtime local. Nada disso foi representado como integração funcional.

Para reproduzir a lógica local na branch:

```bash
node --test capture-pro/decreto10278.test.js capture-pro/persistencia.test.js capture-pro/openarch/adapter.test.js capture-pro/openarch/runtime.test.js
```

Os workflows existentes testam apenas os módulos anteriores; este PR não altera workflows. Os testes novos ainda não têm execução automática em CI. Não foram comprovados RLS real, ACL OpenArch, OCR, busca remota, exportação, backup/restauração ou autorização da API Railway.

## Escopo da revisão e próximos passos

A autorização cobre branch nova `pilot/openarch-021-adapter`, commit dos quatro arquivos e deste relatório, e PR em rascunho para `master`. Não cobre merge, ativação de flag, stack, instalação de dependências em servidor ou alteração em Railway/produção. Os módulos existentes permanecem sem alteração.

Antes da escrita remota foram revisados os gatilhos dos workflows da base: para os arquivos deste PR, os workflows aplicáveis são `capture-persistencia-ci.yml` e `testar-metadados-capture.yml`, ambos com testes e permissões de leitura. Nenhum workflow de deploy foi adicionado ou acionado manualmente. Os serviços Railway consultados apontam para outras branches ou imagens; Capture Hub permanece uma função Bun sem fonte Git conectada.

Antes de liberar transporte: validar binário 0.2.1 com checksum/assinatura, executar help/version reais, obter autorização específica para stack isolada, testar schema e pais, credenciais exclusivas, negativas cruzadas no servidor e RLS com role restrita, ledger/outbox, retries/timeout, integridade ponta a ponta, busca, backup/restauração e rollback. Não compartilhar stdin entre senha e `--file -`.

Rollback deste PR: remover os cinco arquivos novos. Não há dados remotos criados pelo adaptador a reverter.

## Fontes primárias

- [Issue #123](https://github.com/arxazure/arquindex/issues/123)
- [Capture Pro na base avaliada](https://github.com/arxazure/arquindex/tree/208fa36c46f37c802f4e801fbb18e6c2dc24e61c/capture-pro)
- [Comandos da CLI 0.2.1](https://github.com/AlfrescoLabs/openarch-cli/tree/v0.2.1/docs/commands)
- [Autenticação](https://github.com/AlfrescoLabs/openarch-cli/blob/v0.2.1/internal/auth/auth.go)
- [Cliente documental](https://github.com/AlfrescoLabs/openarch-cli/blob/v0.2.1/internal/api/documents.go)
- [OpenAPI embarcado](https://github.com/AlfrescoLabs/openarch-cli/blob/v0.2.1/api/openapi.json)
