# Medição de conversões — Arquindex

## Situação
O rastreador `assets/js/arquindex-conversions-v1.js` está em branch de revisão, **não está implantado**. Não inferir conversões a partir de cliques orgânicos.

## Checklist antes de implantar
1. Confirmar qual repositório, pasta e pipeline publicam cada domínio. A raiz `index.html` deste repositório contém outro projeto; **não substituí-la**.
2. Confirmar o GA4 Measurement ID e a propriedade correspondente a cada hostname, sem instalar tags duplicadas.
3. Confirmar a URL comercial e o número de telefone autorizado antes de padronizar CTAs.
4. Testar em homologação os links `wa.me`, `api.whatsapp.com`, `tel:` e `mailto:` e verificar no DebugView do GA4 `contact_whatsapp_click`, `contact_phone_click`, `contact_email_click`.
5. Nos formulários, emitir `arquindex:lead-confirmed` **apenas após confirmação real do servidor**, nunca em `submit` nem ao clicar em enviar. Exemplo: `document.dispatchEvent(new CustomEvent('arquindex:lead-confirmed',{detail:{service:'digitalizacao',form_id:'orcamento'}}))`.
6. Não transmitir nome, telefone, e-mail, CPF, texto livre, URL com query string, identificador pessoal ou conteúdo de documentos em eventos.
7. Testar prevenção de duplicidade, consentimento aplicável, validação de formulário, bloqueio de spam e não interrupção do envio.
8. Definir `generate_lead` como evento principal no GA4 somente após confirmar recepção de leads; cliques de contato são eventos de intenção e não contratos.
9. Criar relatórios por `page_path`, serviço e canal. Cruzar com CRM por identificador interno permitido, sem dados pessoais no GA4.
10. Testar HTTP/HTTPS e www/sem-www com redirecionamento e canonical antes de editar; preservar páginas que já têm tráfego.

## Critérios de aceite
- Formulário válido gera exatamente um evento após confirmação de sucesso.
- Formulário inválido ou falha do servidor gera zero eventos `generate_lead`.
- Nenhum dado pessoal é transmitido ao GA4.
- Eventos aparecem no DebugView e em relatório de teste, com hostname correto.
- O site permanece funcional; deploy reversível com backup e URL pública verificada.

## Referências de verificação
- Google Analytics: https://support.google.com/analytics/answer/9267735
- Site institucional: https://www.arquindex.com.br/
