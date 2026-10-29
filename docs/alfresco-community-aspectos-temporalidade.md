# Manual técnico: aspectos e temporalidade no Alfresco Community

ARQUINDEX | Guia de configuração e preenchimento | 29/10/2026

Escopo: Alfresco Community com Share e Model Manager. Configuração sem instalar AMPs. Os nomes internos abaixo são exemplos para modelo novo; a instalação existente deve preservar seus QNames e aspectos.

## O que pode ser feito sem AMP

No Alfresco Community com Share e Model Manager disponíveis, é possível criar modelos, aspectos e propriedades pela administração, definir formulários e aplicar aspectos aos documentos. Regras de pasta podem executar scripts JavaScript do repositório. Isso utiliza pontos de configuração existentes, mas exige modelagem e homologação: os 16 campos não vêm prontos como uma tabela de temporalidade brasileira.

## 1. Preparar o modelo

Em homologação, entre no Share com usuário autorizado no grupo ALFRESCO_MODEL_ADMINISTRATORS. Acesse Admin Tools > Model Manager (Ferramentas administrativas > Gerenciador de modelos). Exporte o modelo existente antes de alterar. Se o documento já usa smsdp, consulte seus QNames e não crie outro modelo com o mesmo prefixo. Neste manual, arqdoc é apenas um namespace ilustrativo, sem equivalência automática ao ambiente do cliente.

## 2. Criar o aspecto e as propriedades

Selecione Create Model e informe nome, URI de namespace e prefixo únicos. Exemplo: modelo temporalidade, URI https://www.arquindex.com.br/model/documental/1.0 e prefixo arqdoc. Crie o aspecto arqdoc:controleDocumental. Em cada propriedade, informe nome interno, rótulo e tipo da tabela. Use listas de valores quando o catálogo estiver aprovado. Evite campos obrigatórios sem permitir o estado de triagem; datas desconhecidas devem continuar vazias.

## 3. Exibir os campos e aplicar ao documento

No aspecto, abra Actions > Layout Designer. Organize classificação, datas e prazos, destinação e bloqueio em grupos. Inclua as propriedades no formulário e salve o layout; ative o modelo conforme a interface da versão. Na biblioteca, abra o documento e a ação Manage Aspects/Gerenciar aspectos, aplique o aspecto e depois Edit Properties/Editar propriedades. Preserve aspectos anteriores. Os rótulos e a disponibilidade das ações variam com versão, tradução, configuração e permissões.

## Dicionário dos campos da tela

### Tipo documental

Proposta: arqdoc:tipoDocumental | d:text — Selecione no catálogo aprovado; NAO_CLASSIFICADO até conferência.

### Código documental

Proposta: arqdoc:codigo | d:text — Código da série no plano de classificação; preserve zeros e pontos.

### Sigla

Proposta: arqdoc:sigla | d:text — Abreviatura institucional validada, sem dedução automática.

### Data do documento

Proposta: arqdoc:dataDocumento | d:date — Data constante do documento, distinta da data de upload.

### Evento de temporalidade

Proposta: arqdoc:evento | d:text — Fato que inicia a contagem, definido pela tabela aprovada.

### Data do evento

Proposta: arqdoc:dataEvento | d:date — Preencher somente com evento confirmado e evidência.

### Fase corrente

Proposta: arqdoc:faseCorrente | d:text — Regra ou duração de uso corrente, com unidade expressa.

### Fase intermediária

Proposta: arqdoc:faseIntermediaria | d:text — Regra ou duração da guarda intermediária; evitar dupla contagem.

### Prazo em anos

Proposta: arqdoc:prazoAnos | d:int — Duração definida na tabela; não confundir zero, vazio e permanente.

### Vencimento

Proposta: arqdoc:vencimento | d:date — Data calculada após validar evento e regra; vazio enquanto faltar base.

### Situação

Proposta: arqdoc:situacao | d:text — Ex.: NAO_CLASSIFICADO, PRAZO_A_VALIDAR, AGUARDANDO_EVENTO, EM_GUARDA, EM_AVALIACAO, BLOQUEADO.

### Destinação

Proposta: arqdoc:destinacao | d:text — Eliminação após avaliação, recolhimento ou guarda permanente conforme tabela.

### Fundamentação

Proposta: arqdoc:fundamentacao | d:text — Referência normativa e versão da tabela, aprovadas pela área responsável.

### Bloqueio legal

Proposta: arqdoc:bloqueioLegal | d:boolean — Indicador de impedimento; campo isolado não impede exclusão.

### Motivo do bloqueio

Proposta: arqdoc:motivoBloqueio | d:text — Justificativa, referência e responsável; acesso restrito quando necessário.

