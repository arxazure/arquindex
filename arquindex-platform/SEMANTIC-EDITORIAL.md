# Integração semântica — Railway real

O serviço Railway `arquindex-web` utiliza o repositório `arxazure/arquindex`, branch `railway-production-2026`, root `/arquindex-platform`, comando `npm start`.

Este módulo analisa **as estruturas reais** `articles.js` e `editorial-production-queue.js`, gerando relatório JSON com recomendações contextuais para revisão.

```bash
node --test arquindex-platform/semantic-editorial-export.test.mjs
node arquindex-platform/semantic-editorial-export.mjs ./seo-editorial-preview
```

Este PR **não** altera `server.js`, `index.html`, títulos HTML, preços ou o deployment. O arquivo exportado exige revisão antes de qualquer alteração editorial. As palavras devem ser incorporadas somente quando cabíveis, com dados e fontes verificáveis. Não há promessa de Top 10.

Próxima etapa de produção: revisão de sugestões -> aplicar alterações em artigos selecionados -> testes das rotas -> deploy -> verificar HTTP 200, conteúdo renderizado, canonical e sitemap.
