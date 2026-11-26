# Plano seguro para desativar listagem de diretórios na HomeHost

Data da constatação: 15/11/2026 (America/Sao_Paulo)

## Evidência pública

- `https://www.arquindex.com.br/assets/` respondeu HTTP 200 com título e conteúdo `Index of /assets/`.
- `https://www.arquindex.com.br/seo/` respondeu HTTP 200 com título e conteúdo `Index of /seo/`.
- A listagem de `/assets/` expõe nomes de 153 arquivos diretos e 12 subdiretórios reais; os subdiretórios testados também permitem navegação.
- A listagem de `/seo/` expõe dez diretórios de páginas regionais Alfresco/OCR existentes.
- Na inspeção pública direta não apareceram nomes com extensões `.zip`, `.sql`, `.log`, `.bak` ou `.env`. Isso não prova que não existam arquivos sensíveis fora do primeiro nível.

## Risco

A listagem facilita inventário não autorizado de nomes, versões, campanhas e estrutura interna. Desativá-la é uma correção de baixo impacto quando aplicada na raiz correta, mas uma regra mal posicionada pode afetar subdomínios, aplicações ou a entrega de arquivos. Por isso, não foi feita alteração em produção nesta rodada.

## Pré-condições obrigatórias

1. Confirmar a raiz pública HomeHost que atende `www.arquindex.com.br`.
2. Confirmar backup completo fora de `public_html`, com marcador de conclusão e teste de restauração isolada.
3. Confirmar conexão FTPS com certificado válido e sem desativar TLS.
4. Copiar o `.htaccess` atual e registrar hash, tamanho, proprietário e permissões.
5. Confirmar se Apache permite `Options -Indexes` no contexto da conta.

## Mudança proposta, não aplicada

Adicionar à configuração efetivamente usada pelo site, preservando as regras existentes:

```apache
# Impede listagem automática; não bloqueia arquivos referenciados diretamente.
Options -Indexes

# Mantém arquivos de índice usuais quando existirem.
DirectoryIndex index.html index.php
```

Se `Options` for proibido pelo provedor, solicitar à HomeHost a diretiva equivalente. Não experimentar regras alternativas em produção sem confirmar compatibilidade.

## Validação pós-mudança

- `/assets/` e `/seo/` devem deixar de exibir inventário, preferencialmente com 403 ou página de índice intencional.
- Homepage e páginas prioritárias devem continuar em HTTP 200.
- CSS, JavaScript, imagens e fontes referenciados devem continuar em HTTP 200.
- `robots.txt`, `sitemap.xml`, canonicals e links internos não devem mudar.
- Testar em janela anônima, dispositivo móvel e pelo menos um navegador adicional.
- Registrar TTFB, cabeçalhos e conteúdo antes/depois.

## Reversão

Restaurar exatamente o `.htaccess` copiado, validar novamente as URLs e registrar o motivo. Não remover arquivos nem mover diretórios como forma de corrigir a listagem.

## Limpeza semanal

Nenhuma limpeza foi feita: 0 bytes liberados, 0 itens movidos e 0 itens removidos. A listagem pública não é inventário suficiente para provar que um arquivo está sem uso. A futura análise deve cruzar referências HTML/CSS/JS, logs do servidor, Search Console, backlinks, rotinas de aplicação e raízes de subdomínios antes de colocar qualquer item em quarentena.
