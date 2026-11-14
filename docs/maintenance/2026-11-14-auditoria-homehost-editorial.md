# Auditoria técnica e editorial Arquindex — 14/11/2026

## Resumo executivo

A decisão operacional continua sendo HomeHost para o site institucional. A evidência pública está coerente com essa orientação: os nameservers consultados foram `ns31.servidorwebsite.com` e `ns32.servidorwebsite.com`, e o domínio resolveu para `177.234.150.42`. HTTPS respondeu sem desabilitar a validação de certificado. Isso não comprova, por si só, a raiz de publicação nem a existência de backup restaurável fora de `public_html`.

Nenhuma escrita foi feita na HomeHost, no DNS, no Railway, no GSC, no IndexNow ou no Blogger. A razão é objetiva: a raiz pública HomeHost e um backup completo restaurável ainda não foram comprovados nesta execução. O módulo semanal de limpeza não era devido neste sábado.

Foram preparados e validados localmente dois artigos técnicos originais, ambos com mais de 1.500 palavras úteis e marcados `noindex,follow` enquanto permanecem fora de produção. Eles foram enviados a uma branch editorial e a uma pull request em rascunho; não são publicações.

## 1. Auditoria e deploy técnico

### Origem e controle de versão

- Repositório: `arxazure/arquindex`.
- Branch base observada: `master`.
- SHA base: `9c683bf8370b31730f11474267a70df0b42f2a4c`.
- `config/site-hosting.json` e `AGENTS.md` em `master` identificam HomeHost como produção institucional.
- A PR #146, de 13/11, continua aberta e em rascunho; no momento da leitura estava `mergeable: false`. Não foi rebaseada nem forçada.
- Branch desta execução: `editorial/2-artigos-20261114`.

### DNS, HTTPS e conteúdo público

| Verificação | Resultado |
|---|---|
| `http://arquindex.com.br/` | 301 para `https://arquindex.com.br/` |
| `https://arquindex.com.br/` | 200; canonical para `https://www.arquindex.com.br/` |
| `http://www.arquindex.com.br/` | 301 para HTTPS |
| `https://www.arquindex.com.br/` | 200; canonical próprio |
| NS públicos | `ns31.servidorwebsite.com`, `ns32.servidorwebsite.com` |
| A público | `177.234.150.42` |
| TLS | conexão HTTPS validada por `curl`, sem ignorar certificado |

A versão HTTPS sem `www` entrega 200, não redireciona, mas declara canonical para `www`. Isso evita a duplicação canônica declarada, embora um redirecionamento permanente para a variante escolhida seja tecnicamente mais claro. Não foi alterado.

O conector Cloudflare permitiu leitura de identidade, mas listou zero zonas. A tentativa inofensiva de ler o antigo zone ID retornou HTTP 400, código 1001, “Invalid zone identifier”. Portanto, o CNAME histórico para Railway não foi tratado como evidência atual. Nenhuma alteração de DNS, nameserver ou e-mail foi feita.

### Páginas prioritárias

| URL | HTTP | TTFB | Canonical/noindex | Achados |
|---|---:|---:|---|---|
| `/` | 200 | 5,79 s | próprio / sem noindex | H1, main e 2 JSON-LD; 2 IDs AW |
| `/guarda_de_documentos.html` | 200 | 6,23 s | próprio / sem noindex | sem elemento main; 1 JSON-LD; rastreamento não detectado |
| `/gestao_de_colaboradores_documentos.html` | 200 | 6,37 s | próprio / sem noindex | sem main e JSON-LD; título repete “| Arquindex” |
| `/digitalizacao.html` | 200 | 3,27 s | próprio / sem noindex | H1, main, 4 JSON-LD; 2 IDs AW |
| `/digitalizacao-com-ocr.html` | 200 | 3,10 s | próprio / sem noindex | H1, main, 3 JSON-LD; 2 IDs AW |

Os tempos acima são amostras de uma requisição e não substituem dados de campo. As páginas prioritárias responderam, mas o tempo até o primeiro byte ficou entre 3,10 s e 6,37 s, justificando análise de servidor/cache em janela controlada.

### Rastreamento, arquivos e sitemaps

- `robots.txt`: 200.
- `sitemap.xml`: 200; 16 sitemaps filhos e 579 entradas contadas.
- `sitemap-index.xml`: 404. Não é, isoladamente, um erro se a propriedade e o robots apontarem para `sitemap.xml`.
- Recursos 404 confirmados: `/arquindex-favicon.png`, `/img/about.webp`, `/assets/img/about.webp` e `/css/IE-fix.css`.
- A cobertura de rastreamento não é uniforme: as duas páginas institucionais antigas auditadas não exibiram os IDs AW vistos na homepage e nas páginas de digitalização.
- Não houve substituição de homepage, menu, CSS ou arquivo restaurado.

### Campanha regional 24 × 3

