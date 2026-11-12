# Correcao editorial segura — WordPress Arquindex

Origem alvo: https://blog-digitalizacao-de-documentos.arquindex.com.br/
Data da auditoria: 2026-10-25
Status: PROPOSTA PARA REVISAO; NAO PUBLICADA.

## Evidencias (leitura publica)
- Pagina inicial: https://blog-digitalizacao-de-documentos.arquindex.com.br/
- Issue: https://github.com/arxazure/arquindex/issues/46
- Conteudo visivel atualmente contem "Empresa Y", "Empresa Z", "Empresa X", percentuais, contagens de clientes, nomes de equipe e testemunhos que carecem de comprovacao.
- Footer apresenta endereco que deve ser confirmado antes de uso.
- A API /wp-json/wp/v2/posts e /robots.txt nao forneceram resposta conclusiva no verificador. Nao interpretar como HTTP 404.

## Texto sugerido para substituir blocos nao comprovados

### Hero
**Digitalizacao de documentos e gestao documental na pratica**

Artigos, guias tecnicos e orientacoes sobre digitalizacao, OCR, PDF/A, LGPD, gestao de arquivos e plataformas ECM. Saiba o que avaliar antes de digitalizar, organizar, preservar ou destinar documentos da sua empresa.

Saiba mais sobre as solucoes da Arquindex: https://www.arquindex.com.br/

### Bloco de servicos
- **Digitalizacao documental:** preparacao, captura, controle de qualidade, indexacao e entrega conforme escopo contratado.
- **OCR e PDF pesquisavel:** reconhecimento de texto com validacao e criterios de qualidade adequados ao acervo.
- **Gestao documental e ECM:** classificacao, metadados, acesso, preservacao, fluxos e temporalidade definidos pelo cliente.
- **Governanca e LGPD:** orientacao sobre controles e responsabilidades na gestao de dados pessoais.

### Conteudo editorial
**Como avaliar um projeto de digitalizacao empresarial?**

Antes de contratar, identifique tipos documentais, quantidades, estado de conservacao, regras de acesso, necessidade de OCR, formato de entrega e prazo de guarda. Defina criterios verificaveis de qualidade, indexacao e rastreabilidade. A digitalizacao nao determina, por si so, o descarte dos originais; a destinacao depende das regras legais e da tabela de temporalidade aplicaveis.

Guia de servicos: https://www.arquindex.com.br/
Contato comercial: comercial@arquindex.com.br
WhatsApp: https://wa.me/5531973632725

### Substituicoes obrigatorias
1. Remover completamente depoimentos com personagens genericos ou nomes nao autorizados.
2. Retirar numero de documentos, empresas, satisfacao e anos de experiencia ate haver fonte interna aprovada.
3. Retirar nomes e imagens de colaboradores que nao tenham confirmacao e autorizacao.
4. Remover projetos de "Empresa Y/Z" ou reescrever como exemplo HIPOTETICO, claramente identificado, sem alegar case real.
5. Verificar endereco comercial antes de publicar. Se nao confirmado, usar somente site e canais de contato aprovados.
6. Evitar promessas automaticas de conformidade e validade juridica.

## Checklist tecnico de publicacao
- [ ] Provar qual painel WordPress/hosting administra a URL
- [ ] Identificar conta com permissoes de edit_posts/edit_pages e mecanismo de backup
- [ ] Backup restauravel de banco e wp-content
- [ ] Inventariar paginas e posts publicos via painel ou REST autenticado de leitura
- [ ] Revisar menus e links quebrados; preservar slugs com impressao no GSC
- [ ] Verificar HTTP, HTML canonical, robots, sitemap principal e sitemap de posts
- [ ] Publicar edicao da PAGINA EXISTENTE, nunca criar clone
- [ ] Ler novamente URL publica, conferir conteudo atualizado e canonical
- [ ] Registrar permalink, autor, horario, status, hash/versao e evidencia HTTP
- [ ] Conferir indexacao em GSC em etapa separada
- [ ] Nao publicar em Blogspot, HomeHost ou Railway como substitutos do WordPress

## Restricoes
Nao executar POST/PUT no WordPress sem identidade de origem e autorizacao de escrita verificadas; nao tratar esta documentacao GitHub como deploy.
Nao reenviar requisicoes de publicacao de resultado desconhecido.
