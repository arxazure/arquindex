# Rodada SEO/GEO/AEO — ARQ-227 a ARQ-232

Data: 2026-11-01  
Escopo: seis URLs auditadas, três melhorias substanciais publicadas  
Produção confirmada: Railway `Arquindex Plataforma / arquindex-web / production`  
Origem de publicação: branch `railway-production-2026`

## Resultado executivo

- Auditadas: ARQ-227, ARQ-228, ARQ-229, ARQ-230, ARQ-231 e ARQ-232.
- Melhoradas e publicadas: ARQ-230, ARQ-231 e ARQ-232.
- Preservadas sem alteração: ARQ-227, ARQ-228 e ARQ-229; não havia justificativa para uma edição genérica ou repetitiva nesta rodada.
- Nenhuma página nova foi criada.
- ARQ-099 não foi alterada nem divulgada.
- Nenhuma publicação social foi repetida.

## Auditoria anterior à alteração

Workflow: https://github.com/arxazure/arquindex/actions/runs/41363591498

As seis URLs responderam HTTP 200 em mobile e desktop, com um H1, canonical para o domínio apex, robots index,follow, presença no sitemap correspondente e sem overflow horizontal.

| ID | URL | Conteúdo observado | Decisão |
|---|---|---:|---|
| ARQ-227 | https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/belem/ | 884 palavras | Preservar até confirmar atendimento e diferenciação regional |
| ARQ-228 | https://www.arquindex.com.br/seo-regional/gestao-documental-ecm-databooks/sabara/ | 845 palavras | Preservar; brief de acervos frágeis ainda requer implementação própria |
| ARQ-229 | https://www.arquindex.com.br/digitalize/ | 473 palavras | Preservar; hub já possui menu e WhatsApp e deve ser ampliado apenas com diferenciação real |
| ARQ-230 | https://www.arquindex.com.br/digitalize/santa-luzia/ | 980 palavras antes da identidade | Aplicar identidade e conversão, preservando SEO e conteúdo local |
| ARQ-231 | https://www.arquindex.com.br/digitalize/ribeirao-das-neves/ | 981 palavras antes da identidade | Aplicar identidade e conversão, preservando SEO e conteúdo local |
| ARQ-232 | https://www.arquindex.com.br/digitalize/ibirite/ | 964 palavras antes da identidade | Aplicar identidade e conversão, preservando SEO e conteúdo local |

## Alterações publicadas

Commit editorial inicial: https://github.com/arxazure/arquindex/commit/44dbbfcbdb4e74e3af933664972ee053657b18aa  
Commit corretivo final: https://github.com/arxazure/arquindex/commit/b02c4d15257d9c0557659d9ff54d02b49e8bb1a2  
Deployment Railway: `fd1a7b16-64e9-4e28-82ff-a2e58ab6cc36` — SUCCESS em 2026-11-01T23:49:56.895Z.

Em ARQ-230, ARQ-231 e ARQ-232 foram adicionados, de modo seletivo:

- wordmark Arquindex e assinatura institucional usados pelo cabeçalho atual;
- cabeçalho e menu responsivos;
- rodapé institucional;
- atendimento flutuante por WhatsApp;
- CTA de proposta para `/contato`;
- parâmetros UTM específicos por cidade;
- testes de regressão que impedem aplicação indiscriminada a outras páginas.

Titles, H1, descriptions, canonical, FAQ, JSON-LD e conteúdo específico de cada cidade foram preservados. Não houve mudança diária de título.

## Validação pública após implantação

Workflow: https://github.com/arxazure/arquindex/actions/runs/41364026141  
Job: `125020268669` — success.

Resultados em mobile 390×844 e desktop 1440×900:

| ID | HTTP | Canonical | H1 | Identidade | Conversão | Palavras mobile | Layout |
|---|---:|---|---:|---|---|---:|---|
| ARQ-230 | 200 | correto | 1 | wordmark, assinatura, menu, rodapé e widget | WhatsApp + CTA UTM | 1007 | sem overflow |
| ARQ-231 | 200 | correto | 1 | wordmark, assinatura, menu, rodapé e widget | WhatsApp + CTA UTM | 1008 | sem overflow |
| ARQ-232 | 200 | correto | 1 | wordmark, assinatura, menu, rodapé e widget | WhatsApp + CTA UTM | 991 | sem overflow |

Também passaram quatro testes de identidade/conversão e dois testes de redirects legados. ARQ-227, ARQ-228 e ARQ-229 foram rechecadas como controles em mobile e desktop.

## Backup e rollback

- Blob anterior ao primeiro ajuste: `b26934a69d89134d964015b7f1f3bbbd5f5208df`.
- Blob antes da correção de wordmark: `974bc7d702d06ea614aae695b272efc1c71a26d4`.
- Blob final publicado: `1c5ce8853ed3b8d245447e82e48266d4aaa4e2c8`.
- Deployment anterior permanece elegível a rollback no Railway; o commit final é descendente direto e reversível.

## Sitemap e descoberta

As três URLs já estavam publicadas e presentes em `https://www.arquindex.com.br/digitalize/sitemap.xml`; o XML foi validado no workflow. Como não houve URL nova nem alteração de localização, o sitemap não foi modificado. Não houve submissão ao Search Console, Bing ou IndexNow nesta rodada e nenhuma indexação é alegada.

## Ocorrências registradas

1. A primeira auditoria falhou porque o teste esperava canonical com `www`, enquanto a produção usa canonical no domínio apex. O teste foi corrigido e a auditoria `41363591498` passou.
2. A primeira verificação pós-publicação, `41363801535`, detectou que o arquivo de imagem do logo apontava para um ativo inexistente na origem Railway. A referência foi removida e substituída pelo wordmark textual já usado no cabeçalho atual; o deployment final e a verificação `41364026141` passaram.
3. Nenhum formulário foi adicionado; as páginas têm CTA de contato e WhatsApp. Eventos de lead e conversões não foram inventados.

## Registro persistente e continuidade

Fila atualizada até ARQ-232 no commit https://github.com/arxazure/arquindex/commit/a22b819f8329a5249cdc287eea5ef5726e387cd6.

Próximo cursor: ARQ-233 a ARQ-238. Prioridades da próxima rodada:

1. auditar as seis fichas finais com o mesmo conjunto técnico e mobile;
2. selecionar no máximo três melhorias realmente distintas;
3. verificar se há lacunas de identidade e conversão sem replicar conteúdo local ou redivulgar ARQ-007/ARQ-099.
