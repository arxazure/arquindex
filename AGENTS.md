# Site institucional: produção na HomeHost

Em 01/11/2026 (America/Sao_Paulo), Marina informou que devolveu o site
`arquindex.com.br` / `www.arquindex.com.br` à **HomeHost**. Esta decisão substitui
instruções anteriores que tratavam Railway como produção desses dois hosts.
O contrato de destino está em `config/site-hosting.json`.

- Audite a resposta atual do domínio; não conclua propagação a partir da decisão da usuária.
- Publique o site principal na origem HomeHost verificada, com backup e FTPS/TLS válido.
- Preserve o conteúdo restaurado, URLs, blog, clientes, planos, menus e recursos. Não substitua o site por páginas resumidas ou textos de planejamento SEO.
- Push em `master`, push em `railway-production-2026` ou deploy SUCCESS no Railway não comprovam publicação no domínio oficial. Confirme por leitura pública do conteúdo.
- Referências históricas a Railway são evidência de operações anteriores, não instrução vigente de hospedagem.
- Não reverta DNS/nameservers e não altere e-mail para tentar recuperar publicação.
- Cloudflare pode permanecer como DNS/proxy; verifique a situação atual sem modificá-la.
- A decisão abrange apenas o site institucional `.com.br`. Não migre aplicativos Capture, LGPD Checklist, Alfresco, portais, MIO/Bem Viver nem o site secundário `.com` e outros projetos independentes.
- Mantenha o escopo e os limites originais de cada rotina; auditorias de leitura continuam de leitura. Não reative rotinas pausadas nem duplique publicações.

Consulte `docs/infraestrutura/homehost-retorno-2026-11-01.md` para o registro operacional.
