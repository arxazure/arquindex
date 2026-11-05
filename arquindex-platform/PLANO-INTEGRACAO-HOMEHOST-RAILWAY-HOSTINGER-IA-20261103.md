# Arquindex — matriz de publicacao SEO, GEO, AEO e indexacao (03/11/2026)

## Projeto correto
- Marca: **Arquindex Gestão Documental LTDA**.
- Fonte de codigo de producao na Railway: `arxazure/arquindex`, branch `railway-production-2026`, diretorio `arquindex-platform/`.
- Site corporativo canonico pretendido: `https://arquindex.com.br/` (verificar resposta HTTPS, redirecionamentos e propriedade efetiva do DNS).
- Railway: projeto **Arquindex Plataforma**, servico **arquindex-web**. Endereco de preview: `https://arquindex-web-production.up.railway.app/`.
- HomeHost: publicacao por FTP/FTPS deve depender de credenciais guardadas em segredos, teste de conectividade e inventario do conteudo atual.
- Hostinger: verificar se hospeda apenas VPS, subdominios, correo ou outro papel; **nao publicar copias concorrentes** sem definir a origem canonica.
- ChatGPT e outros assistentes: `robots.txt`, HTML acessivel e conteudo referenciado ajudam descoberta, mas nao existe uma API universal de submissao para garantir exibicao em respostas de IA.

## Conteudo preparado na Railway
Cinco novos guias empresariais em `arquindex-platform/arquindex-seo-nov2026.js`, importados no `server.js`, sao publicados na rota `/conteudo/<slug>` quando a implantacao finalizar.

## Regras obrigatorias antes da replicacao
1. Confirmar o DNS/servidor efetivo de `arquindex.com.br`; Railway e HomeHost nao devem responder com conteudos divergentes para a mesma URL.
2. Conferir respostas HTTP 200, titulo, canonical, meta robots, JSON-LD, links internos e sitemap.
3. Para HomeHost: gerar arquivos HTML estaticos com paths equivalentes ou configurar proxy/rewrite validado; **nao copiar o codigo Node puro para hospedagem PHP** supondo execucao.
4. Para Hostinger: somente conectar quando houver dominio/subdominio definido e ownership verificado; evitar duplicar conteudo da HomeHost/Railway.
5. Publicar sitemaps somente com URLs definitivas 200/canonicas e aprovadas; utilizar GSC da propriedade verificada. IndexNow vale para motores participantes, nao substitui GSC nem comprova indexacao.
6. Referencias e estudos: nao apresentar supostas notas oficiais do Google/Bing nem recomendar resultados garantidos.
7. Medir queries, paginas, impressões, CTR, cliques e posicao real, separando RM BH, RM SP e consultas nacionais.
8. Nenhuma pagina da Clinica Bem Viver ou Dra. Maria Olimpia integra esta publicacao: esses projetos sao independentes.

## Condicoes para declarar 'publicado em todos os hosts'
- Evidencia de commit+deploy Railway SUCCESS e GET publico de cada URL.
- Evidencia de copia e GET publico correspondente na HomeHost, sem sobrescrita nao auditada.
- Evidencia de destino configurado na Hostinger, se aplicavel, e retorno do deploy.
- Propriedade GSC validada e comprovante de submissao; checagem posterior de indexacao.
