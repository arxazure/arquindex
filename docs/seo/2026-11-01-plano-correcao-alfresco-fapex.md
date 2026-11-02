# Plano de recuperação SEO - 2026-11-01

## Evidências
- `/empresa.html`: HTTP 404 na auditoria GSC Wizard.
- `/blog/alfresco-cloud-ocr-inteligencia-documental/`: HTTP 404 na auditoria GSC Wizard.
- Arquivo-fonte HTML do artigo já existe no repositório em `campanhas/oportunidades-20261021/blog/alfresco-cloud-ocr-inteligencia-documental/index.html`. Ainda não foi confirmada a inclusão dessa pasta no artefato efetivamente servido no Railway.
- `/solucoes/digitalizacao-documentos`: HTTP 200 e canonical coerente.
- Sitemap `https://www.arquindex.com.br/sitemap-alfresco-cloud-20261021.xml`: GSC registra 16 URLs, um erro e processamento pendente; XML não foi obtido via consulta anterior.
- `seo-rotinas/publicar-sitemap-alfresco-llm-20261024.py` usa FTPS e IndexNow e **não deve ser executado** antes de validação do ambiente, pois altera arquivos remotos e envia notificações.

## Procedimento seguro de implantação pendente
1. Identificar serviço Railway/Cloudflare efetivamente responsável pelas rotas públicas e commit de deploy, sem presumir que este repositório publica automaticamente.
2. Confirmar a versão de produção do artigo e seu direito de publicação, além de validar autor e conteúdo técnico.
3. Mapear `/empresa.html` para conteúdo institucional equivalente comprovado ou restaurar conteúdo original.
4. Implantar em homologação rotas para o artigo e empresa; conferir respostas HTTP, canonical, dados estruturados e links.
5. Executar `python3 scripts/seo_alfresco_preflight.py` em homologação e inspecionar relatório JSON. Ele faz somente GET HTTP, não publica.
6. Para o sitemap, obter o XML existente, validar lista real de 16 URLs e **excluir páginas 404** antes de disponibilizar nova versão por pipeline identificado.
7. Preparar rollback com commit e artefato anterior, aprovar janela de alteração e somente depois publicar em produção.
8. Depois de confirmado HTTP 200 no servidor de produção, revisar sitemaps e solicitar reprocessamento por procedimento separado e explicitamente autorizado.

## FAPEX e estudo GED
Usar Seleção Pública 053/2026 apenas como referência de contratação integrada. Custos de conservação, restauração, descrição, digitalização, GED, treinamento e manutenção devem ser segregados. Não dividir R$ 1.314.000 por 900.000 para alegar preço de digitalização. Evitar afirmar economia percentual ou vantagem frente a concorrentes sem comparáveis auditados.

## Critérios de aceite
- Artigo e página institucional respondem 200 ou 301 para equivalente validado.
- Sitemap 200 e XML bem formado; cada URL tem resultado de validação individual; URLs elegíveis 200 e canonical coerente.
- Marcação Organization usa URL verdadeira de logo, comprovadamente acessível.
- Títulos, autoria técnica e fontes do estudo revisados por responsáveis reais.
- Nenhuma submissão de sitemap ou postagem ocorre automaticamente nesta branch.
