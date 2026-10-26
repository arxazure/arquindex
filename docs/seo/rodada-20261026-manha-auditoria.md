# Rodada SEO/GEO/AEO — 26/10/2026, manhã

## Estado de segurança

- PR [#41](https://github.com/arxazure/arquindex/pull/41) integrado no commit `45666ba84ec96f90d87bf0b03189ecc37649ae54`: workflow histórico aposentado, escrita na fila removida e cursor ARQ-119 preservado.
- PR [#40](https://github.com/arxazure/arquindex/pull/40) integrado no commit `61884110a761d6b121533aa77b28fb218eeb27ec`: mecanismo de backup retomável disponível.
- A integração do PR #40 não equivale a backup concluído.
- Backup real iniciado no workflow [40316676565](https://github.com/arxazure/arquindex/actions/runs/40316676565), com testes aprovados e etapa de cópia privada em andamento no momento deste registro.
- A issue [#28](https://github.com/arxazure/arquindex/issues/28) permanece aberta. Nenhuma página existente foi substituída nesta rodada.

## Auditoria atual — ARQ-119 a ARQ-124

As seis URLs responderam e foram extraídas em HTTPS. Todas apresentaram canonical própria, viewport móvel, `index,follow,max-image-preview:large`, title, description, um H1 observado e links funcionais para o WhatsApp +55 31 97363-2725.

| ID | URL | intenção declarada | diagnóstico atual |
|---|---|---|---|
| ARQ-119 | https://contratar-digitalizacao-documentos-armazenamento-nuvem.arquindex.com.br/ | digitalização com entrega/armazenamento em nuvem | title e H1 ainda enfatizam digitalização genérica em BH; não respondem com clareza a exportação, acesso, segurança, aceite e limites do armazenamento |
| ARQ-120 | https://compliance-digitalizacao-preco.arquindex.com.br/ | custo de governança e mapeamento | title, description e H1 permanecem focados em digitalização genérica em BH; intenção de compliance/preço não está diferenciada |
| ARQ-121 | https://consultoria-mapeamento-mg.arquindex.com.br/ | mapeamento documental em Minas Gerais | title cita MG e BH ao mesmo tempo; H1 observado continua em BH. Não ampliar alegação estadual sem comprovação de atendimento |
| ARQ-122 | https://empresas-brasileiras-especializadas-digitalizacao-documental-se.arquindex.com.br/ | digitalização genérica | conteúdo e metadados permanecem muito próximos do modelo comum; preservar até definir papel próprio |
| ARQ-123 | https://mapeamento-juridico.arquindex.com.br/ | mapeamento jurídico | title/H1 citam mapeamento e jurídico, mas ainda usam texto-base amplo; melhoria específica já está preparada no commit `811c27f` |
| ARQ-124 | https://precos-empresas-digitalizacao-documental-pequenas-medias-empres.arquindex.com.br/ | preço para pequenas e médias empresas | title/H1 ainda repetem digitalização genérica em BH; sobreposição com outras URLs de preço permanece |

Achado comum: as seis páginas expõem `og:url=https://www.arquindex.com.br/index-seo.html`, divergente de suas canonicals próprias. O `og:image` aponta para `/assets/img/about.jpg`, enquanto auditorias públicas anteriores registraram referências relacionadas a `about.webp` com 404; validar o arquivo JPG separadamente antes de alterar.

## Decisão da rodada

- ARQ-119, ARQ-120 e ARQ-123: manter as melhorias preparadas, aguardando `BACKUP_COMPLETE_VERIFIED` e restauração isolada.
- ARQ-121, ARQ-122 e ARQ-124: não publicar mudanças; falta diferenciação comprovada ou há risco de sobreposição.
- Não incluir novas URLs em sitemap nem enviar ao Search Console/Bing/IndexNow.
- Não produzir divulgação social para páginas ainda não diferenciadas.
- Não alterar títulos diariamente antes da publicação planejada e de uma janela de medição.

## Infraestrutura e métricas

A auditoria técnica registrada no commit [9466704](https://github.com/arxazure/arquindex/commit/946670446b33a1b8f2af1b835603ef95cf2a5bde) confirmou 72 páginas regionais no Railway com HTTP 200/canonical/H1/viewport, mas conteúdo ainda fino/mecânico; elas continuam fora de sitemap e sem submissão. Essa auditoria pertence ao Railway e não deve ser usada como prova de publicação na HomeHost.

A leitura do Search Console está bloqueada por `subscription_required`; nenhuma nova posição, clique, impressão ou indexação é atribuída nesta rodada.

## Próximas prioridades

1. acompanhar o backup retomável até checkpoint terminal e registrar o caminho privado sem expor credenciais;
2. executar restauração isolada após `BACKUP_COMPLETE_VERIFIED`;
3. publicar ARQ-119/120/123 com backup individual, rollback e validação pública; corrigir `og:url` apenas junto da versão revisada.
