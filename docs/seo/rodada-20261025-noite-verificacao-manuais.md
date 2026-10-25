# Rodada SEO/GEO/AEO — 25/10/2026, noite

## Resultado real de publicação

O workflow [40239912496](https://github.com/arxazure/arquindex/actions/runs/40239912496) terminou como `failure`, mas o log comprova que o envio FTPS e a releitura dos dois arquivos foram concluídos antes de uma falha transitória na consulta HTTP:

- `digitalizacao-ocr-manual-tecnico-bh` — `FTPS_VERIFIED` SHA-256 `89b13d40d711621424d0c1949fc1f99ef39442af60ebb12b0b093dbc150445b7`
- `guarda-fisica-custodia-manual-planos-bh` — `FTPS_VERIFIED` SHA-256 `9c67a7b5e4a2ece21f91f8049c4509ba37a63a921d3a8877c3f08cb24e5e175c`

Verificação pública independente repetida em 25/10/2026 à noite:

| URL | HTTP/acesso | Canonical | Robots | Viewport | H1 |
|---|---|---|---|---|---|
| https://www.arquindex.com.br/digitalizacao-ocr-manual-tecnico-bh/ | acessível | própria | index,follow | presente | Do papel à pesquisa: digitalização com critérios de aceite |
| https://www.arquindex.com.br/guarda-fisica-custodia-manual-planos-bh/ | acessível | própria | index,follow | presente | Guarda física com localização e rastreabilidade |

A falha final do workflow foi `RemoteDisconnected` durante a validação HTTP e não desfaz o envio FTPS já verificado. Isso não comprova indexação.

## Qualidade e pendências

As duas páginas têm conteúdo distinto, resposta direta, manual, condições comerciais contextualizadas, fontes públicas e canonical própria. Entretanto, ainda não devem ser divulgadas como concluídas porque:

1. o cabeçalho exibe apenas texto `ARQUINDEX`, sem logo oficial em imagem;
2. não há imagem própria da peça/página;
3. não há CTA WhatsApp funcional nem atendimento flutuante para +55 31 97363-2725;
4. o texto visível informa que a revisão técnica e comercial está pendente;
5. as URLs ainda não foram cadastradas em sitemap confirmado;
6. não houve submissão autenticada ao Search Console, Bing Webmaster ou IndexNow;
7. não houve publicação social nesta rodada.

Qualquer substituição dos arquivos agora existentes deve preservar cópia recuperável por URL e rollback. O bloqueio da issue [#28](https://github.com/arxazure/arquindex/issues/28) continua aplicável às alterações pendentes em arquivos existentes até existir backup integral validado.

## Outras auditorias da rodada

- [40241906950](https://github.com/arxazure/arquindex/actions/runs/40241906950): leitura FTPS confirmou que seis URLs de cobertura não existem como diretórios estáticos; cinco dependem do roteador `gestao-documental/index.php` e o caminho `geo-ai-search` não existe na raiz consultada.
- [40245664293](https://github.com/arxazure/arquindex/actions/runs/40245664293): inventário somente leitura confirmou `/public_html/.htaccess` com 358 diretivas, `gestao-documental/.htaccess` encaminhando para `index.php` e ausência do diretório `geo-ai-search`.

Não alterar nem promover as seis rotas apenas com base nesses achados; primeiro validar resposta pública, canonical e intenção.

## Estado da fila

- ARQ-119, ARQ-120 e ARQ-123 permanecem preparadas, mas não publicadas por falta de `BACKUP_COMPLETE_VERIFIED` e restauração isolada.
- PR [#40](https://github.com/arxazure/arquindex/pull/40) continua aberto, não integrado e sem execução real contra a HomeHost.
- PR [#41](https://github.com/arxazure/arquindex/pull/41) continua em rascunho; o workflow legado ainda pode falhar em pushes.
- Cursor preservado: ARQ-119.

## Próximas prioridades

1. concluir backup retomável e validar restauração isolada;
2. corrigir identidade, CTA e revisão das duas páginas novas com backup individual/rollback e depois atualizar sitemap;
3. somente após publicação final validada, executar submissões autenticadas sem confundir recebimento com indexação.
