# Rodada SEO/GEO/AEO — LGPD, parâmetros e CONARQ

**Data da verificação:** 21/11/2026  
**Escopo:** ARQ-009, ARQ-010, ARQ-011, ARQ-012, ARQ-013 e ARQ-015  
**Publicações em produção nesta rodada:** 0

## Resultado executivo

As seis URLs responderam HTTP 200, resolveram para `177.234.150.42` e apresentaram TLS válido. A validação pós-JavaScript foi necessária porque ARQ-010 e ARQ-015 alteram metadados e conteúdo depois do carregamento inicial.

O principal achado é a **ARQ-015**, que renderiza simultaneamente dois canonicals e dois H1:

- canonical-base inválido: `https://www.arquindex.com.br/escolher-servico-confiavel-digitalizacao-documentos-brasil.arquindex.com.br/erros-comuns.html`;
- canonical dinâmico correto do artigo parametrizado;
- H1 da página-base “Erros comuns” e H1 do artigo CONARQ.

ARQ-011, ARQ-012 e ARQ-013 continuam sendo três parâmetros ignorados: todos exibem a mesma página-raiz LGPD/DPO, com o mesmo title, H1, descrição e canonical. Portanto, não representam páginas editoriais de OCR, maneiras de digitalizar ou custo real, apesar dos endereços.

ARQ-010 foi confirmada como página dinâmica funcional: após JavaScript, possui title, H1, descrição e canonical próprios do artigo, além de três blocos JSON-LD. ARQ-009 passou nos critérios técnicos, mas tem somente 639 palavras.

Nenhuma correção foi publicada porque a origem de ARQ-015 não foi localizada no repositório e o backup HomeHost ainda não tem restauração comprovada. Não houve FTP, sitemap, IndexNow, Search Console, Bing ou divulgação social.

## Evidências

- Auditoria HTTP/DNS/TLS: [run 44931011533](https://github.com/arxazure/arquindex/actions/runs/44931011533), job `136927408572`, artefato `14717513351`, digest `sha256:0ecc7b130a1d637e6f1790129e0963569b94d9fe50767776c2a4273659d1913c`.
- Mobile/desktop: [run 44931012741](https://github.com/arxazure/arquindex/actions/runs/44931012741), job `136927412378`, artefato `14717232594`, digest `sha256:d5d4c2536847d9eb51679186be22a471ae47c35193275c9362929b96cd6e5317`.
- Canonical pós-JavaScript: [run 44931136725](https://github.com/arxazure/arquindex/actions/runs/44931136725), job `136927794785`, artefato `14717598148`, digest `sha256:15450e14a9fbff893c69c8e47413a10068f128309968d942427687c984da7e36`.
- Fila atualizada: [commit 366f17d](https://github.com/arxazure/arquindex/commit/366f17dc2fb112153adaf799c4dc767ae064e5a1).
- Integridade da fila: [run 44931270395](https://github.com/arxazure/arquindex/actions/runs/44931270395), concluído com sucesso.

## Achados por URL

| ID | Conteúdo renderizado | Canonical / H1 | Mobile e conversão | Decisão |
|---|---|---|---|---|
| ARQ-009 | Diagnóstico LGPD, 639 palavras | próprio; 1 H1 | 390/390; logo/menu/WhatsApp; sem formulário; sitemap contém a URL | Preservar e ampliar somente com entregáveis comprovados |
| ARQ-010 | Artigo “Como digitalizar documentos em qualquer impressora”, 1 artigo e 3 JSON-LD | próprio do parâmetro após JavaScript; 1 H1 | 390/390; WhatsApp; sem formulário; parâmetro fora do sitemap | Preservar e documentar dependência de JS |
| ARQ-011 | Página-raiz DPO, 6.125 palavras | canonical da raiz; H1 de LGPD/DPO | 390/390; logo/menu/WhatsApp; sem formulário | Não promover/submeter; localizar artigo OCR próprio |
| ARQ-012 | Mesma página-raiz DPO | canonical da raiz; mesmo H1 | 390/390; logo/menu/WhatsApp; sem formulário | Não promover/submeter; consolidar intenção |
| ARQ-013 | Mesma página-raiz DPO | canonical da raiz; mesmo H1 | 390/390; logo/menu/WhatsApp; sem formulário | Não promover/submeter; usar guia canônico de custo |
| ARQ-015 | Artigo CONARQ, 3.377 palavras | **2 canonicals e 2 H1** | 390/390; sem logo, WhatsApp ou formulário; fora do sitemap | Corrigir template e identidade antes de qualquer submissão |

## Melhoria de verificação implementada

Foi adicionado o workflow [validar-canonical-dinamico-20261121-tarde.yml](https://github.com/arxazure/arquindex/blob/master/.github/workflows/validar-canonical-dinamico-20261121-tarde.yml), que audita o DOM renderizado e registra canonical, title, H1, descrição, robots, artigos e JSON-LD. Ele evitou dois diagnósticos incorretos:

- confirmou que ARQ-010 troca corretamente o canonical-base pelo canonical do artigo após JavaScript;
- comprovou que ARQ-015 não substitui o canonical-base: ela acrescenta outro, mantendo dois sinais concorrentes.

## Próxima correção segura para ARQ-015

1. recuperar o HTML/template efetivamente publicado e vinculá-lo a uma origem versionada;
2. validar backup completo e restauração isolada;
3. remover o canonical-base inválido e o H1 da página-base quando o artigo for renderizado;
4. manter apenas o canonical do artigo;
5. aplicar logo, cabeçalho/rodapé e WhatsApp oficiais;
6. retestar HTML inicial e DOM renderizado;
7. somente então atualizar sitemap e considerar submissão.

## Deduplicação e limites

- ARQ-007 e ARQ-099 foram preservadas.
- Nenhum parâmetro ignorado foi divulgado ou submetido.
- O script geral de identidade não foi executado.
- O inventário consolidado dos 56 subdomínios permanece em [rodada-20261113-tarde-inventario-56-consolidado.md](https://github.com/arxazure/arquindex/blob/master/docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md).
- Não se inferiram indexação, posição, tráfego ou leads.
