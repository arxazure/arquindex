# Plano de otimização por URL real — Arquindex (revisão editorial)
Data da coleta: 30/10/2026. Fonte: GSC Wizard, propriedade https://www.arquindex.com.br/, período 30/09 a 27/10/2026.

## 1) Página inicial https://www.arquindex.com.br/
Consulta: "serviço de digitalização de documentos" — 69 impressões, 1 clique, posição média 24,55 na combinação consulta+URL.
**Teste proposto**, sem sobrescrever a home atual:
- Posicionar no primeiro bloco uma apresentação clara dos serviços B2B de digitalização, OCR e indexação, com link para uma landing page transacional canônica.
- CTA: "Solicitar orçamento de digitalização empresarial".
- Explicar preparação, captura, conferência, organização e entrega; não declarar conformidade certificada sem documentação do processo.
- Links contextuais para soluções Alfresco ECM, LGPD e gestão documental.
- Conferir título, description, H1, canonical e links antes da mudança. Não usar a home para capturar todas as buscas setoriais.

Consulta: "digitalização de documentos" — 28 impressões, 1 clique, posição média 2,61 **somente nesta combinação consulta+URL**. Preservar esse desempenho e evitar mudança brusca de arquitetura.

## 2) Landing existente https://www.arquindex.com.br/adequacao-lgpd-para-empresas.html
Consulta: "adequação lgpd empresas" — 4 impressões, 0 cliques, posição média 10,75.
- H1 proposto (revisão): "Adequação à LGPD para empresas: diagnóstico, ROPA, RIPD e DPO".
- Responder a dúvidas de decisão B2B: quais entregáveis, fases, papéis internos, prazos dependentes do escopo e acompanhamento.
- Vincular fontes oficiais ANPD e Lei 13.709/2018; apontar responsável técnico e data de revisão.
- Manter termos de serviço precisos; não prometer conformidade garantida ou atestado estatal inexistente.
- Inserir JSON-LD Service somente se corresponder ao conteúdo efetivo.

## 3) Sobreposição de subdomínios
"assessoria lgpd" apareceu em múltiplos hosts e URLs, normalmente com poucas impressões por combinação.
Antes de 301/canonical/noindex:
- Auditar cada endereço e identificar o ambiente que publica o conteúdo.
- Comparar texto e intenção de busca; verificar GSC por host, acessos e backlinks.
- Definir somente uma URL principal por intenção quando houver duplicação real.
- Preparar tabela antiga->nova e backup; nunca redirecionar todos os subdomínios para a homepage.

## Qualidade e E-E-A-T
Conteúdo útil: método, fluxos, exemplos reais autorizados, autoria/revisão e fontes. E-E-A-T não é um campo Schema.org específico nem uma nota oficial do Google.
GEO/AEO: resumos factuais diretos e parágrafos respondendo dúvidas comuns dos compradores, sem blocos ocultos para robôs.
Blog/noticiário: comentar publicações verificadas de ANPD, Google Search Central e projetos open source relacionados, distinguindo notícia de opinião técnica.

## Critérios antes do deploy
[ ] Backup do site e versão atual.
[ ] URL HTTP 200 verificada no host correto.
[ ] Nenhum título/canonical substituído sem revisão.
[ ] Dados estruturados consistentes com o conteúdo visível.
[ ] Testes GitHub Actions aprovados.
[ ] Teste de staging, posterior publicação e GSC monitorado 14–28 dias.
