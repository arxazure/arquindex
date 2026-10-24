# Kit Arquindex — IA local + Alfresco (piloto)

**Estado:** kit de laboratório; nenhum deploy, processamento clínico ou cliente foi executado. Não usar com dados pessoais reais antes de homologação, RIPD quando necessário, autorização, controle de acesso e validação jurídica.

## Quatro trilhas
1. **Manuscritos históricos**: PDF/imagem -> pré-processamento -> HTR/OCR especializado -> transcrição com marcações de incerteza -> conferência palaeográfica -> indexação.
2. **Classificação/separação**: PDF misto -> OCR/texto -> regras e modelo de classificação -> fronteiras de documento -> revisão visual -> PDF por documento.
3. **Manuais de engenharia**: manuais -> OCR -> fragmentos identificados por documento/versão/página -> recuperação por busca -> resposta com citações -> validação técnica.
4. **Prontuários ocupacionais/hospitalares**: coleta autorizada -> OCR impresso/manuscrito -> identificação condicionada a campos rotulados -> separação conservadora -> conferência por identificadores -> aprovação humana antes de saída final.

## Início rápido no terminal
Requer Python 3.11+ e PyMuPDF. Use ambiente virtual:
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r kits/alfresco-ia-local/requirements.txt
python kits/alfresco-ia-local/scripts/inventariar_pdf.py --entrada C:\\lote-teste --saida C:\\lote-teste\\inventario.json
python kits/alfresco-ia-local/scripts/planejar_separacao.py --pdf C:\\lote-teste\\amostra.pdf --saida C:\\lote-teste\\revisao.json
```
No Linux:
```bash
python3 -m venv .venv && . .venv/bin/activate
python -m pip install -r kits/alfresco-ia-local/requirements.txt
python kits/alfresco-ia-local/scripts/inventariar_pdf.py --entrada ./amostras --saida ./inventario.json
python kits/alfresco-ia-local/scripts/planejar_separacao.py --pdf ./amostras/lote.pdf --saida ./revisao.json
```
Nenhum script de separação escreve PDFs automaticamente. O relatório é apenas uma sugestão para conferência. Conteúdo clínico **nunca** é enviado a modelos externos pelo kit.

## Integração Alfresco
Use `scripts/alfresco_api.py` para **verificar** conexão HTTPS e permissões. O upload é bloqueado por padrão: requer `--confirmar-upload`, nó-pai explícito, HTTPS e credenciais em variáveis de ambiente. Nunca sobrescreve arquivos existentes. Ver `MANUAL_OPERACAO.md`.

## Critérios de aceite
- 100% das páginas mantidas em ordem na entrada e saídas, sem mistura de pessoas.
- Conferência obrigatória de fronteiras sugeridas em documentos multipágina e caligrafia.
- Ausência de nomes/CPF/dados de saúde em logs e artefatos públicos.
- Respostas a manuais somente com fonte, versão e página; sem inventar instrução de segurança.
- Nenhuma credencial em código, tickets em URL ou reenvio automático destrutivo.
- Rastrear versão da IA, modelo, configuração, operador, aprovação, amostras e erros.
