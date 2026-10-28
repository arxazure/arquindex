# Revisão de segurança editorial — identidade Arquindex (28/10/2026)

## Achado no script reutilizável
Arquivo: `scripts/padronizar-identidade-arquindex.py`. A constante `FOOTER` inclui a afirmação "Sede em Belo Horizonte. Unidades em São Paulo e Lisboa." Não há, nas evidências desta rodada, comprovação de unidades físicas operacionais nessas duas cidades. Não reutilizar esta frase automaticamente nas 238 páginas ou 56 subdomínios sem comprovação comercial/jurídica. Substituir, após aprovação, por texto institucional comprovado ("Atendimento a projetos conforme escopo e disponibilidade contratual"), sem alegar filiais.

O mesmo rodapé inclui link para Railway; validar HTTP 200, canonical e conteúdo antes de tratá-lo como site corporativo ativo. O link para mapa de plataformas deve ser auditado antes de ampliar interlinking. Validar URLs de menu e imagem do logo, e evitar inserção duplicada de cabeçalho/rodapé e widget WhatsApp.

## Protocolo de patch mínimo para ARQ-133
URL: https://ecm.arquindex.com.br/custo.html
- Alterar apenas canonical para URL própria **se** a URL final permanecer 200, indexável e não redirecionar.
- Title único proposto: `Quanto custa GED e ECM? Fatores de preço | Arquindex`.
- Não alterar H1, menu, logo, CTA, scripts de medição nem preço sem revisão da oferta.
- Verificar uma canonical, um title, um H1, links internos e versão mobile. Registrar diff e hash antes/depois.

## Protocolo de patch mínimo para ARQ-141
URL: https://digitacao-de-documentos.arquindex.com.br/
- Corrigir canonical indevida com /output/.../index.html somente se a raiz for a URL indexável oficial e permanecer 200.
- Title proposto, **condicional à confirmação do serviço**: `Digitação de documentos: escopo e orçamento | Arquindex`.
- Não afirmar equivalência entre digitação manual e digitalização certificada.
- Identidade/CTA/formulário exigem revisão individual de layout, não injeção em lote.

## Critérios para links
Inserir 1–3 links contextuais em cada página somente para serviços com destino público verificado (200, canonical coerente, conteúdo próprio). Priorizar jornadas digitalização → OCR → guarda/GED e LGPD → DPO; não adicionar backlinks artificiais entre domínios próprios nem repetir âncoras em escala.

## Estado
Revisão de código/documentação; nenhuma alteração pública, FTP, sitemap, indexação, post ou alegação de conversão. Backup HomeHost checkpoint 45 ainda parcial. Próximo passo: preparar patch testado em staging e registrar validações antes de publicação.
