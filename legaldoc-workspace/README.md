# Arquindex LegalDoc — Workspace Privado (MVP operacional)

Este serviço fica isolado do site público e usa PostgreSQL exclusivo do projeto LegalDoc AI.

## Entregue

- Setup inicial bloqueado por token `ADMIN_SETUP_TOKEN`, desativado assim que existir uma empresa.
- Login com hash scrypt, sessões de 8 horas em cookies Secure/HttpOnly/SameSite=Strict e proteção CSRF.
- Criação de participantes por administrador; senha temporária gerada aleatoriamente, exigindo troca no primeiro login.
- Verificação manual de identidade pelo administrador, com justificativa registrada.
- Criação e edição de documentos por autor; versões persistentes e SHA-256 de cada versão.
- Uma ou duas rodadas jurídicas, revisão cliente, revisão técnica, aprovação e homologação.
- Atribuição de revisores da mesma organização; jurídico limitado aos e-mails autorizados.
- Aprovação com justificativa e bloqueio de decisões sobre versão alterada; devolução exige nova edição.
- Histórico de eventos e auditabilidade operacional inicial.
- Importação de JSON criado pelo Construtor do site de demonstração.
- Documento final permanece **AGUARDANDO_ASSINATURA** ou **AGUARDANDO_PUBLICACAO**, sem executar ações externas.

## Ambiente

`DATABASE_URL` deve apontar para o PostgreSQL privado (`\u0024{{Postgres.DATABASE_URL}}` no Railway).
`ADMIN_SETUP_TOKEN`: código longo e aleatório, usado apenas na instalação.
`PUBLIC_ORIGIN`: URL HTTPS exata do workspace, obrigatória para autenticação e CSRF.
`PORT`: Railway fornece dinamicamente. O domínio deve apontar para o mesmo porto.

Não comitar variáveis nem segredos no GitHub.

## Testes

`.github/workflows/legaldoc-workspace-ci.yml` contém integração com um PostgreSQL de teste e verifica instalação, autenticação, autorização, versões, revisões e rotação de senha.
A existência do workflow não comprova execução; acompanhar resultado no GitHub Actions.

## Antes de documentos jurídicos reais

Ainda faltam:
- RLS e conta de DB com privilégios restritos (hoje isolamento é feito por parâmetros de tenant nas consultas), backup e restauração testados;
- testes de penetração, rate limiting distribuído/MFA, expiração e revogação administrativa de sessões;
- convite por e-mail com validação independente, recuperação de senha e trilha de entrega;
- editor rico e exportador DOCX/PDF com estilos de qualidade de publicação, armazenamento privado de anexos;
- IA com RAG em fontes oficiais com vigência e curadoria, 60 mil modelos homologados e revisão humana;
- prestador de assinatura digital/eletrônica, prova de identidade do signatário, carimbo de tempo quando aplicável e validação;
- auditoria jurídica completa, políticas de privacidade, retenção e DPIA/RIPD quando exigido.

**Não inserir dados sigilosos ou documentos jurídicos reais antes de homologar esses controles.**
