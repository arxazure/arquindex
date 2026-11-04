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

O workflow é acionado pelo push da branch específica para executar a criação solicitada. É deliberadamente restrito a novos hosts: não repetir para atualizar instalações existentes sem adaptar o preflight e a estratégia de backup.

## QA e acompanhamento

Confira portais-tecnicos/qa-report.json e publish-report/portais-tecnicos-20.json no artefato da execução. Após publicação, medir descoberta, cobertura, impressões, cliques e consultas reais; nenhuma nota 0–10 é assumida. Cada host contém dois URLs no sitemap, com canonical própria e links contextuais entre temas. A navegação para a Home institucional não implica transferência garantida de autoridade. FAQ estruturada e llms.txt não garantem exibição especial.
