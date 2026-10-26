# Arquindex Capture Pro — metadados do Decreto 10.278/2020

**Status:** contrato de implementação e validação; NÃO conectado ao backend nem publicado em produção.

Fonte: Decreto nº 10.278/2020, Anexo II: https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10278.htm

## Dados mínimos (perfil comum)
| Chave API | Nome | Origem | Regra |
|---|---|---|---|
| assunto | Assunto | OCR/IA + operador | Palavras-chave revisadas, vocabulário por cliente |
| autor_nome | Autor (emissor) | OCR/IA + operador | Não confundir com operador; ausência exige pendência/exceção documentada |
| digitalizado_em | Data e hora de digitalização | Servidor/captura | ISO 8601 com offset de fuso; imutável após captura |
| local_digitalizacao | Local de digitalização | Unidade do projeto | Código de unidade + descrição de local |
| documento_digital_id | Identificador digital | Backend | UUID atribuído na captura, único, não reutilizável, imutável |
| responsavel_digitalizacao | Responsável | Projeto + autenticação | Pessoa jurídica/física responsável; guardar operador_id separadamente |
| titulo | Título | OCR/IA + operador | titulo_origem: formal ou atribuido |
| tipo_documental | Tipo documental | Catálogo por cliente | Código da espécie documental ligado ao processo, não MIME |
| hash_imagem | Hash (checksum) | Backend | SHA-256 dos bytes do artefato definido (preferencialmente imagem matriz), imutável e verificável |
| algoritmo_hash | Algoritmo | Backend | sha256; registrar escopo: matriz ou derivado |

## Dados adicionais condicionais
Obrigatórios **quando a digitalização for realizada por pessoa jurídica de direito público interno**:
- classe: código do plano de classificação aprovado;
- data_producao_original: registro de produção do original; campo específico de local_producao_original quando aplicável;
- destinacao_prevista: transferência, eliminação, recolhimento ou guarda permanente conforme tabela;
- genero: gênero documental padronizado;
- prazo_guarda: valor/unidade/marco de contagem segundo tabela de temporalidade.

## Outras evidências de processo (não substituem os metadados mínimos)
- cliente_id, projeto_id, unidade_id, lote_id, operador_id, estacao_id;
- original_formato, formato_saida, resolucao_dpi, modo_cor, quantidade_paginas, controles_de_qualidade;
- versao_do_modelo_ocr, valores_sugeridos, confianca, revisado_por, revisado_em, motivo_da_excecao;
- arquivo_matriz_id, arquivo_entrega_id, hash_matriz, hash_entrega, instante_calculo_hash;
- assinatura_digital, cadeia_de_certificados e resultado_de_verificacao quando exigidos pelo regime aplicável;
- eventos_append_only de captura, correção de metadados, validação, assinatura, entrega e reprocessamento.

## Regras de implementação
1. O tenant é obrigatório em cada consulta/escrita, incluindo catálogos, lotes e documentos.
2. Não confiar nos campos de identificação, captura, hash e operador fornecidos pelo navegador; gerar e validar no servidor.
3. Gravar documento em estados `capturado`, `indexacao_pendente`, `revisao`, `validado`, `assinado` (quando aplicável), `entregue`.
4. Não permitir finalização ou status 'conforme' com campos mínimos ausentes, exceções sem aprovação ou hash não verificado.
5. OCR/IA só sugere; o sistema conserva o valor original, a sugestão, a decisão do revisor e a versão do modelo.
6. Alterações posteriores criam nova versão com auditoria; nunca sobrescrever hashes ou identificadores da captura anterior.
7. Distinguir metadado do original (autor, data de produção) do metadado da captura (responsável, data de digitalização).
8. A assinatura ICP-Brasil e os parâmetros técnicos do Anexo I devem ser aplicados conforme tipo documental e hipótese legal; metadados e hash, isoladamente, não certificam equivalência jurídica.
9. Exportar metadados em JSON e CSV, preservando vínculo ao arquivo e identidade da versão; mapear propriedades compatíveis ao Alfresco ECM.
10. Proteger dados sensíveis de prontuários, aplicar menor privilégio, criptografia, retenção e logs sem conteúdo sensível.

## Critérios de aceite
- Captura cria UUID e timestamp imutáveis do servidor.
- Um arquivo alterado falha na verificação SHA-256.
- Documento sem tipo ou autor não pode ser finalizado sem tratamento de exceção aprovado pela governança.
- Cliente A não pode ler nem usar catálogos de cliente B.
- Perfil público exige os cinco campos adicionais; perfil privado não.
- Metadados por IA são sempre revisáveis, com trilha de decisão.
- Exportação retorna metadados mínimos, versão e hashes e preserva relações com artefatos.
- Testar com documento multipágina e separação por tipo sem mover página para documento seguinte.
