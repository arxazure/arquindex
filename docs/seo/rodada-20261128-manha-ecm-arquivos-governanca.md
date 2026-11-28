# Rodada da manhã — ARQ-133 a ARQ-138

**Data:** 28/11/2026 (horário de Brasília)  
**Escopo:** seis URLs da fila de 238 fichas  
**Tipo:** auditoria somente leitura, revalidação móvel e governança  
**Publicações em produção:** nenhuma  
**Melhorias de página publicadas:** 0 (backup/origem e validações editoriais/comerciais pendentes)

## Resultado executivo

As seis URLs existem e estão publicadas. Todas resolveram DNS para `177.234.150.42`, validaram TLS, responderam HTTP 200, mantiveram canonical própria, `index,follow`, meta description, H1, logo, menu, WhatsApp e UTF-8 correto.

ARQ-133 a ARQ-136 não apresentam overflow em 390/1440 px. ARQ-137 e ARQ-138 mantêm o defeito móvel já conhecido: `scrollWidth 512` para `clientWidth 390`; desktop 1440/1440. Nenhuma das seis páginas possui formulário e nenhuma é mencionada pelo sitemap local.

## URLs auditadas

| ID | URL | Conteúdo/estrutura | Mobile | Sitemap | Estado |
|---|---|---|---|---|---|
| ARQ-133 | https://ecm.arquindex.com.br/custo.html | 3.533 palavras; title/H1 de custo ECM; 3 JSON-LD; identidade e WhatsApp | 390/390 | 200, URL ausente | Validar preços, licenças, migração, infraestrutura e suporte antes de promover |
| ARQ-134 | https://servicos.arquindex.com.br/ | 6.141 palavras; hub genérico; identidade e WhatsApp | 390/390 | 200, URL ausente | Definir função do hub e organizar links para serviços verificados |
| ARQ-135 | https://arquivardocumento.arquindex.com.br/ | 6.153 palavras; title/H1/conteúdo amplos; identidade e WhatsApp | 390/390 | 200, URL ausente | Diferenciar por protocolo de guarda e consulta |
| ARQ-136 | https://arquivos-educacao.arquindex.com.br/ | 6.160 palavras; H1 educação/BH; corpo ainda amplo | 390/390 | 200, URL ausente | Aprofundar temporalidade, acesso e sigilo educacional |
| ARQ-137 | https://arquivos.arquindex.com.br/ | 6.041 palavras; conteúdo genérico de arquivos; identidade e WhatsApp | **512/390, overflow** | 200, URL ausente | Corrigir somente após mapear origem e backup recuperável |
| ARQ-138 | https://auditoria-governanca-dados.arquindex.com.br/ | 6.065 palavras; title/H1 genéricos; identidade e WhatsApp | **512/390, overflow** | 200, URL ausente | Diferenciar de ARQ-114/compliance e corrigir mobile após backup |

O marcador de mojibake do cliente HTTP simples é falso positivo nesta família: o navegador confirmou `charset=UTF-8` e texto acentuado correto.

## Evidências verificáveis

- Auditoria SEO: https://github.com/arxazure/arquindex/actions/runs/46140963857  
  Commit: `2a0ea80c4e28f0051a6db6a65120fd5b63915147`  
  Artefato: `auditoria-prioridades-20261128-manha`  
  SHA-256: `060dd2745ee32ccf5ea371732af9eef245082118e61f7748d002f6b9bc509cf3`
- Mobile/desktop: https://github.com/arxazure/arquindex/actions/runs/46140967057  
  Commit: `0dc9f8e41103979a10090e85f936d1f323f1e88e`  
  Artefato: `validacao-mobile-prioridades-20261128-manha`  
  SHA-256: `804c672ee6b9506509da64b26f3fdbae2373aa571d96bca4a2f68df2a17833aa`
- Canonical renderizada: https://github.com/arxazure/arquindex/actions/runs/46140968748  
  Commit: `10270729260029096f9157f9bd7b9918ca513c2c`  
  Artefato: `canonical-dinamico-20261128-manha`  
  SHA-256: `2c8121b0d009b7490c3f6dd9b49337a7be2ac1929bdf0a429fe25c01bd9cce2e`

Todos os workflows terminaram com `success`.

## Governança e deduplicação

- Evidência móvel adicionada à issue existente #159: https://github.com/arxazure/arquindex/issues/159#issuecomment-7238719967
- Fila atualizada: commit `05ef119dc298383cfeb33368a4923610ee63a871`
- Validação: 238 IDs únicos e um registro de ficha para cada ARQ-133 a ARQ-138.
- ARQ-007 e ARQ-099 foram preservadas; nenhuma republicação ou peça social foi criada.
- O inventário consolidado dos 56 subdomínios permanece em `docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md`; não foi alegada nova cobertura integral.

## Publicação e indexação

- FTP Homehost: não utilizado.
- Railway, Hostinger e ChatGPT Site: nenhum deploy executado ou declarado.
- Sitemap: nenhuma alteração; as páginas ainda exigem correção ou definição editorial.
- Search Console, Bing e IndexNow: nenhum envio.
- Artigo/notícia e redes sociais: nenhum material novo, pois não houve publicação substantiva.
- Indexação, posição e leads: não verificados nem alegados.

## Próximas ações seguras

1. Mapear template/document root de ARQ-137 e ARQ-138 e concluir backup com restauração comprovada.
2. Corrigir o elemento responsável pelos 512 px, preservando canonical, identidade, conteúdo e desktop.
3. Validar preços/serviços de ECM e diferenciar ARQ-134 a ARQ-138 antes de sitemap, divulgação ou submissão.
