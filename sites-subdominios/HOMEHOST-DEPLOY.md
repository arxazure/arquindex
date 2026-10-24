# Subdomínios temáticos — HomeHost / Arquindex

**Hospedagem confirmada pelo usuário:** HomeHost (cPanel/FTPS). Não usar Cloudflare como autoridade DNS ou destino de deploy.

## Escopo
Seis candidatos de subdomínios em `sites-subdominios/<hostname>/index.html`: guarda-digital, arquivo-fisico-digital, digitalizacao-certificada-mg, gestao-documental-sp, decreto-10278-documentos, alfresco-gestao-arquivos.

**Estado atual: código versionado, não publicado.** Não presumir que há registro DNS, site criado no cPanel, certificado TLS ou índice no Google.

## Inventário e pré-implantação

1. Confirmar no painel de domínio/registrador os nameservers autoritativos de `arquindex.com.br` e a zona DNS gerenciada no HomeHost, que pode diferir da hospedagem.
2. No cPanel HomeHost, verificar os seis nomes existentes em Domínios/Subdomínios e suas **raízes documentais**; nunca assumir que `public_html/subdominios/<hostname>` já está conectado. Se houver site ativo, não substituir; usar migração controlada.
3. Conferir host, usuário e credenciais FTPS apenas por GitHub Actions secrets. O repositório utiliza `FTP_PASSWORD` nos workflows autorizados; nunca registrar ou copiar senha em código.
4. Rodar inspeção `GET https://<host>/` para DNS, TLS, status HTTP, canonical e documento publicado, antes de habilitar `index,follow`.
5. Verificar que há material suficientemente diferente dos conteúdos existentes. Para subdomínios que apenas repetem a campanha `/transformacao-digital-guarda-documental/`, **consolidar conteúdo na página principal ou usar canonical explícita para URL preferida**. Não promover múltiplas versões concorrentes à indexação.
6. Adicionar `robots.txt` e `sitemap.xml` específicos para cada host somente após confirmar hospedagem. Em ambiente de pré-publicação usar `noindex` e acesso restrito.
7. Só após QA e backup, efetuar FTPS protegido por TLS com caminho de raiz aprovado. Verificar hash de arquivos, status 200, canonical correta e links internos; depois submeter os sitemaps a Google/Bing sem alegar indexação.

## Workflow HomeHost existente

Há um workflow `.github/workflows/publicar-56-subdominios.yml`, mas ele é **específico para 56 hosts** em `seo-regional/56-sites`, com exigências de 3.000 palavras e manifesto próprio. **Não reutilizar aquele deploy automaticamente para estes seis hosts** e não modificar os 56 sites existentes.

A campanha anterior Alfresco usa `.github/workflows/publicar-alfresco-pr20.yml` com backup FTPS, QA e confirmação HTTP. Seu padrão de salvaguardas pode inspirar um deploy novo dedicado, após confirmação das raízes HomeHost.

## Registro de publicação

Para cada host guardar: nome, root cPanel aprovado, DNS observado, TLS, HTTP GET e SHA256 da versão pública, canonical final, robots, sitemap, data/hora, executor e evidência de backup. Só contar como publicado quando todos os requisitos passarem.

## Sobre busca e snippets IA

Schema.org FAQPage/WebPage é dado estruturado, não garantia de exibição ou indexação. Não declarar endereço físico local ou casos de clientes sem evidência. Evitar páginas doorway, variações com título trocado ou conteúdo idêntico.
