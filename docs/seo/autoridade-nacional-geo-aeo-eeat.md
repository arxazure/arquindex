# Arquindex | Protocolo Nacional de SEO, GEO, AEO e E-E-A-T
Data: 27/10/2026. Estado: proposta de implementação em branch; sem deploy.

## Ordem de execução e bloqueios
1. Antes de alterar o HomeHost, comprovar BACKUP_COMPLETE_VERIFIED e restauração isolada conforme docs/seo/rodada-20261027-manha-auditoria.md.
2. Corrigir primeiro HTTP 404 relevantes, canonical 4xx, robots e sitemap; cada URL apenas se houver página real, útil e publicada.
3. Executar `python3 scripts/seo_authority_preflight.py --out seo-report/authority-preflight.json`. O relatório é apenas de arquivos HTML locais; revisar manualmente os resultados.
4. Usar Search Console para desempenho real e cobertura do Google; não tratar posições da concorrência como dados próprios do GSC.
5. Reaproveitar `.github/workflows/indexnow-daily.yml` e `scripts/indexnow_daily.py`; não adicionar submissão concorrente. Cada host necessita DNS, HTTPS, sitemap e prova de chave na raiz; IndexNow não assegura indexação e não é API de indexação universal do Google.
6. Não criar subdomínios SEO sem propósito editorial próprio, documentação, responsáveis, DNS e conteúdo substancial que não duplique o site principal.

## Modelo obrigatório por página editorial
- Intenção de busca distinta, resumo-resposta direto, perguntas frequentes genuínas quando pertinentes.
- Evidências e fontes primárias (Google Search Central, Bing, CONARQ, ANPD, legislação); referências datadas e linkáveis.
- Autor real, cargo e revisão técnica aprovada; URL para perfil profissional apenas mediante validação.
- Datas de publicação/alteração verdadeiras, metodologia replicável, casos de uso reais autorizados.
- Title exclusivo, meta description, H1 único, URL canônica HTTPS única, links contextuais adequados e JSON-LD válido coerente com a página (Article, Organization, BreadcrumbList quando aplicável); não inventar avaliação/review nem usar FAQ schema como promessa de rich result.
- Páginas de serviços devem ter escopo, diferenciais verificáveis, regiões realmente atendidas e CTA claro; nenhuma alegação geográfica fictícia.
- Links cruzados seletivos entre dominios, não criar esquemas de link circular, âncoras exatas repetitivas nem páginas satélites.

## PR digital responsável
- Propor estudo de TCO documental (usuários, infraestrutura, suporte, implantação, retenção, governança) com planilha de fontes, amostra, metodologia, limitação e revisão. Não citar '40% de economia' sem cálculo comprovado.
- Oferecer dados verificáveis a imprensa setorial, sem comprar backlinks e sem garantir publicação em veículos de terceiros.
- Medir cobertura editorial confirmada e domínios de referência com ferramentas autorizadas, separando oportunidade, contato, publicação e link efetivo.

## Painel Top10 Google — métricas com proveniência
- GSC: cliques, impressões, CTR, posição média por consulta/página/período; registrar fuso e janela.
- GA4: visitas e conversões atribuídas, se autorizado.
- Bing Webmaster Tools: cobertura e consultas, se disponível.
- IndexNow: URL notificada e resposta HTTP, NÃO indexação garantida.
- SERP externo: Stoque/Arquivar somente via fonte, local, dispositivo e data reproduzíveis.
- Estados: observado / estimado / indisponível; não produzir nota Google 9.0 como métrica oficial.

## Critérios de aceite
- Workflow de auditoria gera relatório artifact e não modifica conteúdo.
- Revisão de duplicações, canonical, robots, sitemap e status HTTP por host antes de qualquer publicação.
- Revisão humana do E-E-A-T, dados estruturados testados e nenhuma autoria inventada.
- Sem merge e deploy automático desta branch.
