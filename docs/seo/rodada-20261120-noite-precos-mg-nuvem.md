# Rodada SEO/GEO/AEO — preços, MG, nuvem e compliance

**Data da verificação:** 20/11/2026  
**Escopo:** 6 URLs da fila por página (ARQ-109, ARQ-115, ARQ-116, ARQ-117, ARQ-119 e ARQ-120)  
**Publicações em produção nesta rodada:** 0

## Resultado executivo

As seis URLs resolvem para `177.234.150.42`, apresentam TLS válido, respondem HTTP 200, declaram canonical próprio e `index,follow,max-image-preview:large`. A inspeção no navegador confirmou UTF-8 sem mojibake, logo, menu e atendimento por WhatsApp. Todas, porém, apresentam largura de documento de 512 px em viewport móvel de 390 px, evidenciando overflow horizontal compartilhado pelo template.

Não houve alteração de produção. O padrão comum indica que a correção deve ser feita na origem do template, com backup completo verificado e restauração isolada, evitando seis edições independentes. Também não houve publicação por FTP, envio a Search Console/Bing/IndexNow, atualização de sitemap ou divulgação social.

## Evidências reproduzíveis

- Auditoria técnica: [run 44839012756](https://github.com/arxazure/arquindex/actions/runs/44839012756), job `136642475145`, artefato `14679842504`, digest `sha256:c6a7553ccfd6ede8935a4ab37920c82f8004f15c1c7133caef87664157cb6887`.
- Validação móvel/desktop: [run 44839014306](https://github.com/arxazure/arquindex/actions/runs/44839014306), job `136642480042`, artefato `14679553196`, digest `sha256:9a43cbbc7eb6389ab6a47d27d7960ae50c7c24dbc2ecd96ea1083f105a5fd55e`.
- Fila atualizada: [commit 5b94a3e](https://github.com/arxazure/arquindex/commit/5b94a3ea49182b66fad0616c37a7bdffdc99d7df).
- Integridade da fila: [run 44839335152](https://github.com/arxazure/arquindex/actions/runs/44839335152), concluído com sucesso.

## Achados por URL

| ID | URL | Evidência atual | Lacuna prioritária | Decisão |
|---|---|---|---|---|
| ARQ-109 | [digitalizar-arquivos-custo](https://digitalizar-arquivos-custo.arquindex.com.br/) | 6.019 palavras; 101 links internos; title de preço | H1/meta genéricos de BH; sobreposição com ARQ-099/112; overflow 512/390; sem formulário; sitemap local não lista a URL | Mapear template e consolidar intenção antes de alterar |
| ARQ-115 | [digitalizar-arquivos-mg](https://digitalizar-arquivos-mg.arquindex.com.br/) | 6.015 palavras; 101 links internos | URL voltada a MG, mas title/H1/meta continuam em BH; overflow; sem formulário; sitemap local não lista a URL | Só ampliar para MG após comprovar atendimento e logística estaduais |
| ARQ-116 | [digitalizar-arquivos-preco](https://digitalizar-arquivos-preco.arquindex.com.br/) | 6.015 palavras; 101 links internos; title de preço | Intenção duplicada com ARQ-099/109/112; H1/meta genéricos; overflow; sem formulário; sitemap local não lista a URL | Consolidar o grupo de preço antes de alterar ou promover |
| ARQ-117 | [lista-empresas-digitalizacao-documentos-regiao](https://lista-empresas-digitalizacao-documentos-regiao.arquindex.com.br/) | 6.047 palavras; 103 links internos; title de lista | H1/meta genéricos; intenção comparativa pouco diferenciada da ARQ-096; overflow; sem formulário; sitemap local não lista a URL | Exigir critérios reais de comparação antes de editar/divulgar |
| ARQ-119 | [contratar-digitalizacao-documentos-armazenamento-nuvem](https://contratar-digitalizacao-documentos-armazenamento-nuvem.arquindex.com.br/) | 6.047 palavras; 103 links internos | Página pública ainda genérica de BH e não expressa armazenamento em nuvem; overflow; sem formulário; sitemap local não lista a URL | Manter implementação preparada sem deploy até backup/restauração isolada e validação de exportação, acesso e aceite |
| ARQ-120 | [compliance-digitalizacao-preco](https://compliance-digitalizacao-preco.arquindex.com.br/) | 6.032 palavras; 101 links internos; title de preço | Página pública ainda genérica de digitalização e não expressa compliance/governança; overflow; sem formulário; sitemap local não lista a URL | Manter implementação preparada sem deploy até diferenciar diagnóstico, implantação e acompanhamento |

Em todas as seis URLs, `/robots.txt` e `/sitemap.xml` responderam HTTP 200. O sitemap local, contudo, não contém a própria URL auditada. A presença do arquivo não foi interpretada como indexação, posição ou cobertura no Google.

## Diagnóstico e próxima ação segura

1. Identificar o repositório/template efetivamente publicado para o conjunto e registrar um backup completo verificável.
2. Corrigir o overflow horizontal na origem comum e validar novamente em 390 px e 1.440 px.
3. Tratar canibalização e intenção antes de editar conteúdo: grupo de preço (ARQ-099/109/112/116), MG versus BH (ARQ-115), comparação (ARQ-117), nuvem (ARQ-119) e governança (ARQ-120).
4. Para ARQ-119 e ARQ-120, manter como **preparada e não publicada** a implementação do [commit 811c27f](https://github.com/arxazure/arquindex/commit/811c27f610643a77f1304b5499cad9d998516682) / PR 40 até `BACKUP_COMPLETE_VERIFIED` e teste de restauração isolada.
5. Somente depois de publicação comprovada, retestar HTTP 200, canonical, conteúdo, mobile, CTA/formulário, sitemap e eventual submissão suportada.

## Deduplicação e limites

- ARQ-007 e ARQ-099 foram preservadas; não houve nova divulgação nem republicação.
- O script `scripts/padronizar-identidade-arquindex.py` não foi executado indiscriminadamente.
- Nenhuma peça social foi criada ou publicada nesta rodada.
- O inventário consolidado dos 56 subdomínios não foi repetido; permanece referenciado em [rodada-20261113-tarde-inventario-56-consolidado.md](https://github.com/arxazure/arquindex/blob/master/docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md).
- Não se inferiram indexação, posição, tráfego, conversões ou leads.
