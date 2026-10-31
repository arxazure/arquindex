# Pipeline de brief e rascunho semântico
Execute:
\`\`\`bash
python3 seo-semantico/content_brief_engine.py --config seo-semantico/briefs-config.json --output saida-seo --offline
\`\`\`
Para pesquisa competitiva, preencha \`competitor_urls\` com URLs HTTPS públicas escolhidas manualmente a partir de SERPs verificadas; então omita \`--offline\`.

- Cria pastas locais por domínio concorrente usando \`os.mkdir()\` quando possível.
- Respeita robots.txt, limita tamanho e frequência de requisições e registra erros em arquivos locais.
- Extrai títulos, cabeçalhos e termos recorrentes; **não** infere que o Google exige palavras específicas.
- Gera \`brief.json\`, \`rascunho.md\` e \`summary.json\`.
- Rascunhos são originais, mas propositalmente genéricos: revisão técnica, dados específicos, exemplos e fontes são obrigatórios.
- Não copia o corpo das páginas concorrentes para o disco, não publica nem dispara indexação.
- URLs não são descobertas automaticamente; coleta de SERPs exige fonte específica e respeito aos seus termos.
- Use somente concorrentes legítimos e evite dados pessoais, paywalls ou informações protegidas.
