# Recuperação SEO Homehost — execução controlada

Destino: Homehost, diretório `public_html`. O Railway é um site separado e não é alterado por este fluxo.

## Preparação
1. Classificar as URLs das duas exportações do Search Console. Não transformar arquivos .bak, .py, .xlsx, .json de configuração, credenciais ou URLs de outros subdomínios em páginas HTML.
2. Para cada página legítima, revisar o conteúdo, URL canônica, links e existência prévia na Homehost.
3. Gerar um manifesto JSON com `schemaVersion: 1`, `host: "www.arquindex.com.br"` e `files` com entradas `{path,content,sha256}`. `path` é relativo a `public_html`, sem barra inicial. `sha256` é o hash SHA-256 em hexadecimal dos bytes UTF-8 de `content`.
4. Rodar com Bun e variáveis de ambiente já existentes `FTP_HOST_PRIMARY`, `FTP_USER`, `FTP_PASSWORD`; opcional `FTP_TLS_SERVERNAME`. Nunca versionar credenciais.
5. Simulação: `bun run homehost-hardening/homehost-ftps-publish.ts ./manifest.json`.
6. Após verificar os resultados e aprovar o lote, aplicar: `FTPS_APPLY=true bun run homehost-hardening/homehost-ftps-publish.ts ./manifest.json`.

## Proteções
- A execução bloqueia substituição de arquivos com conteúdo diferente. Não apaga arquivos.
- Um arquivo idêntico é preservado.
- Criação de diretórios e uploads só ocorrem com `FTPS_APPLY=true`.
- Conferir os códigos HTTP, canonicals, sitemap e conteúdo publicado após o envio.
- O script não configura uma sincronização automática GitHub → Homehost; precisa ser executado num ambiente com credenciais e acesso FTPS.
- Não publicar automaticamente todas as URLs da planilha: status de indexação não significa ausência física do arquivo.


## Auditoria real dos URLs do Search Console (sem publicação)
O script `audit-ftps.ts` recebe JSON `{"urls":[{"url":"https://www.arquindex.com.br/caminho/"}]}`, ou array de URLs.
Use a exportação de auditoria `arquindex_auditoria_homehost_2026-10-12.json` gerada a partir das duas planilhas; ela contém 2.000 registros em `urls`, inclusive subdomínios, que são marcados como `other-host` e NÃO publicados.
No ambiente que já tem as variáveis de FTP:
```sh
bun run homehost-hardening/audit-ftps.ts ./arquindex_auditoria_homehost_2026-10-12.json > homehost-ftps-audit-result.json
```
O comando é somente leitura. Não use o serviço do site Railway para servir páginas da Homehost; caso use infraestrutura auxiliar para executar o comando, não altere a aplicação web.
O resultado distingue `ftp-file-present`, `ftp-file-missing`, `directory-missing-or-inaccessible`, `other-host` e arquivos internos. Falha de acesso não equivale a 404.
Para publicar, é necessário revisar o conteúdo original, montar manifesto `{schemaVersion:1,host:"www.arquindex.com.br",files:[{path,content,sha256}]}` e primeiro simular com `homehost-ftps-publish.ts`.
ATENÇÃO: o relatório do Search Console não é manifesto de publicação; não gere páginas em massa a partir dos slugs.
