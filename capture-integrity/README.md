# Integração de integridade Capture — revisão de 27/10/2026

## Origem operacional localizada

O código operacional foi localizado no projeto Sites `appgprj_6ac67fe07cf881918d15facc73386f57`, Arquindex Capture • Digitalização e indexação, publicado em https://arquindex-captura-online.arquindex-ex-2480.chatgpt.site (versão 22 na inspeção). O Git privado do projeto foi aberto em cópia isolada, a partir do commit `267342f55b0adfb43bf03e67ec7156050df39f82`. Não é um repositório GitHub chamado Capture/DocDigital. A relação histórica com o Replit não foi comprovada: a consulta ao app Upload Drive não retornou conteúdo de inspeção.

O Railway Capture Hub usa uma função Bun com proxy `/repositorio/*`, configurado por CAPTURE_BACKEND_URL (valor indisponível via OAuth). O código operacional inclui a cópia de implantação `deploy/railway-copy` que gera esse backend. O Inventário usa `arquindex-inventario-capture-release` e só possui caixas/movimentações; não foi acoplado artificialmente ao receptor de documentos.

## Entradas e pontos de integração

| Entrada | Implementação operacional | Ponto de hash e persistência |
|---|---|---|
| Upload manual/arrastar arquivo | public/app.js importFiles | bytes originais antes de renderizar/aplicar OCR -> /api/capture-input -> SHA-256, R2 privado com condição de não sobrescrita, releitura e registro D1 |
| Scanner TWAIN | public/app.js botão scan, SDK Dynamsoft | PNG entregue por ConvertToBlob antes do OCR -> mesma entrada; não prova bytes internos do driver/sensor |
| Pasta PaperStream | agent/paperstream.py next, public/app.js psReceive | PDF final estável produzido pelo PaperStream, hash local e nova conferência do servidor; captura anterior ao OCR proprietário permanece fora do alcance |
| Arquivo processado | app/api/upload/route.ts | hash final e releitura do objeto, verificação das fontes por owner + client_id, manifesto imutável e auditoria na mesma transação D1 do documento |
| Assinatura | app/api/signatures/route.ts | verificar original, registrar binário incremental como versão separada; validação ICP-Brasil segue pendente |
| Entrega | rotas files, signatures e portal/files | consulta autorizada e verificação do SHA-256 antes da resposta privada |

A implementação operacional recebe tabelas D1 aditivas capture_inputs/capture_versions com bloqueio de UPDATE/DELETE. Novas entregas com fontes ou metadados obrigatórios pendentes são bloqueadas na liberação. Documentos históricos não são reescritos nem declarados retroativamente conformes. O formulário atual usa campos canônicos do modelo para metadados; configuração e homologação dos campos por cliente continuam necessárias. Data de digitalização, autoria e origem não são inventadas. A rotina PaperStream passa a preservar o original e registrar recibo por escopo; foi removida a exclusão automática de IndexedDB ao carregar a tela.

## Componentes PostgreSQL deste PR

- service.js: identidade fornecida pelo servidor, canais explícitos, verificação da fonte antes/depois do processamento e auditoria de falhas.
- storage.js: cliente real S3/R2 com PUT condicional e chaves por empresa; armazenamento em disco privado para testes/staging. PUT condicional não equivale a retenção WORM contra administradores.
- ingestion.js/persistence.js: snapshot inicial, validação anterior à escrita, hash/releitura, transações e versões ligadas à fonte.
- file-input.js: leitura de arquivo finalizado sem apagar/renomear a origem; não instala agente ou driver.
- processing.js: OCRmyPDF real e conferência de texto; PDF/A requer relatório de validador independente. Estes componentes Node/pg não são importados diretamente em Workers: o projeto operacional usa a adaptação WebCrypto + D1.

## Evidências executadas

`CAPTURE_REAL_OCR=1 npm test`: 15 testes aprovados, 0 falhas, 0 ignorados. SQL executado no motor PostgreSQL embarcado PGlite com persistência em disco e reabertura; não é banco Railway. OCR real com OCRmyPDF/Tesseract e pdftotext em PDF raster fictício. Conversão PDF/A foi invocada; ausência de validação independente bloqueou sua persistência, conforme esperado.

No projeto operacional: testes dos handlers com SQLite real e armazenamento em memória identificado como substituto; teste separado com bindings locais Cloudflare D1/R2, reinício durável, PUT condicional, separação de escopo e corrupção; testes Python da fila PaperStream; TypeScript e sintaxe JS. Resultados completos e commit operacional são registrados na entrega. O workflow agora instala dependências e adiciona job PostgreSQL 16 + OCR; configuração de CI não significa execução remota aprovada.

## Limites e próximas validações

Não houve merge na railway-production-2026, alteração de DNS, migração de dados, implantação operacional nem teste com documentos de clientes. Confirmar o destino efetivo do proxy, versão do backend, políticas e credenciais restritas do R2, D1/backup/restauração, isolamento de operadores (owner não é por si autorização individual por cliente), licença/driver/scanner físico e atualização do ZIP do agente antes de publicação. O fluxo local SQLite do agente ainda não usa o manifesto PostgreSQL/D1 novo; seus arquivos e dados existentes foram preservados. PDF/A validado, autoria/assinatura ICP-Brasil e conformidade integral continuam pendentes.

Referências: Decreto https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10278.htm ; operações condicionais R2 https://developers.cloudflare.com/r2/api/s3/api/ . SHA-256 é verificação de integridade, não assinatura digital.


## Validação adicional em 28/10/2026

O Railway confirmou em seus registros DNS conexões ao host `arquindex-capture-clientes.arquindex-cloud.workers.dev`. Foi implantado separadamente o Worker de homologação `arquindex-capture-integrity-stage`, sem troca de DNS/proxy ou alterações em documentos de produção.

Passaram por HTTPS real: entrada com backup independente obrigatório, OCR real com saída pesquisável, upload/releitura SHA-256, histórico de metadados, login de colaborador, segregação de empresas, entrega privada, revogação e negação de aprovação ao operador. Original e saída OCR foram restaurados de outro bucket, com os mesmos hashes; um segundo D1 recebeu o snapshot de cliente/modelo/documento/fontes/revisões e cinco eventos. Os três buckets novos tiveram r2.dev verificado como desabilitado. Evidências e fixtures fictícias ficam em deploy/evidence no repositório privado operacional.

`verapdf.js` liga um veraPDF CLI independente ao processador Node. Execução local com veraPDF 1.30.3: 16 testes aprovados, zero ignorados; PDF normal recusado; PDF/A-2b real validado, persistido como versão 3, com hash do relatório e vínculo à versão OCR, preservando a versão 1. O binário CLI deve ser instalado separadamente num worker restrito e configurado por caminho confiável. A CI sem CAPTURE_VERAPDF ignora apenas esse teste adicional e não comprova PDF/A validado.

A validação do arquivo fictício não é assinatura ICP-Brasil nem comprova o processo físico. O fluxo Workers continua marcando PDF/A como não validado; o processador Node com veraPDF ainda requer serviço de execução para operar nesse fluxo em produção. Scanner Windows, preservação pré-OCR proprietário PaperStream e validação ICP-Brasil continuam pendentes. Não houve merge ou implantação de produção.
