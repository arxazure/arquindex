# Plano de remediacao das cinco URLs Alfresco — 2026-11-05

## Evidencia
Inspecao GSC Wizard: Belo Horizonte = Discovered - currently not indexed; Contagem, Nuvem dedicada, OCR inteligente e hub Alfresco = URL is unknown to Google. Nenhuma das cinco indexada. Sitemap Alfresco foi aceito e processado com 16 URLs e zero erros; isso nao garante indexacao.

## URLs
- https://www.arquindex.com.br/seo/alfresco-cloud-ocr-ia-belo-horizonte/
- https://www.arquindex.com.br/seo/alfresco-cloud-ocr-ia-contagem/
- https://www.arquindex.com.br/blog/nuvem-dedicada-governanca-alfresco/
- https://www.arquindex.com.br/blog/ocr-inteligente-vs-busca-ecm/
- https://www.arquindex.com.br/alfresco-cloud-ocr-ia/

## Gate de publicacao
1. Confirmar que os arquivos do GitHub correspondem ao HTML realmente servido no HomeHost.
2. Para cada URL testar HTTPS GET, status 200, Content-Type text/html, canonical autorreferente, ausencia de noindex em meta e X-Robots-Tag, robots.txt e resposta em mobile.
3. Verificar links HTML rastreaveis a partir do hub /alfresco-cloud-ocr-ia/ e de artigos Alfresco ja indexados; corrigir links ausentes sem alterar layout.
4. Verificar se as paginas regionais oferecem dados locais realmente distintos, evitando substituicao apenas do nome da cidade.
5. Apenas apos gate passar, publicar alteracoes com backup e conferir novamente URLs ao vivo.
6. Solicitar indexacao manual no URL Inspection e acompanhar; a API de inspecao nao fornece o botao de solicitar indexacao.

## Estado
Diagnostico e plano somente. Nenhum deploy nem indexacao garantidos.
