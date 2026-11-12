# Como aceitar um lote de OCR antes de importar dossiês de RH no ECM

Autoria: Equipe técnica Arquindex — revisão editorial a confirmar antes da publicação.
Atualizado em 04/11/2026. Estado: material preparado; publicação não confirmada.
Descrição: roteiro de conferência de PDFs pesquisáveis, páginas, nomes, índices e exceções antes da importação de dossiês de RH.
Intenção: aceite operacional do lote; complementar os guias existentes de OCR, sem substituir suas URLs.

Um lote de OCR está pronto para importação quando existe evidência de que seus arquivos correspondem aos documentos recebidos, mantêm a sequência correta, permitem recuperar informações relevantes e possuem índices conferidos. Abrir o PDF ou encontrar uma palavra isolada não demonstra tudo isso. O aceite precisa combinar conferência visual, testes de pesquisa, validação dos campos e registro das exceções, com responsáveis definidos.

Este artigo propõe um procedimento de qualidade para equipes de arquivo, RH e tecnologia. Os critérios de amostragem, tolerância e aprovação devem ser ajustados ao projeto antes da produção. Os exemplos são hipotéticos e não representam resultados medidos de clientes da Arquindex. O roteiro não estabelece prazo legal de guarda nem autoriza descarte de documentos físicos.

## 1. Comece por uma unidade de controle verificável

Defina o que será aceito: uma caixa, uma pasta, um dossiê ou um lote fechado. A unidade precisa ter identificação estável, relação de origem e quantidade esperada. Registre o recebimento, a preparação, a digitalização e a conferência sem depender exclusivamente do nome do operador. Cada etapa deve permitir localizar o documento e explicar quem realizou a ação.

Uma planilha de controle pode registrar identificador do lote, identificação física, intervalo de produção, número de arquivos, páginas contabilizadas, versão do processamento e estado de aprovação. Não transforme essa planilha em uma cópia indiscriminada de dados pessoais. Utilize identificadores internos e conceda acesso apenas às pessoas que precisam acompanhar a execução.

### Quando a contagem física é incompleta

Se o recebimento não informou páginas, registre essa lacuna. A contagem digital passa a ser um dado produzido pela operação, não uma confirmação independente da integralidade. A conferência deve comparar amostras com o acervo físico e registrar o alcance do teste. Não declare “todas as páginas conferidas” quando houve apenas amostragem.

## 2. Separe quatro perguntas que costumam ser confundidas

A primeira pergunta é se a imagem está legível. A segunda é se o texto foi reconhecido de maneira útil. A terceira é se o arquivo foi associado ao dossiê correto. A quarta é se o conjunto documental está completo. Cada pergunta exige evidência própria; melhorar o OCR não corrige automaticamente uma associação incorreta de paciente ou funcionário.

Considere um documento com nome semelhante ao do arquivo anterior. O texto pode estar perfeito, enquanto a separação pertence à pessoa errada. Em outra situação, o arquivo está no dossiê correto, mas uma página final ficou na pasta seguinte. Essas falhas são documentais e precisam aparecer no relatório de qualidade, mesmo quando o motor de reconhecimento termina sem erro.

## 3. Preserve uma referência antes de processar

Mantenha o conjunto recebido identificado e protegido durante a validação. Produza os derivados de trabalho em local controlado e relacione cada saída à sua origem. Quando o projeto exigir substituição de arquivos, faça essa substituição apenas depois da aprovação e com mecanismo de recuperação definido. Uma execução bem-sucedida do programa não equivale ao aceite documental.

Um identificador de integridade ajuda a verificar se determinado arquivo permaneceu igual entre duas transferências. Ele não demonstra sozinho que o conteúdo está correto, completo ou autorizado. Use esse recurso para comparar versões e rastrear movimentações, acompanhado dos demais controles. Registre também qual versão foi efetivamente entregue ou importada.

## 4. Confira orientação e sequência antes de avaliar o texto

