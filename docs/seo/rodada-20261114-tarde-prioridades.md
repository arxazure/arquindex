# Rodada SEO/GEO/AEO — prioridades — 2026-11-14 tarde

## Escopo

Auditoria de seis URLs prioritárias da fila persistente, com DNS, TLS, HTTP, canonical, title, H1, meta description, robots, sitemap, conteúdo, identidade, WhatsApp, links internos e renderização real em mobile/desktop.

A rodada foi somente de leitura em produção. Nenhuma gravação foi feita via FTP/HomeHost, Railway, Hostinger ou outro publicador. ARQ-007 e ARQ-099 foram preservadas sem republicação ou nova divulgação.

O inventário dos 56 subdomínios permanece concluído (56/56) desde 2026-11-13 e não foi repetido sem mudança comprovada de DNS.

## Evidências

- Auditoria HTTP/SEO: [workflow 43622374705](https://github.com/arxazure/arquindex/actions/runs/43622374705), sucesso.
- Artefato: `auditoria-prioridades-20261114-tarde`, ID `14124850997`, SHA-256 `aa7b06e4f81e97be151c65faf26314bf718fff0cfa73db769c91fc6c65c991ea`.
- Chromium mobile 390×844 e desktop 1440×1000: [workflow 43622516433](https://github.com/arxazure/arquindex/actions/runs/43622516433), sucesso.
- Artefato mobile: `validacao-mobile-prioridades-20261114-tarde`, ID `14124219158`, SHA-256 `8484e482d85564d446ed215437a3f6d0fd3540faac022c45deb4b8dd4e0395e1`.
- Fila atualizada no commit [6f193f843fc01f510c271367494654912b34a626](https://github.com/arxazure/arquindex/commit/6f193f843fc01f510c271367494654912b34a626).
- Integridade da fila: [workflow 43622672185](https://github.com/arxazure/arquindex/actions/runs/43622672185), sucesso.

## Resultados

| ID | URL | Evidência positiva | Pendência confirmada |
|---|---|---|---|
| ARQ-140 | https://decreto10278-educacao.arquindex.com.br/ | HTTP 200, canonical própria, indexável, 6.027 palavras, identidade, menu, logo e WhatsApp | Overflow mobile 512/390; URL ausente do sitemap próprio |
| ARQ-143 | https://digitalizar-lgpd-sp.arquindex.com.br/ | HTTP 200, canonical própria, identidade e 6.015 palavras | URL/intenção LGPD-SP publica title, H1 e descrição de digitalização em Belo Horizonte; overflow 512/390; fora do sitemap |
| ARQ-146 | https://gestao-arquivos-custo.arquindex.com.br/ | HTTP 200, canonical própria, identidade e 5.996 palavras | H1 genérico; overflow 512/390; fora do sitemap |
| ARQ-147 | https://ia.arquindex.com.br/custo.html | HTTP 200, 3.417 palavras, H1, identidade e WhatsApp | Canonical aponta para `www/ia.arquindex.com.br/custo.html`; title triplica Arquindex; overflow 414/390; fora do sitemap |
| ARQ-148 | https://implantacao-arquivos-mg.arquindex.com.br/ | HTTP 200, canonical própria, identidade e 6.049 palavras | URL MG publica title, H1 e descrição de Belo Horizonte; overflow 512/390; fora do sitemap |
| ARQ-149 | https://incineracaodocumentos.arquindex.com.br/ | HTTP 200, canonical própria, indexável, 6.023 palavras, identidade, menu, logo e WhatsApp | Overflow mobile 512/390; URL ausente do sitemap próprio |

O navegador confirmou `UTF-8` e ausência de mojibake nas seis páginas. O aparente texto corrompido da extração HTTP era decodificação do cliente de auditoria, não o conteúdo renderizado.

## Decisão de publicação

Nenhuma melhoria de produção foi publicada. A pesquisa no repositório encontrou relatórios e workflows de auditoria, mas não localizou a fonte HTML ou o mapeamento individual de publicação dessas páginas. Sem origem, destino e backup comprovados, alterar por FTP poderia sobrescrever a versão pública recuperada ou atingir uma raiz incorreta.

Também não houve publicação social nem envio manual a Search Console, Bing ou IndexNow, porque nenhuma URL nova ou revisão de conteúdo foi publicada nesta rodada.

## Próximas correções seguras

1. Prioridade técnica: localizar a fonte de ARQ-147, fazer backup e corrigir canonical, title e overflow; validar antes/depois em Chromium.
2. Prioridade editorial: reconstruir ARQ-143 e ARQ-148 em staging, respeitando respectivamente São Paulo/LGPD e Minas Gerais, sem inventar unidade ou cobertura.
3. Corrigir overflow e sitemap de ARQ-140, ARQ-146 e ARQ-149 após mapear a raiz de cada página, preservando canonical, conteúdo e identidade já recuperados.
