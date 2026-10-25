# Pré-publicação controlada — correções Arquindex (25/10/2026)

## Objetivo
Publicar somente após validação dos originais, backup integral e rollback. Este documento não autoriza deploy automático nem altera o cursor SEO.

## Arquivos preparados (staging, noindex)
1. `staging/seo/correcoes-20261025/governanca-documental-sharepoint-engenharia-bh.html`
   - URL solicitada: `https://arquindex.com.br/governanca-documental-e-automacao-sharepoint-para-engenharia-em-belo-horizonte.html`
2. `staging/seo/correcoes-20261025/digitalizacao-contabilidade-bh.html`
   - URL solicitada: `https://arquindex.com.br/digitalizacao-de-documentos-belo-horizonte-contabilidade-lentidao-operacional/`
3. `staging/seo/correcoes-20261025/validade-juridica-documento-digitalizado.html`
   - URL solicitada: `https://mapeamento.arquindex.com.br/?post=validade-juridica-documento-digitalizado`

Remover `srsltid` das URLs canônicas; não usá-lo em sitemap. O terceiro destino usa parâmetro `post`: confirmar a implementação do roteador antes de alterar o index do subdomínio. Não sobrescrever `mapeamento.arquindex.com.br/index.html` com o artigo.

## Bloqueios obrigatórios
- [ ] Issue #28: backup integral Homehost verificado (manifesto, hashes, restauração de amostra, retenção e acesso)
- [ ] PR #40: revisar mecanismo de backup, concluir testes, aprovar e integrar quando seguro
- [ ] Verificar e corrigir YAML do workflow legado sem disparar regravação do cursor SEO
- [ ] Baixar e guardar os três HTML originais, inclusive a resposta do roteador `?post=`
- [ ] Confirmar mapeamento FTP/cPanel e raiz pública de cada host
- [ ] Integrar imagens licenciadas/institucionais verificadas; não deixar arte inexistente
- [ ] Definir canonical final de cada URL e remover `noindex` somente após deploy validado
- [ ] Verificar que há apenas um H1, apenas um botão flutuante e sem overflow em 390px
- [ ] Verificar links internos e evitar reciprocidade automática ou páginas-cidade duplicadas
- [ ] Fazer backup dos arquivos específicos e testar rollback antes do primeiro upload
- [ ] Fazer deploy atômico, uma página por vez; verificar HTTP 200, title, H1, canonical, conteúdo e assets
- [ ] Atualizar sitemap somente com URLs públicas verificadas e registrar commit, hashes e resultados
- [ ] Submeter IndexNow/Search Console/Bing somente com confirmação autenticada e registrar IDs

## Alerta do workflow legado
`.github/workflows/atualizar-fila-20261024-tarde.yml` tem bloco Python heredoc com relatório multilinha (a partir de `report.write_text("""`), contendo linhas não indentadas no bloco YAML. **Não executar nem corrigir diretamente na branch principal sem isolar o disparo:** esse workflow escreve novamente `seo/fila-seo-geo-aeo.csv` e redefine o cursor para ARQ-113, embora a fila atual esteja em ARQ-119. Uma correção deve ocorrer em branch/PR, com workflow desativado para push ou sem alteração de cursor, e com validação estática do YAML.

## Aceite
Só marcar `publicado` após evidência HTTP pública e conteúdo correto em cada destino. Até lá: **3 rascunhos, 0 deploys**.
