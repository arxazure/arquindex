# Central de Cotação de Digitalização — Arquindex

Implementação planejada para www.arquindex.com.br.

## Fluxo de qualificação
17 perguntas, uma de cada vez: tipo documental, volume, localização, caixa, conservação, individualização de PDFs, organização, indexação, datas, duplex, prazo, periodicidade, destino digital, TI, destinação dos originais e segmento.

## Cadastro
Nome, empresa, WhatsApp e e-mail, aviso de privacidade e confirmação antes de enviar.

## Envio comercial
Backend autenticado envia histórico completo e resumo para comercial@arquindex.com.br. Configurar SMTP por segredo no ambiente, nunca no repositório.

## Publicação
Não ativar o formulário publicamente antes de validar SMTP, HTTPS, privacidade, proteção contra spam e vínculo do domínio ao deploy. O domínio .com.br precisa ser confirmado no provedor de hospedagem.

## WhatsApp
O atendimento via Meta AI não substitui uma integração com WhatsApp Business Platform/API. Usar webhook, estado persistente da conversa, consentimento, envio autenticado e encaminhamento humano.
