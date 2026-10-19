# Auditoria dos 56 subdomínios — 18/10/2026 (Brasília)

Issue: https://github.com/arxazure/arquindex/issues/10

## Resultado confirmado

- 55/56 nomes retornaram NXDOMAIN para A e AAAA em Cloudflare (1.1.1.1) e Google (8.8.8.8). TLS, HTTP, conteúdo, title, H1, canonical, robots, sitemap e links nesses hosts não são verificáveis enquanto não houver resolução DNS. Não há evidência para dizer que seus arquivos estão ausentes.
- adequacaolgpd.arquindex.com.br: A=177.234.150.42; HTTPS 200; HTTP 301 para HTTPS próprio; TLSv1.3 válido, expiração 28/12/2026. Conteúdo institucional com canonical https://www.arquindex.com.br/, divergente da página comercial do manifesto. Possível alias ou document root compartilhado: requer confirmação no cPanel. Não sobrescrever o conteúdo institucional.
- Nenhum dos 56 foi certificado como página comercial correta e funcional.

## Único endereço com conteúdo público inspecionável

| Campo | Observado | Previsto na fonte comercial |
|---|---|---|
| Title | Arquindex · Digitalização de Documentos, Gestão Documental, LGPD e Databooks em Belo Horizonte · Arquindex | Adequação LGPD em Belo Horizonte · Arquindex |
| H1 | Líder no Brasil em Digitalização de Documentos Gestão de Arquivos Físicos e Digitais. | Adequação LGPD em Belo Horizonte |
| Canonical | https://www.arquindex.com.br/ | https://adequacaolgpd.arquindex.com.br/ |
| Robots | HTTP 200, permite raiz, anuncia sitemap institucional | sitemap do próprio host |
| Sitemap | HTTP 200, índice com URLs www.arquindex.com.br | URL canônica do próprio host |
| Links comerciais | /contato-orcamento/ e /solicitar-proposta-contratacao.html no www retornaram HTTP 200 | WhatsApp/contato comercial |

Links WhatsApp tiveram apenas inspeção de URL: nenhuma mensagem ou lead de teste foi enviado. Conteúdo não renderizado em navegador nesta auditoria; analisado o HTML público. Indexação no Google/Bing não foi consultada nem alegada.

## Correções executadas no mecanismo

Commit: https://github.com/arxazure/arquindex/commit/dcf4cee110387d3519b7b2c5fcd12e3a14dea25d

- Workflow existente agora exige DNS, TLS válido, HTTP 200, destino HTTPS e canonical próprios para os 56 hosts antes de qualquer upload. Falhar bloqueia o lote inteiro.
- Após upload, auditoria individual dos 56 cobre conteúdo, metadados, robots, sitemaps e links. Divergências impedem declarar sucesso. Artefatos são preservados mesmo quando há falha.
- FTPS passa a validar certificado com contexto TLS padrão.
- Cinco testes automatizados passaram: evidência completa, rejeição de DNS/TLS/alias/redirecionamento, sitemap inválido, host ausente e H1 duplicado. As 56 fontes locais têm title/H1 únicos e canonical próprio.

Validação real: https://github.com/arxazure/arquindex/actions/runs/39179976862 · job 117830455000. Conclusão failure **esperada pela proteção**; etapa de envio FTPS skipped; artefato validacao-publica-56 preservado. Nenhum arquivo remoto foi escrito nesta rodada.

Outros commits: auditor inicial c22262558760b6160be791808149c987b1e66afc; diagnóstico independente eb10f1c215a57e8aba56ffe3b9a2733851b8dade.

## Bloqueio remanescente e continuação

CPANEL_HOST, CPANEL_USER e CPANEL_API_TOKEN não estão configurados. Tentativa de leitura no endpoint conhecido https://cpanel.arquindex.com.br:2083 com credencial de hospedagem já utilizada pelo workflow anterior retornou HTTP 401. Nenhuma configuração alterada.

O navegador chegou à Área de Cliente da HomeHost, sem sessão autenticada. É necessário login seguro para inspecionar os registros e document roots existentes antes de criar DNS/domínios ou corrigir o host LGPD. Não foi usada credencial em chat e não há segredo neste relatório.

Após acesso: ler inventário e DNS atuais; associar cada host somente à sua pasta validada; preservar aplicações existentes; testar um endereço por vez com TLS e conteúdo próprio; repetir a auditoria. Não publicar as 56 páginas sobre a raiz institucional.

Preservados: index.html principal (projeto Se-joga), aplicações existentes, ARQ-007/008/009 e suas melhorias. Nenhuma publicação social, submissão de sitemap ou IndexNow.

Reversão: nenhum rollback de site é necessário porque não houve escrita remota. Para desfazer apenas a proteção do workflow, restaurar exclusivamente .github/workflows/publicar-56-subdominios.yml do commit pai de dcf4cee; não reverter commits de outros trabalhos nem index.html. Isso reabre o risco original e não corrige DNS.

## Evidências individuais

## Auditoria pública individual dos 56 subdomínios

Commit auditado: `dcf4cee110387d3519b7b2c5fcd12e3a14dea25d`. Execução: https://github.com/arxazure/arquindex/actions/runs/39179976919

0/56 sem falhas nos testes; 56/56 com falhas ou divergências. Evidência DNS/TLS/HTTP e detalhes de title, H1, canonical, robots, sitemap e links no artefato audit-56/results.json.

