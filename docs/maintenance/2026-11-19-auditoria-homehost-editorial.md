# Auditoria Arquindex — 19/11/2026

## Escopo e decisão de hospedagem

A decisão operacional é HomeHost como origem autorizada do site institucional. A leitura pública em 19/11/2026 confirmou delegação para `ns31.servidorwebsite.com` e `ns32.servidorwebsite.com`, apex `177.234.150.42` e `www` como CNAME de `arquindex.com.br`. Requisições HTTPS com validação TLS normal foram concluídas. O PR #103 já está incorporado à `master`, apesar de instruções históricas ainda o descreverem como pendente.

Essas evidências sustentam a propagação pública para a infraestrutura HomeHost. Elas não comprovam a raiz de documentos, um backup restaurável nem a rota FTPS de escrita. Portanto, nenhuma alteração foi enviada ao servidor e nenhum deploy Railway foi tratado como publicação do domínio principal.

## Auditoria técnica pública

- 15 alvos prioritários consultados: todos responderam HTTP 200; não houve 3xx, 4xx ou 5xx nesses alvos.
- `robots.txt`, `sitemap.xml`, 16 sitemaps filhos e 22 recursos CSS/JS/imagem responderam HTTP 200.
- Os 16 sitemaps filhos somam 579 referências declaradas. Quatro das seis páginas regionais verificadas já constam nos sitemaps dedicados; duas estão ausentes: `/digitalizacao-documentos-belo-horizonte.html` e `/consultoria-lgpd-belo-horizonte.html`.
- `/assets/` e `/seo/` ainda exibem `Index of /`; não houve correção sem confirmar a configuração HomeHost e o backup.
- Em `gestao_de_colaboradores_documentos.html`, há um `href` malformado com espaço inicial para um endereço antigo de recrutamento. O destino normalizado redireciona para `/trabalhe-conosco/`, mas o HTML deve ser corrigido na origem depois da validação de escrita.
- A mesma página tem título duplicando a marca e não contém JSON-LD. A homepage apresenta dois H1. Os demais alvos prioritários têm canonical próprio e robots indexável.
- Nenhum recurso quebrado foi encontrado. O widget externo de LGPD foi o recurso mais lento no teste e redireciona para outro domínio do fornecedor.

## Search Console

Propriedade ativa consultada: `http://arquindex.com.br/`. A propriedade de domínio existe, mas não está ativada no conector e retornou argumento inválido para análise.

- Período consolidado: 20/10 a 16/11/2026; dados completos até 17/11.
- Atual: 0 cliques, 46 impressões, CTR 0%, posição média 5,83.
- Comparação anterior: 0 cliques, 56 impressões, CTR 0%, posição média 6,21.
- Variação: -10 impressões e melhora de 0,39 posição média.
- Distribuição das consultas visíveis: 15 impressões em posições 1–3, 9 em 4–10 e 2 em 11–20. As consultas apresentadas são majoritariamente irrelevantes para os serviços Arquindex, portanto não justificam novas páginas.
- Nenhuma canibalização detectada, mesmo após relaxamento automático para uma impressão.
- Quatro dias de queda a zero foram marcados como anomalias em 90 dias: 28/08, 23/10, 30/10 e 13/11.
- Core Web Vitals de campo não foram lidos porque a chave CrUX não está configurada.
- O GSC mantém 18 submissões históricas de sitemap/listas. O sitemap principal tem 579 URLs declaradas, três avisos e zero erros; várias submissões legadas têm erros ou avisos e devem ser reconciliadas sem novo envio em massa.

## Railway e Cloudflare

- Railway autenticado; projeto Arquindex Plataforma legível.
- Serviço `arquindex-web`: branch `railway-production-2026`, raiz `/arquindex-platform`, sem staged changes. O último deploy resumido permanece `FAILED` em 28/10/2026; nenhum status Railway foi usado como evidência do site institucional.
- O conector Cloudflare autenticou, mas a conta conectada não expõe a zona `arquindex.com.br`; apenas `arquindex-capture.stream`. Isso é ausência do recurso nessa conta, não falha 401. A leitura DNS pública foi concluída de forma independente.

## Páginas SEO regionais

As 72 URLs planejadas do inventário 24 cidades × 3 serviços foram verificadas individualmente em 19/11: 72 responderam HTTP 404 e permanecem PLANEJADAS, sem evidência de publicação, submissão ou indexação. O manifesto registra serviços, cidades, template e o estado uniforme aplicável a cada URL, preservando como fonte detalhada por URL o manifesto do PR #148. As seis páginas regionais existentes revalidadas em 18/11 continuam HTTP 200 em 19/11; elas não usam essas URLs planejadas e não foram contabilizadas como novas. Nenhuma das dez vagas editoriais foi preenchida: o GSC não apresentou intenção comercial distinta e comprovada que justificasse nova página, enquanto há pendências existing-first de sitemap, directory listing, título, schema e link interno. Estados do lote de novas páginas: PLANEJADA 72; CRIADA 0; TESTADA 0; PUBLICADA 0; SUBMETIDA 0; INDEXADA confirmada 0. Déficit frente à capacidade diária: 10 páginas, deliberadamente não produzidas para evitar doorway/canibalização.

## Dois artigos técnicos originais

1. `ARQ-ARTICLE-20261119-ALFRESCO-TRANSFORM` — 1.584 palavras úteis — estado TESTADA, não publicada.
2. `ARQ-ARTICLE-20261119-GUARDA-AMBIENTAL` — 1.584 palavras úteis — estado TESTADA, não publicada.

Ambos possuem H1/H2/H3, resposta direta, procedimento, riscos, checklist, FAQ, fontes oficiais, autoria, canonical proposto, Open Graph, JSON-LD e CTA. A busca no repositório não encontrou conteúdo com as mesmas intenções. Publicação, sitemap e submissão permanecem bloqueados pela falta de confirmação da raiz HomeHost, backup restaurável e FTPS de escrita com TLS válido.

Entrega GitHub: branch `editorial/2-artigos-20261119`, PR draft #150. O diff final contém somente os dois artigos, este relatório e o manifesto. O PR está mergeável; não há status checks registrados para o head. Nenhum merge foi executado.

## Blogger

Leitura pública do feed do blog `2545952967912533152`: 36 posts; feed atualizado em 18/10/2026; publicação pública mais recente em 01/05/2026. Nenhum dos oito títulos da fila histórica foi encontrado. Não havia Blogger v3 OAuth, Apps Script autenticado nem conector oficial com escrita; nenhum POST foi tentado e nenhum rascunho foi chamado de publicado.

## Rotina semanal e Merchant Center

Hoje não é domingo em America/Sao_Paulo. A limpeza HomeHost não foi executada: zero arquivo removido, zero arquivo em quarentena e zero byte liberado. Merchant Center permaneceu separado e sem alteração.

## Próxima ação segura

Confirmar no HomeHost a raiz de publicação, o backup restaurável e uma leitura/escrita FTPS inofensiva com certificado válido. Depois: corrigir o `href` malformado, desabilitar listagem de diretório sem afetar assets, ajustar H1/título/schema, inserir as duas páginas regionais ausentes no sitemap apropriado, publicar os dois artigos e somente então validar HTTP/canonical/robots antes de submeter URLs elegíveis.
