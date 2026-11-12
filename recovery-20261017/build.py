#!/usr/bin/env python3
"""Rebuild requested public hosts without duplicating keyword-variant landing pages."""
import json, re
from pathlib import Path
from html import escape as e
from urllib.parse import quote
from xml.etree import ElementTree as ET
BASE=Path(__file__).resolve().parent
OUT=BASE/'dist'
DOMAIN='arquindex.com.br'
TECHNICAL={'assets','bin','cache','css','cast','artigos','cidades'}
APPS={'alf','acervonet','arcadiagp','arxbox','centralinf','dashboard','dados','datagestao','digiout','digitaldoc'}
# Each public hub has a defined purpose. Variants consolidate to that hub rather
# than creating hundreds of near-identical self-canonical doorway pages.
CONTENT={
'acervo':('Preservação e digitalização de acervos',
 'Acervos históricos, administrativos e institucionais precisam conservar o contexto de produção dos documentos. A Arquindex planeja a identificação, a captura e a recuperação das informações conforme o estado dos originais e os objetivos da instituição.',
 [('Diagnóstico e conservação','O levantamento registra suportes, formatos, fragilidade, organização existente e restrições de manuseio. Livros encadernados e documentos frágeis precisam de método de captura compatível com sua conservação.'),('Descrição e pesquisa','A descrição relaciona documentos à sua proveniência, assunto e estrutura. OCR facilita a busca textual, enquanto os metadados permitem localizar itens mesmo quando o reconhecimento não é preciso.'),('Entrega e preservação','O projeto define formatos, estrutura de pastas, identificação dos arquivos e cópias de segurança. A preservação digital exige acompanhamento contínuo de integridade, acesso e disponibilidade.')]),
'arquivos':('Organização de arquivos físicos e digitais',
 'Um arquivo organizado permite localizar documentos, controlar responsabilidades e planejar a guarda. A Arquindex estrutura projetos de inventário, classificação, identificação de caixas, indexação e integração com o acervo digital.',
 [('Inventário por unidade e departamento','As caixas podem ser registradas por empresa, unidade, departamento, tipo documental e período. A identificação física precisa corresponder ao inventário para permitir recuperação rastreável.'),('Classificação e temporalidade','A classificação considera funções e atividades que originaram os documentos. Os prazos de guarda dependem da espécie documental e das obrigações aplicáveis; suspensões de descarte devem ser respeitadas.'),('Consultas e movimentações','O projeto estabelece quem pode solicitar um documento, como registrar empréstimos e devoluções e quais informações serão usadas na busca. O controle de acesso também se aplica aos documentos físicos.')]),
'cedoc':('CEDOC: centro de documentação empresarial',
 'Um centro de documentação reúne processos de recebimento, organização, guarda e consulta. A Arquindex apoia a implantação ou reorganização de CEDOCs com inventário, procedimentos operacionais e critérios de atendimento.',
 [('Entrada e rastreabilidade','O recebimento registra origem, responsável, volume e condição do acervo. A identificação dos lotes permite acompanhar preparação, digitalização e transferência para guarda.'),('Rotina de atendimento','Solicitações de consulta precisam de identificação do solicitante, autorização e registro de entrega. Prazos de atendimento e modalidades de consulta devem constar do projeto.'),('Indicadores de operação','Volume recebido, caixas inventariadas, documentos localizados e pendências de classificação ajudam a acompanhar a operação. Metas precisam considerar a complexidade real do acervo.')]),
'conarq':('Classificação documental e referências do CONARQ',
 'A Arquindex auxilia empresas e instituições a organizar documentos com critérios arquivísticos e referências técnicas aplicáveis. A adoção de uma referência exige avaliar o contexto da organização e a natureza do acervo.',
 [('Plano de classificação','O plano organiza séries documentais segundo funções e atividades. Sua implantação envolve levantamento dos processos, identificação dos documentos e validação com as áreas produtoras.'),('Tabela de temporalidade','Prazos e destinação precisam ser fundamentados e validados pelos responsáveis. Uma tabela de outra instituição não deve ser aplicada automaticamente ao acervo de uma empresa.'),('Descrição e acesso','Metadados de contexto, datas, autoria, unidade produtora e relações documentais favorecem a recuperação. Referências de descrição devem ser selecionadas conforme o tipo de acervo e o objetivo do projeto.')]),
'digitalizacao':('Digitalização de documentos empresariais',
 'A Arquindex transforma documentos físicos em arquivos digitais organizados. O projeto combina preparação dos originais, captura, controle de qualidade, nomenclatura e entrega conforme as necessidades de consulta e segurança.',
 [('Preparação do lote','O levantamento identifica quantidade, formatos, conservação e tipos documentais. A preparação organiza os lotes e define como tratar anexos, páginas frente e verso e documentos de diferentes tamanhos.'),('Captura e conferência','Resolução, cor e formato são definidos para o uso pretendido. A conferência verifica legibilidade, sequência, cortes e correspondência entre os originais e os arquivos entregues.'),('Indexação e orçamento','O orçamento considera volume, preparação, campos de indexação, OCR, logística e prazo. Para receber uma proposta, informe município, estimativa de páginas ou caixas e uma amostra representativa do acervo.')]),
'digitalizacao-ocr-empresas':('OCR para empresas: documentos pesquisáveis',
 'OCR reconhece caracteres presentes na imagem e permite pesquisar texto nos arquivos. A Arquindex combina digitalização, reconhecimento textual e indexação para facilitar a localização de contratos, dossiês e documentos administrativos.',
 [('Texto pesquisável e metadados','A busca por palavras depende da qualidade do reconhecimento. Campos como número, nome, data e departamento podem complementar o OCR e precisam de regras próprias de preenchimento e conferência.'),('Qualidade dos originais','Borrões, carimbos, inclinação, impressão fraca e manuscritos afetam o resultado. Um lote piloto permite avaliar limitações antes de dimensionar prazos e critérios de aceitação.'),('Integração com GED','Os PDFs pesquisáveis e índices podem ser preparados para importação em um repositório. O modelo de metadados e o formato da entrega devem ser combinados antes da execução.')]),
'adequacaolgpd':('Consultoria LGPD e governança de dados',
 'A Arquindex apoia organizações no levantamento de tratamentos de dados pessoais, definição de prioridades e implantação de procedimentos de privacidade. O trabalho começa pelo entendimento dos processos e das responsabilidades internas.',
 [('Mapeamento de tratamentos','O diagnóstico identifica dados tratados, finalidades, áreas responsáveis, sistemas, fornecedores e compartilhamentos. O registro deve refletir o processo real e ser atualizado quando houver mudanças.'),('Plano de adequação','O plano reúne ações sobre transparência, atendimento a titulares, contratos, acessos, retenção e resposta a incidentes. Cada ação precisa de responsável, prazo e evidência de execução.'),('Documentos e acompanhamento','Políticas e procedimentos devem corresponder à operação. Treinamentos, revisão de contratos e acompanhamento das pendências ajudam a manter a governança após o diagnóstico inicial.')]),
'auditoria-lgpd':('Auditoria de privacidade e proteção de dados',
 'Uma auditoria de privacidade compara processos, documentos e evidências com critérios definidos no escopo. A Arquindex apoia a identificação de lacunas e a organização de um plano de correção com responsáveis e prioridades.',
 [('Preparação da auditoria','O escopo identifica unidades, processos, sistemas e critérios que serão avaliados. Entrevistas e amostras documentais precisam ser suficientes para sustentar cada conclusão.'),('Evidências e achados','Cada achado registra condição observada, evidência, impacto e recomendação. A presença de uma política isolada não comprova que um controle seja executado na rotina.'),('Plano de correção','As ações devem conter responsável, prazo e evidência de conclusão. A revisão posterior verifica a execução e registra pendências que continuam exigindo acompanhamento.')]),
'7-motivos-contar-dpo-terceirizado':('7 motivos para avaliar um DPO terceirizado',
 'O serviço de encarregado terceirizado pode apoiar a rotina de privacidade da organização. A contratação deve definir atribuições, canais, disponibilidade e a interface com a equipe interna.',
 [('1. Organizar o canal de privacidade','Um fluxo documentado ajuda a receber demandas, encaminhá-las aos responsáveis e acompanhar respostas.'),('2. Acompanhar o inventário de dados','O encarregado pode apoiar a atualização dos registros quando processos, sistemas e fornecedores mudam.'),('3. Orientar a equipe','Treinamentos e orientações práticas aproximam as políticas da rotina de trabalho.'),('4. Apoiar a revisão de documentos','Avisos, procedimentos e contratos precisam refletir as atividades efetivamente realizadas.'),('5. Estruturar a resposta a incidentes','Papéis e fluxos previamente definidos favorecem o encaminhamento das ocorrências às áreas responsáveis.'),('6. Registrar decisões e pendências','Um histórico de recomendações e encaminhamentos facilita a continuidade da governança.'),('7. Definir acompanhamento periódico','Reuniões e indicadores permitem revisar prioridades. A terceirização não transfere automaticamente as responsabilidades da organização.')]),
'alfresco':('Alfresco ECM: implantação e gestão documental',
 'A Arquindex desenvolve projetos de implantação e organização de repositórios Alfresco. A solução deve ser dimensionada conforme volume, usuários, infraestrutura, processos e requisitos de acesso.',
 [('Estrutura e metadados','O levantamento define empresas, sites, departamentos, pastas e modelos de conteúdo. Campos configurados por tipo documental melhoram a padronização e a busca.'),('Permissões e processos','Os acessos precisam refletir as responsabilidades dos usuários. Fluxos de revisão, aprovação e publicação são definidos a partir de processos documentados e da versão escolhida.'),('Migração e operação','A migração deve validar quantidade, integridade, metadados e permissões. Backup, atualização, monitoramento e testes de restauração fazem parte do planejamento operacional.')]),
'bpm':('BPM documental: modelagem de processos',
 'Processos documentais claros reduzem dúvidas sobre quem produz, confere, aprova e guarda cada documento. A Arquindex apoia o levantamento e a modelagem desses fluxos antes da automação.',
 [('Mapeamento do processo atual','Entrevistas e observação identificam entradas, responsáveis, decisões, exceções e saídas. O desenho deve representar a execução real, incluindo etapas manuais.'),('Definição do fluxo desejado','O novo fluxo estabelece critérios de aprovação, prazos, responsabilidades e tratamento de pendências. Mudanças devem ser validadas com as áreas envolvidas.'),('Indicadores e melhoria','Tempo de ciclo, retrabalho e documentos pendentes ajudam a medir o processo. A automação deve ser acompanhada por revisão dos resultados e das exceções.')]),
'automacao':('Automação de documentos e rotinas empresariais',
 'A automação documental pode padronizar captura, identificação, encaminhamento e registro. A Arquindex avalia oportunidades de automação mantendo controles de validação e tratamento das exceções.',
 [('Entradas e regras','O projeto define origens dos arquivos, campos obrigatórios, padrões de nome e condições de encaminhamento. Amostras reais ajudam a identificar variações e casos que exigem revisão.'),('Validação e integrações','Integrações precisam registrar resultados e permitir identificar falhas. Informações críticas extraídas por OCR ou outros mecanismos devem ter conferência compatível com o risco.'),('Acompanhamento da execução','Logs e filas de pendências tornam a operação verificável. O projeto deve definir responsáveis por erros, reprocessamento e mudanças nas regras.')]),
'databook':('Elaboração e organização de Databooks de engenharia',
 'A Arquindex organiza Databooks a partir de índices, requisitos contratuais e documentos do projeto. A estrutura reúne capítulos, itens e evidências para facilitar a conferência e a entrega técnica.',
 [('Estrutura e nomenclatura','O índice orienta capítulos e subitens. Os arquivos podem ser nomeados pelo número da seção e título validado da capa, preservando uma relação clara com a estrutura de entrega.'),('Conferência documental','A revisão verifica presença dos itens, identificação, revisões, legibilidade e correspondência com o índice. Pendências devem ser registradas para validação com os responsáveis técnicos.'),('Entrega e rastreabilidade','A entrega pode incluir arquivos organizados, PDFs pesquisáveis e controle de pendências. A aprovação técnica dos documentos permanece com os profissionais responsáveis pelo projeto.')]),
'digitacao':('Digitação e indexação de dados documentais',
 'A Arquindex apoia a transcrição e indexação de informações de documentos para bases estruturadas. O projeto define campos, regras de preenchimento e critérios de conferência antes do processamento.',
 [('Modelo de dados','Os campos devem conter definições, exemplos e regras para datas, números, nomes e valores ausentes. Um dicionário de dados reduz interpretações divergentes.'),('Conferência de informações','A estratégia de revisão depende da criticidade dos dados e da qualidade dos originais. Divergências e informações ilegíveis precisam de tratamento explícito.'),('Formato de entrega','Planilhas e arquivos de importação devem ser compatíveis com o sistema de destino. A validação de um lote piloto permite ajustar campos e regras antes do processamento completo.')]),
'decreto10278':('Planejamento técnico para digitalização documental',
 'Projetos que pretendem atender requisitos normativos de digitalização precisam avaliar o regime aplicável aos documentos e os requisitos técnicos do caso. OCR e armazenamento em PDF, isoladamente, não comprovam equivalência jurídica ao original.',
 [('Diagnóstico do acervo','A análise identifica tipos documentais, finalidades, responsáveis e restrições de guarda. Regras setoriais e obrigações específicas precisam ser consideradas no escopo.'),('Requisitos e evidências','O projeto deve documentar parâmetros de captura, metadados, integridade, autoria e controle de qualidade conforme os requisitos aplicáveis. Os critérios de aceite precisam ser verificáveis.'),('Destinação dos originais','A eliminação do papel não é automática após a captura. Antes de qualquer descarte, os responsáveis devem validar prazos, restrições e demais obrigações aplicáveis.')]),
'armazenamento':('Armazenamento e acesso a documentos digitais',
 'Um repositório documental precisa reunir organização, controle de acesso e recuperação confiável. A Arquindex apoia o planejamento do armazenamento e da integração de arquivos digitalizados ao ambiente da organização.',
 [('Acesso e responsabilidades','A definição de perfis deve considerar quem consulta, inclui, altera e administra documentos. Contas individuais e revisão de acessos favorecem a rastreabilidade.'),('Integridade e cópias de segurança','O projeto deve diferenciar armazenamento de backup, definir cópias e testar a recuperação. A integridade dos arquivos precisa ser acompanhada conforme os requisitos do acervo.'),('Pesquisa e retenção','Metadados, nomenclatura e classificação ajudam a localizar documentos. A política de retenção precisa ser integrada às obrigações de guarda e à gestão de permissões.')]),
'aplicativos-facilitam-digitalizacao-documentos-pelo-celular':('Captura de documentos pelo celular: cuidados práticos',
 'A captura pelo celular pode atender necessidades pontuais de envio de documentos. Antes de incorporá-la à rotina empresarial, é preciso definir qualidade, conferência e destino seguro dos arquivos.',
 [('Preparar a captura','Utilize iluminação uniforme, enquadre toda a página e evite sombras e reflexos. Confira frente, verso, anexos e sequência antes de concluir.'),('Revisar o resultado','Verifique cortes, legibilidade e orientação. O texto reconhecido automaticamente pode conter erros, especialmente em carimbos e documentos com impressão fraca.'),('Encaminhar e guardar','Use o repositório autorizado pela organização e aplique as regras de acesso. A captura pelo celular não atende automaticamente requisitos de digitalização certificada.')])
}

