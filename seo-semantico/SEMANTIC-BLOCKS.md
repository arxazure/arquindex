# Blocos semânticos para as páginas comerciais da Arquindex
O arquivo `semantic-blocks.json` define três blocos de conteúdo (digitalização, Alfresco, LGPD).
**Os caminhos são exemplos de staging, não arquivos confirmados do website hospedado.** O `index.html` da raiz, associado ao projeto alheio "Se-joga", não é usado e foi excluído do branch principal.
Para aplicar a páginas HTML reais, inserir manualmente no ponto editorial escolhido os marcadores de cada bloco, por exemplo:
```html
<!-- ARQ-SEMANTIC:digitalizacao-b2b:START -->
<!-- ARQ-SEMANTIC:digitalizacao-b2b:END -->
```
Com uma cópia local do site:
```sh
python3 seo-semantico/semantic_block_injector.py --config seo-semantico/semantic-blocks.json --root ./site-copia --output ./staging-seo --apply
```
A ferramenta recusa páginas sem o par exato de marcadores, preserva o HTML fora do bloco e grava a saída somente em staging. Faça revisão, diff e backup antes de publicar. Não faça deploy automático nem declare ranking garantido.
