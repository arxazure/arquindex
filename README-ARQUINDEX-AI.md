# Arquindex IA Documental - homologação
Branch isolada do site institucional. Executar via Dockerfile da raiz desta branch.
## Funções
- Painel responsivo, autenticação Bearer ADMIN_TOKEN
- Upload PDF/JPG/PNG, extração de texto PyMuPDF, OCR Tesseract português/inglês
- SQLite em DATA_DIR (/data), persistência exige volume Railway em /data
- API de consulta documental, download autenticado
- Chat documental com endpoint OpenAI compatível (/chat/completions)
## Variáveis Railway
- ADMIN_TOKEN: obrigatório, segredo aleatório forte (não usar token de outro sistema)
- DATA_DIR=/data
- LLM_BASE_URL: URL de API compatível OpenAI, sem /chat/completions
- LLM_MODEL: nome do modelo
- LLM_API_KEY: segredo se exigido
- PORT: fornecida pelo Railway
## Validação
- GET /health retorna status, auth_configured, llm_configured
- GET /api/session exige Authorization: Bearer ADMIN_TOKEN
- Teste com PDF sem dados reais; só habilitar uso de dados de clientes após controle de acesso individual e retenção.
## Limitações
Homologação com autenticação única. Ainda NÃO possui multiusuários, filas, RAG vetorial, auditoria completa, isolamento multiempresa, assinatura digital e automação de workflows. Não ofertar como serviço produtivo antes de endurecimento de segurança e testes.
