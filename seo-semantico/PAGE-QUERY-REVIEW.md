# Mapa de páginas e consultas do Search Console
## Uso
Exportar do GSC (dimensões **query** + **page**) CSV com colunas query,page,clicks,impressions,position. Executar:
```bash
python3 seo-semantico/page_query_audit.py --input consultas-paginas.csv --output page-query-report.json
```
O script agrupa URLs por consulta e destaca sobreposição potencial. **Não** remove páginas, edita canonicals, altera redirecionamentos ou divulga dados de consultas em repositório público. Para decidir consolidação, verificar intenção, conteúdo, linkagem e desempenho real de cada URL.

## Evidência direta (GSC 30/09–27/10/2026)
- `serviço de digitalização de documentos` → `https://www.arquindex.com.br/`: 69 impressões, 1 clique, posição 24,55.
- `digitalização de documentos` → `https://www.arquindex.com.br/`: 28 impressões, 1 clique, posição 2,61 (**isto é uma linha específica de página, não o agregado de todas as páginas**).
- `adequação lgpd empresas` → `https://www.arquindex.com.br/adequacao-lgpd-para-empresas.html`: 4 impressões, posição 10,75.
- `assessoria lgpd`: aparecem diversas páginas/subdomínios no relatório, com uma impressão cada em muitas linhas. Sobreposição deve ser investigada, não tomada como prova automática de conteúdo duplicado.

## Ação editorial segura
1. Garantir disponibilidade HTTP 200 e equivalência dos conteúdos canônicos.
2. Reforçar a landing page existente de digitalização B2B, com escopo, OCR, metodologia e CTA.
3. Revisar página LGPD com fontes oficiais, serviços reais e chamada comercial.
4. Auditar subdomínios de baixo desempenho antes de migrar, unificar ou redirecionar.
5. Confirmar indexação por URL no Search Console antes de solicitar reprocessamento.
