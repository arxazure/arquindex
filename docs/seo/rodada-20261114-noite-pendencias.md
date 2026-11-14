# Rodada SEO/GEO/AEO — pendências — 2026-11-14 noite

## Escopo

Auditoria de seis URLs ainda não reauditadas no dia, com DNS, TLS, HTTP, canonical, title, H1, meta description, robots, sitemap, conteúdo, identidade, WhatsApp, links internos e renderização real em mobile/desktop.

Execução somente leitura em produção. Nenhuma gravação via FTP/HomeHost, Railway, Hostinger ou outro publicador. ARQ-007 e ARQ-099 foram preservadas sem republicação ou nova divulgação. O inventário dos 56 subdomínios permanece concluído desde 2026-11-13 e não foi repetido sem mudança comprovada de DNS.

## Evidências

- Auditoria HTTP/SEO: [workflow 43654758225](https://github.com/arxazure/arquindex/actions/runs/43654758225), sucesso.
- Artefato: `auditoria-pendencias-20261114-noite`, ID `14137581628`, SHA-256 `36fb030df0687735f1d60780a6c692eb696ec54d12d34416d2b839b53598ff0c`.
- Chromium mobile 390×844 e desktop 1440×1000: [workflow 43654847734](https://github.com/arxazure/arquindex/actions/runs/43654847734), sucesso.
- Artefato mobile: `validacao-mobile-pendencias-20261114-noite`, ID `14137078371`, SHA-256 `395668eca1085201d5424f973f72a3c89d8a19a818225b97e8fd05c8e2c055c0`.
- Fila atualizada no commit [9f28ea85dbee4741e97515227fa526771e3ff42f](https://github.com/arxazure/arquindex/commit/9f28ea85dbee4741e97515227fa526771e3ff42f).
- Integridade da fila: [workflow 43654987586](https://github.com/arxazure/arquindex/actions/runs/43654987586), sucesso.

## Resultados

| ID | URL | Evidência positiva | Pendência confirmada |
|---|---|---|---|
| ARQ-141 | https://digitacao-de-documentos.arquindex.com.br/ | HTTP 200, UTF-8, sitemap contém URL, mobile 390/390 | Canonical para `/output`, title duplicado, 314 palavras, sem logo, WhatsApp ou formulário |
| ARQ-142 | https://digitalizar-arquivos-empresas.arquindex.com.br/ | HTTP 200, canonical própria, 6.019 palavras, identidade, menu, logo e WhatsApp | Conteúdo sobreposto; overflow 512/390; fora do sitemap |
| ARQ-144 | https://digitalizardocumentos.arquindex.com.br/ | HTTP 200, canonical própria, 6.017 palavras, identidade, menu, logo, WhatsApp e URL no sitemap | Conteúdo sobreposto; overflow 512/390 |
| ARQ-145 | https://exin-rh-maua.arquindex.com.br/ | HTTP 200, canonical própria, H1 RH/Mauá, 6.061 palavras, identidade e WhatsApp | Atendimento/logística não confirmados; overflow 512/390; fora do sitemap |
| ARQ-152 | https://negocios.arquindex.com.br/ | HTTP 200, canonical própria, 6.040 palavras, identidade, menu, logo e WhatsApp | Função editorial do hub ainda genérica; overflow 512/390; fora do sitemap |
| ARQ-155 | https://tabela-de-temporalidade-documental.arquindex.com.br/ | HTTP 200, UTF-8, sitemap contém URL, mobile 390/390 | Canonical para `/output`, title duplicado, 317 palavras, sem logo, WhatsApp ou formulário |

O navegador confirmou UTF-8 e ausência de mojibake nas seis URLs.

## Decisão de publicação

Nenhuma melhoria de produção foi publicada. As quatro páginas recuperadas ainda têm overflow móvel e a fonte/raiz FTP individual não está comprovada. As duas páginas `/output` exigem correção conjunta de canonical, title, identidade e conteúdo original; publicar apenas um ajuste superficial preservaria páginas artificiais e finas.

Não houve divulgação nem envio manual a Search Console, Bing ou IndexNow, pois nenhuma URL nova ou revisão de conteúdo foi publicada nesta rodada.

## Próximas ações seguras

1. Localizar fonte e destino de ARQ-141 e ARQ-155, fazer backup e reconstruir conteúdo útil antes de corrigir canonical/title.
2. Corrigir overflow de ARQ-142, ARQ-144, ARQ-145 e ARQ-152 após preflight individual; não usar o script de 56 sites indiscriminadamente.
3. Confirmar atendimento em Mauá antes de promover ARQ-145 e diferenciar ARQ-142/ARQ-144/ARQ-152 para evitar canibalização.
