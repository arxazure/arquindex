# Retorno do site institucional à HomeHost — 01/11/2026

Origem: instrução expressa de Marina nesta conversa. Escopo: somente
arquindex.com.br e www.arquindex.com.br. Hospedagem declarada: HomeHost.
Propagação pública: ainda não confirmada nesta atualização; registrar observações
atuais separadamente da decisão. Não houve alteração de DNS, e-mail, segredos,
permissões, arquivos públicos ou aplicativos independentes nesta atualização.

## Comunicação operacional

- 14 automações ChatGPT de SEO, auditoria, conteúdo e redes receberam o aviso,
  preservando prompts anteriores, horários e estado ativo/pausado.
- Contrato legível por máquinas: config/site-hosting.json.
- Instruções para futuras intervenções no repositório: AGENTS.md e README.md.
- 221 workflows GitHub, com 224 jobs, recebem uma etapa inicial que registra a
  hospedagem vigente em logs, resumo e variáveis de contexto. As demais etapas,
  gatilhos, cron, permissões e condições permanecem idênticos.
- A etapa é informativa; não converte publicadores legados nem comprova que
  credenciais FTPS funcionam. A publicação deve confirmar origem e leitura pública.
- Não executar lotes de publicação antigos só para transmitir o aviso. A alteração
  de workflows usa [skip ci] para evitar execuções por push; agendas futuras e
  disparos manuais continuam com os horários e limites existentes.
- Referências históricas a Railway permanecem para rastreabilidade. Deploy de
  aplicativos Railway é distinto da publicação do site institucional na HomeHost.

## Conferência necessária antes de publicar

Verificar DNS/HTTP/TLS, raiz correta HomeHost, inventário restaurado, backup,
certificado FTPS e permissões. Preservar blog, clientes, cases, planos, menus e
assets. Não migrar nem modificar o site secundário .com ou aplicativos separados.
Não submeter URLs de prévia como domínio oficial. Confirmar arquivo novo por GET
público antes de informar publicação ou solicitar rastreamento.

## Divergência observada no Cloudflare

A leitura autorizada da zona Cloudflare conectada encontrou o registro CNAME
`arquindex.com.br → tevuusva.up.railway.app` e
`www.arquindex.com.br → arquindex.com.br`. A zona consta como active e lista
armfazh.ns.cloudflare.com e naya.ns.cloudflare.com. Isso registra a configuração
consultada, sem comprovar a delegação atual no registrador após a mudança da
usuária. Não afirmar que a propagação já terminou nem sobrescrever esses registros
automaticamente. Os registros de e-mail não foram alterados.
