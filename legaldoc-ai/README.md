# Arquindex LegalDoc AI — MVP comercial e demonstração

Este diretório contém duas páginas estáticas independentes:
- `index.html`: landing page com proposta comercial e preços indicativos.
- `app.html`: simulação local de preparação de documento e etapas de análise, aprovação, assinatura e arquivamento.

## Importante
**Não se trata de um sistema de assinatura digital ou aprovação jurídica operante.** Nenhum dado é gravado ou transmitido. As páginas estão marcadas `noindex,nofollow` até validação e publicação comercial. Não conectar este protótipo ao banco de dados do LGPD Checklist nem alterar deploy de produção sem testes.

## Backend necessário
1. Multiempresa e RBAC com proteção por tenant.
2. Upload privado com antivírus, validação de formatos e armazenamento criptografado.
3. Extração DOCX/PDF com evidência e campos de baixa confiança.
4. Gestão de templates: criação, homologação por perfil autorizado, hash da versão e controle de revogação.
5. Fluxo: RASCUNHO -> EM_ANALISE -> EM_REVISAO -> APROVADO -> AGUARDANDO_ASSINATURA -> ASSINADO -> ARQUIVADO, com rejeição e reabertura versionada.
6. Integração de assinatura eletrônica/digital apropriada ao documento, com autenticação dos signatários, carimbo de tempo quando aplicável, certificado e trilha de evidências; sem declarar ICP-Brasil quando não houver.
7. Logs imutáveis e retenção LGPD; exportações DOCX/PDF; APIs para LGPD Checklist, Capture Pro e Alfresco.
8. Segurança: CSRF, validação, autenticação robusta, audit logs, testes de isolamento, plano de incidentes.

## Publicação
Servir o diretório `legaldoc-ai/` como estático em ambiente de homologação. Antes de produção, remover noindex apenas após revisão de preços, termos, política de privacidade, proposta de suporte e QA. Evitar configurar o deploy existente do LGPD Checklist para servir este diretório por engano.

## Catálogo brasileiro estruturado — etapa inicial

A área `builder.html` agora oferece um catálogo editorial inicial de 16 famílias documentais em Contratos, LGPD, Governança, SESMT/SST, RH e Gestão Documental. `legal-catalog.js` contém as cláusulas e os metadados, com status **DRAFT_UNREVIEWED**. As referências oficiais remetem à legislação/órgãos competentes para conferência humana; não equivalem a parecer jurídico ou certificação de conformidade.

- **Essencial do modelo**: exige presença no documento-base, mas não significa obrigatoriedade legal universal.
- **Condicional**: exige análise do contexto de aplicação para determinar se deve entrar no documento.
- **Opcional**: escolhida conscientemente, sujeita a compatibilidade com a lei e a finalidade.
- As versões exportadas do catálogo recebem o aviso **MINUTA EDITORIAL — MODELO NÃO HOMOLOGADO JURIDICAMENTE** e informam campos pendentes.
- O exportador cria HTML A4 estilizado, que pode ser impresso em PDF no navegador. Não gera DOCX fiel, PDF/A, assinatura ICP-Brasil nem certificado de validade.
- As normas técnicas ABNT/ISO são protegidas por direitos e licenças; o sistema deve cadastrar referências, controles e modelos originais, **não copiar o texto integral de normas sem autorização**.

### Meta escalável de 60 mil modelos

A meta de 60.000 modelos é um objetivo do catálogo, **não um número já disponível**. A expansão deve seguir: família documental -> versão -> setor, riscos, jurisdição, cláusulas condicionais -> revisão legal -> homologação -> publicação. O esquema proposto `legal-catalog-schema.sql` implementa entidades de fontes legais, famílias, versões, referências e fila de revisão; **a migração não foi executada**.

### Radar diário das fontes oficiais

`check-legal-sources.mjs` verifica disponibilidade, última alteração informada pelo servidor e fingerprint do conteúdo público em URLs oficiais em lista permitida. `.github/workflows/legaldoc-legal-radar.yml` define agendamento diário e artefato JSON para inspeção. **O agendamento GitHub Actions baseado em `schedule` precisa estar na branch padrão para começar a executar; neste PR ainda não está ativado.** Resultados não aprovam modelos nem atualizam automaticamente cláusulas: apenas sinalizam pontos para revisão. Mudanças legais, vigência e exceções exigem confirmação especializada.

### Próximas dependências para produção

- Base relacional privada multiempresa, autenticação e segregação de usuários, ações auditadas, backups e retenção LGPD;
- Coleta e versionamento de fontes oficiais, comparação com versão previamente aprovada e fila de revisão humana;
- Editor rico de DOCX/PDF com formatação preservada e exportação A4 testada em documentos reais;
- Regras legais de elegibilidade e cláusulas aplicáveis com evidências e validade temporal;
- Homologação de cláusulas/modelos por profissional habilitado, sem autopublicação da IA;
- Provedor de assinatura eletrônica/digital com identidade dos signatários, trilha de autenticação e integridade;
- Integração autorizada com LGPD Checklist, Capture Pro e Alfresco.

## Assistente de entrada e roteamento de revisão
- `intake.html` oferece um **assistente guiado local**, sem API de IA generativa ou envio ao servidor, para colher solicitação, tipo de documento, contexto, e-mails jurídicos (até oito), 1 ou 2 rodadas jurídicas, revisão técnica, aprovação/homologação e destino `ASSINAR` ou `PUBLICAR`.
- `intake.js` mostra a sequência de estados e permite simular transições, com exportação JSON. **Não envia e-mails, convites, PDF ou assinatura; nenhum evento equivale a aprovação jurídica real**.
- `intake-workflow-schema.sql` contém uma proposta **não aplicada** para solicitações, revisores, pareceres e eventos segregados por empresa. O backend deverá autenticar revisores, exigir autorização, registrar hash da versão analisada, invalidar aprovações quando houver mudanças e aceitar assinatura somente por webhook verificado do provedor.
- Para IA conversacional em produção: servidor autenticado com provedor LLM configurado por segredo, limites de custo e rate limiting, regras de privacidade, RAG em fontes verificadas e confirmação humana. Não incluir segredos ou documentos privados no JavaScript público.
