# Interlinking e monitor de engenharia/Databooks

A fila `seo/fila-seo-geo-aeo.csv` é a fonte de URLs. A seleção procura engenharia ou Databooks no serviço, consulta-alvo ou URL e inclui automaticamente novas fichas cadastradas com esses termos. A matriz CSV contém sete propostas editoriais; nenhum HTML é alterado neste PR.

Em 25/10/2026 as cinco URLs regionais/Databooks retornaram inicialmente 503 neste ambiente e depois 200, com canonical próprio único, um H1 e sem noindex ou bloqueio no robots.txt para Googlebot. O relatório datado registra a segunda consulta. Isso não comprova indexação nem estabilidade contínua. Os destinos da matriz são auditados em relatório separado.

## Fluxo comercial

Páginas regionais e subdomínio de Databooks → guia de montagem → solução ECM, quando pertinente. O guia deve apresentar CTA de orçamento com serviço, volume, cidade e prazo. Preservar o WhatsApp validado de cada página, a ressalva de não afiliação na página Petrobras e canonical próprio. Evitar links indiscriminados entre todas as cidades e UTM em links internos. Registrar eventos de CTA sem dados pessoais e conferir mensuração entre subdomínios.

## Monitor

```bash
python -m unittest discover -s tests -p test_monitor_engenharia_databooks.py -v
python scripts/monitor_engenharia_databooks.py --fila seo/fila-seo-geo-aeo.csv --previous .databooks-state/previous.json --output databooks-report/resultado.json
```

Verifica HTTP, title, H1, canonical, noindex e robots.txt. Extrai links internos, calcula hash e compara com estado anterior. Não consulta todos os links extraídos, não descobre URLs fora da fila, não consulta GSC nem declara indexação. Canonical diferente exige análise manual. Timeout de 10 segundos, limite de 2 MB por resposta, três consultas simultâneas. Restringe URLs e redirects a HTTPS em arquindex.com.br e seus subdomínios.

O workflow usa a fila atual do checkout, sem cópia estática. Seis testes usam respostas simuladas para validar HTTP 503, HTML válido, duplicações, noindex/robots, domínio e redirect. Fila sem URLs gera erro. Código de saída 1 sinaliza alertas, preservando artifact. Cache mantém estado entre execuções fora de PR; ausência/expiração cria baseline. PR não grava cache compartilhado. Relatórios ficam disponíveis por 30 dias; falhas usam a notificação padrão do GitHub conforme preferências do usuário, sem envio adicional de mensagens.

A rotina diária está proposta para 07h35 de Brasília e só passa a valer após integração na branch padrão. Enquanto o PR estiver aberto, apenas o check de PR pode executar consultas públicas. O workflow tem `contents: read`, não recebe credenciais de FTP, não publica, não envia IndexNow e não altera o repositório durante a execução. Não substitui o backup integral e as verificações de produção da issue #28 antes de mudanças no site.
