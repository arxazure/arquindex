# Restauração solicitada em 17/10/2026

A lista contém 209 entradas: 192 endereços comerciais, 10 possíveis aplicações e 7 nomes sem domínio completo que parecem pastas. A lista original está em `hosts.txt`; decisões por entrada em `manifest.json`.

`build.py` gera páginas completas, navegação, metadados, dados estruturados e sitemaps. São 17 conteúdos principais com escopos diferentes. As 175 variações de intenção equivalente apontam por 301 para o conteúdo principal, inclusive o antigo hostname aninhado. O sitemap de cada alias redireciona ao sitemap canônico. Não há XML com URLs de outros hosts nem um índice global entre hosts sem validação de propriedade.

Nomes de clientes ou empresas nos antigos hostnames não são usados como afirmação de parceria. Não são inventados escritórios locais, certificações institucionais ou comparações com concorrentes. Conteúdos não foram recuperados de backup: são uma reconstrução editorial nova e consolidada, não uma restauração idêntica ao servidor anterior.

## Execução

1. `python recovery-20261017/build.py`
2. Configure secrets `CPANEL_HOST` (origem HTTPS com porta 2083), `CPANEL_USER` e `CPANEL_API_TOKEN` ou `CPANEL_PASSWORD`. O destino precisa ser um dos hosts Arquindex explicitamente permitidos em `restore.py`.
3. Configure `FTP_PASSWORD` para a conta `arquind2`.
4. Execute o workflow **Restaurar registros e rede documental Arquindex**.

A senha FTP não é usada automaticamente para autenticar no cPanel. A tentativa anterior recebeu HTTP 401. Nenhum segredo deve entrar no repositório, em argumentos de comandos ou em logs.

O processo confirma a conta cPanel e cada document root antes de publicar por FTPS. Cria somente os registros ausentes; não apaga nem muda DNS, MX ou domínios existentes. cPanel deve criar a zona/registro local durante o cadastro; se DNS for externo, será necessário configurar os registros no provedor autoritativo. AutoSSL é solicitado, e a verificação HTTPS mantém validação de certificado habilitada.

Os novos sites ficam em `public_html/subdominios/<hostname>` como uma única cópia. Domínios existentes usam a raiz informada pelo cPanel. Raízes compartilhadas são recusadas. Não há exclusão de arquivos. Arquivos públicos substituídos são preservados em um ZIP no artifact do workflow, fora do servidor web. `.htaccess` mantém as regras anteriores após um bloco gerenciado idempotente. Aplicações PHP existentes são preservadas e registradas para revisão.

O diretório `/rede-documental/` interliga os conteúdos publicados e recebe um link na homepage HTML quando essa inserção puder ser validada. Sitemaps só contêm URLs canônicas do próprio host. Não há alegação de submissão ao Search Console nem de indexação.

## Itens que não são páginas comerciais

- `assets`, `bin`, `cache`, `css`, `cast`, `artigos`, `cidades`: preservar como entradas ambíguas/pastas. Não criar hostnames inferidos para elas sem confirmar sua função.
- `alf`, `acervonet`, `arcadiagp`, `arxbox`, `centralinf`, `dashboard`, `dados`, `datagestao`, `digiout`, `digitaldoc`: provisionar registro, preservando conteúdo. Código, bases de dados, autenticação e documentos não podem ser recriados a partir do hostname; exigem backups próprios. Permanecem pendentes no relatório.

## Verificação

`result.json` distingue cadastro, upload, DNS, HTTPS, sitemap e pendências. O workflow termina com falha se o acesso administrativo faltar, a publicação estiver incompleta, houver erro HTTPS/sitemap ou aplicações ainda exigirem recuperação. Um upload FTP isolado nunca é relatado como restauração concluída.
