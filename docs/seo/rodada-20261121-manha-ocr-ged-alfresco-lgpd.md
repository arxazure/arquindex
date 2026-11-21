# Rodada SEO/GEO/AEO — OCR, GED, Alfresco e LGPD

**Data da verificação:** 21/11/2026  
**Escopo:** ARQ-001, ARQ-004, ARQ-005, ARQ-006, PILAR-ALFRESCO-BH e ARQ-008  
**Publicações em produção nesta rodada:** 0

## Resultado executivo

As seis URLs resolveram para `177.234.150.42`, apresentaram TLS válido, HTTP 200, canonical próprio e `index,follow,max-image-preview:large`. O navegador confirmou UTF-8 sem mojibake, WhatsApp funcional e um único H1 coerente em cada página.

Foram encontrados quatro pontos acionáveis:

1. **ARQ-001 e ARQ-004:** páginas responsivas e incluídas em seus sitemaps, porém muito curtas (278 e 285 palavras), com somente sete links internos e sem o logo oficial detectável.
2. **ARQ-005:** 6.020 palavras, mas title/H1/meta ainda tratam digitalização genérica em Belo Horizonte, não OCR corporativo; há overflow móvel de 512 px em viewport de 390 px.
3. **ARQ-006:** conteúdo GED robusto (3.403 palavras), porém com overflow móvel de 422/390 e ausente do sitemap local.
4. **PILAR-ALFRESCO-BH:** passou em mobile e identidade, mas não aparece no sitemap raiz consultado. ARQ-008 passou nos critérios técnicos e está no sitemap.

Não houve alteração de produção porque as correções exigem identificar a origem publicada e validar backup/restauração. Não foi executado FTP, IndexNow, Search Console, Bing, divulgação social nem o script geral de identidade.

## Evidências

- Auditoria técnica: [run 44900181838](https://github.com/arxazure/arquindex/actions/runs/44900181838), job `136834245671`, artefato `14706060560`, digest `sha256:b49869a254e0d90160309c97a03ca925e7dc7eee0e2c54863b68cc2a1e3337d3`.
- Validação móvel/desktop: [run 44900184681](https://github.com/arxazure/arquindex/actions/runs/44900184681), job `136834252815`, artefato `14705278555`, digest `sha256:75c62c974467a56cae0717c13477549e4d06467af976af651859ec8b38f0d514`.
- Fila atualizada: [commit 1adca3c](https://github.com/arxazure/arquindex/commit/1adca3c871448cbab516a3f84a50677b683ca681).
- Integridade da fila: [run 44900353315](https://github.com/arxazure/arquindex/actions/runs/44900353315), concluído com sucesso.

## Achados por página

| ID | Estado verificado | Conteúdo e conversão | Mobile / sitemap | Próxima ação segura |
|---|---|---|---|---|
| ARQ-001 | HTTP 200, canonical próprio, title/H1 de OCR | 278 palavras; 7 links; WhatsApp; sem formulário; logo oficial não detectado | 390/390, sem overflow; URL no sitemap | Enriquecer com limites do OCR, QA, entradas/entregáveis e identidade, após backup |
| ARQ-004 | HTTP 200, canonical próprio, title/H1 de OCR em SP | 285 palavras; 7 links; WhatsApp; sem formulário; logo oficial não detectado | 390/390, sem overflow; URL no sitemap | Confirmar atendimento/logística em SP e só então enriquecer, sem alegar unidade local |
| ARQ-005 | HTTP 200, canonical próprio | 6.020 palavras; 101 links; logo/menu/WhatsApp; sem formulário; intenção OCR desalinhada | 512/390, com overflow; URL fora do sitemap local | Corrigir template móvel e alinhar intenção OCR corporativa após análise de sobreposição |
| ARQ-006 | HTTP 200, canonical próprio, title/H1 de GED | 3.403 palavras; 37 links; logo/menu/WhatsApp; sem formulário | 422/390, com overflow; URL fora do sitemap local | Corrigir overflow e sitemap; diferenciar GED de ECM nas FAQs sem trocar title novamente |
| PILAR-ALFRESCO-BH | HTTP 200, canonical próprio, title/H1 Alfresco | 1.814 palavras; 38 links; logo/menu/WhatsApp; sem formulário | 390/390, sem overflow; URL fora do sitemap raiz | Preservar title/H1 e incluir no sitemap correto após localizar a origem |
| ARQ-008 | HTTP 200, canonical próprio, title/H1 de escolha de consultoria LGPD | 3.486 palavras; 68 links; logo/menu/WhatsApp; sem formulário | 390/390, sem overflow; URL no sitemap | Preservar; medir CTR apenas com amostra suficiente |

## Observação sobre codificação

O coletor HTTP baseado em `requests` sinalizou caracteres corrompidos em cinco respostas porque o cabeçalho não declarou charset de forma suficiente para a decodificação automática. A inspeção real em Chromium informou `UTF-8` e exibiu títulos/H1 corretamente, sem mojibake. Portanto, não foi registrado defeito visual de acentuação; a melhoria possível é declarar explicitamente `charset=UTF-8` no cabeçalho HTTP quando a infraestrutura permitir.

## Decisão de publicação

Nenhuma das lacunas justificou uma edição direta sem origem e rollback comprovados. ARQ-001 e ARQ-004 têm fonte geradora localizada em `scripts/priority_subdomains_ocr.py`, mas esse script gera vários domínios em conjunto; não foi executado para evitar alteração indiscriminada. ARQ-005 não possui fonte específica localizada no repositório além da fila, reforçando a necessidade de inventariar o template/FTP antes de alterar.

## Deduplicação e limites

- ARQ-007 e ARQ-099 foram preservadas, sem nova publicação ou divulgação.
- Nenhum preço, oferta, caso, indexação, posição ou lead foi inferido.
- O inventário consolidado dos 56 subdomínios permanece em [rodada-20261113-tarde-inventario-56-consolidado.md](https://github.com/arxazure/arquindex/blob/master/docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md), sem repetição desnecessária.