Uma página girada, um verso invertido e uma folha inclinada são problemas diferentes. A documentação do OCRmyPDF distingue a correção da orientação em ângulos cardinais da correção de inclinação. Também recomenda revisão visual depois de certos tratamentos de imagem, porque o processamento pode alterar elementos relevantes. A escolha dos parâmetros deve ser testada em cópias representativas, não aplicada indiscriminadamente ao acervo.

No procedimento de aceite, examine páginas iniciais, centrais e finais do dossiê, além das ocorrências sinalizadas pelo operador. Verifique assinaturas, carimbos, margens, anexos e informações próximas das bordas. Um tratamento que torna o fundo mais limpo pode prejudicar uma anotação clara ou um carimbo fraco. O resultado precisa preservar a informação documental que motivou a captura.

### Atenção especial às páginas de transição

O ponto mais crítico pode ser a passagem entre duas pessoas ou tipos documentais. Compare a última página de um arquivo e a primeira do seguinte. Quando uma página não contém nome, a regra de associação precisa considerar a continuidade e a revisão humana prevista no projeto. Não use apenas semelhança textual para decidir a identidade.

## 5. Teste a pesquisa com termos escolhidos antes do processamento

Monte uma lista de consultas de referência com base em documentos conhecidos. Inclua identificadores internos, datas, títulos documentais e palavras que ajudem a localizar o conteúdo. Evite usar somente palavras comuns, presentes em quase todos os arquivos. O teste deve mostrar se o mecanismo recupera documentos relevantes e se a pessoa consegue reconhecer o resultado correto.

Registre consulta, arquivo esperado, página esperada, resultado encontrado e decisão do conferente. Para um projeto que indexa por campos, teste o campo separadamente do texto integral. Encontrar um nome dentro do PDF não prova que o metadado “nome do funcionário” foi preenchido corretamente. Do mesmo modo, pesquisar uma data não confirma que ela foi interpretada no formato certo.

## 6. Diferencie arquivo pesquisável de conformidade PDF/A

A presença de uma camada de texto e a conformidade com um perfil PDF/A são verificações diferentes. O veraPDF oferece validação de requisitos do formato por perfis específicos. Esse teste não substitui a comparação visual, a identificação da pessoa nem o exame da sequência. O relatório deve apresentar cada resultado separadamente, sem usar uma aprovação técnica como garantia de toda a qualidade documental.

Se houver exigência de PDF/A, estabeleça o perfil requerido, a ferramenta de validação e o tratamento dos arquivos reprovados. Não escolha um perfil apenas porque aparece como opção no software. Combine-o com o repositório de destino, os requisitos do projeto e as possibilidades de preservação. Registre qualquer transformação posterior, pois ela pode exigir nova validação.

## 7. Verifique os índices com regras por campo

Defina quais campos são obrigatórios e de onde cada um deve ser extraído. Nome pode vir de um rótulo explícito; data documental pode depender do tipo; código de cadastro pode exigir um padrão definido pelo cliente. Quando duas fontes divergem, encaminhe para conferência. Não substitua uma divergência por um valor presumido para fazer o lote parecer completo.

A validação deve distinguir campo ausente, campo ilegível e campo não aplicável. Esses estados têm consequências diferentes. Um documento sem data visível não deve receber automaticamente a data da digitalização como se fosse a data documental. Atribuições administrativas podem existir, mas precisam ser nomeadas corretamente e permanecer separadas dos valores extraídos do documento.

## 8. Organize exceções para que possam ser resolvidas

Uma fila de exceções útil informa qual arquivo precisa de revisão, qual regra falhou, qual evidência foi observada e quem pode decidir. Evite descrições genéricas como “OCR ruim” para problemas de identidade, paginação ou classificação. Categorias claras ajudam a separar o que exige nova captura do que exige ajuste de índice ou revisão documental.

Defina estados como pendente, em revisão, corrigido, aprovado e recusado, registrando a justificativa das mudanças. Se um modelo automático erra de maneira recorrente, suspenda seu uso no contexto afetado até que seja reavaliado. A aprovação de um lote não deve aprovar silenciosamente o modelo para outros clientes ou tipos documentais ainda não testados.

## 9. Faça um piloto de importação com retorno ao usuário

