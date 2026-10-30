# Uso do GSC sem publicar dados de consulta em repositório
Exportar manualmente consultas relevantes do Google Search Console como CSV com colunas `query,clicks,impressions,position` e executar:
```bash
python3 seo-semantico/gsc_opportunities.py --input consultas.csv --output oportunidades.md
```
O arquivo de entrada não é enviado ao GitHub. O relatório separa consultas próximas do Top 10 (posição 4–20) daquelas que precisam de melhorias mais profundas. Examinar **página e consulta juntas** antes de alterar title, canonical ou conteúdo. Validar período, território, presença de marca, páginas duplicadas e consultas irrelevantes. Evitar qualquer publicação em massa sem revisão editorial.

## Evidências observadas em 30/10/2026
Consulta conectada à propriedade HTTPS WWW da Arquindex (28 dias encerrados em 27/10):
- `digitalização de documentos`: 102 impressões, 1 clique, posição média 27,25.
- `serviço de digitalização de documentos`: 99 impressões, 1 clique, posição média 35,58.
- `adequação lgpd empresas`: 4 impressões, 0 cliques, posição média 10,75 (abaixo do filtro padrão de dez impressões).
Dados são consultas e **não** evidenciam qual página ranqueou. A origem é o GSC Wizard conectado. Não pressupor que os valores se mantenham em períodos futuros.
