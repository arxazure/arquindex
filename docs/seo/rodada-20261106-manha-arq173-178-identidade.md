# Rodada da manhã — ARQ-173–178 — 06/11/2026

## Escopo e evidências
- Auditoria técnica: https://github.com/arxazure/arquindex/actions/runs/42211821777
- Commit do auditor: 891bda2892ecb9945406b0615298b8c56ac8a3ca
- Publicação isolada: https://github.com/arxazure/arquindex/actions/runs/42212024154
- Commit do publicador: 0edb1f0fe105e72efe0ec3560d2af05d4a928662
- Artefato de backup: https://github.com/arxazure/arquindex/actions/runs/42212024154/artifacts/13499561180
- Limite respeitado: seis URLs auditadas e duas melhorias publicadas.
- ARQ-099 não foi alterada ou republicada.

## Resultado por URL

| ID | URL | Diagnóstico atual | Ação |
|---|---|---|---|
| ARQ-173 | https://digitalizacao-digitalizacao-sp.arquindex.com.br/ | HTTP 200 e canonical própria, mas URL São Paulo mantém title, H1 e conteúdo de Belo Horizonte; identidade ausente e 512/390 | Preservada; não promover até confirmar atendimento e produzir conteúdo local distinto |
| ARQ-174 | https://digitalizar-arquivos-corporativo.arquindex.com.br/vantagens.html | HTTP 200, canonical própria, title/H1 distintos, identidade, WhatsApp e 390/390 | Preservada; alteração de 29/10 continua íntegra |
| ARQ-175 | https://digitalizar-digitalizacao-custo.arquindex.com.br/ | HTTP 200 e canonical própria; intenção de custo preservada no title, mas identidade ausente e 512/390 | Identidade oficial, menu, rodapé e WhatsApp publicados; overflow corrigido |
| ARQ-176 | https://digitalizar-mapeamento-mg.arquindex.com.br/o-que-e.html | HTTP 200, canonical própria, identidade e 390/390 | Preservada; alteração de 29/10 continua íntegra |
| ARQ-177 | https://documentos.arquindex.com.br/ | HTTP 200 e canonical própria; identidade ausente e 512/390 | Identidade oficial, menu, rodapé e WhatsApp publicados; overflow corrigido |
| ARQ-178 | https://docusign.arquindex.com.br/ | HTTP 200, canonical própria, guia independente, identidade e sitemap com URL | Preservada; transparência de ausência de afiliação mantida |

## Backups e hashes
- ARQ-175: `/seo-backups/identidade-20261106T114135Z/496ea540caa533e87727.html`; SHA-256 `31085151aa46237bb45cb98356ae37c448456479a50c9a15dd7748815110b108`.
- ARQ-177: `/seo-backups/identidade-20261106T114154Z/28eacdd26aa33000f1ca.html`; SHA-256 `f575af4c35853255a9615163309dc1ce231f1a7f1aeb0b02baf448464b67277a`.

## Verificação posterior
- ARQ-175 e ARQ-177: HTTP 200, canonical própria, H1 único, `index,follow`, logo, menu, atendimento flutuante e WhatsApp.
- Responsividade: 390/390 no mobile e 1440/1440 no desktop.
- Robots: HTTP 200 e referência ao sitemap.
- Sitemaps próprios: HTTP 200, mas ainda não contêm ARQ-175 ou ARQ-177.
- Title, H1 e conteúdo comercial foram preservados nesta publicação; nenhuma oferta ou preço foi inventado.

## Descoberta, métricas e divulgação
- Nenhuma URL nova foi criada.
- Os sitemaps não foram alterados porque a origem segura dos XMLs ainda não foi localizada neste escopo.
- Não houve submissão ao Search Console, Bing ou IndexNow.
- Não houve publicação social; materiais anteriores não foram duplicados.
- Não foram inferidos indexação, ranking, cliques ou leads sem dados consolidados.

## Próximas ações
1. Corrigir ARQ-173 somente após confirmar atendimento em São Paulo e substituir o conteúdo incompatível de Belo Horizonte.
2. Diferenciar editorialmente ARQ-175 por fatores verificáveis de orçamento, sem publicar preço genérico não validado.
3. Definir o papel exclusivo de ARQ-177 frente a dados, compliance e gestão documental antes de qualquer expansão de conteúdo.
