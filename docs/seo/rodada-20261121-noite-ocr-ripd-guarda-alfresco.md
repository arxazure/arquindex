# Rodada SEO/GEO/AEO — OCR, RIPD, guarda e Alfresco

**Data da verificação:** 21/11/2026  
**Escopo:** ARQ-016, ARQ-017, ARQ-019, ARQ-020, ARQ-021 e ARQ-022  
**Publicações em produção nesta rodada:** 0

## Resultado executivo

As seis URLs responderam HTTP 200, resolveram para `177.234.150.42` e apresentaram TLS válido. A inspeção pós-JavaScript confirmou quatro artigos com metadados próprios e dois artigos com conflito estrutural.

- **ARQ-016, ARQ-017, ARQ-021 e ARQ-022:** canonical, title, H1 e descrição próprios após JavaScript.
- **ARQ-019 e ARQ-020:** dois canonicals e dois H1 após renderização. Ambas preservam o canonical-base inválido no domínio `www` e acrescentam o canonical correto do artigo.
- **ARQ-017:** o overflow móvel reapareceu: 414 px de largura em viewport de 390 px.
- **ARQ-020:** houve mudança desde a auditoria de 19/10. O artigo OCR agora renderiza title, H1 e descrição próprios, mas ainda mantém os sinais duplicados da página-base.
- Nenhuma das seis URLs parametrizadas aparece no sitemap local consultado.

Nenhuma correção foi publicada porque a origem efetiva dos templates conflitantes não foi localizada no repositório e o backup HomeHost permanece sem restauração comprovada. Não houve FTP, IndexNow, Search Console, Bing ou divulgação social.

## Evidências

- Auditoria HTTP/DNS/TLS: [run 44963106650](https://github.com/arxazure/arquindex/actions/runs/44963106650), job `137026049492`, artefato `14730178255`, digest `sha256:746dbd8d485e696a26eb8c1897eeda783bb10e5262c483cd72766324149a5bd4`.
- Mobile/desktop: [run 44963090856](https://github.com/arxazure/arquindex/actions/runs/44963090856), job `137026001184`, artefato `14730561880`, digest `sha256:1a428a59374add5644e6e41a26a9056b5fbfa9ba130b3c62bb56361a0f816b46`.
- Canonical pós-JavaScript: [run 44963092114](https://github.com/arxazure/arquindex/actions/runs/44963092114), job `137026005453`, artefato `14730153423`, digest `sha256:b19ba6d116d9f3025a478ad195843bf008ec885d35d4ce38c4765a6ec08e0103`.
- Fila atualizada: [commit 5d0019d](https://github.com/arxazure/arquindex/commit/5d0019d4c5f844ee8bc9e58c52d455f92bff1602).
- Integridade da fila: [run 44963243297](https://github.com/arxazure/arquindex/actions/runs/44963243297), concluído com sucesso.

## Achados por URL

| ID | Estado renderizado | Mobile / identidade | Sitemap | Decisão |
|---|---|---|---|---|
| ARQ-016 | Artigo OCR corporativo; canonical próprio; 1 H1; 2 JSON-LD | 390/390; logo/menu/WhatsApp; sem formulário | Parâmetro não listado | Preservar; confirmar logística em Mauá antes de ampliar |
| ARQ-017 | Artigo RIPD; canonical próprio; 1 H1; 3 JSON-LD | **414/390 com overflow**; logo/menu/WhatsApp; sem formulário | Parâmetro não listado | Corrigir regressão móvel sem alterar os metadados |
| ARQ-019 | Artigo CONARQ; **2 canonicals e 2 H1**; 2 JSON-LD | 390/390; sem logo ou WhatsApp; sem formulário | Parâmetro não listado | Corrigir com ARQ-015/020 no template comum |
| ARQ-020 | Artigo OCR agora renderizado; **2 canonicals e 2 H1**; 2 JSON-LD | 390/390; sem logo ou WhatsApp; sem formulário | Parâmetro não listado | Não promover; corrigir template e identidade |
| ARQ-021 | Artigo de organização de arquivo morto; canonical próprio; 1 H1; 2 JSON-LD | 390/390; logo/menu/WhatsApp; sem formulário | Parâmetro não listado | Preservar; não divulgar endereço operacional |
| ARQ-022 | Artigo SharePoint versus Alfresco; canonical próprio; 1 H1; 2 JSON-LD | 390/390; logo/menu/WhatsApp; sem formulário | Parâmetro não listado | Preservar; confirmar versão/arquitetura antes de ampliar |

## Grupo de correção consolidado

ARQ-015, ARQ-019 e ARQ-020 apresentam o mesmo padrão:

1. o HTML inicial declara canonical-base incorreto, concatenando o subdomínio dentro de uma URL em `www.arquindex.com.br`;
2. o JavaScript adiciona o canonical correto do artigo sem remover o primeiro;
3. o H1 da base permanece junto com o H1 do artigo;
4. a identidade oficial e o WhatsApp não aparecem.

A correção deve ocorrer uma vez no template/origem comum: remover o canonical e o H1 da base quando houver artigo válido, manter apenas os metadados do artigo e aplicar os componentes oficiais. Depois, retestar o HTML inicial, o DOM renderizado, mobile, sitemap e somente então considerar submissão.

## Fechamento do dia

Foram auditadas **18 URLs distintas** nas três rodadas de 21/11, todas com evidências no GitHub e registros individuais na fila. Não houve republicação da ARQ-007 ou ARQ-099, nem execução indiscriminada do script de identidade. O inventário consolidado dos 56 subdomínios permanece referenciado em [rodada-20261113-tarde-inventario-56-consolidado.md](https://github.com/arxazure/arquindex/blob/master/docs/seo/rodada-20261113-tarde-inventario-56-consolidado.md).

Não se inferiram indexação, posição, tráfego ou leads.
