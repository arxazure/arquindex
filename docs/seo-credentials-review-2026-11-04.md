# Proposta de correção — aguardando aprovação

Base: master a32bbb9b193203218107b73e814f25864abad9a1. Preparação local; nenhum push, alteração de Secret, chamada autenticada de SEO, publicação ou pedido de indexação foi executado.

## Evidências

- Wix 41688064089: GOOGLE_API_KEY, GOOGLE_CX_ID, OPENAI_API_KEY e WIX_API_KEY vazios; Google respondeu 403. Upload executou, mas nenhum arquivo foi encontrado. A API de artefatos retorna lista vazia.
- GSC 41689452055: testes passaram; coleta falhou com GSC_NOT_CONFIGURED (GSC_CLIENT_ID, GSC_CLIENT_SECRET, GSC_REFRESH_TOKEN); commit foi pulado.
- Nenhuma execução posterior dessas duas rotinas aparece entre as 100 execuções mais recentes consultadas. Esse histórico alcança 02/11 e inclui execuções de 04/11 UTC.
- GSC 41419675229 em 02/11 foi sucesso apenas nos testes: job collect foi skipped por evento push. Não comprova dados reais.
- Não foi possível auditar a existência, escopo ou validade atuais dos Secrets: o conector não expõe endpoints de Secrets. Vazio no runner pode decorrer de ausência, escopo ou regras de acesso.

## Correções locais

- Wix: preflight condicional, rejeitando espaços em branco; diagnósticos apenas com nomes de variáveis, etapa, tipo de erro e HTTP, sem texto de exceções que possa conter chave em URL.
- Pesquisa Google salva antes de chamar OpenAI; rascunho local salvo antes de criar rascunho Wix; gravação atômica. Cache entre execuções e upload mesmo em falha. Cache/artifacts têm retenção finita: não são backup permanente.
- Resultado diário existente não é sobrescrito nem reenviado ao Wix. Uma falha ambígua na criação Wix exige reconciliação manual; não se repete automaticamente.
- OpenAI: uma tentativa sem retries automáticos, timeout de 60 segundos, máximo de 2.000 tokens de conclusão; modelo existente gpt-4o-mini. A chamada continua tendo custo potencial.
- GSC: mantém preflight e escrita atômica existentes; rejeita credenciais em branco; distingue OAuth, listagem, leitura, configuração e resposta vazia. Resposta vazia preserva arquivo anterior e falha, exigindo revisão do período.
- Workflow GSC anexa diagnóstico e arquivo existente, inclusive em falha. O arquivo anterior não deve ser tratado como coleta nova: consultar generated_at e status.json.
- Workflows serializam execuções por plataforma; Wix usa contents: read. GSC mantém commit de dados somente após coleta bem-sucedida.
- Não há endpoint de publicação ou indexação na rotina Wix. Criar draft não publica.

## Configuração segura a conferir após autorização

| Plataforma/etapa | GitHub Actions Secrets necessários | Observação |
|---|---|---|
| Google pesquisa | GOOGLE_API_KEY, GOOGLE_CX_ID | API habilitada, motor cx válido, restrições compatíveis e projeto elegível para Custom Search |
| OpenAI geração | OPENAI_API_KEY | Projeto com acesso ao modelo e orçamento definido |
| Wix draft opcional | WIX_API_KEY, WIX_SITE_ID | Permissão mínima de criação de rascunhos no site Arquindex correto; não usar client ID headless como site ID |
| Search Console coleta | GSC_CLIENT_ID, GSC_CLIENT_SECRET, GSC_REFRESH_TOKEN | Mesmo cliente OAuth; autorização offline e escopo webmasters.readonly; usuário com acesso à propriedade Arquindex |

WIX_CREATE_DRAFT é controle de execução, não credencial. WIX_SITE_ID e GOOGLE_CX_ID são identificadores, mas os workflows atuais os leem de Secrets. Não enviar valores em chat, código, logs ou artefatos. Configurar no GitHub Settings → Secrets and variables → Actions. Um conector Google/Wix conectado no chat não injeta credenciais no runner.

## Validação e aprovação pendente

10 testes offline passaram: seis GSC e quatro Wix. Dados simulados usados apenas em testes; não constituem evidência real de APIs.

Solicitar aprovação para aplicar o diff ao GitHub e executar uma validação controlada: uma pesquisa Google, uma geração OpenAI (até 2.000 tokens de saída) e uma coleta GSC. Criação de um rascunho Wix é aprovação separada; publicação e indexação ficam excluídas. Nenhuma alteração de credenciais sem autorização específica e canal seguro disponível. Após configuração, verificar conteúdo dos artefatos, datas, fontes e IDs, e não apenas conclusão verde do workflow.
