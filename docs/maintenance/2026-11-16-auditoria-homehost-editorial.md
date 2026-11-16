# Arquindex — auditoria HomeHost, editorial e Blogger — 16/11/2026

## Resultado executivo

Execução somente leitura nos ambientes públicos e conectores de infraestrutura. A HomeHost permanece como destino autorizado do site institucional. Não houve escrita no servidor, alteração de DNS, deploy, limpeza, submissão a mecanismos de busca nem publicação no Blogger.

O aviso operacional de retorno à HomeHost mudou de estado: o PR #103 foi incorporado à `master`, no merge commit `269707b86875477d953eae3721a36b3a22f4d19a`. O arquivo `config/site-hosting.json` continua exigindo descoberta da raiz pública, backup restaurável e FTPS com TLS válido. A incorporação do aviso aos workflows reduz o risco de tratar o Railway como prova de publicação, mas não prova que o domínio já esteja servido pela HomeHost.

Foram preparados dois artigos técnicos originais com 2.262 e 2.252 palavras visíveis. Ambos permanecem `noindex,follow`, estado `CRIADA`, sem URL pública comprovada. Nenhuma das dez páginas SEO opcionais foi criada: os dados disponíveis não sustentam dez novas intenções, e a origem HomeHost ainda não está validada para escrita segura.

## Frente 1 — auditoria e deploy técnico

### Origem e branch

- GitHub `master` no início da rodada: `552e15df1b9900244c68b2a9574c856d7a96749f`.
- PR #103: incorporado; aviso HomeHost agora está na branch padrão.
- PR #148, com os artigos de 15/11: continua aberto e em rascunho; não foi contado como publicado.
- Destino institucional autorizado: HomeHost.
- Raiz pública HomeHost: não confirmada nesta execução.
- Backup restaurável HomeHost: não confirmado.
- FTPS/TLS HomeHost: não confirmado.
- Escritas na HomeHost: zero.

### Leitura pública

As páginas inicial, de guarda documental, de digitalização e de digitalização com OCR foram acessíveis pelo leitor público. `robots.txt` foi lido e permite o rastreamento geral, com bloqueios explícitos para áreas administrativas, APIs e diretórios internos. O `sitemap.xml` foi lido como índice com 16 sitemaps filhos.

Duas listagens públicas permanecem expostas:

- `https://www.arquindex.com.br/assets/` — título `Index of /assets/`, com diretórios e arquivos de front-end enumeráveis;
- `https://www.arquindex.com.br/seo/` — título `Index of /seo/`, com diretórios regionais enumeráveis.

Não houve correção remota porque desabilitar a listagem pode depender de `.htaccess`/configuração do servidor e a rotina não confirmou raiz, backup e FTPS TLS. A correção recomendada é aplicar `Options -Indexes` no escopo correto, ou um `index.html` neutro quando a diretiva não for permitida, testando antes em cópia e validando que arquivos conhecidos continuam acessíveis. Nenhum arquivo deve ser apagado como parte dessa correção.

### Railway — projeto separado

Leitura inofensiva funcionou com a identidade de Marina. O projeto `Arquindex Plataforma` tem o serviço `arquindex-web` ligado ao repositório `arxazure/arquindex`, branch `railway-production-2026`, raiz `/arquindex-platform`. Não há mudanças staged. O deployment que o resumo do serviço marca como mais recente está em `FAILED` (`84f59841-da49-4fce-9687-914a5fa0b1e4`, 28/10/2026). A lista de deployments mais recentes contém execuções `REMOVED`, não prova de publicação no domínio.

O Railway ainda lista `arquindex.com.br` como domínio customizado do serviço. Isso é configuração remanescente e não deve ser usado como prova de origem. Nenhuma alteração foi feita no domínio, no Railway ou no DNS.

### Cloudflare e DNS

O conector Cloudflare está autenticado, mas a conta conectada só expõe a zona `arquindex-capture.stream`; `arquindex.com.br` não aparece na lista de zonas. Portanto, o bloqueio é de acesso ao recurso — não autenticação expirada — e a configuração DNS indicada no aviso não pôde ser revalidada por essa conta. A leitura HTTPS pública confirma que o domínio responde com TLS no navegador, mas não identifica por si só o origin efetivo.

Passo humano exato: conceder acesso de leitura à zona `arquindex.com.br` na conexão Cloudflare correta ou fornecer leitura equivalente do registrador/Cloudflare. Não alterar nameservers, registros de e-mail nem CNAME durante a validação.

### Search Console — 28 dias

Propriedade legível: `http://arquindex.com.br/`. Período 17/10 a 13/11, comparado a 19/09 a 16/10:

- cliques: 0 vs. 0;
- impressões: 50 vs. 52;
- CTR: 0% vs. 0%;
- posição média: 7,08 vs. 4,96.

Entre as linhas de consultas nomeadas, 16 de 29 impressões ficaram em Top 3 e 9 em posições 4–10, sem clique. A consulta de marca `arquindex` teve 15 impressões e posição média aproximada 2,13. A consulta comercial `empresa de digitalização de documentos` teve 2 impressões e posição média 25,5. Não foi detectada canibalização, mesmo com limiar reduzido por causa do volume baixo.

