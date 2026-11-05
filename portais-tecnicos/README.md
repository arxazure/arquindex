# Vinte portais técnicos Arquindex

Pedido autorizado em 04/11/2026: criar vinte subdomínios com guias, manuais, FAQ, blocos de resposta, vídeos e seções de notícias regulatórias.

O catálogo contém vinte temas distintos, três etapas próprias, controles, cenário didático, FAQ e fontes por tema. Cada host recebe guia, manual, ficha CSV, vídeo MP4 de 24 segundos, legendas VTT, poster, transcrição, robots, sitemap e llms.txt. Não há promessas de ranking ou endossos públicos. Autoria institucional sem credenciais pessoais inventadas. GEO descreve planejamento de atendimento a partir de BH; não cria endereços ou filiais fictícias.

## Execução

```sh
python scripts/portais-tecnicos/build.py --videos
python scripts/portais-tecnicos/qa.py
python scripts/portais-tecnicos/publish.py
```

Dependências: Python 3.12, Pillow 11.3.0, FFmpeg e DejaVu Sans. O workflow usa os secrets existentes de hospedagem, sem imprimi-los. As notícias são uma seleção estática datada; não existe uma rotina de monitoramento implícita. O vídeo é visual, sem narração, com transcrição e legendas.

## Publicação

A produção institucional permanece na HomeHost, conforme AGENTS.md. A zona Cloudflare cadastrada não é prova de delegação ativa. Nenhum nameserver, serviço de e-mail, app ou homepage é modificado. Somente os novos hosts são provisionados pelo cPanel autenticado da mesma conta. Domínios existentes provocam bloqueio; suas páginas são preservadas. O script valida raiz documental e FTPS com TLS. Como não sobrescreve sites existentes, a referência de recuperação é a ausência dos novos arquivos; ele conserva a homepage e confere que seus bytes não mudaram. Não remove automaticamente domínios criados se houver falha posterior.

O conteúdo inicia com noindex. A promoção para indexação exige leitura pública por HTTPS, igualdade dos bytes do guia e do manual e verificação dos recursos, incluindo vídeo. Se DNS ou TLS não estiverem prontos, o host permanece pendente e noindex. Se a promoção falhar, o script restaura noindex. Não há submissão a buscadores sem confirmar publicação. Provisionado, publicado e indexado são estados diferentes.

O push na branch do PR executa testes e preflight de leitura; não publica. A publicação é manual, em modo pilot, com --portal e --approval APPROVED:<slug>. Somente um host é aceito por execução. A aprovação humana deve existir antes do disparo; o argumento não substitui essa aprovação. Não repetir para atualizar instalações existentes sem adaptar o preflight e a estratégia de backup.

## QA e acompanhamento

Confira portais-tecnicos/qa-report.json e publish-report/portais-tecnicos-20.json no artefato da execução. Após publicação, medir descoberta, cobertura, impressões, cliques e consultas reais; nenhuma nota 0–10 é assumida. Cada host contém dois URLs no sitemap, com canonical própria e links contextuais entre temas. A navegação para a Home institucional não implica transferência garantida de autoridade. FAQ estruturada e llms.txt não garantem exibição especial.

## Correção e piloto autorizado

O preflight exige CPANEL_HOST, CPANEL_USER, CPANEL_API_TOKEN e FTP_PASSWORD separados. Não há fallback da senha FTP para autenticação cPanel. Endpoint confirmado no painel HomeHost: https://h59.servidorhh.com:2083; usuário arquind2. O token cPanel concede todas as APIs disponíveis à conta, portanto deve permanecer somente no secret do GitHub e ter vencimento definido. Ausência de configuração, HTTP 401, 403, outros HTTP, TLS, timeout e rede têm códigos distintos e sem textos de exceções externas.

Sete testes unitários passaram. Preflight real da execução 41951522359, tentativa 2: preflight_passed, cpanel_authenticated=true, leitura FTPS confirmada. Execução piloto 41958456978: artefato original 13370953459 recuperado; QA aprovado para 20 portais, 40 páginas e 20 vídeos; somente conarq-guias.arquindex.com.br publicado. SHA256 do index: a459c0fdab7cab08b0d95d251947bee9a1f98b3f849d53a13efaaa4860e84cd2. Relatório: published=1, planned=20, indexed_confirmed=null, state=published_verified. Raiz: public_html/portais-tecnicos/conarq-guias. Leitura pública HTTPS conferiu páginas e todos os demais arquivos antes de remover noindex; homepage institucional conferida antes da promoção e ao final. AutoSSL de conta não foi disparado. Nenhuma submissão aos buscadores foi executada.

Como o workflow ainda não está na branch padrão, o piloto foi disparado em pilot/conarq-guias-approved-20261104, isoladamente, condicionado a uma mensagem exata de commit e limitado ao portal autorizado. Não foi feito merge do PR. Os outros 19 portais foram autorizados e publicados em 05/11/2026, conforme o relatório consolidado abaixo. Indexabilidade não comprova indexação em Google ou Bing.

## Publicação completa em 05/11/2026

Os 20 portais estão em published_verified, totalizando 40 páginas e 20 vídeos MP4. Evidência por host, raiz, SHA256 e execuções: `docs/portais-tecnicos-publicacao-20261105.json`. Execução final 41961007394 concluída com sucesso. Falhas transitórias de DNS foram resolvidas por novas verificações dos arquivos já enviados, sem recriar domínios ou sobrescrever sites existentes. Cada portal passou pela leitura pública HTTPS antes da promoção para index,follow; a homepage institucional foi comparada em bytes antes da promoção e ao final. Não foram alterados nameservers, e-mail ou aplicativos. Não foi feito merge do PR. Submissão a buscadores não executada; indexação real ainda não confirmada.

O modo verify permite retomar a verificação de um host já provisionado: exige aprovação do slug e raiz documental compatível; não recria o domínio nem reenvia os recursos. Falhas de DNS têm código COMMUNICATION_DNS. Diretórios FTPS já verificados são reutilizados na mesma conexão; todos os uploads continuam com conferência de leitura. A lista de promoção é registrada antes da escrita para permitir restaurar noindex também quando a conferência de um upload falhar.
