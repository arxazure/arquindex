# Formulário comercial — guarda documental BH

## Origem da publicação verificada em 16/10/2026

- Branch: `master`, repositório `arxazure/arquindex`.
- Fonte do publisher ativo: `seo-regional/56-sites/guardadocumentalembh.arquindex.com.br/index.html`.
- Workflow `.github/workflows/publicar-56-subdominios.yml`, execução 38959097620, job 117169359488: conclusão `success`; log `HOMEHOST FTP_VERIFIED guardadocumentalembh.arquindex.com.br`.
- Destino configurado: raiz pública descoberta pelo workflow, seguida de `subdominios/guardadocumentalembh.arquindex.com.br/index.html`. A configuração de provisionamento cPanel usa `public_html/subdominios/guardadocumentalembh.arquindex.com.br`.
- O acesso HTTPS a partir do ambiente de implementação retornou 502; o envio FTPS anterior não comprova que DNS, certificado e virtual host estejam corretos. Confirmar o HTML público após o deploy.

## Fonte única e atualização

O componente editável é `scripts/templates/guarda-commercial-form.html`. Execute `python scripts/sync_guarda_form.py` após editá-lo. O script instala o componente na fonte de publicação e espelha a página integral para `deploy/subdominios/guardadocumentalembh/index.html`. A execução é idempotente; não editar o espelho manualmente.

O gerador de 56 páginas executa esse script antes do commit. Ambos os publishers executam os testes em navegador antes de qualquer upload. Pushes de branches de trabalho não publicam pelo FTPS. A URL canônica permanece `https://guardadocumentalembh.arquindex.com.br/`.

## Atendimento e privacidade

Destino encontrado no código: `https://wa.me/5531973632725`. A pesquisa no repositório não encontrou webhook, YCloud ou chatbot verificável. Nenhum endpoint de robô foi criado ou presumido. Verificação do robô no provedor exige evidência externa; não faz parte do funcionamento deste formulário.

Campos são processados no navegador, sem persistência pelo componente. Abrir o link compartilha o texto preenchido com WhatsApp/Meta; o visitante precisa confirmar o envio. A ciência de privacidade é exigida, sem inscrição em marketing. O aviso descreve finalidade, destinatário e contato de privacidade sem inventar prazo de retenção ou política corporativa. Nenhuma mensagem comercial é enviada durante os testes.

## Verificação

`NODE_PATH=<pasta-com-playwright>/node_modules node tests/guarda-form.cjs`

Cobertura: telas 360/390/1280 px; ausência de rolagem horizontal; campos obrigatórios; espaços em branco; telefone/e-mail inválidos; ciência de privacidade; pelo menos um serviço; seleção dos sete serviços; quantidade inválida; campos condicionais; exclusão dos dados ocultos; rótulos e teclado; mensagem, número e codificação; fallback sem JavaScript; ausência de erros JS e igualdade entre as cópias.

O workflow de teste conserva capturas de tela como artefatos. O teste intercepta `wa.me`; nenhum envio é realizado.

## Resultado da validação inicial

Execução de teste isolada [38962369759](https://github.com/arxazure/arquindex/actions/runs/38962369759): sucesso em Chromium nas três larguras e no fallback sem JavaScript. Capturas de tela de celular e desktop inspecionadas visualmente; campos, rótulos e botão legíveis, sem sobreposição. Os publishers repetem os testes antes do envio e verificam a presença da versão do formulário no HTML HTTPS depois.

O job anterior de ativação de subdomínios (execução 38938586697) falhou com `CPANEL_API_BLOCKED HTTPError 401`; o log informou que nenhum domínio foi alterado. Não presumir provisionamento concluído com base somente no upload FTPS.

## Publicadores concorrentes

A revisão identificou que os dois workflows de publicação usavam grupos de concorrência diferentes. A execução completa 38962639797 encontrou `HASH_MISMATCH` em um sitemap de outro subdomínio enquanto o publicador principal também escrevia no mesmo destino. O fluxo completo foi mantido como acionamento manual e passou a compartilhar `arquindex-deploy-56` com o principal, impedindo gravações simultâneas nas próximas execuções. O formulário de guarda BH já havia passado nos testes antes de ambas as tentativas.
