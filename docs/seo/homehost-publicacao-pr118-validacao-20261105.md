# Validação de publicação HomeHost — PR #118

Data: 2026-11-05 (America/Sao_Paulo)

## Decisão e escopo
- Destino autorizado do site institucional: **HomeHost**.
- Não usar merge GitHub, push ou deploy Railway como prova de publicação.
- Manter site restaurado, menus, URLs, blog, planos, clientes e recursos.
- Nenhuma escrita DNS, e-mail, Google Search Console ou Bing é autorizada por este documento.

## Constatações da leitura pública
1. `https://www.arquindex.com.br/` foi legível na ferramenta de consulta pública e apresentou menu e conteúdo institucional.
2. `https://www.arquindex.com.br/digitalizacao.html` apresenta página de digitalização empresarial extensa, com conteúdo técnico, casos e critérios de contratação.
3. `https://www.arquindex.com.br/guias-digitalizacao/documentos-empresas.html` apresenta guia específico da mesma temática.
4. As três URLs propostas neste PR não puderam ser abertas pela ferramenta de consulta web nesta verificação. Isso **não equivale necessariamente a HTTP 404** nem comprova ausência no servidor.
5. A rede do ambiente de execução local retornou erro de resolução DNS; portanto, não foi possível verificar, por ela, IP público, cadeia TLS, certificados FTPS, document root ou resposta HTTP.
6. `config/site-hosting.json` e `AGENTS.md` fixam a HomeHost como origem autorizada. O PR #103 já foi mesclado à master, mas contém somente aviso operacional; não demonstra FTPS ou publicação.

## Tratamento específico das páginas deste PR
- `solucoes/digitalizacao-documentos/index.html`: **NÃO publicar como página indexável** antes de avaliar sobreposição com `/digitalizacao.html`. Se a URL antiga estiver quebrada e for equivalente, preferir 301 para `/digitalizacao.html`, **após confirmar a origem e as regras de redirecionamento**. Não criar redirect automático agora.
- `solucoes/ocr-indexacao/index.html`: revisar diferenciação em relação às páginas OCR existentes; publicar apenas com proposta de valor própria e canonical autorreferente após QA.
- `estudos/custo-ged-saas/index.html`: material atual é **metodologia, não pesquisa concluída**. Identificar como pauta técnica e não anunciar percentuais de economia ou estudo nacional com resultados inexistentes.

## Bloqueios obrigatórios antes de qualquer FTPS
- [ ] Identificar delegação DNS e origem real respondendo por `www` e domínio raiz.
- [ ] Confirmar document root HomeHost via cPanel, com acesso de leitura.
- [ ] Confirmar inventário restaurado e não colisão de paths, inclusive arquivos `index.*` preexistentes.
- [ ] Obter checkpoint de **backup íntegro** e restauração testada em diretório isolado; backup parcial não é suficiente.
- [ ] Verificar FTPS explícito com hostname correto e certificado TLS válido (sem desativar verificação).
- [ ] Confirmar contatos, autoria institucional e revisão editorial de todas as páginas.

## Sequência segura de publicação (quando desbloqueada)
1. Guardar manifesto com arquivos de destino, caminhos completos e SHA-256 dos conteúdos.
2. Executar deploy isolado apenas de arquivos novos, sem espelhamento destrutivo (`--delete` proibido).
3. Em caso de colisão, interromper antes de escrever e solicitar revisão.
4. Publicar inicialmente com `noindex` e verificar conteúdo efetivo por GET da URL oficial.
5. Corrigir canonical autorreferente, assets, links, H1, metadata, contato e compatibilidade móvel.
6. Só após aprovação editorial remover `noindex` nas páginas selecionadas e revisar inclusão no sitemap.
7. Registrar status HTTP, header cache, redirecionamento, hash público e evidência da hospedagem.
8. Submissão aos buscadores em ação distinta e somente depois de leitura pública aprovada.

## Critérios de falha e rollback
Em erro de FTPS, IP/origem divergente, conflito de arquivo, backup não restaurável, TLS inválido, canonical incorreta ou layout quebrado: **não publicar**. Se nova página isolada tiver sido escrita e falhar, efetuar rollback exclusivamente do arquivo criado mediante manifesto e confirmação de que não substitui conteúdo anterior. Nunca limpar pastas inteiras.

## Observação
Os HTMLs do PR estão com `noindex,follow` intencional e não devem ser promovidos a páginas públicas indexáveis por mero merge. É necessário integrar a identidade visual existente após inspecionar o template real da HomeHost.