def group(s):
 if s in CONTENT:return s
 if 'decreto10278' in s:return 'decreto10278'
 if any(x in s for x in ('dpo','lgpd','exin','auditoria','compliance','mapeamento','governanca')):
  if 'dpo' in s:return '7-motivos-contar-dpo-terceirizado'
  if 'auditoria' in s:return 'auditoria-lgpd'
  return 'adequacaolgpd'
 if 'alfresco' in s:return 'alfresco'
 if 'databook' in s:return 'databook'
 if 'conarq' in s:return 'conarq'
 if any(x in s for x in ('cedoc','cedo')):return 'cedoc'
 if 'bpm' in s:return 'bpm'
 if 'automacao' in s:return 'automacao'
 if 'digitacao' in s:return 'digitacao'
 if any(x in s for x in ('digitaliz','bhdigital','pje')):
  return 'digitalizacao-ocr-empresas' if 'ocr' in s else 'digitalizacao'
 if 'armazenamento' in s:return 'armazenamento'
 if 'acerv' in s:return 'acervo'
 return 'arquivos'

CSS='''*{box-sizing:border-box}body{margin:0;color:#173047;background:#f6f9fc;font:17px/1.7 system-ui,sans-serif}header,footer{background:#10344d;color:white;padding:22px max(5%,calc((100% - 1120px)/2))}header a,footer a{color:white}a{color:#006684}main{max-width:1120px;margin:auto;padding:32px 24px}nav{display:flex;gap:16px;flex-wrap:wrap}h1{font-size:clamp(2.2rem,5vw,3.6rem);line-height:1.15;max-width:900px}h2{line-height:1.3;font-size:1.55rem}.hero{background:#e6f1f4;border-radius:20px;padding:32px}.tag{color:#18677b;font-weight:700;font-size:.85rem;letter-spacing:.08em}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px;margin:30px 0}article,section.panel{background:white;padding:26px;border:1px solid #dae5ec;border-radius:14px}.cta{display:inline-block;padding:12px 20px;margin:8px 8px 8px 0;background:#14664d;color:white;border-radius:8px;font-weight:700;text-decoration:none}li{margin:10px 0}details{padding:14px 0;border-bottom:1px solid #dae5ec}summary{font-weight:700;cursor:pointer}footer{margin-top:35px;font-size:.9rem}:focus-visible{outline:3px solid #e49600;outline-offset:4px}@media(max-width:600px){main{padding:20px 14px}.hero{padding:24px}header nav{font-size:.9rem}}'''

