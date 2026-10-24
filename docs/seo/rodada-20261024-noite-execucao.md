# Rodada SEO/GEO/AEO — 24/10/2026, noite

## Resultado

Foram auditadas ARQ-113 a ARQ-118 e publicadas três melhorias substanciais, com backup, FTP, verificação pública e validação independente.

| ID | URL | Antes | Depois | Hash publicado |
|---|---|---|---|---|
| ARQ-113 | https://mapeamento-ocr-rj.arquindex.com.br/ | Title/H1 diziam Belo Horizonte apesar do endereço RJ; sem identidade atual, CTA ou resposta AEO; overflow móvel | OCR e indexação com testes, campos críticos, exceções e aceite; ressalva explícita de que atendimento/logística no RJ dependem de confirmação, sem alegação de unidade local | `1dc93c61396c3b17432a2e1693ac3a0b2c22d6a88b438fe20f8664ab7f54e0d7` |
| ARQ-114 | https://compliance-arquivos-corporativo.arquindex.com.br/ | Conteúdo genérico e título local de BH sem base inequívoca; sem identidade, CTA ou AEO; overflow móvel | Governança da informação com inventário de repositórios, responsáveis, acessos, ciclo de vida, riscos e plano | `af65a6687f7f2730fafdf3a141b8fbc0b2d09848308112c8ca61b9d0f946b97b` |
| ARQ-118 | https://arquivamento.arquindex.com.br/custo.html | Canonical apontava para `www.arquindex.com.br/arquivamento.arquindex.com.br/custo.html`; title repetia “Arquindex” três vezes; sem identidade ou AEO; overflow móvel | Canonical própria, fatores verificáveis de orçamento de guarda, premissas, exclusões, CTA e resposta AEO | `51e9f614e2e1be94aa14136c6743e366d0fc5e5d338e6bc7d1151824d0eb68a6` |

Títulos publicados:

- ARQ-113: **OCR e Indexação: Teste, Revisão e Aceite | Arquindex**
- ARQ-114: **Governança da Informação: Mapeamento e Responsáveis | Arquindex**
- ARQ-118: **Custo da Guarda Documental: Fatores do Orçamento | Arquindex**

## Verificações

As três páginas passaram em 390×844 e 1440×900 com:

- HTTP 200;
- canonical própria;
- um H1;
- `index,follow`;
- logo, menu responsivo e atendimento flutuante oficial;
- ausência de widgets antigos;
- CTA rastreável;
- resposta AEO visível;
- zero overflow horizontal;
- URL presente em sitemap XML válido.

Backups: `/seo-backups/rodada-20261024-noite-20261024T234814Z/`.

Artes individuais verificadas:

- https://www.arquindex.com.br/assets/social-arq113-118/ocr-indexacao-teste-aceite-arq113-20261024.jpg
- https://www.arquindex.com.br/assets/social-arq113-118/governanca-informacao-mapeamento-arq114-20261024.jpg
- https://www.arquindex.com.br/assets/social-arq113-118/custo-guarda-documental-arq118-20261024.jpg

## Evidências

- Auditoria: https://github.com/arxazure/arquindex/actions/runs/40143940885
- Publicação, backups, sitemaps e artes: https://github.com/arxazure/arquindex/actions/runs/40144123678
- Validação independente: https://github.com/arxazure/arquindex/actions/runs/40144337579
- Commit da fila: https://github.com/arxazure/arquindex/commit/30cdaf7b4118241bac60a15c816dc6aec65a349f

## Search Console — linha de base

Período recente completo: 08–21/10/2026. Comparação: 24/09–07/10/2026. Dados anteriores à publicação.

| ID | Recente: cliques / impressões / posição | Anterior: cliques / impressões / posição |
|---|---|---|
| ARQ-113 | 0 / 8 / 11,25 | sem linha |
| ARQ-114 | 0 / 8 / 44,50 | 0 / 3 / 63,00 |
| ARQ-115 | 0 / 6 / 10,33 | 0 / 2 / 51,50 |
| ARQ-116 | 0 / 10 / 49,20 | 0 / 11 / 72,55 |
| ARQ-117 | 0 / 14 / 94,43 | 0 / 1 / 100,00 |
| ARQ-118 | 0 / 6 / 19,00 | 0 / 3 / 18,67 |

As amostras são pequenas, todas com zero cliques, e não comprovam efeito das mudanças.

## Páginas preservadas

- ARQ-115: URL MG com conteúdo de BH; mantida sem alteração até confirmar atendimento e logística em Minas Gerais.
- ARQ-116: sobreposição direta com ARQ-099, ARQ-109 e ARQ-112 no grupo de preço.
- ARQ-117: sobreposição com ARQ-096 no grupo de comparação de fornecedores.

## Divulgação e descoberta

Não houve nova postagem social na rodada noturna, evitando duplicar a promoção diária feita pela manhã. As artes ficaram registradas para rotação futura. Os três sitemaps foram atualizados e validados publicamente.

Não houve submissão ao Google Search Console, Bing Webmaster ou IndexNow: as integrações disponíveis nesta execução não ofereceram ação autenticada de envio com confirmação. Sitemap publicado não significa URL indexada.

## Continuidade

Cursor: **ARQ-119**.

Próximas prioridades:

1. Auditar ARQ-119 a ARQ-124.
2. Consolidar o grupo de preço antes de alterar ARQ-109, ARQ-112 e ARQ-116.
3. Medir ARQ-113, ARQ-114 e ARQ-118 após janela completa, sem trocar títulos prematuramente.
