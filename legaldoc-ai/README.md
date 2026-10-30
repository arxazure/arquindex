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