Consultas irrelevantes como `slice` e variações de `exclusive` continuam associadas à homepage. A leitura pública da página inicial não mostrou esses termos. Isso sugere associação histórica, ruído ou escopo de propriedade, e não justifica inserir esse vocabulário no conteúdo. A ação segura é investigar inspeção histórica, propriedade HTTPS/domain e versões antigas antes de editar.

O sitemap principal aparece no GSC com 579 URLs enviadas, último download em 10/11, três avisos e zero erros. Há diversos sitemaps históricos com avisos/erros. Nenhum foi removido automaticamente, pois URLs com tráfego ou backlinks podem depender deles.

### Campanha 24 × 3 e páginas SEO

As 72 intenções permanecem `PLANEJADA`. A fila persistente está referenciada no manifesto. Não foram criadas páginas regionais por simples troca de cidade. Resultado do dia:

- `PLANEJADA`: 72 intenções;
- `CRIADA`: 0 páginas SEO;
- `TESTADA`: 0;
- `PUBLICADA`: 0;
- `SUBMETIDA`: 0;
- `INDEXADA`: 0;
- déficit em relação ao limite diário de até 10: 10.

Motivos: ausência de prova de origem HomeHost para escrita, falta de backup/FTPS TLS comprovados, demanda regional insuficiente nos dados GSC atuais e risco de doorway/canibalização. O limite de dez não é uma obrigação de fabricar páginas.

### Rotina semanal

16/11/2026 é segunda-feira em America/Sao_Paulo. O módulo de limpeza semanal não foi executado. A exposição pública foi revalidada, mas nenhum item foi movido ou removido. Espaço liberado: 0 byte.

## Frente 2 — dois artigos técnicos originais

### Artigo 1

- Título: `Lista Mestra (MDR) em Databooks: revisões, transmittals, pendências e aceite final`.
- Contagem visível: 2.262 palavras.
- Estado: `CRIADA`.
- Canonical proposto: `https://www.arquindex.com.br/blog/lista-mestra-mdr-databooks-revisoes-transmittals-aceite/`.
- Publicação: não realizada.

O artigo distingue MDR, índice, transmittal, comentários e pendências; cobre campos, estados, revisão, qualidade, segurança, exemplo hipotético, limites, checklist, FAQ e fontes ISO. Nenhum case ou resultado comercial foi inventado.

### Artigo 2

- Título: `Reindexação no Alfresco: diagnóstico, rebuild seguro e validação da busca`.
- Contagem visível: 2.252 palavras.
- Estado: `CRIADA`.
- Canonical proposto: `https://www.arquindex.com.br/blog/reindexacao-alfresco-diagnostico-rebuild-validacao-busca/`.
- Publicação: não realizada.

O artigo separa falha de consulta, permissão, transformação, rastreamento e índice antes de propor rebuild. Inclui inventário técnico, backup, estratégias, capacidade, segurança, observabilidade, exemplo hipotético, checklist, FAQ e documentação oficial do Alfresco.

Ambos contêm H1/H2/H3, resposta direta, metadados, Open Graph, `TechArticle`, `FAQPage`, autoria, data, CTA e links internos. `noindex,follow` evita interpretar os artefatos de revisão como páginas públicas. Eles não foram adicionados ao sitemap.

## Frente 3 — Blogger

A leitura pública direta do Blogger não funcionou no leitor web; buscas exatas no índice público pelos quatro primeiros títulos da fila histórica não retornaram correspondências. Isso não prova ausência definitiva dos posts, apenas que não houve confirmação pública por essas leituras.

Não há conector Blogger v3 com OAuth de escrita disponível nesta execução. O bloqueio é ausência de autorização do serviço/operação, não Gmail ou Drive. Nenhum `POST` foi feito, logo não existe risco de resultado incerto nem de duplicação.

- publicações confirmadas hoje: 0;
- títulos da fila marcados como publicados: 0;
- próximo passo exato: conectar Blogger v3 para `arquindex@gmail.com` com escopo de escrita, listar o blog e os posts, conferir título/blog ID e só então fazer uma única publicação com readback de ID/URL.

## Submissão e Merchant Center

Nenhuma URL foi enviada ao GSC ou IndexNow: não houve nova URL publicada e comprovada. Submissão e indexação continuam estados distintos.

Merchant Center permaneceu separado. Nenhuma leitura da conta 101490673 foi executada sem acesso próprio autorizado; nenhum número histórico foi reapresentado como atual.

## Alterações e pendências

Alterações efetivas desta rodada: dois artigos e este manifesto/relatório preparados em branch editorial; nenhuma alteração em produção. Pendências prioritárias:

1. confirmar origin HomeHost por DNS e conteúdo, sem alterar DNS;
2. descobrir a raiz pública HomeHost, validar backup fora do diretório público e FTPS TLS;
3. corrigir `Index of /assets/` e `Index of /seo/` de forma reversível;
4. investigar propriedade GSC HTTPS/domain e consultas irrelevantes associadas à homepage;
5. reconciliar sitemaps históricos apenas depois de mapear tráfego, backlinks e canonicals;
6. revisar e incorporar os PRs editoriais antes de qualquer deploy HomeHost;
7. obter OAuth Blogger v3 de escrita para deduplicação e publicação controlada.
