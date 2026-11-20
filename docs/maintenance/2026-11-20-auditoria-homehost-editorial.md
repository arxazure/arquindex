# Auditoria Arquindex — 20/11/2026

## Resumo executivo

O domínio institucional respondeu por HTTPS com conteúdo, canonical e metadados do site restaurado; a delegação pública observada aponta para `ns31.servidorwebsite.com` e `ns32.servidorwebsite.com`, o A da raiz para `177.234.150.42` e `www` como CNAME da raiz. Isso é compatível com a decisão HomeHost, mas não substitui prova da raiz, backup e acesso FTPS. Não houve escrita, limpeza, deploy, sitemap ou submissão. Foram preparados dois artigos originais em branch editorial separada, ambos acima de 1.500 palavras e com `noindex,follow`.

## 1. Auditoria e deploy técnico

### Origem, GitHub e hospedagem

- `master`: `e804ff83ad506030fca5f17bab61aff2a4943884`, commit de 19/11/2026 20:47 BRT.
- O PR [#103](https://github.com/arxazure/arquindex/pull/103) está **incorporado**, commit de merge `269707b86875477d953eae3721a36b3a22f4d19a`; a premissa antiga de que aguardava merge não é mais atual.
- `AGENTS.md` e `config/site-hosting.json` em `master` determinam HomeHost como destino do site institucional. O JSON ainda mantém `public_propagation_status: not_confirmed` e raiz de deploy a descobrir.
- DNS público via Google DNS em 20/11/2026: NS `ns31.servidorwebsite.com` e `ns32.servidorwebsite.com`; A `177.234.150.42`; `www` CNAME `arquindex.com.br`.
- HTTPS/TLS foi aceito para raiz e `www`, ambos HTTP 200, com o mesmo conteúdo, tamanho e `Last-Modified: 08/11/2026 18:38:54 BRT`.
- A conexão Cloudflare autenticou (`arquindex@gmail.com`), mas a conta conectada não retornou zona `arquindex.com.br`. O CNAME Railway registrado no aviso de 01/11 não foi tratado como estado atual nem alterado.

### Railway separado

- Projeto lido: `Arquindex Plataforma`, ambiente `production`, serviço `arquindex-web`.
- Origem configurada: repositório `arxazure/arquindex`, branch `railway-production-2026`, raiz `/arquindex-platform`.
- Mudanças staged: nenhuma.
- Os cinco deployments mais recentes retornados estão `REMOVED`; o mais novo foi criado em 05/11/2026. Não há deployment ativo usado como prova do domínio institucional.
- A configuração Railway ainda lista `arquindex.com.br` como custom domain, mas o DNS público atual aponta para o par de nameservers HomeHost. Nenhuma alteração foi feita em Railway ou DNS.

### HTTP, SEO técnico e conteúdo

| URL | HTTP | Canonical | H1 | Schema | Achado |
|---|---:|---|---:|---:|---|
| `/` | 200 | própria | 1 | 2 | título ainda repete a marca no início e no fim |
| `/guarda_de_documentos.html` | 200 | própria | 1 | 1 | href interno com espaço inicial antes da URL de recrutamento |
| `/gestao_de_colaboradores_documentos.html` | 200 | própria | 1 | 0 | título termina em `| Arquindex | Arquindex`; sem JSON-LD |
| `/digitalizacao.html` | 200 | própria | 1 | 4 | indexável |
| `/digitalizacao-com-ocr.html` | 200 | própria | 1 | 3 | indexável |

Todos os cinco documentos têm `viewport`, `index,follow` e canonical autorreferente. Os recursos `/arquindex-favicon.png`, `/img/about.webp`, `/assets/img/about.webp` e `/css/IE-fix.css` continuam HTTP 404. Os diretórios `/assets/` e `/seo/` continuam HTTP 200 com `Index of /`; nenhuma proteção foi aplicada porque não há prova de backup/raiz.

O `robots.txt` responde 200 e permite rastreamento público, bloqueando áreas administrativas e privadas. O `sitemap.xml` responde 200 como índice; as 16 partes responderam 200 e somam 579 URLs. As quatro páginas prioritárias de serviço estão incluídas. `sitemap-index.xml` responde 404. Nenhuma alteração ou submissão foi feita.

### Fila regional e canibalização

- As 72 rotas planejadas (24 cidades × digitalização, guarda e consultoria LGPD) foram revalidadas: **72 HTTP 404**.
- Novas páginas: 0; criadas: 0; testadas: 0; publicadas: 0; submetidas: 0; indexadas confirmadas: 0.
- Déficit explícito contra o teto de dez: 10. O teto não é obrigação de criar páginas sem demanda e diferenciação.
- Seis páginas existentes da fila foram relidas. ARQ-072, 074, 077, 079 e 083 seguem como variações extensas com provável template comum; ARQ-080 mantém canonical incorreta. Nenhuma delas foi alterada.
- O GSC não apontou canibalização na pequena amostra disponível. Isso não comprova ausência global; a propriedade ativa é HTTP e tem cobertura limitada.

### Search Console — saúde: **Em risco**

`get_site_summary`, 21/10–17/11/2026, comparado a 23/09–20/10/2026: 0 cliques, 47 impressões, CTR 0% e posição média 5,74; período anterior: 0 cliques, 55 impressões e posição 6,20. A posição melhorou 0,46, mas as impressões caíram 8 e não houve clique.

`get_position_distribution`, mesma janela: das 26 impressões atribuídas a consultas, 15 (57,7%) ficaram nas posições 1–3, 9 (34,6%) nas posições 4–10 e 2 (7,7%) nas posições 11–20. A oportunidade automática principal é a consulta `slice`, 9 impressões, posição 8 e 0 clique — termo sem relação comercial clara com Arquindex. Portanto, não deve orientar conteúdo.

`detect_anomalies`, 20/08–17/11/2026, marcou quatro dias de zero impressões como quedas críticas; com volume diário esperado de apenas 3, os alertas são de baixa base e não justificam mudança isolada. `get_decay_overview`, ago–out/2026, registrou 149 impressões e 0 cliques. `get_core_web_vitals` não trouxe dados configurados. A lista do GSC contém 18 submissões históricas; o `sitemap.xml` principal registra 579 URLs, 3 avisos, 0 erros e download em 18/11/2026. Não houve exclusão ou nova submissão.

### Bloqueios e ações preservadas

- HomeHost: não existe conector que prove leitura FTPS, raiz pública e backup integral restaurável. Bloqueio de capacidade, não 401/403/429/5xx.
- GSC: leitura funcionou; não pedir reconexão. Nenhuma URL nova elegível foi publicada.
- Cloudflare: autenticação funcionou, mas a zona `arquindex.com.br` não está na conexão consultada; nenhuma escrita.
- Central privada Top10: leitura inofensiva funcionou; há registros históricos em estados `claimed` e `unknown`, por isso nenhuma repetição ou nova publicação foi tentada.
- Merchant Center: não auditado nesta frente e permanece separado.
- Limpeza semanal: hoje é sexta-feira; módulo semanal não executado. Removidos/movidos: 0; espaço liberado: 0 bytes.

## 2. Dois artigos originais do dia

| Artigo | Palavras úteis | Estado | URL proposta |
|---|---:|---|---|
| Auditoria no Alfresco: como planejar trilhas, logs e integração com SIEM | 1.793 | CRIADA, não publicada | `/blog/auditoria-alfresco-trilhas-logs-siem/` |
| Databook e Plano de Inspeção e Testes: rastreabilidade do critério à evidência | 1.941 | CRIADA, não publicada | `/blog/databook-plano-inspecao-testes-pit-rastreabilidade/` |

Os dois HTMLs incluem H1/H2/H3, resposta direta, definições, etapas, requisitos/entregáveis, segurança, qualidade, rastreabilidade, limites, exemplo hipotético, checklist, FAQ, fontes oficiais datadas, autoria, links internos, CTA, canonical, Open Graph e `TechArticle`. Ambos ficam `noindex,follow` até deploy HomeHost e readback público. As URLs propostas estavam ausentes do inventário e não repetem os temas dos PRs editoriais abertos.

## 3. Gestão da fila Blogger

- Blog ID público: `2545952967912533152`.
- Feed atualizado em 18/10/2026; 36 posts.
- Postagem pública mais recente observada: “Workflow documental: como o Alfresco atende”, publicada em 01/05/2026.
- Correspondências exatas com os oito títulos históricos: 0.
- Publicações nesta execução: 0.
- Bloqueio: não há conector Blogger v3/Apps Script autenticado com escopo de escrita e readback. Nenhum POST foi tentado; não existe resultado incerto.

## Próximos passos exatos

1. HomeHost: confirmar backup integral fora da raiz pública, restauração testada, mapeamento de `public_html` e leitura FTPS com certificado válido.
2. Depois disso, corrigir primeiro `Options -Indexes`, os quatro recursos 404, o href com espaço e o título/schema da página de colaboradores, com rollback e teste público.
3. Revisar a família ARQ-072/074/077/079/083 como template, não por substituições cegas; corrigir ARQ-080 somente após mapear origem e atendimento local.
4. Revisar o PR editorial; publicar os artigos apenas após retirar `noindex` no pacote aprovado, deploy HomeHost e leitura pública HTTP/canonical/conteúdo.
5. Reconciliar sitemaps históricos no GSC depois de corrigir origem, sem exclusão em massa e sem confundir submissão com indexação.
6. Conectar Blogger v3 ou Apps Script com OAuth de escrita e readback antes de publicar uma pauta da fila.
