# Enriquecimento semântico para blogs e artigos

O módulo `blog_semantic_enrichment.py` propõe novos termos apenas quando coerentes com o tema da página. Não altera diretamente páginas nem adiciona automaticamente listas de palavras-chave irrelevantes. O campo HTML `meta name="keywords"` não é um fator de ranking do Google; priorize títulos úteis, descrições, H2 contextuais, links internos e conteúdos realmente informativos.

```sh
PYTHONPATH=seo-semantico python -m unittest discover -s seo-semantico/tests -v
python3 seo-semantico/blog_semantic_enrichment.py --articles artigos.json --research termos-pesquisa.json --output propostas.json
```

Entrada `artigos.json`: lista de objetos com `url`, `title`, `description`, `body`, `topic`.
Entrada `termos-pesquisa.json`: objeto indexado por tópico; cada tópico pode ter `seed_topics` e `candidate_phrases`, compatível com saída semântica do gerador de briefs.

A publicação exige inventário de URLs reais, autorização editorial, revisão de fatos, backup, prévia e testes. O motor funciona como camada de sugestões revisáveis para todos os blogs alimentados com os inventários correspondentes.
