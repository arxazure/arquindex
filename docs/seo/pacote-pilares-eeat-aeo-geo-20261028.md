# Pacote editorial E-E-A-T, SEO e AEO/GEO — páginas pilares Arquindex
**Estado:** pronto para revisão editorial e implantação controlada; **não publicado**. Atualização: 28/10/2026.

## Regras de publicação
- Inserir seções dentro do conteúdo principal, preservando o H1, canonical, navegação, identidade visual, responsividade e CTAs existentes.
- Não afirmar credenciamento, certificação, autoria individual, cliente atendido ou tempo de experiência sem evidência. Informar data de atualização real, responsável editorial validado e fontes primárias por seção.
- Não publicar FAQPage com perguntas/respostas que não estejam visíveis no HTML; não usar marcação de avaliação fictícia. Não prometer que schema ou blocos de IA geram indexação.
- Não criar páginas por cidade com conteúdo intercambiável; preferir página pilar + exemplos de escopo local comprovado.
- Reutilizar links internos somente após verificar status 200, destino final e canonical.

## Pilar 1 — Digitalização de documentos
**Intenção:** contratação empresarial, segurança, qualidade, orçamento e conformidade.
**Title sugerido:** Digitalização de documentos para empresas | Arquindex
**Descrição:** Digitalização empresarial com organização, OCR, controle de qualidade e rastreabilidade. Entenda etapas, entregáveis e como solicitar uma proposta.
**Resumo objetivo para mecanismos de resposta (visível):**
> A digitalização empresarial transforma documentos físicos em arquivos digitais pesquisáveis, com preparação, captura, conferência e indexação. O escopo pode incluir OCR, PDF/A, classificação e gestão de acesso. A adequação ao Decreto 10.278/2020 depende dos requisitos técnicos e legais aplicáveis a cada documento e processo; a digitalização, por si só, não garante equivalência jurídica.
**Seções a inserir após validar oferta:** escopo/entrada; preparação e captura; resolução e legibilidade; OCR e suas limitações; indexação e metadados; cadeia de custódia e auditoria; entregáveis e critérios de aceite; orçamento por volume/complexidade; limites e casos em que preservar original; FAQ.
**Perguntas visíveis:** Qual a diferença entre escanear e digitalizar com rastreabilidade? O OCR substitui a conferência humana? Quando preservar originais? Quais dados são necessários para cotação?
**Evidências necessárias:** amostra de checklist de qualidade anonimizada, exemplo de índice de entrega e descrição de equipamentos/processo confirmados.
**Links contextuais candidatos:** OCR, guarda física, GED/ECM, consultoria LGPD; validar destinos antes de aplicar.

## Pilar 2 — Guarda e custódia física
**Title:** Guarda de documentos empresariais e custódia | Arquindex
**Resumo visível:** Guarda documental envolve identificação, acondicionamento, localização, controle de movimentações, acesso autorizado e destinação conforme prazos de retenção e obrigações aplicáveis. Não significa descarte automático ao fim de um prazo genérico.
**Seções:** inventário de caixas; cadastro e rastreabilidade; solicitações de consulta; segurança física; retenção/temporalidade; logística; relatórios; SLA contratado; destinação com autorização; integração com GED.
**Perguntas:** Como localizar uma caixa? Quem pode solicitar retirada? Como definir prazo de guarda? Quando digitalizar antes de eliminar?
**Evidências:** modelo de inventário anonimizado, fluxograma de solicitação e cláusulas SLA validadas.

## Pilar 3 — GED / ECM Alfresco
**Title:** GED e ECM com Alfresco: implantação e operação | Arquindex
**Resumo visível:** GED/ECM centraliza documentos, metadados, permissões, pesquisa e fluxos de trabalho. Em implantação Alfresco, arquitetura, licença, integrações, backup, retenção e custos dependem da edição, versão, infraestrutura e requisitos contratados; software de código aberto não equivale a operação sem custo.
**Seções:** diagnóstico e requisitos; arquitetura cloud/on-premises; acesso e papéis; captura/OCR; workflows; versionamento; retenção; backup e restauração; integrações; implantação e sustentação; critérios de aceite.
**Perguntas:** Qual a diferença entre GED e ECM? Alfresco é gratuito? Como funciona o backup? Como integrar com SharePoint/Nextcloud?
**Evidências:** diagrama de arquitetura revisado, matriz de responsabilidades e exemplo de SLA.

