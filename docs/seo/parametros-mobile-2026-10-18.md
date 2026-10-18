# Parâmetros e mobile — 18/10/2026

Canal: Homehost via GitHub Actions; ação autorizada de correção técnica e verificação. Última revisão: 18/10/2026, Brasília. Sem divulgação social ou submissão de sitemaps nesta ação.

## Diagnóstico atualizado

Os dois artigos existem no fornecedor Soro e aparecem após JavaScript e rolagem até o incorporador. A extração anterior não demonstrava ausência de artigo. O navegador reproduziu duas canônicas após carregamento, além de overflow DPO (scrollWidth 512 para clientWidth 390). Títulos dos artigos: Como digitalizar documentos em qualquer impressora (06/04/2026) e OCR para documentos: onde gera valor real (25/03/2026). Não apresentar esses conteúdos como notícias novas.

## Publicado e verificado

- Descrição completa da página de governança e alinhamento de description/og:description/twitter:description: commit 440b70dcfdf10bc0a80190eba15bc87cf85e814f, execução https://github.com/arxazure/arquindex/actions/runs/39153910647, job 117753035630. Título e corpo preservados.
- Normalização da canônica somente após confirmar artigo incorporado, preservando parâmetro post válido: commit 58690a85a8f36b9919ee3cc3d9fde75bfdf97438, execução https://github.com/arxazure/arquindex/actions/runs/39154199155. Nenhum redirecionamento ou exclusão de artigo.
- CSS mobile do cartão trust-card e botão flutuante de WhatsApp DPO: commit 9a0cd58cc373b3c7fda0ab4b568d660524b8bc5b, execução https://github.com/arxazure/arquindex/actions/runs/39154288586. Contatos preservados. Backup protegido, comparação concorrente, readback FTP TLS e validação pública dos arquivos.

## Aceite em navegador

Execução https://github.com/arxazure/arquindex/actions/runs/39154330435 — job 117754304076. Chrome headless com viewport mobile 390×844, carregamento JavaScript e rolagem ao incorporador. Todas as quatro URLs HTTP 200, uma canônica e scrollWidth/clientWidth 390/390. Artigos encontrados nos dois incorporadores. Capturas e report.json anexados como artifact arquindex-mobile-audit-20261018.

```json
[
  {
    "id": "ARQ-010",
    "url": "https://governanca.arquindex.com.br/bh.html?post=como-digitalizar-documentos-em-qualquer-impressora",
    "http": 200,
    "clientWidth": 390,
    "scrollWidth": 390,
    "canonical": [
      "https://governanca.arquindex.com.br/bh.html?post=como-digitalizar-documentos-em-qualquer-impressora"
    ],
    "articleRendered": true
  },
  {
    "id": "ARQ-011",
    "url": "https://7-motivos-contar-dpo-terceirizado.arquindex.com.br/?post=ocr-para-documentos",
    "http": 200,
    "clientWidth": 390,
    "scrollWidth": 390,
    "canonical": [
      "https://7-motivos-contar-dpo-terceirizado.arquindex.com.br/?post=ocr-para-documentos"
    ],
    "articleRendered": true
  },
  {
    "id": "ARQ-050",
    "url": "https://www.arquindex.com.br/digitalize/belo-horizonte/",
    "http": 200,
    "clientWidth": 390,
    "scrollWidth": 390,
    "canonical": [
      "https://www.arquindex.com.br/digitalize/belo-horizonte/"
    ],
    "articleRendered": null
  },
  {
    "id": "ARQ-047",
    "url": "https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/belo-horizonte/",
    "http": 200,
    "clientWidth": 390,
    "scrollWidth": 390,
    "canonical": [
      "https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/belo-horizonte/"
    ],
    "articleRendered": null
  }
]
```

Fila: ARQ-010 / digitalização em impressora / BH / estado publicado e verificado / próxima ação avaliar sobreposição e métricas sem nova troca repetitiva. ARQ-011 / OCR para documentos / estado publicado e verificado / próxima ação conferir outros destinos internos ainda não auditados. ARQ-050 e ARQ-047 / regionais BH / revisadas nesta data, sem alteração por esta ação.

Limites: teste automatizado em um viewport, sem declaração de revisão visual de todas as capturas ou de todos os dispositivos; não confirma canônica escolhida pelo Google ou indexação. Dois H1 nas páginas incorporadas permanecem como tema editorial a avaliar, sem classificar automaticamente como erro. DNS/ativação dos dois subdomínios BH continua dependente de acesso cPanel; este trabalho não os ativou.
