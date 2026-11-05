# ECM — investigação e proposta sem publicação

## Resultado confirmado
PR #116, head original d7a33153e3aaa0f7cd02f24f4f56642cb7953a1c, contém somente workflow de leitura e script. A condição original de `ready_for_human_review` permitia reprovações e gerava XML parcial. Corrigido para exigir aprovação de todas as candidatas editoriais; remove candidato antigo antes de retornar quando há bloqueios. Adicionadas verificação de robots.txt (Googlebot, bingbot e *), reconhecimento de `none` como noindex e aceitação de index.html como alias somente após raiz 200, canonical própria e bytes iguais. Nenhuma escrita remota ou submissão.

## Evidência atual e limitações
As issues #115/#117 relatam sete páginas 200 na execução anterior, cinco com canonical cruzada. Na coleta desta rodada, GET das sete páginas, raiz, cinco destinos no principal, robots e sitemap retornou HTTP 503 text/plain com mensagem de conexão upstream por Envoy. Esses corpos não são conteúdo editorial e não demonstram equivalência nem indisponibilidade global do site. Uma consulta HEAD anterior da raiz respondeu 200, 101124 bytes. A divergência impede concluir o estado atual.

| Página ECM | Destino indicado na evidência anterior | Conclusão nesta rodada |
|---|---|---|
| bh.html | https://www.arquindex.com.br/ecm.arquindex.com.br/bh.html | Equivalência e intenção não confirmadas |
| empresas.html | https://www.arquindex.com.br/ecm.arquindex.com.br/empresas.html | Equivalência e intenção não confirmadas |
| o-que-e.html | https://www.arquindex.com.br/ecm.arquindex.com.br/o-que-e.html | Equivalência e intenção não confirmadas |
| vantagens-ecm.html | https://www.arquindex.com.br/ecm.arquindex.com.br/vantagens-ecm.html | Equivalência e intenção não confirmadas |
| vantagens.html | https://www.arquindex.com.br/ecm.arquindex.com.br/vantagens.html | Equivalência e intenção não confirmadas |

## Origem dos arquivos
Não localizada no checkout a fonte HTML dessas sete páginas. O script histórico `scripts/corrigir-mobile-arq024-20261019.py` procura custo.html em quatro caminhos diferentes e não registra qual foi usado: isso não confirma document root. `config/site-hosting.json` também exige descoberta da raiz. `deploy/subdominios/alfresco-ecm` e `seo-regional/56-sites/ecmembh...` pertencem a outros hosts. Não reutilizá-los. O login HomeHost não resultou em sessão autenticada verificável; painel continua mostrando formulário.

## Próximas verificações de leitura
1. Abrir cadastro do domínio ECM no painel e registrar document root, servidor e eventual alias/rewrite; ler .htaccess do domínio e ancestrais.
2. Baixar os sete HTMLs, sitemap, robots e arquivos de verificação reais. Comparar hashes do servidor com respostas públicas e registrar SHA-256, tamanho e timestamp.
3. Comparar cada página cruzada com destino: cadeia de redirects, URL final, title, H1, conteúdo principal, canonical, meta robots e X-Robots-Tag. Igualdade de corpo não prova intenção editorial.
4. Se destino incorreto, propor troca somente do href canonical nos cinco arquivos; se duplicata intencional, preservar canonical e documentar a escolha antes de definir sitemap. Conferir raiz/index como alias.

## Operações condicionais a apresentar para aprovação posterior
Não há autorização de publicação solicitada neste relatório: faltam caminho real, corpos e hashes para uma lista exata revisável.

Após confirmar origem e conteúdo, apresentar uma nova lista com caminho absoluto, SHA antes/depois e diff de cada arquivo. Escopo máximo inicialmente esperado: cinco href canonical e sitemap.xml; nenhuma alteração de layout, conteúdo, assets, tokens, DNS ou email. A eventual correção de alias/root ou robots exige diff próprio se necessária.

Backup: antes de qualquer substituição, baixar originais completos para pasta fora da raiz pública; registrar permissões e hashes e testar releitura/restauração. Preservar também .htaccess e inventário de tokens sem modificá-los. Abortar se arquivo mudou desde a revisão.

Publicação: somente após aprovação da lista exata; transferir arquivos temporários por FTPS com TLS verificado, conferir bytes, substituir individualmente com operação de renomeação suportada pelo servidor; HTML primeiro e sitemap por último, somente quando todas as páginas legítimas finais tiverem passado. Não usar exclusão recursiva nem sincronização que apague arquivos.

Sitemap esperado se todas as sete páginas forem legítimas e raiz for preferencial: URLs absolutas de /, /bh.html, /custo.html, /empresas.html, /o-que-e.html, /vantagens-ecm.html, /vantagens.html. Esta lista é hipótese para revisão, não XML publicável. Arquivos de verificação permanecem acessíveis e saem apenas da lista editorial.

Validação antes/depois: HTTP GET 200 final, TLS válido, cadeia de redirects sem loop, HTML, canonical única coerente, sem noindex/none em meta ou cabeçalho, robots permitindo rastreamento; cobertura do inventário completo; XML namespace correto, loc HTTPS absolutos únicos e mesmo host. Comparar HTML antes/depois com diferença limitada a canonical, e conferir assets/layout em desktop e mobile. Arquivos técnicos devem manter hashes.

Reversão: em falha de hash, disponibilidade, XML, canonical ou perda de conteúdo, restaurar exatamente os originais alterados a partir do backup verificado; reler via FTPS e publicamente. Registrar falha e interromper submissões.

Publicação, submissão e indexação são estados distintos. Depois de publicação autorizada, verificar respostas públicas primeiro; só depois tratar submissão Google/Bing conforme autorização. Indexação exige evidência própria dos buscadores.

## Testes realizados
`python -m py_compile scripts/seo_ecm_sitemap_proposal.py`: passou.
`python -m unittest discover -s tests -p test_ecm_sitemap_completeness.py -v`: quatro testes passaram: cobertura parcial bloqueada, tokens excluídos do XML, candidato antigo removido em execução incompleta, robots none rejeitado.
Validação pública final e XML completo: pendentes por acesso; nenhum XML substituto produzido nesta rodada.
