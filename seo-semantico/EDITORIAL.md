# Arquindex: arquitetura semântica SEO/GEO/AEO
## Pilares e intenções
- **Digitalização B2B:** custo por página, preparação, digitalização certificada, OCR, indexação e segurança. Página pilar com escopo, processo, perguntas objetivas e CTA comercial.
- **Alfresco ECM:** Community, implantação local/nuvem, metadados, temporalidade, integração e automação de aprovação; documentar versões verificadas e limitações.
- **Gestão documental:** GED, organização de arquivos, guarda, política de retenção, rastreabilidade e descarte.
- **LGPD:** diagnóstico, ROPA, RIPD, contratos, atendimento aos titulares e DPO; revisões jurídicas com fontes oficiais da ANPD.
- **Noticiário:** guias ou comentários sobre mudanças oficiais, sempre com data, autoria, fonte original e checagem humana.

## Aplicação
O arquivo examples.json contém **URLs ilustrativas ainda não verificadas**. Antes de publicar, substituir cada URL por uma página real (HTTP 200), revisar conteúdo visível, validar JSON-LD e confirmar um único canonical. Incluir bloco `<script type="application/ld+json">` apenas quando a informação for verdadeira na página. Evitar avaliações falsas, FAQ com finalidade exclusiva de rich results, páginas locais clones e link farms.

## Execução
```bash
python3 seo-semantico/generate_schema.py --input seo-semantico/examples.json --output schemas.json
PYTHONPATH=seo-semantico python3 -m unittest discover -s seo-semantico/tests
```
A geração é offline e não publica nem solicita indexação.
