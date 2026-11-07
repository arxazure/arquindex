# Plano de correção Ahrefs — Arquindex (07/11/2026)

## Fonte e escopo
Resumo informado pelo usuário: 78 páginas órfãs; 139 meta descriptions ausentes; 127 Open Graph incompletos; 9 títulos longos; 181 páginas lentas; 6 URLs não submetidas ao IndexNow; 1 mudança de contagem de palavras; 1 H1 múltiplo; 1 queda de referring domains; 1 FAQ sem schema.

Esses números são *ocorrências do painel*, não uma lista de URLs confirmadas. Não há CSV do crawl anexado. O audit local `scripts/ahrefs_seo_audit.py` é apenas triagem dos arquivos presentes em disco; as URLs do site hospedado devem ser confirmadas separadamente. A soma é 543 ocorrências e pode ter sobreposição.

## Passos para cruzamento seguro
1. Ahrefs > Site Audit > All issues > Exportar linhas com URL, issue, data de crawl, link de origem, URL canônica e evidência; preservar relatório original.
2. Antes de alterar cada URL: comparar HTTP final, canonical, robots, sitemap publicado, template/fonte, e se o arquivo está mesmo na HomeHost. Diferenciar `www.arquindex.com.br`, `arquindex.com.br`, subdomínios e `arquindex.com` (Wix).
3. Executar localmente `python3 -m unittest discover -s tests -p 'test_ahrefs_seo_audit.py'` e `python3 scripts/ahrefs_seo_audit.py --root DIRETORIO_ESPELHO_PUBLICADO --out seo-report/ahrefs-audit.json`. Evitar passar a raiz do repositório se nela coexistirem protótipos, staging ou pastas não publicadas.
4. Para órfãs, verificar se são páginas canônicas 200/indexáveis: adicionar **links editoriais relevantes** a partir de páginas-pilar e guias, sem footers globais artificiais e sem vincular 404/noindex/redirecionamentos.
5. Meta descriptions: uma descrição fiel e útil por URL e por intenção de busca; sem texto duplicado em massa.
6. OG: checar `og:title`, `og:description`, `og:url`, `og:image` e disponibilidade pública da imagem.
7. Title: considerar objetivo e legibilidade, não cortar automaticamente em 60 caracteres; alinhar com H1, canonical e intenção.
8. Desempenho: medir página real com Core Web Vitals/Lighthouse antes de mexer em fontes, imagens, scripts e cache; confirmar ganhos em mobile.
9. H1 múltiplo: manter o título primário da página e rebaixar subtítulos para H2/H3 se semanticamente adequado.
10. FAQ: inserir schema somente quando refletir perguntas/respostas visíveis, válidas e mantidas; marcação não garante rich result.
11. IndexNow: manter as verificações existentes em `scripts/indexnow_daily.py`; validar host, keyLocation, resposta final, self-canonical e HTTP 200 antes de submeter; não confundir aceite com indexação.
12. Backlinks/word count: comparar dados Ahrefs de antes e depois; mudança isolada não comprova prejuízo SEO.
13. Publicar em lotes após revisão, backup e verificação do pipeline FTPS separado; fazer nova varredura e registrar diff por URL.

## Regras de bloqueio
- Não realizar FTP, HomeHost, alteração DNS, execução de Actions, merge, ou submissão IndexNow no estágio de diagnóstico.
- Não alterar páginas que não tenham correspondência verificável com URLs afetadas pelo crawl.
- Não publicar metadados sintéticos genéricos, cases não autorizados, FAQ fictício ou páginas doorway.
- Não declarar resolução de ocorrências antes de nova auditoria pública.

## Arquivos
- Diagnóstico: `scripts/ahrefs_seo_audit.py`
- Testes: `tests/test_ahrefs_seo_audit.py`
- Rotina existente de IndexNow: `scripts/indexnow_daily.py`
- Prioridades anteriores: `scripts/seo_priority_queue.py`
