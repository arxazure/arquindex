# Deduplicação de sitemaps — 18/10/2026

Execução: https://github.com/arxazure/arquindex/actions/runs/39137038581
Commit: 28ea37ea1608403db1364b98e74c99b7cbbe8caa
Job de publicação: 117703544516 — concluído com sucesso.
Job de diagnóstico cPanel: 117703544291 — diagnóstico concluído; CPANEL_API_TOKEN ausente. Não houve ativação de domínio.

Ação: remover somente seis entradas repetidas de https://www.arquindex.com.br/sitemap-legado.xml, preservando todas as URLs nos mapas específicos.

URLs preservadas em /atendimento-rmbh/sitemap.xml:
- https://www.arquindex.com.br/digitalizacao-documentos-belo-horizonte.html
- https://www.arquindex.com.br/digitalizacao-documentos-betim.html
- https://www.arquindex.com.br/digitalizacao-documentos-contagem.html

URLs preservadas em /sitemap-paginas.xml:
- https://www.arquindex.com.br/digitalizacao.html
- https://www.arquindex.com.br/gestao-documental.html
- https://www.arquindex.com.br/lgpd-consultoria.html

Verificações: backup e readback FTP com TLS; nenhuma mudança concorrente no arquivo de origem; XML válido; conjunto de URLs preservado; publicação pública byte a byte; permanência das seis URLs nos mapas específicos. Conferência HTTP independente do sitemap legado: 200.

Estado: publicado e verificado. Nenhuma página removida. Nenhuma submissão Google/Bing realizada nesta ação; não implica indexação.

Pendência: cadastrar CPANEL_API_TOKEN com acesso à conta correta nos secrets do GitHub e confirmar mapeamento físico dos dois subdomínios antes da ativação. Não reutilizar senha FTP como prova de acesso cPanel. Não repetir a deduplicação se o arquivo já estiver correto.
