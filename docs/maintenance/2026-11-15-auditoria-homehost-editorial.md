# Auditoria Arquindex — 15/11/2026

## Resumo executivo

O domínio institucional permaneceu acessível, mas as páginas prioritárias responderam lentamente e dois diretórios públicos expõem listagem automática. Não houve escrita na HomeHost, alteração de DNS, limpeza, deploy, submissão de sitemap ou envio de URL: faltam prova de backup completo restaurável, raiz pública e leitura FTPS segura da origem. Foram preparados dois artigos originais, ambos acima de 1.500 palavras úteis, em branch editorial separada e com `noindex,follow` até publicação comprovada.

## 1. Auditoria e deploy técnico

### Origem e governança

- Decisão operacional vigente: HomeHost é a produção de `arquindex.com.br` e `www.arquindex.com.br`.
- `master` consultada no GitHub: `7383179a2806be15250e55906e97a1596c9d3ea1`.
- `config/site-hosting.json` continua indicando HomeHost, propagação não confirmada e raiz de deploy ainda a descobrir/verificar.
- Railway permanece separado: `arquindex-web` aponta para `railway-production-2026`, não possui mudança staged e seu último deployment conhecido está falho/antigo. Nada disso foi usado como prova do site principal.
- DNS público consultado: nameservers `ns31.servidorwebsite.com` e `ns32.servidorwebsite.com`. Nenhuma alteração de DNS, nameserver ou e-mail foi feita.

### HTTP e SEO técnico

| URL | HTTP | TTFB | Canonical | Robots | H1 |
|---|---:|---:|---|---|---:|
| `/` | 200 | 6,206 s | própria | indexável | 1 |
| `/guarda_de_documentos.html` | 200 | 5,682 s | própria | indexável | 1 |
| `/gestao_de_colaboradores_documentos.html` | 200 | 4,750 s | própria | indexável | 1 |
| `/digitalizacao.html` | 200 | 4,911 s | própria | indexável | 1 |
| `/digitalizacao-com-ocr.html` | 200 | 4,761 s | própria | indexável | 1 |

Pendências mantidas:

- `/gestao_de_colaboradores_documentos.html` tem título duplicado `| Arquindex | Arquindex` e não apresenta JSON-LD.
- `/guarda_de_documentos.html` e a página de colaboradores não apresentaram o rastreamento observado nas demais páginas.
- Assets `/arquindex-favicon.png`, `/img/about.webp`, `/assets/img/about.webp` e `/css/IE-fix.css` continuam HTTP 404.
- `sitemap.xml` responde 200 e lista 579 URLs em 16 partes; `sitemap-index.xml` continua ausente no histórico. Não houve reconciliação nem submissão automática.
- As 72 rotas propostas para 24 cidades × três serviços continuam HTTP 404. Nenhuma foi criada para não produzir doorway pages nem concorrer com URLs existentes.

### Achado novo do módulo semanal

- `/assets/` responde 200 com `Index of /assets/`: 153 arquivos diretos e 12 subdiretórios reais visíveis.
- `/seo/` responde 200 com `Index of /seo/`: dez diretórios regionais Alfresco/OCR visíveis.
- As dez páginas regionais existentes responderam 200, têm canonical própria e conteúdo por cidade; serão preservadas e revisadas antes de qualquer expansão.
- Não foi encontrado nome evidentemente sensível no primeiro nível público, mas a listagem deve ser desativada.
- Plano de correção reversível: `docs/maintenance/2026-11-15-directory-listing-remediation.md`.
- Limpeza: 0 bytes liberados, 0 itens movidos, 0 itens removidos.

### Search Console e indexação

O conector de leitura funcionou. A propriedade `sc-domain:arquindex.com.br` aparece com acesso de proprietário, mas não está ativada para relatório. A propriedade ativa `http://arquindex.com.br/` mostrou, de 16/10 a 12/11/2026, 0 cliques, 54 impressões, CTR 0% e posição média 6,81; no período anterior foram 52 impressões e posição 5,00. A consulta `arquindex` teve 17 impressões e posição média 2,12.

Essa propriedade HTTP cobre apenas uma visão limitada e não substitui a propriedade de domínio. A lista de sitemaps contém submissões antigas, duplicadas e com avisos/erros. Nenhuma foi excluída. Próxima ação correta: ativar/validar a propriedade de domínio, reconciliar o sitemap público vigente e só então decidir sobre submissões obsoletas.