As 72 rotas previstas no padrão `/seo/{servico}/{cidade}/empresa` retornaram 404: zero estavam públicas. Cada intenção foi registrada no manifesto como `PLANEJADA`, não como criada ou publicada. Nenhuma página regional foi gerada porque o GSC não forneceu a demanda/consulta necessária e a produção mecânica criaria risco de doorway pages e canibalização.

Resultado diário de páginas SEO: **0 criadas, 0 testadas para produção, 0 publicadas, 0 submetidas, 0 indexadas** (limite de até 10, não uma obrigação de preencher sem evidência).

### GSC, IndexNow e Railway

A leitura da lista de propriedades do GSC funcionou. `sc-domain:arquindex.com.br` apareceu com permissão `siteOwner`, mas `activated: false`. Oito leituras de auditoria foram tentadas e retornaram `INVALID_ARGUMENT`; não foi 401, 403, 429 ou 5xx. Passo necessário: selecionar/ativar essa propriedade no GSC Wizard. Nenhuma URL foi submetida.

No Railway, o projeto Arquindex Plataforma foi lido separadamente. Não havia staged changes. O serviço web não possuía deploy ativo atual: os recentes constavam como `REMOVED`, e havia um deploy antigo `FAILED`. Nenhum status do Railway foi usado como comprovação do site institucional e nenhum redeploy foi iniciado.

### HomeHost e módulo semanal

- FTPS: nenhuma escrita tentada.
- Backup completo restaurável fora de `public_html`: não comprovado.
- Volume Railway `/backups` e bucket com nome de backup não provam que exista snapshot restaurável atual da HomeHost.
- Limpeza semanal: não executada, pois a data era sábado. O próximo módulo só pode remover ou colocar em quarentena depois de inventário, cruzamento com referências/GSC e comprovação do backup.

## 2. Dois artigos técnicos originais

| Título | Palavras úteis no main | Estado | URL planejada |
|---|---:|---|---|
| Plano de emergência para acervos físicos: água, fogo, pragas e cadeia de custódia | 1.935 | CRIADA E TESTADA LOCALMENTE | `/blog/plano-emergencia-acervos-fisicos-agua-fogo-pragas-cadeia-custodia/` |
| Alfresco WebDAV no Windows: limites, segurança e sincronização controlada | 2.024 | CRIADA E TESTADA LOCALMENTE | `/blog/alfresco-webdav-windows-limites-seguranca-sincronizacao/` |

Os dois HTMLs possuem H1/H2/H3, resposta direta, etapas, riscos, checklist, FAQ visível, fontes oficiais datadas, autoria, links internos, canonical planejado, Open Graph, TechArticle, FAQPage e CTA Arquindex. JSON-LD foi parseado sem erro. O texto de exemplo do artigo de emergência está explicitamente marcado como hipotético, sem cliente, volume ou resultado inventado.

Fontes primárias usadas incluem CONARQ, National Archives dos Estados Unidos, Microsoft Learn e documentação oficial Alfresco/Hyland. Como os arquivos não estão na HomeHost, estão com `noindex,follow` e **não são publicados**.

## 3. Gestão da fila Blogger

A leitura pública do feed funcionou:

- 36 posts públicos encontrados.
- Nenhum dos oito títulos da fila histórica apareceu como correspondência exata.
- O post público mais recente identificado continua sendo de 01/05/2026.
- Não há conector Blogger v3, Apps Script autenticado ou outro canal oficial com escopo de escrita nesta execução.

Resultado: **0 posts publicados**. Nenhum POST foi tentado e não há resultado incerto para repetir. A fila histórica continua pendente.

## Alterações efetivamente realizadas

- Preparados dois artigos inéditos.
- Criado manifesto completo com as 72 intenções regionais e estado por URL.
- Criado este relatório de evidências.
- Branch e PR em rascunho preparadas no GitHub.
- HomeHost: 0 arquivos alterados.
- DNS/Cloudflare: 0 alterações.
- Railway: 0 alterações.
- GSC/IndexNow: 0 submissões.
- Blogger: 0 publicações.

## Pendências e próximo passo exato

1. **HomeHost — publicação institucional:** comprovar a raiz pública e um backup completo restaurável fora de `public_html`; depois validar uma leitura FTPS com certificado válido. Só então revisar a PR, publicar arquivos aprovados e fazer readback HTTP.
2. **GitHub — PR #146:** resolver o conflito com `master` por revisão humana ou rebase controlado antes de qualquer merge; não forçar.
3. **GSC Wizard — `sc-domain:arquindex.com.br`:** selecionar/ativar a propriedade que já aparece com `siteOwner`; repetir auditorias antes de decidir novas páginas.
4. **Site público:** localizar referências reais dos quatro assets 404 antes de restaurar ou remover; corrigir título/schema/main/rastreamento das páginas antigas em lote reversível.
5. **Performance:** medir cache/origem em várias amostras e fora do pico antes de modificar servidor.
6. **Blogger:** autorizar Blogger API v3/Apps Script com a conta correta, conferir blog ID e títulos, publicar uma vez e fazer readback de ID/URL.

