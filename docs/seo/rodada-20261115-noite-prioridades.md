# Rodada SEO/GEO/AEO — 15/11/2026 — noite

## Escopo

Auditoria sem escrita em produção de seis fichas ainda sem revalidação recente: ARQ-137, ARQ-138, ARQ-139, ARQ-156, ARQ-163 e ARQ-166. A seleção evita repetir as URLs auditadas nas rodadas anteriores de 14 e 15/11 e preserva ARQ-007 e ARQ-099.

## Evidências

- Auditoria DNS/TLS/HTTP/SEO: [run 43776119810](https://github.com/arxazure/arquindex/actions/runs/43776119810)
  - job: `133002696766`
  - artifact: `14185794361`
  - SHA-256: `0f7e8068b3da556c3294aecd7d11a8251dd57a3a4c5c21bc5a476f799fe9b516`
- Validação Chromium mobile/desktop: [run 43776117734](https://github.com/arxazure/arquindex/actions/runs/43776117734)
  - job: `133002690502`
  - artifact: `14186741215`
  - SHA-256: `58b8503380ac32197756f735d2f21a6a5f0e597e9e55e1c2069694671306e8aa`
- Atualização da fila: [commit eb0ecb1](https://github.com/arxazure/arquindex/commit/eb0ecb16890e1e2bc6b64b7fc3583388e1f107a7)
- Integridade da fila: [run 43776330955](https://github.com/arxazure/arquindex/actions/runs/43776330955) — sucesso.

## Resultado consolidado

As seis páginas resolveram DNS, negociaram TLS 1.3 e retornaram HTTP 200. Todas declararam canonical própria, `index,follow`, meta description, um H1, logo, menu e WhatsApp. A identidade pública, ausente ou incompleta na evidência anterior, aparece recuperada nas seis páginas. Essa recuperação foi observada, não publicada por esta rodada.

O teste em navegador confirmou UTF-8 e ausência de mojibake. A leitura HTTP simples apresentou caracteres mal decodificados porque o servidor respondeu `text/html` sem charset explícito no cabeçalho; o documento carregado pelo Chromium declarou UTF-8 corretamente.

Todas apresentam o mesmo overflow horizontal em mobile: 512 px de conteúdo para viewport de 390 px. Em desktop, todas ficaram em 1440/1440.

| Ficha | URL | Conteúdo e identidade | Sitemap | Pendência |
|---|---|---|---|---|
| ARQ-137 | https://arquivos.arquindex.com.br/ | 6.041 palavras; title/H1 de organização de arquivos em BH; logo, menu e WhatsApp | 200, URL ausente | Diferenciar da página pilar de guarda e corrigir overflow após localizar origem e fazer backup. |
| ARQ-138 | https://auditoria-governanca-dados.arquindex.com.br/ | 6.065 palavras; title/H1 ainda genéricos de gestão da informação; logo, menu e WhatsApp | 200, URL ausente | Diferenciar de ARQ-114, compliance e dados antes de publicar. |
| ARQ-139 | https://cedoc-educacao-duque-de-caxias.arquindex.com.br/ | 6.058 palavras; identidade recuperada | 200, URL ausente | Divergência crítica: URL cita Duque de Caxias, mas title, H1 e description continuam em Belo Horizonte. Confirmar atendimento/logística antes de reconstruir. |
| ARQ-156 | https://acervos-medico-baixada-fluminense.arquindex.com.br/ | 6.082 palavras; intenção saúde/Baixada Fluminense coerente; identidade recuperada | 200, URL presente | Confirmar atendimento/logística e requisitos de saúde antes de corrigir o overflow. |
| ARQ-163 | https://compliance.arquindex.com.br/ | 5.988 palavras; title/H1 de compliance documental em BH; identidade recuperada | 200, URL ausente | Diferenciar de dados e auditoria por controles, responsáveis e evidências. |
| ARQ-166 | https://dados.arquindex.com.br/ | 6.048 palavras; title/H1 genéricos de gestão da informação; identidade recuperada | 200, URL ausente | Definir papel exclusivo frente a compliance e auditoria. |

Nenhuma das seis páginas contém formulário; o WhatsApp é o único CTA detectado.

## Publicação e submissão

- Melhorias substanciais publicadas nesta rodada: **0**.
- Motivo: origem/raiz FTP individual e backup restaurável ainda não comprovados; três páginas também dependem de diferenciação editorial ou validação regional.
- Sitemaps alterados: **0**.
- Search Console, Bing e IndexNow: **nenhum envio**, pois não houve publicação nova.
- Divulgação social: **nenhuma**; não há peça nova validada nem mudança publicada.
- Indexação, posição e leads: não inferidos.

## Próxima ação segura

1. Localizar a origem de ARQ-137 e corrigir o componente que fixa 512 px no mobile, com backup e teste de regressão.
2. Tratar ARQ-138, ARQ-163 e ARQ-166 como um conjunto de canibalização: auditoria, compliance e governança de dados precisam de entregáveis e intenções distintas.
3. Manter ARQ-139 fora de divulgação até confirmar atendimento em Duque de Caxias e substituir todos os sinais locais de Belo Horizonte.
