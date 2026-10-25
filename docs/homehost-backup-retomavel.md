# Backup HomeHost retomável — preparação para a issue #28

## Diagnóstico verificado

A execução 40084543361, tentativa 2, começou a etapa de backup em 24/10/2026 às 16:40:49 UTC e foi cancelada às 21:40:59 UTC. O limite do job era 300 minutos. O último progresso registrou 14.000 arquivos e 252.202.080 bytes. A API de artifacts retornou zero itens.

O script anterior monta um único tar.gz local e só começa o envio remoto depois de ler todas as raízes. Portanto, o trecho coletado nessa execução não chegou à etapa de publicação e leitura de retorno do backup. Isso não prova que inexistam outras cópias no servidor; não houve inventário FTPS remoto nesta revisão. Não repetir o mesmo job esperando que ele retome os arquivos já lidos.

## Implementação proposta

O novo script usa o mesmo FTPS com validação de certificado, TLS mínimo 1.2 e conferência do IP contra o servidor FTP institucional. Reutiliza a descoberta de raízes públicas do script anterior. Não altera o script anterior nem seu workflow.

Cada parte recebe nome único em `/seo-backups/resumable/<execução>/`, fora das raízes públicas. Após o envio, a parte é relida integralmente, com comparação de tamanho e SHA-256. Só depois o progresso é gravado em um checkpoint JSON, também relido e verificado. Não há DELETE, rename, limpeza, deploy ou publicação de conteúdo. Nenhum arquivo de origem é escrito. Nomes com traversal ou quebras de linha são rejeitados; entradas de tipo não suportado interrompem a cópia em vez de serem omitidas.

Partes têm limite padrão de 250 arquivos ou 64 MiB de conteúdo de origem, com interrupção entre arquivos após 20 minutos. Um arquivo individual pode exceder o alvo de tamanho/tempo; os limites globais de 200 mil arquivos e 8 GiB permanecem. O job trabalha por cerca de 40 minutos antes de parar entre partes; a janela de 90 minutos permite transferência e verificações. Uma transferência isolada ou a leitura final ainda pode consumir a janela: os checkpoints anteriores continuam recuperáveis.

Arquivos temporários de um envio interrompido ficam preservados como órfãos no diretório privado; não são usados como partes válidas. A retomada cria novos nomes para não sobrescrevê-los. Não há coleta automática de lixo.

## Operação após revisão

1. Revisar este PR e disponibilizar o workflow manual conforme a política do repositório. Ele não executa por push nem por agenda. A CI de PR executa somente testes com FTP simulado, sem segredo ou rede.
2. Antes do primeiro backup real, confirmar no FTPS a raiz da conta, espaço livre e que `seo-backups` não é publicado por nenhum domínio/alias. A localização fora de `public_html` não substitui essa conferência. Verificar se já existe outra cópia íntegra. Nenhum segredo deve ser enviado em comentários ou logs.
3. Executar `HomeHost private resumable backup` com `resume_checkpoint` vazio para iniciar uma cópia nova. O segredo `FTP_PASSWORD` existente só é usado pelo job manual. A concorrência usa o mesmo grupo do backup anterior.
4. Se aparecer `BACKUP_PARTIAL_RESUME_REQUIRED`, copiar o caminho da última linha `BACKUP_CHECKPOINT` verificada para `resume_checkpoint` na próxima execução. Se o job for interrompido, usar igualmente o último checkpoint verificado. Não usar partes órfãs nem reiniciar com campo vazio. Manter o recibo de tamanho/SHA-256 do checkpoint em registro privado.
5. A retomada valida o checkpoint e relê todas as partes referenciadas antes de continuar. O marcador `BACKUP_COMPLETE_VERIFIED` só aparece após esgotar as tarefas e reler integralmente todas as partes, inclusive as criadas em jobs anteriores. O checkpoint com `state: complete` relaciona todas as partes e seus hashes.
6. Registrar a conclusão, abrangência, contagens e hashes em evidência privada. Fazer restauração de teste em diretório isolado, sem extrair em `public_html`. O conjunto restaurável é formado pelo checkpoint final e todas as partes referenciadas, não por uma parte isolada.

## Limites para liberar os PRs

Este é backup de conteúdo das raízes públicas descobertas, não backup de banco de dados, e-mails, configurações completas do cPanel ou um snapshot atômico da hospedagem. Diretórios vazios, arquivos ocultos e arquivos de tamanho zero são incluídos. As permissões originais e metadados completos do servidor não são preservados. O conteúdo pode mudar entre partes: usar janela sem alterações ou fazer reconciliação final de inventário e conteúdo antes de liberar deploy. Alterações de tamanho durante a leitura interrompem a parte; alterações mantendo o tamanho não são detectadas como mudança da origem.

A implementação ainda não foi executada contra a HomeHost. Testes locais simulam restauração do conteúdo, retomada, envio incompleto, SHA-256 divergente, alteração de arquivo vazio, caminhos inseguros, limites e proteção contra sobrescrita. Não encerrar a issue #28 nem liberar os PRs #36/#37 apenas por CI verde ou por um checkpoint parcial. Preservar as restrições de merge/deploy até existir comprovação da cópia completa e validação de restauração.