Auditoria somente leitura, sem deploy, sem submissão de indexação. Raiz principal e ARQ-007/008/009 preservadas. HTTP 200 não comprova indexação. Falha de rede não prova conteúdo ausente.

| Endereço | DNS | TLS | HTTPS / HTTP final | Resultado |
|---|---|---|---|---|
| https://digitalizacaodedocumentosembh.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://guardadocumentalembh.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://gestaodocumentalembh.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://incineracaodedocumentosembh.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://escaneardocumentosembh.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://alfrescoembh.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://consultorialgpd.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://adequacaolgpd.arquindex.com.br/ | 177.234.150.42 | válido | 200 / 200 | title diverge do manifesto de conteúdo; h1 diverge do manifesto de conteúdo; canonical diverge do manifesto de conteúdo; canonical não é próprio; Sitemap não anunciado em robots; Raiz canônica ausente no sitemap; Sitemap contém URL relativa/externa/HTTP |
| https://dpoembh.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://canaldedenunciaslgpd.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://ecmembh.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://escanearprontuariomedicoembh.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://escaneardossiefuncionario.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://digitalizacaodepartamentopessoal.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://digitalizacaodedocumentosembetim.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://guardadocumentalembetim.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://gestaodocumentalembetim.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://incineracaodedocumentosembetim.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://escaneardocumentosembetim.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://alfrescoembetim.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://consultorialgpd-betim.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://adequacaolgpd-betim.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://dpoembetim.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://canaldedenunciaslgpd-betim.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://ecmembetim.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://escanearprontuariomedicoembetim.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://escaneardossiefuncionario-betim.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://digitalizacaodepartamentopessoal-betim.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://digitalizacaodedocumentosemcontagem.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://guardadocumentalemcontagem.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://gestaodocumentalemcontagem.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://incineracaodedocumentosemcontagem.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://escaneardocumentosemcontagem.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://alfrescoemcontagem.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://consultorialgpd-contagem.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://adequacaolgpd-contagem.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://dpoemcontagem.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://canaldedenunciaslgpd-contagem.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://ecmemcontagem.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://escanearprontuariomedicoemcontagem.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://escaneardossiefuncionario-contagem.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://digitalizacaodepartamentopessoal-contagem.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://digitalizacaodedocumentosemnovalima.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://guardadocumentalemnovalima.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://gestaodocumentalemnovalima.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://incineracaodedocumentosemnovalima.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://escaneardocumentosemnovalima.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://alfrescoemnovalima.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://consultorialgpd-novalima.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://adequacaolgpd-novalima.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://dpoemnovalima.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://canaldedenunciaslgpd-novalima.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://ecmemnovalima.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://escanearprontuariomedicoemnovalima.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://escaneardossiefuncionario-novalima.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |
| https://digitalizacaodepartamentopessoal-novalima.arquindex.com.br/ | erro | erro | erro / erro | DNS indisponível; TLS/HTTP/conteúdo/SEO não verificáveis |


## Confirmação DNS e acesso à configuração (somente leitura)

Execução: https://github.com/arxazure/arquindex/actions/runs/39179976877

cPanel: Autenticação/endpoint não disponível

| Endereço | Cloudflare A / AAAA | Google A / AAAA |
|---|---|---|
| digitalizacaodedocumentosembh.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| guardadocumentalembh.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| gestaodocumentalembh.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| incineracaodedocumentosembh.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| escaneardocumentosembh.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| alfrescoembh.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| consultorialgpd.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| adequacaolgpd.arquindex.com.br | ANSWER / NOANSWER | ANSWER / NOANSWER |
| dpoembh.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| canaldedenunciaslgpd.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| ecmembh.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| escanearprontuariomedicoembh.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| escaneardossiefuncionario.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| digitalizacaodepartamentopessoal.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| digitalizacaodedocumentosembetim.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| guardadocumentalembetim.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| gestaodocumentalembetim.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| incineracaodedocumentosembetim.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| escaneardocumentosembetim.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| alfrescoembetim.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| consultorialgpd-betim.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| adequacaolgpd-betim.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| dpoembetim.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| canaldedenunciaslgpd-betim.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| ecmembetim.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| escanearprontuariomedicoembetim.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| escaneardossiefuncionario-betim.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| digitalizacaodepartamentopessoal-betim.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| digitalizacaodedocumentosemcontagem.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| guardadocumentalemcontagem.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| gestaodocumentalemcontagem.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| incineracaodedocumentosemcontagem.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| escaneardocumentosemcontagem.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| alfrescoemcontagem.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| consultorialgpd-contagem.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| adequacaolgpd-contagem.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| dpoemcontagem.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| canaldedenunciaslgpd-contagem.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| ecmemcontagem.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| escanearprontuariomedicoemcontagem.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| escaneardossiefuncionario-contagem.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| digitalizacaodepartamentopessoal-contagem.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| digitalizacaodedocumentosemnovalima.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| guardadocumentalemnovalima.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| gestaodocumentalemnovalima.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| incineracaodedocumentosemnovalima.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| escaneardocumentosemnovalima.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| alfrescoemnovalima.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| consultorialgpd-novalima.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| adequacaolgpd-novalima.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| dpoemnovalima.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| canaldedenunciaslgpd-novalima.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| ecmemnovalima.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| escanearprontuariomedicoemnovalima.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| escaneardossiefuncionario-novalima.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |
| digitalizacaodepartamentopessoal-novalima.arquindex.com.br | NXDOMAIN / NXDOMAIN | NXDOMAIN / NXDOMAIN |