### Fonte da classificação

Proposta: arqdoc:fonteClassificacao | d:text — Tabela e versão, classificação manual ou sugestão de IA com revisão.

## 4. Configurar a regra de pasta

Na pasta piloto, abra Manage Rules/Gerenciar regras e Create Rule/Criar regra. Escolha entrada de itens e condição que limite o processamento aos documentos desejados. Utilize a ação de aplicação de aspecto se exposta nessa versão ou Execute script/Executar script. O script, revisado por administrador, fica em Data Dictionary/Scripts. Habilite subpastas somente para a árvore prevista. Para documentos existentes, execute a regra em lote piloto; criar uma regra não comprova atualização retroativa do acervo.

## 5. Definir a lógica de temporalidade

A regra deve consultar código e versão da tabela, validar classificação, verificar bloqueio e confirmar o evento disparador. Sem regra aprovada: PRAZO_A_VALIDAR. Sem data de evento: AGUARDANDO_EVENTO, sem vencimento. Com evento e duração válidos: calcular por anos de calendário e registrar a data. Especifique a convenção para 29 de fevereiro, feriados quando aplicáveis e fuso. Defina se prazoAnos é total ou de uma fase; não some novamente fases já contidas nele. Guarda permanente não deve receber uma data artificial de descarte.

## 6. Revisar o passar do tempo

Uma regra disparada por upload ou alteração não executa apenas porque um aniversário ocorreu. A revisão de vencimentos precisa de rotina periódica explicitamente configurada, relatório revisado ou integração autorizada. A consulta deve considerar permissões e atraso de indexação. Faça leitura atualizada do documento antes da decisão. Alterações de evento ou de tabela exigem recálculo controlado e registro do valor anterior.

## 7. Tratar bloqueio e destinação

Um booleano chamado bloqueioLegal é informativo até que controles de permissão e todos os caminhos de exclusão o respeitem. Operadores, integrações, API, administradores e lixeira precisam fazer parte da avaliação. Não chame esse campo de legal hold nativo equivalente ao Governance Services. O vencimento encaminha o documento à avaliação; não autoriza eliminação automática. Documente aprovação, obrigação aplicável e cadeia de custódia antes de qualquer destinação.

## Exemplo operacional sem prazo universal

Um contrato recebe tipo e código do catálogo aprovado. O evento é encerramento do contrato. Enquanto a data não estiver confirmada, a situação é AGUARDANDO_EVENTO e o vencimento fica vazio. Depois da confirmação, um prazo hipotético de cinco anos só pode ser usado em teste e deve ser substituído pelo prazo aprovado da série. O cálculo utiliza a data do evento; a data do upload não a substitui. Este exemplo não define prazo legal para contratos nem para documentos de pessoal.

## Conferência e aceite

Teste: classificação ausente; regra sem prazo; evento ainda não ocorrido; data válida; ano bissexto; guarda permanente; bloqueio ativo; reaplicação sem mudanças; correção da data; alteração da tabela; documento em subpasta; aspectos anteriores; leitor sem permissão; integração por API; restauração de backup. A repetição do processo não deve apagar metadados existentes, criar versões desnecessárias ou disparar regras em ciclo. Guarde evidências de antes e depois e valide um lote pequeno antes da expansão.

## Falhas comuns e correção

Campo não aparece: confirme layout, modelo ativo, aspecto aplicado e permissão. Campo aparece vazio: aspecto aplicado não significa classificação preenchida; confira os QNames reais. PRAZO_A_VALIDAR: verifique correspondência do código e versão da tabela. Evento em branco: mantenha vencimento vazio. Pasta com aspecto: não presume que documentos herdaram os campos. Erro no script: interrompa o lote, preserve originais e revise o log sem expor dados pessoais.

## Referência visual fornecida

## Fontes oficiais

Criar modelo — Community 26.1
https://docs.hyland.com/r/Alfresco/Alfresco-Content-Services-Community-Edition/26.1/Alfresco-Content-Services-Community-Edition/Configure/Content-models/Create-a-content-model

Layout Designer — Community 23.3
https://hyland.fluidtopics.net/r/Alfresco/Alfresco-Content-Services-Community-Edition/23.3/Alfresco-Content-Services-Community-Edition/Configure/Content-models/Layout-Designer/Properties-in-the-Layout-Designer/Using-the-Layout-Designer

Ações de regras — Community 23.3
https://docs.hyland.com/r/Alfresco/Alfresco-Content-Services-Community-Edition/23.3/Alfresco-Content-Services-Community-Edition/Using/Content/Folder-rules/Defining-rules-for-a-folder/Rule-actions
