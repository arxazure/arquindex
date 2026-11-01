# Rodada SEO/GEO/AEO — 1º de novembro de 2026 (manhã)

## Escopo e resultado

- Fichas revisadas: ARQ-215 a ARQ-220 (6 URLs).
- Melhorias preparadas no repositório: ARQ-215, ARQ-217 e ARQ-218 (3 URLs).
- Publicações públicas confirmadas nesta rodada: **0**.
- Motivo: o workflow recusou a conexão antes de qualquer gravação porque `ftp.arquindex.com.br` não apresentou certificado FTPS legível. Nenhuma credencial foi enviada por canal não verificado, nenhum arquivo remoto foi alterado e não houve rollback a executar.
- ARQ-099 foi preservada; não houve republicação nem nova divulgação.
- Nenhuma peça social foi publicada nesta rodada.

## Evidências

| Item | Evidência |
|---|---|
| Auditoria pública | [workflow 41303248562](https://github.com/arxazure/arquindex/actions/runs/41303248562), job 124838382428, sucesso |
| Proteção do publicador | [commit 4250d73cae365fa577d10a19d52e9f87812de1b6](https://github.com/arxazure/arquindex/commit/4250d73cae365fa577d10a19d52e9f87812de1b6) |
| Conteúdo preparado | [commit 4af60a7083411d81f37ac319aa699a607a90a22b](https://github.com/arxazure/arquindex/commit/4af60a7083411d81f37ac319aa699a607a90a22b) |
| Tentativa de publicação | [workflow 41303499812](https://github.com/arxazure/arquindex/actions/runs/41303499812), job 124839098865, falha segura |
| Fila persistente | [commit f6c2723c707799f8fb0b3ac6e66642488e301c40](https://github.com/arxazure/arquindex/commit/f6c2723c707799f8fb0b3ac6e66642488e301c40) |

## Auditoria das seis URLs

Todas resolveram DNS para `104.21.21.82` e `172.67.197.14`, responderam por HTTPS, tiveram `/robots.txt` e `/sitemap.xml` com HTTP 200 e não apresentaram overflow horizontal nas larguras de 390 px e 1440 px.

| ID | URL | Resultado público antes da tentativa |
|---|---|---|
| ARQ-215 | /seo-regional/gestao-documental-ecm-databooks/ | HTTP 200; canonical correto; title e H1 únicos; 199 palavras; sem meta robots, logo oficial, menu, widget, CTA, formulário ou JSON-LD detectado |
| ARQ-216 | /porto-velho/ | HTTP 200; canonical, title, H1, description, `index,follow` e 1 JSON-LD; 894 palavras; sem logo/menu/widget/CTA/formulário detectado |
| ARQ-217 | /vespasiano/ | HTTP 200; canonical, title, H1, description, `index,follow` e 1 JSON-LD; 860 palavras; sem logo/menu/widget/CTA/formulário detectado |
| ARQ-218 | /ibirite/ | HTTP 200; canonical, title, H1, description, `index,follow` e 1 JSON-LD; 889 palavras; sem logo/menu/widget/CTA/formulário detectado |
| ARQ-219 | /ribeirao-das-neves/ | HTTP 200; canonical, title, H1, description, `index,follow` e 1 JSON-LD; 909 palavras; sem logo/menu/widget/CTA/formulário detectado |
| ARQ-220 | /lagoa-santa/ | HTTP 200; canonical, title, H1, description, `index,follow` e 1 JSON-LD; 893 palavras; sem logo/menu/widget/CTA/formulário detectado |

A auditoria confirmou a existência e a publicação pública dessas seis entradas do inventário, mas não confirma indexação, posição ou leads.

## Melhorias preparadas, não publicadas

### ARQ-215 — hub regional

- Identidade institucional com logo oficial, navegação responsiva, rodapé e atendimento flutuante.
- Resposta direta sobre gestão documental, GED, ECM e databooks.
- Tabela de decisão, etapas, FAQ visível e dados estruturados compatíveis.
- Autoria/revisão, fontes primárias (CONARQ e Decreto 10.278/2020).
- Links contextuais para quatro soluções e CTAs com UTM.

### ARQ-217 — Vespasiano

- Preservados title, H1, canonical e conteúdo existente.
- Acrescentado bloco AEO diferenciado sobre documentos recebidos de fornecedores, nomenclaturas, revisões e completude.
- Identidade institucional, fontes, WhatsApp, CTA com UTM e atendimento flutuante.

### ARQ-218 — Ibirité

- Preservados title, H1, canonical e conteúdo existente.
- Acrescentado bloco AEO diferenciado sobre ordens de manutenção, situação, evidência e recuperação por equipamento.
- Identidade institucional, fontes, WhatsApp, CTA com UTM e atendimento flutuante.

## Publicador e segurança

O workflow foi alterado para selecionar apenas HTML modificado, validar H1/canonical/logo/WhatsApp/viewport, obter backup remoto antes da escrita, fazer upload seletivo, comparar hash por leitura de retorno, testar público em mobile e desktop, validar sitemap e executar rollback automático após falha posterior à gravação.

Na execução 41303499812, a validação local dos três HTMLs passou. A etapa seguinte falhou ao tentar ler o certificado do endpoint FTPS. As etapas de backup, upload e validação pública foram puladas. O log registra explicitamente que não houve gravação comprovada.

## Sitemap e descoberta

Nenhuma URL nova foi criada e nenhuma alteração chegou ao site público. Portanto:

- sitemap não foi alterado;
- não houve submissão ao Google Search Console, Bing Webmaster ou IndexNow;
- não há alegação de indexação.

## Próximas ações

1. Confirmar com a HomeHost um endpoint FTPS/SFTP com certificado válido para `arquindex.com.br` ou instalar/corrigir o certificado do endpoint atual; não rebaixar para FTP sem criptografia.
2. Reexecutar a publicação seletiva dos três arquivos já versionados e exigir backup, readback, HTTP 200, canonical, identidade, CTA e teste mobile antes de atualizar o estado para “publicado”.
3. Continuar o cursor em ARQ-221–ARQ-226 e manter ARQ-216, ARQ-219 e ARQ-220 na rotação de identidade/conversão sem repetir o conteúdo preparado nesta rodada.
