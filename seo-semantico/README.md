# Arquindex SEO Semântico — etapa 1
Motor Python de auditoria somente leitura, sem publicação e sem alterações de DNS, MX ou hospedagem.

## Executar
```bash
python3 seo-semantico/audit.py --sites seo-semantico/sites.txt --output seo-audit.json
```

## O que valida
HTTP, redirecionamento final, título, H1, descrição, canonical, meta robots, volume textual e cobertura lexical inicial para digitalização, ECM/Alfresco, LGPD e guarda. A pontuação lexical é apenas diagnóstico: não prevê posição no Google.

## Roadmap de implantação por ambiente
1. Confirmar quais sites estão online, qual repositório publica cada host e fazer backup.
2. Corrigir 404, canonical, redirecionamentos, sitemap e robots antes de expandir conteúdo.
3. Usar entidades semânticas e JSON-LD **válido e fiel ao conteúdo visível** (Organization, Service, Article e BreadcrumbList conforme cada página).
4. Criar páginas-pilar originais para serviços B2B, com autoria/revisão técnica, fontes e cases autorizados.
5. Vincular posts a páginas-pilar por navegação útil, evitando redes artificiais de links e páginas doorway.
6. Medir cliques, impressões, consultas e URLs indexadas no GSC; Bing/IndexNow após comprovar domínio e chave.
7. Atualizar noticiário apenas com fontes verificadas e revisão editorial; não gerar notícias automaticamente sem validação.

## Regras de segurança
Não gerar centenas de páginas geográficas idênticas; não criar avaliações, depoimentos ou resultados inventados; não enviar URLs ainda inexistentes para indexação. Publicação requer confirmação do deploy e teste HTTP 200 da página final. Não há promessa de Top 10.
