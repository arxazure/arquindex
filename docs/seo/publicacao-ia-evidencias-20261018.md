# Publicação IA documental — 18/10/2026 (Brasília)
Autorização: usuária solicitou “Continua e publicar”.
Destino preparado: https://www.arquindex.com.br/noticias/ia-documental-evidencias-sandbox-anpd-2026.html
Conteúdo-fonte commit: fe551c62e57834e45609dc28fc1015f3f4d516db.
Workflow atual: https://github.com/arxazure/arquindex/actions/runs/39175921953
Estado: publicação em andamento; não divulgar destino até HTTP 200 e verificação.
Deduplicação: Instagram já tem post de IA 18146587129575477, https://www.instagram.com/p/DepRZbNkfux/, com imagem; Google já tem post IA 3745048192412054004 LIVE com imagem. Preservar, atualizar CTA/complementar somente após artigo válido. LinkedIn leitura de 18/10 retornou zero linhas, recorte 17–18 só trouxe 17/10; não interpretar ausência como exclusão de posts.
Correção anterior autorizada de artes: seis posts Google existentes sem mídia receberam update_local_post apenas no campo media; retorno PROCESSING, não confirmar LIVE por esta alteração ainda.
IDs: accounts/111390525053034972643/locations/2344229015359741158/localPosts/4137904185121464806, accounts/111390525053034972643/locations/2344229015359741158/localPosts/4561807689816400013, accounts/111390525053034972643/locations/2344229015359741158/localPosts/1796669045977739482, accounts/111390525053034972643/locations/2344229015359741158/localPosts/3135480289760791973, accounts/111390525053034972643/locations/2344229015359741158/localPosts/1465042719566009576, accounts/111390525053034972643/locations/2344229015359741158/localPosts/8442530750504024896.
Nenhuma exclusão ou anúncio pago.

## Resultado confirmado
- Artigo: https://www.arquindex.com.br/noticias/ia-documental-evidencias-sandbox-anpd-2026.html
- HTTP 200, bytes publicados, imagem JPEG 800×800 (161531 bytes), canonical e um H1 conferidos. Índices /noticias/ e /blog/ contêm link real para o artigo.
- Publicação: workflow https://github.com/arxazure/arquindex/actions/runs/39175921953 — success. Script dc7fddaccce56219012a46979b7f205b29ad8fb3; conteúdo fe551c62e57834e45609dc28fc1015f3f4d516db.
- Hash artigo: c6a7585ce1814ebe4f5927b30948d6b5b0e64a0a80df8826d743472f6fe72b49.
- Imagem: https://www.arquindex.com.br/assets/social/ia-evidencias-20261018.jpg, arte existente reaproveitada do post IA, normalizada em JPEG; não foi gerada nova arte.
- Sitemap de notícias e sitemap.xml atualizados, parseados e acessíveis por HTTP 200.
- LinkedIn: create_image_post confirmou urn:li:share:7517726067898490880 com a URL da imagem e texto contendo o artigo. Link: https://www.linkedin.com/feed/update/urn:li:share:7517726067898490880/
- Instagram: post com arte já existente https://www.instagram.com/p/DepRZbNkfux/ foi preservado. Comentário complementar confirmado 18060777266546724 com endereço do artigo e aviso de URL não clicável. Nenhum novo feed duplicado.
- Google Business: post existente 3745048192412054004 atualizado com arte, resumo e CTA do artigo; retorno PROCESSING. A imagem já constava LIVE antes desta alteração, mas o novo CTA/mídia ainda exige revalidação.
- Seis correções de mídia anteriores: aceitas pelo Google com PROCESSING, sem criar novos posts.
- As leituras sem force_refresh funcionaram. A opção force_refresh foi recusada pelo plano TRIAL; não é falha de autenticação. Dados LinkedIn de 18/10 não estavam disponíveis, por isso a ação nova foi restrita ao artigo ainda inédito em URL própria, sem alegar auditoria completa do feed atual.

## Pendências
- Submissão Google Search Console/Bing/IndexNow não executada: nenhum endpoint de envio autenticado suportado foi exposto neste conector. Registrar URL/sitemap para a fila de submissão, sem afirmar envio ou indexação.
- Posts antigos do LinkedIn de 17/10 sem mídia: o conector expõe criação, não edição/exclusão de posts. Não republicados em massa para evitar duplicações.
- ARQ-012 continua na fila técnica; esta publicação não alterou páginas parametrizadas.
