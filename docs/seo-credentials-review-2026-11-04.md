# Correção SEO — validação autorizada e bloqueada por configuração

Base inicial: master a32bbb9b193203218107b73e814f25864abad9a1. A usuária autorizou a continuidade após revisar a proposta. Alterações aplicadas à branch ops/seo-credentials-validation-20261104 e submetidas no PR #109. Nenhuma alteração de Secret, publicação ou pedido de indexação foi executado.

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

## Validação realizada e impedimentos atuais

10 testes offline passaram: seis GSC e quatro Wix. Dados simulados usados apenas em testes; não constituem evidência real de APIs.

Execução autorizada: https://github.com/arxazure/arquindex/actions/runs/41767131159, iniciada em 04/11/2026 às 00:26 no fuso America/Sao_Paulo.

- Job tests passou nos 10 testes da versão 838b213a42fb5c578d831abc9b91529440a9b80f.
- Wix bloqueou antes de qualquer API com SEO_NOT_CONFIGURED: GOOGLE_API_KEY, GOOGLE_CX_ID, OPENAI_API_KEY, WIX_API_KEY, WIX_SITE_ID ausentes no runner.
- GSC bloqueou antes do OAuth com GSC_NOT_CONFIGURED: GSC_CLIENT_ID, GSC_CLIENT_SECRET, GSC_REFRESH_TOKEN ausentes no runner.
- Artefato wix-validation-41767131159 (13293600150), contendo apenas status.json. SHA-256: 983e5fb0df704210188ec17bf6446bf8e97b1e39961ce2b192fc523ead62a5a1.
- Artefato gsc-validation-41767131159 (13292079261), contendo apenas artifacts/gsc/status.json. SHA-256: 322b7374cfb9da2b22be0e0d886a76ab1c83b51adc1d6182b351cd9e729062cd.
- Ambos os ZIPs foram baixados e inspecionados; hashes conferem com os metadados GitHub. Não contêm pesquisa, rascunho Wix ou dados reais GSC. A geração efetiva de diagnósticos foi validada, a geração de conteúdo e métricas continua bloqueada.
- O primeiro diagnóstico GSC informa previous_data=preserved como garantia genérica; o checkout não tinha gsc-real.json. A revisão seguinte corrige para not_available quando não há arquivo anterior e acrescenta teste offline para esse caso. Não foi constatada perda de dados anteriores.
- Nenhuma chamada Google, OpenAI ou Wix ocorreu após o preflight nessa execução. Não houve publicação nem indexação confirmada.

A integração em master permanece suspensa porque painel-seo/collect_gsc.py também aciona publicar-painel-seo.yml, que publica o painel por FTP. A autorização desta etapa exclui publicação externa. Nenhum auto-merge foi habilitado.

Para desbloquear as integrações, a usuária precisa configurar ou disponibilizar corretamente os oito nomes de Secrets citados acima em GitHub Actions. Alterar credenciais requer autorização específica e canal seguro; o conector disponível não permite ler ou escrever Secrets. Não enviar valores em chat. Depois da configuração, fazer nova validação controlada e conferir conteúdo, datas, fontes e ID de rascunho, e não apenas o estado verde do workflow. A criação de rascunho Wix está autorizada; publicação e indexação não estão autorizadas nesta etapa.
