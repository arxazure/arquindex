# ECM Arquindex — pacote de revisão, não implantado

Destino lógico: `https://ecm.arquindex.com.br/`. **Não é** `alfresco-ecm.arquindex.com.br`.

Arquivos editoriais próprios: `index.html`, `bh.html`, `empresas.html`, `o-que-e.html`, `vantagens-ecm.html`, `vantagens.html`.

A URL `custo.html` já retornou HTTP 200 e canonical autorreferente na inspeção de 05/11/2026: **preservar a versão publicada** até obter sua origem e backup. O sitemap referencia a URL pública existente, mas este pacote **não** substitui seu arquivo. A página `/index.html` deve continuar canonicalizando para a raiz `/`.

## Pré-publicação obrigatória
1. Confirmar no cPanel/HomeHost o document root exato de `ecm.arquindex.com.br` (não confundir com o outro host Alfresco).
2. Obter backup completo dos arquivos atuais, inclusive `custo.html`, sitemap, robots e tokens de propriedade, e comprovar restauração em ambiente isolado.
3. Comparar conteúdo já existente e preservar links, formulários e recursos úteis que possam estar fora deste pacote. Revisar a redação e identidade das seis páginas.
4. Fazer deploy limitado aos oito arquivos previstos (seis HTML, sitemap e robots), com diff e hashes; não remover tokens de verificação da raiz, apenas excluí-los do sitemap.
5. Validar HTTP 200, títulos, canonical, meta robots, responsividade, links e conteúdo em todos os endereços. Verificar explicitamente `custo.html` e a URL da raiz.
6. Confirmar inexistência de redirects/canonicals para destinos `www.arquindex.com.br/ecm.arquindex.com.br/...`. Restaurar backup caso falhe.
7. Só após comprovação da publicação, avaliar submissão aos mecanismos de busca pelas ferramentas já existentes, sem garantia de indexação.

## Princípios editoriais
Sem valores comerciais inventados, afirmações de certificações novas ou alegações jurídicas absolutas. Conteúdos são informativos e exigem revisão editorial antes de publicação.
