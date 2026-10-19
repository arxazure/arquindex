# Medição de conversões — Arquindex

## Estado verificado em 19/10/2026
O PR #11 foi integrado em 18/10/2026 às 20:07:32 UTC. O JavaScript está **publicado**, mas a coleta GA4 das landing pages não está operacional: o script exige `window.gtag`, ausente no HTML dessas páginas, que também não contém carregador GA4/GTM ou scripts locais adicionais.

Evidência atual: [auditoria HTTP somente leitura](https://github.com/arxazure/arquindex/actions/runs/39253922479). A execução não carrega bibliotecas do Google, não executa JavaScript público nem envia formulários. Artefato: `ga4-public-audit.json`. As falhas 503 de uma rota de verificação local não devem ser apresentadas como indisponibilidade global: o runner confirmou os 200 abaixo.

## URLs publicadas e cobertura

| URL | HTTP | Inclusões do rastreador | GA4 no HTML e JS local |
|---|---:|---:|---|
| https://www.arquindex.com.br/ | 200 | 0 | Nenhum G- identificado; configurações AW-17029507720 e AW-17020939105 de Google Ads |
| https://www.arquindex.com.br/solucoes-documentais-brasil.html | 200 | 1 | Sem gtag/carregador GA4/GTM |
| https://www.arquindex.com.br/alfresco-belo-horizonte/ | 200 | 1 | Sem gtag/carregador GA4/GTM |
| https://www.arquindex.com.br/gestao-documental-belo-horizonte/ | 200 | 1 | Sem gtag/carregador GA4/GTM |
| https://www.arquindex.com.br/consultoria-lgpd-belo-horizonte/ | 200 | 1 | Sem gtag/carregador GA4/GTM |
| https://www.arquindex.com.br/blog/montagem-de-databooks-de-engenharia/ | 200 | 0 | Sem gtag/carregador GA4/GTM |

Arquivo publicado: https://www.arquindex.com.br/assets/js/arquindex-conversions-v1.js — HTTP 200, application/javascript, bytes idênticos à versão do repositório no momento da auditoria, SHA-256 `de4f4c779f48fc271ee0104e69096a5b8d957b2d067e4359583217f49b30af40`.

O caminho de origem `seo-nacional/solucoes-documentais-brasil.html` é mapeado pelo workflow para a raiz pública `/solucoes-documentais-brasil.html`; não usar a pasta de origem como URL comercial.

Não foram detectadas URLs de scripts duplicadas no HTML das páginas acima. Isso não substitui a inspeção administrativa dos destinos da Google tag e de eventuais tags externas. A home contém o carregador Google Ads em código inline e seus três JS locais não contêm gtag/GTM/Measurement ID GA4. AW- é ID de Ads, não Measurement ID GA4. Vínculos de destinos configurados fora do HTML ainda precisam de revisão.

Os hosts https://guardadocumentalembh.arquindex.com.br/ e https://digitalizacaodedocumentosembh.arquindex.com.br/ falharam em resolução DNS no runner; não foi possível validar sua publicação ou instrumentação.

## Eventos: código versus recepção no Analytics

| Evento | Resultado do teste isolado | Produção GA4 |
|---|---|---|
| contact_whatsapp_click | wa.me, api.whatsapp.com e web.whatsapp.com reconhecidos, um evento por clique | Não confirmado; quatro landing pages sem gtag |
| contact_phone_click | tel: reconhecido, um evento por clique | Não confirmado; não há CTA tel: nas quatro landing pages |
| contact_email_click | mailto: reconhecido, um evento por clique | Não confirmado |
| generate_lead | Apenas o hook explícito arquindex:lead-confirmed gera evento; submit, invalid e erro geram zero | Sem integração de recebimento identificada; não ativar como evento principal |

Os testes usam gtag em memória e DOM simulado, sem rede: não comprovam ingestão pelo GA4 nem recebimento real de um formulário. A segunda inclusão do script não instala outro listener. Query string, fragmento e destinos de WhatsApp/e-mail/telefone não entram no payload desses testes.

O hook `arquindex:lead-confirmed` confia no chamador; não consulta servidor nem valida recibo. Repetir a confirmação pode repetir o evento. Um fluxo futuro precisa confirmar sucesso real da aplicação e impedir reprocessamento do mesmo recibo, sem transmitir recibos pessoais ao Analytics.

O formulário público `#lead` da página Databooks apenas abre o WhatsApp por `window.open`. O template de guarda `scripts/templates/guarda-commercial-form.html` também apenas prepara uma mensagem. Abrir WhatsApp não confirma envio ou recebimento. Não conectar generate_lead ao submit desses formulários. Eles não foram enviados ou alterados nesta auditoria.

## Privacidade: falha reproduzida e correção preparada
O validador publicado aceita qualquer sequência alfanumérica/underscore/hífen até 60 caracteres em service/form_id. Foi reproduzida a passagem de um nome sintético e de um identificador numérico sintético: regex de caracteres não garante ausência de dados pessoais.

[PR #15](https://github.com/arxazure/arquindex/pull/15) restringe esses valores a categorias estáticas e usa unknown nos demais casos. Correção em revisão, **não publicada**. Seis testes aprovados localmente com:
```sh
EXPECT_PRIVACY_FIX=1 node tests/conversions-isolated.cjs
```
Categorias propostas de serviço: digitalizacao, ocr, gestao_documental, guarda_documental, lgpd, dpo, alfresco, databooks. Formulários: orcamento, commercial-form, lead. Estes são rótulos estáticos, não uma confirmação de que exista formulário com recebimento implementado.

Nunca transmitir campos de formulário, CPF, nome, telefone, e-mail, texto livre, conteúdo documental, URL com query/fragmento ou identificador pessoal. Revisar separadamente page_view, page_referrer, mensuração otimizada e URLs de saída da tag base antes de ativar coleta; o rastreador não controla todas as coletas automáticas do GA4. Preservar o mecanismo de consentimento aplicável.

## Acesso ao GA4 e pendências administrativas
Windsor identificou a propriedade `311737260`, nome `http://www.arquindex.com.br – GA4`. Isso não informa o Measurement ID G- nem comprova que o fluxo está associado a cada hostname. Consultas agregadas de eventos entre 18–19/10 e 19/09–19/10 retornaram zero linhas; a consulta measurement_id/property_timezone também retornou zero linhas. Não interpretar isso como prova de zero tráfego ou ausência de eventos.

GSC Wizard recusou leitura por ausência de assinatura ativa; nenhuma contratação realizada. O conector Windsor disponível não expôs DebugView, criação de relatórios administrativos ou configuração de dimensões. Esses itens permanecem pendentes.

Antes de ativar coleta:
1. Abrir a propriedade 311737260 e verificar fluxo web, domínio, Measurement ID G-, destinos da Google tag e existência de outra instalação via GTM.
2. Preservar Ads e instalar uma única tag GA4 por página, com consentimento e limpeza de URLs apropriados. Não adivinhar o G- e não substituir a raiz index.html deste repositório, que contém outro projeto.
3. Validar em propriedade/fluxo de homologação os três eventos de contato. Para DebugView de produção, primeiro conferir filtro ativo de tráfego de desenvolvedor e estratégia de exclusão; debug_mode sozinho não basta para assegurar ausência de poluição dos relatórios.
4. Validar generate_lead contra sucesso real, inválido, erro de servidor e repetição, usando endpoint de teste ou recibo real autorizado; nenhuma submissão sintética em produção.
5. Só após essas validações configurar generate_lead como evento principal. Cliques são intenção, não contratos ou leads recebidos.
6. Revisar o FTPS: o preflight estrito de 19/10 detectou certificado incompatível com ftp.arquindex.com.br. Corrigir hostname/certificado e usar contexto SSL validado antes de qualquer novo deploy; não desabilitar validação.

## Relatórios a configurar após liberar o acesso
Não foram criados relatórios na interface GA4 nesta auditoria.

- Contatos por página: hostname + pagePath + eventName, métrica eventCount, filtro para os três contact_*; origem/mídia e grupo de canais da sessão como detalhamento.
- Leads recebidos: generate_lead por página, serviço (parâmetro lead_service) e formulário (form_id), filtrando apenas fluxos com recebimento confirmado.
- Aquisição: sessionSourceMedium e sessionDefaultChannelGroup por página de entrada; separar cliques de contato de leads efetivamente recebidos.
- Serviço: registrar lead_service como dimensão personalizada de escopo evento. Os cliques atuais só enviam contact_method, não lead_service; usar mapeamento estático de página para serviço ou adicionar categoria estática revisada. A página nacional abrange vários serviços e não deve receber um serviço único inferido.
- Registrar contact_method quando necessário; verificar se form_id já está disponível como dimensão padrão antes de criar duplicata. Não enviar origem/mídia inventada pelo rastreador.

## Referências
- https://github.com/arxazure/arquindex/pull/11
- https://github.com/arxazure/arquindex/actions/runs/39167169744 (PUBLIC_OK em 18/10)
- https://github.com/arxazure/arquindex/actions/runs/39253922479 (auditoria atual)
- https://github.com/arxazure/arquindex/actions/runs/39249890644 (preflight TLS)
- https://developers.google.com/analytics/devguides/collection/ga4/reference/events
- https://support.google.com/analytics/answer/13296662
