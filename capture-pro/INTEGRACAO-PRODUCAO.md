# Plano de integracao e liberacao — Capture Pro

## Entregue na branch
- Biblioteca existente de metadados e integridade.
- Esquema PostgreSQL 16 com RLS de cliente, versoes e trilha append-only.
- Adaptador `persistencia.js` com captura e aprovacao transacionais, abstraindo storage imutavel.
- Testes unitarios com simulacao de banco/storage. Workflow CI.

## Limites atuais
- Railway `capture-hub` e `ocr-revisao-documental-isolado` usam funcao Bun hospedada diretamente, sem repositório vinculado. Nao ha deploy automatico destes arquivos.
- O repositorio Alfresco teve falha na ultima implantacao. Nao se deve alterar a infraestrutura Alfresco para implantar este modulo.
- O adaptador nao gera OCR, nao autentica usuarios nem assina arquivos. Isso deve vir dos componentes confiaveis do Capture Pro.
- A validacao da classe, temporalidade, data do original e outros atributos precisa de catalogos aprovados por cliente e revisao.
- O adapter recebe `perfilPublico` e `tiposPermitidos` somente de configuracao do projeto no servidor; nunca da requisicao do usuario.
- Persistencia do objeto antecede a transacao para evitar metadado sem imagem. Em caso de falha de banco, processo de reconciliacao deve remover objetos orfaos, com retencao e auditoria.
- Implementar verificacao no armazenamento apos escrita, monitoramento, backups e retencao, e assinatura ICP-Brasil nos casos legais aplicaveis.
- O esquema exige role PostgreSQL sem BYPASSRLS, nao proprietaria e com privilegios minimos. Revisar DDL, permissoes e backup antes de aplicar.

## Sequencia segura de implantacao
1. Identificar e versionar o codigo real do endpoint da captura e do servidor Bun.
2. Garantir staging isolado com banco PostgreSQL 16, storage de teste e contas de teste.
3. Fazer backup verificavel do banco e do repositorio de documentos.
4. Aplicar migration em staging com role apropriada e testar RLS em duas conexoes/tenants.
5. Ligar adaptador com identidade obtida da sessao validada, storage com write-once.
6. Testar upload PDF multipagina, OCR, revisao, validacao, hash, assinatura e entrega.
7. Executar testes de regressao e de seguranca multiempresa.
8. Planejar e executar implantacao controlada, verificar logs e habilitar rollback.

**Status:** nao implantado em staging ou producao. Nenhuma migracao executada.