## Pilar 4 — Consultoria LGPD
**Title:** Consultoria LGPD e governança de dados | Arquindex
**Resumo visível:** Adequação à LGPD envolve mapear tratamentos, identificar bases legais, avaliar riscos, definir controles e responsabilidades, preparar políticas e implementar monitoramento. Documentos-modelo não garantem conformidade; as decisões dependem do contexto e de análise jurídica quando aplicável.
**Seções:** diagnóstico; inventário/ROPA; bases legais; riscos e RIPD quando cabível; direitos de titulares; fornecedores; segurança; incidentes; treinamento; DPO; acompanhamento.
**Perguntas:** Toda empresa precisa de DPO? O que é ROPA? Quando elaborar RIPD? Quanto tempo leva um projeto?
**Evidências:** entregáveis anonimizados, metodologia, credenciais verificáveis de responsáveis e política editorial.

## Pilar 5 — OCR e documentos pesquisáveis
**Title:** OCR de documentos e PDFs pesquisáveis | Arquindex
**Resumo visível:** OCR identifica caracteres em imagens e permite pesquisa textual, mas pode errar números, nomes, tabelas e manuscritos. Qualidade da captura, idioma, tipografia e conferência determinam a confiabilidade. OCR não substitui revisão quando a precisão é crítica.
**Seções:** preparação; resolução; pré-processamento; OCR; pós-correção; amostragem; taxa de erro e critérios de aceite; PDF pesquisável; acessibilidade; tratamento seguro.
**Evidências:** comparação de amostras anonimizadas e critérios de teste.

## Estrutura de bloco AEO reutilizável (HTML visível)
```html
<section class="aq-resposta-direta" aria-labelledby="aq-resposta-titulo">
  <h2 id="aq-resposta-titulo">Como funciona o serviço?</h2>
  <p><!-- resposta objetiva, específica e revisada por responsável técnico --></p>
  <h3>Etapas e entregáveis</h3>
  <ol><li>Diagnóstico e definição de escopo</li><li>Execução com controles de qualidade</li><li>Conferência, aceite e entrega documentada</li></ol>
  <p class="aq-atualizacao">Revisado em <!-- data real --> por <!-- responsável validado -->.</p>
</section>
```
**Atenção:** esse bloco é um modelo editorial. O texto de cada página precisa refletir o serviço efetivamente ofertado, sem promessas universais.

## JSON-LD mínimo, após conferir identidade e URL final
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Digitalização de documentos empresariais",
  "serviceType": "Digitalização de documentos",
  "provider": {
    "@type": "Organization",
    "name": "Arquindex",
    "url": "https://www.arquindex.com.br/"
  },
  "description": "Preparação, captura, conferência e indexação de documentos, conforme escopo contratado."
}
</script>
```
Não duplicar JSON-LD existente nem inventar `aggregateRating`, `review`, `award` ou `sameAs`. URL e entidades devem ser coerentes com a página pública. FAQPage apenas se apropriado e com conteúdo visível, sem expectativa de rich result.

## Checklist de QA e mensuração
1. HTTP 200; HTTPS; canonical única e coerente; title e H1 únicos; indexabilidade; sitemap somente para URL canônica publicada.
2. Layout igual ao institucional, logo carregado, sem overflow mobile e com um único widget de WhatsApp.
3. Texto original, fontes oficiais ligadas a alegações regulatórias, autor/revisor comprovado, data de atualização verdadeira, links internos 200.
4. Eventos GA4 de clique no WhatsApp, formulário enviado e lead qualificado sem contagem duplicada; respeitar consentimento e privacidade.
5. Comparar semanalmente GSC por URL/consulta (cliques, impressões, CTR e posição), não atribuir ganhos antes de medição.
