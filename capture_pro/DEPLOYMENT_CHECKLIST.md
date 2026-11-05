# Gate de implantação — Capture Pro

Estado: **não pronto para produção**.

- [ ] Corrigir no Dockerfile a ausência do binário veraPDF (origem oficial, integridade conferida).
- [ ] Aplicar schema.sql em banco de homologação; nunca diretamente em produção.
- [ ] Rever e testar RLS com dois tenants e papel sem BYPASSRLS. O usuário dono do esquema não deve ser usado pelo worker.
- [ ] Garantir `WORKER_TENANT_ID` autenticado e vinculado ao serviço; iniciar com apenas um cliente de testes.
- [ ] Usar endpoint S3 privado e credenciais separadas por ambiente; nunca expor ao navegador.
- [ ] Implementar estado intermediário de upload idempotente e reconciliação de órfãos entre S3/Postgres.
- [ ] Implementar heartbeat, expiração e retentativa segura de jobs travados.
- [ ] Executar testes com PDFs multipágina, sem texto, já OCRizados, girados, inválidos e com digitalização colorida.
- [ ] Integrar aprovação humana de QA; não permitir assinatura durante revisão OCR.
- [ ] Implementar API com identidade derivada da sessão e escopos de clientes por matrícula/membership.
- [ ] Criar backup e restauração testada do PostgreSQL e bucket S3; ZIP local não substitui backup remoto.
- [ ] Gerar ambiente de homologação independente antes de conectar credenciais de produção.
- [ ] Não armazenar certificados A1/ICP-Brasil nem suas senhas no repositório.
- [ ] Incluir logs sem dados pessoais do texto OCR.
