# Reconciliação de ocorrências Ahrefs com fontes locais

O painel Ahrefs de 07/11/2026 apresentou contagens mas não forneceu a relação de URLs.

## Entradas
1. Exporte as linhas do Ahrefs como CSV com colunas **URL** (ou Page URL / Affected URL) e **Issue** (ou Issue Type / Type / Problem).
2. Gere candidatos HTML locais de um **espelho verificado** do site principal, não da raiz inteira do repositório, que inclui protótipos e outros subdomínios:

```bash
python3 scripts/ahrefs_seo_audit.py --root /CAMINHO/ESPELHO-WWW --out seo-report/ahrefs-audit.json --csv seo-report/ahrefs-review.csv
python3 scripts/ahrefs_reconcile.py --ahrefs /CAMINHO/EXPORT-AHREFS.csv --candidates seo-report/ahrefs-review.csv --out seo-report/ahrefs-reconciled.csv --json seo-report/ahrefs-reconciled.json
python3 -m unittest discover -s tests -p 'test_ahrefs_reconcile.py'
python3 -m unittest discover -s tests -p 'test_ahrefs_seo_audit.py'
```

## Interpretação dos resultados
- `MATCH_REQUIRES_LIVE_VERIFICATION`: mesmo URL e mesmo tipo de alerta no inventário local, mas é preciso verificar HTML, canonical, HTTP, robots e versão implantada na HomeHost.
- `NO_EXACT_LOCAL_MATCH`: URL ou alerta não corresponde exatamente; **não** autoriza alteração ou exclusão.
- `MANUAL_REVIEW_EXTERNAL_OR_UNKNOWN_ISSUE`: issues de performance, backlinks, IndexNow, contagem de palavras e terminologias não mapeadas não são verificáveis pelo arquivo HTML.
- `INVALID_URL`: linha que precisa ter origem corrigida no CSV.

## Cuidados
- O reconciliador preserva barra final, query string, path e subdomínio para evitar correspondência falsa.
- A ferramenta **não** faz crawling da HomeHost, não altera páginas e não chama IndexNow.
- As diferenças no CSV não demonstram resolução de ocorrências.
- Não inserir links ou metadados em páginas cuja publicação não foi comprovada.
- Testes precisam ser executados em ambiente com checkout real; commits de testes não significam aprovação dos testes.

### Pendências
Exportação detalhada do Ahrefs; cópia verificada do HTML publicado; execução da suíte no ambiente de checkout; correções pontuais em branch; confirmação de backup/rollback e revisão antes de publicar.
