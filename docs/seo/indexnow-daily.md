# IndexNow diário

Workflow: `.github/workflows/indexnow-daily.yml`. Execução diária às 06h17
de Brasília (09h17 UTC); GitHub pode atrasar execuções agendadas. Também aceita
execução manual e roda ao alterar seus próprios arquivos em master.

O inventário reúne o domínio principal e os hosts arquindex.com.br encontrados
nos sitemaps XML versionados. Não é descoberta exaustiva via DNS. Para incluir
outro subdomínio, versione seu sitemap XML com a URL HTTPS do host.

Para cada host, publique previamente `/indexnow-key.txt` contendo apenas uma
chave IndexNow válida de 8 a 128 caracteres (a-z, A-Z, 0-9 ou hífen).
A URL fica na raiz e é enviada como `keyLocation`. Cada subdomínio precisa de
arquivo próprio; a chave do domínio principal não o verifica automaticamente.
O script apenas lê os sites: não altera FTP, DNS, páginas ou sitemap.

O script valida a chave pública, lê `/sitemap.xml` e seus índices, busca cada
página pública HTTP 200 sem redirecionamento e compara SHA-256 do corpo com a
última versão recebida pelo endpoint IndexNow. Envia URLs novas ou alteradas
em lotes de até 10.000 separados por host. Não notifica exclusões implícitas:
remoção do sitemap não prova exclusão da página. HTML dinâmico pode causar
novos envios; nesse caso, adapte o fingerprint a um manifesto de deploy.

O estado usa cache do GitHub Actions. Se o cache for removido/expirar, haverá
um novo envio inicial das páginas encontradas. O primeiro envio cobre todas
as páginas válidas; as execuções seguintes filtram corpos inalterados.
HTTP 200 registra recebimento; 202 permanece pendente e será tentado novamente.
Nenhum desses códigos garante rastreamento, indexação ou posicionamento.

Falhas de DNS, TLS, chave, HTTP, sitemap ou limite deixam evidências por host e
fazem o job falhar após concluir os outros hosts. Respostas 429 e 5xx têm
tentativas limitadas; Retry-After maior que 60 s fica para a próxima execução.
Limites: 200 sitemaps e 25.000 URLs por host, 8 MiB por resposta e 45 minutos
por job. Limites atingidos precisam de ajuste, sem truncamento silencioso.
Relatórios ficam nos artifacts por 30 dias e o resumo no job. Confira a primeira
execução: agendamento ativo não significa que todos os subdomínios passaram.

Referências: https://www.indexnow.org/documentation e https://www.indexnow.org/faq

## Diagnóstico sem envios

O workflow `indexnow-preflight.yml` executa os testes e um inventário somente
de leitura por host: DNS, chave e sitemap. Não acessa credenciais, não publica
DNS/FTP, não envia URLs ao IndexNow e não altera o cache de recebimentos.
Chave e sitemap são conferidos independentemente para não esconder a segunda
falha quando a primeira ocorre. O inventário conserva todos os candidatos,
inclusive os indisponíveis.

O sucesso desse workflow significa que a coleta diagnóstica terminou; não
significa que os hosts estão prontos. Consulte `status`, `blocked_hosts` e
as etapas/códigos em `indexnow-preflight/report.json`, além do resumo Markdown.
O remetente diário permanece inalterado e continua falhando quando qualquer
host apresenta erro. `ready_for_page_checks` exige validar as páginas antes
de enviar; não comprova recebimento ou indexação.

Diagnóstico da execução 40198973376 (25/10/2026): dos 68 hosts candidatos,
64 falharam na resolução DNS; `adequacaolgpd.arquindex.com.br` e
`arquindex.com.br` rejeitaram URLs de sitemap fora do próprio host;
`digitalizacaodedocumentosbh.arquindex.com.br` retornou HTTP 404 antes
da checagem das páginas. `www.arquindex.com.br` verificou 545 URLs,
preservou 531 inalteradas e recebeu HTTP 200 para 14 alteradas.
Essas são evidências daquela execução, não uma afirmação do estado atual.
Os bloqueios de DNS/hospedagem dos sites preparados já são tratados nas issues
#10 e #35; não criar apontamentos a partir de IPs históricos nem subir páginas
para eliminar artificialmente os erros do relatório.