def url(slug):return 'https://'+slug+'.'+DOMAIN+'/'
def page(s,g):
 title,intro,sections=CONTENT[g]
 canonical=url(g)
 contact='https://wa.me/5531973632725?text='+quote('Olá, Arquindex. Quero uma proposta: '+title)
 cards=''.join('<article><h2>'+e(h)+'</h2><p>'+e(p)+'</p></article>' for h,p in sections)
 related=[x for x in ('digitalizacao','arquivos','adequacaolgpd','alfresco','databook','armazenamento') if x!=g][:4]
 links=''.join(f'<li><a href="{url(x)}">{e(CONTENT[x][0])}</a></li>' for x in related)
 schema={'@context':'https://schema.org','@type':'Service','name':title,'url':canonical,'provider':{'@type':'Organization','name':'Arquindex','url':'https://www.arquindex.com.br/'}}
 return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | Arquindex</title><meta name="description" content="{e(intro[:160],quote=True)}"><link rel="canonical" href="{canonical}"><meta name="robots" content="index,follow,max-image-preview:large"><meta property="og:title" content="{e(title,quote=True)}"><meta property="og:description" content="{e(intro[:160],quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:type" content="website"><style>{CSS}</style><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head><body><header><nav aria-label="Navegação principal"><a href="https://www.arquindex.com.br/">ARQUINDEX</a><a href="https://www.arquindex.com.br/rede-documental/">Serviços e guias</a><a href="#orcamento">Solicitar proposta</a></nav></header><main><section class="hero"><p class="tag">GESTÃO DOCUMENTAL · TECNOLOGIA · PRIVACIDADE</p><h1>{e(title)}</h1><p>{e(intro)}</p><a class="cta" href="{e(contact,quote=True)}">Conversar com a Arquindex</a></section><div class="grid">{cards}</div><section class="panel" id="orcamento"><h2>O que informar para receber uma proposta</h2><p>Envie o município, o tipo de documento ou processo, o volume aproximado, os objetivos e o prazo desejado. Informe também se há necessidade de coleta, indexação ou integração com sistemas.</p><p>A sede da Arquindex fica em Belo Horizonte. Atendimento em outras localidades e condições de logística dependem da análise do projeto.</p><a class="cta" href="{e(contact,quote=True)}">Solicitar orçamento pelo WhatsApp</a><a href="https://www.arquindex.com.br/">Conhecer a empresa</a></section><section class="panel"><h2>Perguntas antes de contratar</h2><details><summary>Como é definido o escopo?</summary><p>O levantamento inicial identifica objetivos, volumes, riscos, entregas e critérios de aceite. Uma amostra ou lote piloto pode ser necessário para dimensionar a execução.</p></details><details><summary>Como são tratados documentos confidenciais?</summary><p>A proposta deve definir responsabilidades, acessos, confidencialidade e condições de entrega e retenção de acordo com o acervo.</p></details><details><summary>Posso combinar serviços?</summary><p>Digitalização, organização, OCR, gestão eletrônica e consultoria podem ser avaliados em um projeto integrado, com entregas e responsabilidades definidas.</p></details></section><section><h2>Serviços relacionados</h2><ul>{links}</ul></section></main><footer>Arquindex — Gestão documental e digitalização.<br><a href="https://www.arquindex.com.br/">Portal principal</a> · <a href="{canonical}sitemap.xml">Sitemap deste conteúdo</a></footer></body></html>'''

def build():
 slugs=BASE.joinpath('hosts.txt').read_text().splitlines()
 assert len(slugs)==209 and len(set(slugs))==209
 rows=[]
 for s in slugs:
  assert all(re.fullmatch('[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?',x) for x in s.split('.')),s
  kind='technical' if s in TECHNICAL else 'application' if s in APPS else 'content'
  row={'slug':s,'host':s+'.'+DOMAIN,'kind':kind}
  if kind!='content':
   row['action']='preserve-and-review';rows.append(row);continue
  g=group(s);row.update(canonical=url(g),target=g+'.'+DOMAIN,action='hub' if s==g else 'alias')
  root=OUT/row['host'];root.mkdir(parents=True,exist_ok=True)
  (root/'index.html').write_text(page(s,g))
  (root/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+url(g)+'sitemap.xml\n')
  if s==g:
   (root/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>'+url(g)+'</loc></url></urlset>\n')
   (root/'.htaccess').write_text('Options -Indexes\n')
  else:
   # Alias sitemap redirects to its canonical hub. No foreign-host URLs in urlsets.
   (root/'.htaccess').write_text('Options -Indexes\nRewriteEngine On\nRewriteRule ^(?:index\\.html)?$ '+url(g)+' [R=301,L]\nRewriteRule ^sitemap\\.xml$ '+url(g)+'sitemap.xml [R=301,L]\n')
  rows.append(row)
 # Directory of original, differentiated hubs. This is not a cross-host XML index.
 root=OUT/'portal';root.mkdir(exist_ok=True)
 links=''.join(f'<li><a href="{url(g)}">{e(CONTENT[g][0])}</a></li>' for g in CONTENT)
 (root/'index.html').write_text(f'<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Serviços e guias documentais | Arquindex</title><link rel="canonical" href="https://www.arquindex.com.br/rede-documental/"><style>{CSS}</style><header><a href="https://www.arquindex.com.br/">ARQUINDEX</a></header><main><h1>Serviços e guias documentais</h1><p>Conheça as soluções e os critérios para planejar seu projeto documental.</p><ul>{links}</ul></main></html>')
 (root/'sitemap.xml').write_text('<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://www.arquindex.com.br/rede-documental/</loc></url></urlset>')
 (BASE/'manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 for p in OUT.rglob('sitemap.xml'):ET.parse(p)
 assert {group(s) for s in slugs if s not in TECHNICAL|APPS}<=set(CONTENT)
 assert all(g in slugs for g in CONTENT)
 print(json.dumps({'entries':len(rows),'hubs':len(CONTENT),'aliases':sum(r['action']=='alias' for r in rows),'preserved':sum(r['kind']!='content' for r in rows),'bytes':sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())}))
if __name__=='__main__':build()