Antes da importação completa, selecione um conjunto representativo e execute o fluxo no destino de testes autorizado. Confirme pasta, tipo documental, campos, permissões, nomes e pesquisa. Peça que o usuário responsável localize documentos pelas consultas previstas. O aceite deve considerar a tarefa real: encontrar o documento certo dentro de um contexto reconhecível.

Inclua um teste com usuário que não tenha acesso ao dossiê. A interface precisa respeitar as permissões definidas no projeto, inclusive em pesquisas e visualizações. Esse teste deve usar documentos sintéticos ou um conjunto autorizado. Não distribua cópias de RH para ampliar informalmente a validação, nem exponha informações pessoais em capturas usadas para relatórios comerciais.

## 10. Registre o aceite e os limites da conferência

O termo de aceite deve informar lote, versão, período de produção, quantidade verificada, método utilizado, exceções abertas e responsável pela decisão. Se a aprovação for parcial, indique exatamente quais arquivos foram liberados. Não mova o lote inteiro para “concluído” quando uma parte permanece sem decisão. Isso evita que importação, faturamento e entrega utilizem números diferentes.

As métricas devem refletir o trabalho efetivamente realizado. Quantidade recebida, digitalizada, processada, conferida e aprovada não são sinônimos. Uma mesma página não deve ser contada novamente como produção nova quando passa por correção. Mostre retrabalho separadamente para identificar causas e dimensionar esforço sem inflar o progresso do contrato.

## Checklist de liberação

- Lote e origem física identificados, com contagem e limitações registradas.
- Sequência, páginas finais e transições entre dossiês conferidas pelo método acordado.
- Legibilidade, orientação e elementos documentais preservados.
- Consultas de referência executadas e resultados registrados.
- Índices obrigatórios validados por campo e divergências encaminhadas.
- Perfil PDF/A validado quando exigido, sem confundir formato com conteúdo.
- Permissões e importação piloto verificadas no destino autorizado.
- Exceções abertas relacionadas ao aceite parcial e aos responsáveis.
- Versão aprovada e forma de recuperação identificadas.
- Aprovação documental registrada antes da liberação definitiva.

## Perguntas frequentes

### Posso aprovar um lote apenas porque o programa terminou?
Não. O término técnico informa que uma execução chegou ao fim, mas o aceite depende dos critérios documentais do projeto. Confira também os avisos, arquivos ignorados e exceções.

### Preciso usar o mesmo limiar de OCR em todos os documentos?
O projeto deve testar critérios por classe documental e qualidade de origem. Uma regra útil para formulários impressos pode falhar em manuscritos, carimbos e cópias degradadas.

### Uma página sem nome pode ser excluída automaticamente?
Não por esse motivo. Ela pode ser continuação legítima. A associação e eventual exclusão precisam seguir regras aprovadas e mecanismos de revisão previstos para o lote.

### O PDF/A autoriza eliminar o documento físico?
Este roteiro não fornece autorização de descarte. A destinação exige avaliação dos requisitos aplicáveis e decisão documental própria, além dos controles de digitalização.

## Planeje o aceite com a Arquindex

A Arquindex organiza fluxos de digitalização, conferência, indexação e integração documental para projetos de RH e arquivos empresariais. O escopo deve definir volumes, tipos, campos, exceções, segurança e responsáveis antes da produção.

Consulte [gestão de dossiês de colaboradores](https://www.arquindex.com.br/gestao_de_colaboradores_documentos.html) e [guarda de documentos](https://www.arquindex.com.br/guarda_de_documentos.html). Atendimento: [WhatsApp (31) 97363-2725](https://wa.me/5531973632725), comercial@arquindex.com.br.

## Fontes e método

Fontes consultadas em 04/11/2026: [OCRmyPDF — Cookbook](https://ocrmypdf.readthedocs.io/en/latest/cookbook.html), [Tesseract — Improve Quality](https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html) e [veraPDF — Validation](https://docs.verapdf.org/validation/). Os itens de aceite, organização da fila e testes de usuário são recomendações operacionais deste artigo, não exigências atribuídas a essas ferramentas. Não foram utilizados dados pessoais ou resultados de clientes.