Não houve URL nova publicada. Portanto: GSC submetidas 0; IndexNow enviadas 0; indexação confirmada 0. Submissão e indexação continuam estados distintos.

### Conectores e bloqueios

- GitHub: leitura e escrita em branch editorial funcionaram.
- Railway: leitura funcionou; nenhuma mutação.
- GSC: leitura da propriedade HTTP funcionou; relatório da propriedade de domínio retornou `INVALID_ARGUMENT`, não 401/403/429/5xx.
- Cloudflare: leitura de identidade funcionou; descoberta adicional de endpoint retornou `INVALID_ARGUMENT`. DNS público foi consultado independentemente; nenhuma reconexão foi solicitada.
- Top10 privado: leitura foi barrada pelo controle de segurança porque a operação é classificada como não somente leitura/destrutiva sem escopo verificável. Não é falha 401/403/429/5xx e não houve contorno.
- CrUX e Bing Webmaster: integrações não configuradas com as chaves exigidas; nenhuma alegação de leitura ou envio.
- HomeHost: sem ferramenta capaz de provar nesta rodada a raiz pública, o backup completo restaurável e a leitura FTPS TLS. A existência de volume/bucket com nome de backup não comprova conteúdo nem restauração.

## 2. Dois artigos originais do dia

| Artigo | Palavras úteis | Estado | URL proposta |
|---|---:|---|---|
| Preservação digital com OAIS: como montar pacotes SIP, AIP e DIP com integridade verificável | 2.258 | CRIADA, não publicada | `/blog/preservacao-digital-oais-sip-aip-dip-integridade/` |
| Backup e restauração do Alfresco: banco, contentstore e índice sem perder consistência | 2.326 | CRIADA, não publicada | `/blog/backup-restauracao-alfresco-banco-contentstore-indice/` |

Os dois HTMLs incluem resposta direta, etapas, requisitos, segurança, qualidade, rastreabilidade, limites, exemplo hipotético, checklist, FAQ, fontes oficiais, autoria, data, links internos, CTA, canonical, Open Graph e schema coerente. Permanecem `noindex,follow` na fila editorial. Não foram adicionados ao sitemap nem chamados de publicados.

## 3. Gestão da fila Blogger

- Feed público consultado: 36 posts.
- Última postagem pública observada: `Workflow documental: como o Alfresco atende`, de 01/05/2026.
- Correspondências exatas com os oito títulos históricos pendentes: 0.
- Publicações hoje: 0.
- Bloqueio real: não há conector Blogger v3/Apps Script autenticado com OAuth de escrita para `arquindex@gmail.com`. Gmail ou Drive não substituem essa autorização. Nenhum POST foi tentado e não há resultado incerto.

## Páginas SEO e campanha regional

- Meta máxima do dia: 10 novas páginas.
- Criadas: 0; testadas: 0; publicadas: 0; submetidas: 0; indexadas confirmadas: 0.
- Déficit explícito: 10 em relação ao teto diário.
- Motivo: as 72 rotas estão públicas como 404 e não há dados suficientes de demanda/intenção por cidade nem origem HomeHost segura para publicar; criar variações agora elevaria risco de doorway e canibalização.
- O manifesto registra individualmente as 72 URLs planejadas e as dez páginas regionais existentes a preservar.

## Próximos passos exatos

1. HomeHost: fornecer/validar o marcador de backup completo fora de `public_html`, evidência de restauração isolada, raiz pública e leitura FTPS com certificado válido.
2. Aplicar então, de forma reversível, `Options -Indexes` na raiz correta; testar homepage, assets, `/seo/`, robots, sitemap, canonicals e subdomínios.
3. Corrigir assets 404 somente após localizar referências e origem real; não apagar nem substituir arquivos restaurados.
4. Ativar e validar o relatório da propriedade `sc-domain:arquindex.com.br`; reconciliar sitemaps antigos sem exclusão em massa.
5. Revisar e aprovar a branch editorial; após deploy HomeHost, fazer leitura pública HTTP/canonical/conteúdo antes de retirar `noindex` e submeter URLs.
6. Conectar Blogger v3 ou Apps Script com OAuth de escrita e readback; publicar uma pauta por vez após checagem de título e ID.
