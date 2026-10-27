# Biblioteca técnica — publicação de enriquecimento

Data: 27/10/2026 (America/Sao_Paulo). Issue: #42.

Publicação solicitada explicitamente pelo usuário após entrega da matriz e dos cinco rascunhos. Base recuperável: `6d3ddc2674f0fea0f18cacc4834b8953250bc40c`. O rollback desta alteração deve restaurar apenas os seis HTMLs modificados, preservando eventuais alterações posteriores nos demais arquivos.

## Alteração

Enriquecidos três manuais operacionais e dois roteiros de decisão nas mesmas URLs. Incluídos procedimentos, entradas, entregáveis, segurança, critérios de qualidade, exemplos sintéticos, perguntas frequentes e referências. Cabeçalho, sumário, tabelas roláveis e estilos de impressão nos cinco recursos. Schema TechArticle nos manuais e WebPage nas apresentações, consistente com conteúdo visível. Resumos dos cinco cards do índice diferenciados.

Não alterados servidor, DNS, sitemap, robots, analytics, workflows nem rotinas de indexação. Não há promessa de validade jurídica automática. Recursos Alfresco permanecem condicionados à edição, versão e configuração do projeto. Não foram criadas variações por cidade.

## Validação anterior ao envio

- Cinco recursos com GET e HEAD 200 no servidor local.
- Uma canonical própria e um H1 por recurso; JSON-LD parseável, tipo e URL conferidos.
- Âncoras resolvidas e links internos testados com HTTP 200.
- Conteúdo novo conferido e nenhum marcador editorial privado incluído.
- Gerador de sitemap sem alteração; recursos continuam fora do sitemap.
- `node --check arquindex-platform/server.js` aprovado; quatro testes existentes de redirecionamento aprovados; `git diff --check` aprovado.
- QA visual/mobile/print por navegador NÃO realizado: instalação de Chromium falhou no ambiente. CSS responsivo e de impressão presente, sem afirmação de validação visual.

## Fontes

Complementadas referências à Resolução CD/ANPD 18/2024 no PDF hospedado pela ANPD e à página oficial de comunicação de incidentes que referencia a Resolução 15/2024. Mantidos Decreto 10.278/2020, LGPD, CONARQ 50/2022 e documentação veraPDF. A documentação Alfresco é uma referência para avaliação da versão, sem promessa de funcionalidade validada nesta publicação.

## Verificação posterior

Acompanhar status do commit no GitHub e validar as cinco páginas públicas, incluindo conteúdo novo e schema. O conector Railway retornou UNAUTHORIZED na preparação; o envio utiliza a branch já vinculada ao deploy automático. Não tratar commit enviado como comprovação de deploy ou indexação. A configuração de GA4 permanece pendente.

## Continuação após deploy

O commit `40f901c84839bd8443563027f59b4d382d46568c` recebeu status de sucesso no serviço Arquindex Plataforma. Foi observada no navegador a versão nova do manual OCR, com sumário, conteúdo ampliado e aparência desktop legível. A avaliação visual móvel e de impressão continua pendente.

A checagem externa encontrou 404 em `https://docs.alfresco.com/content-services/`. Corrigida a referência nas duas páginas para `/content-services/latest/`, que respondeu HTTP 200 após redirecionar para a documentação oficial Hyland. Fontes ANPD e veraPDF responderam 200. Nenhuma capacidade específica Alfresco foi inferida dessa checagem de disponibilidade.
