"""Acrescenta conteúdo visível por serviço, preservando HTML e backup de produção."""
import ftplib, hashlib, io, json, os, re, ssl, urllib.request
from pathlib import Path
from datetime import datetime, timezone
from bs4 import BeautifulSoup

MARK='aq-respostas-20261022'
ROOT='https://www.arquindex.com.br/'
DATA={
 'digitalizacao': ('Digitalização com OCR: como definir a entrega?', 'A digitalização produz imagens dos documentos; o OCR acrescenta texto para pesquisa. Para uma entrega útil, o projeto também define nomes de arquivos, campos de indexação, controle de qualidade e registro de exceções.', ['Separe os tipos documentais e informe volume, formatos e estado dos originais.','Teste uma amostra representativa, incluindo páginas difíceis, antes de processar o acervo.','Confira campos críticos, sequência das páginas e abertura dos PDFs na entrega.'], 'digitalizacao-com-ocr.html'),
 'gestao': ('O que deve constar em um diagnóstico de gestão documental?', 'O diagnóstico registra tipos documentais, volumes, localização, responsáveis, frequência de consulta e regras de acesso. Essas informações orientam classificação, indexação e procedimentos de movimentação do acervo.', ['Identifique os processos que produzem e utilizam os documentos.','Defina responsáveis e critérios de acesso, localização e controle de versões.','Documente as decisões de guarda e destinação antes de executar qualquer eliminação.'], 'gestao_documental_documentos.html'),
 'guarda': ('Como contratar guarda de documentos com rastreabilidade?', 'A guarda começa com inventário e identificação das unidades armazenadas. O escopo deve estabelecer coleta, protocolo de recebimento, localização das caixas, pessoas autorizadas e prazo para atender consultas.', ['Informe quantidade de caixas, medidas e frequência de consulta.','Combine identificação, lacres, transporte e registro de movimentações.','Defina como solicitar documentos, registrar devoluções e encerrar a custódia.'], 'guarda_de_documentos.html'),
 'lgpd': ('Como dimensionar uma consultoria de adequação à LGPD?', 'O dimensionamento parte dos processos que tratam dados pessoais, sistemas, fornecedores e responsabilidades. O diagnóstico orienta o inventário, a priorização de riscos, as políticas e o plano de ação adequado à organização.', ['Relacione processos, sistemas e categorias de titulares, sem enviar dados pessoais desnecessários.','Defina responsáveis internos e os entregáveis que serão revisados e aprovados.','Estabeleça uma rotina para atualizar registros, capacitar pessoas e acompanhar pendências.'], 'lgpd-consultoria.html'),
 'dpo': ('Como definir a atuação de um DPO terceirizado?', 'O apoio ao encarregado precisa de escopo, canais e responsabilidades claros. O contrato define as rotinas de orientação, o tratamento de solicitações, a interação com as áreas internas e os registros das atividades.', ['Indique o responsável por aprovar decisões e mobilizar as áreas internas.','Combine canal de contato, periodicidade de acompanhamento e regras de escalonamento.','Registre solicitações, orientações, responsáveis e prazos acordados.'], 'dpo-terceirizado.html'),
 'ecm': ('O que avaliar antes de implantar Alfresco ou ECM?', 'Uma implantação de ECM depende da estrutura do acervo e das regras de negócio. Taxonomia, metadados, grupos de acesso, migração e testes de recuperação devem ser definidos junto com a infraestrutura e a operação.', ['Mapeie classes documentais e permissões por grupo de usuários.','Valide importação, pesquisa, versionamento e trilhas de auditoria em um piloto.','Preveja capacidade, monitoramento, backup e teste de restauração no custo total.'], 'gestao_documental_documentos.html'),
 'descarte': ('Como preparar documentos para destinação segura?', 'Antes de destruir documentos, a organização precisa identificar o acervo, verificar as regras de guarda e obter a autorização responsável. O serviço deve registrar coleta, cadeia de custódia, método e evidência da destinação contratada.', ['Identifique séries documentais, períodos e responsáveis pela autorização.','Verifique impedimentos de eliminação e segregue itens que devem permanecer guardados.','Combine protocolo de coleta e conteúdo do comprovante de destinação.'], 'gestao_documental_documentos.html'),
}
def kind(host):
 for term,k in [('incinera','descarte'),('dpo','dpo'),('lgpd','lgpd'),('alfresco','ecm'),('ecm','ecm'),('guarda','guarda'),('gestao','gestao')]:
  if term in host:return k
 return 'digitalizacao'
def fragment(k,url):
 q,a,steps,link=DATA[k]
 city=next((n for s,n in [('contagem','Contagem'),('betim','Betim'),('novalima','Nova Lima'),('embh','Belo Horizonte')] if s in url),'Belo Horizonte e outras localidades')
 items=''.join('<li>'+x+'</li>' for x in steps)
 return f'<section id="{MARK}" aria-label="Respostas e critérios de contratação"><h2>{q}</h2><p><strong>Resposta direta:</strong> {a}</p><h3>Checklist antes de solicitar proposta</h3><ol>{items}</ol><h3>Atendimento e logística</h3><p>Para demandas em {city}, informe onde está o acervo, volume aproximado e prazo desejado. Coleta, execução no local e disponibilidade são confirmadas na proposta; esta página não indica unidade física em cada cidade.</p><p><a href="{ROOT+link}">Conheça o serviço e as opções de entrega</a> · <a href="https://wa.me/5531973632725">Solicitar avaliação pelo WhatsApp</a></p><p>Autoria institucional: Arquindex · Revisão: 22/10/2026.</p></section>'
STYLE=f'<style id="{MARK}-style">#{MARK}{{box-sizing:border-box;max-width:1120px;margin:32px auto;padding:24px;border:1px solid #d9e2ef;border-radius:16px;background:#fff;color:#102a43;font:17px/1.7 system-ui,sans-serif;overflow-wrap:anywhere}}#{MARK} h2,#{MARK} h3{{color:#123d70;line-height:1.3}}#{MARK} a{{color:#085b9f;text-decoration:underline}}@media(max-width:760px){{#{MARK}{{margin:24px 12px;padding:20px}}}}</style>'
def transform(old,k,url):
 s=BeautifulSoup(old.decode('utf-8'),'html.parser')
 assert s.head and s.body and 'arquindex' in s.get_text().lower()
 for ident in [MARK,MARK+'-style',MARK+'-schema']:
  for n in s.find_all(id=ident):n.decompose()
 s.head.append(BeautifulSoup(STYLE,'html.parser'))
 block=BeautifulSoup(fragment(k,url),'html.parser'); target=s.find('footer')
 if target:target.insert_before(block)
 else:s.body.append(block)
 q,a,*_=DATA[k]
 ld=s.new_tag('script',type='application/ld+json',id=MARK+'-schema')
 ld.string=json.dumps({'@context':'https://schema.org','@type':'WebPageElement','@id':url+'#'+MARK,'name':q,'text':a,'isPartOf':{'@id':url},'inLanguage':'pt-BR'},ensure_ascii=False)
 s.head.append(ld)
 out=str(s).encode();check=BeautifulSoup(out,'html.parser')
 assert len(check.find_all('h1'))==len(BeautifulSoup(old,'html.parser').find_all('h1'))
 assert len(check.find_all(id=MARK))==1
 return out
def get(f,p):
 b=bytearray();f.retrbinary('RETR '+p,b.extend);return bytes(b)
def put(f,p,b):
 f.storbinary('STOR '+p,io.BytesIO(b));assert get(f,p)==b
def public(url):
 req=urllib.request.Request(url,headers={'User-Agent':'ArquindexEditorial/1.0','Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=20) as r:return r.status,r.url,r.read(),r.headers
def main():
 hosts=json.loads(Path('seo-regional/56-sites/manifest.json').read_text())
 targets=[('www.arquindex.com.br',p,k) for p,k in [('index.html','gestao'),('digitalizacao.html','digitalizacao'),('digitalizacao-com-ocr.html','digitalizacao'),('gestao_documental_documentos.html','gestao'),('guarda_de_documentos.html','guarda'),('lgpd-consultoria.html','lgpd'),('dpo-terceirizado.html','dpo')]]
 targets += [(x['host'],'index.html',kind(x['host'])) for x in hosts]
 report=[];stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
 with ftplib.FTP_TLS(context=ssl.create_default_context(),timeout=45) as f:
  f.connect('h59.servidorhh.com',21);f.login('arquind2',os.environ['FTP_PASSWORD']);f.prot_p()
  assert b'arquindex' in get(f,'/public_html/index.html').lower()
  backup='/seo-backups/blocos-aeo-'+stamp
  try:f.mkd('/seo-backups')
  except ftplib.error_perm:pass
  f.mkd(backup);put(f,backup+'/.htaccess',b'Require all denied\n')
  for host,filename,k in targets:
   url='https://'+host+('/' if filename=='index.html' else '/'+filename)
   row={'url':url,'status':'skipped'};report.append(row)
   try:
    status,final,body,headers=public(url)
    assert status==200 and final==url,'PUBLIC_REDIRECT_OR_STATUS'
    parsed=BeautifulSoup(body,'html.parser')
    assert 'noindex' not in headers.get('X-Robots-Tag','').lower()
    assert not any('noindex' in m.get('content','').lower() for m in parsed.find_all('meta',attrs={'name':'robots'}))
    candidates=['/public_html/'+filename] if host=='www.arquindex.com.br' else ['/public_html/subdominios/'+host+'/'+filename,'/public_html/'+host+'/'+filename,'/subdominios/'+host+'/'+filename,'/'+host+'/'+filename]
    path=old=None
    for candidate in candidates:
     try:old=get(f,candidate);path=candidate;break
     except ftplib.error_perm:pass
    assert path and old,'FTP_TARGET_MISSING'
    source=BeautifulSoup(old,'html.parser');canonical=source.find('link',rel='canonical')
    assert not canonical or canonical.get('href')==url,'CANONICAL_CONFLICT'
    out=transform(old,k,url)
    bp=backup+'/'+hashlib.sha256(path.encode()).hexdigest()+'.html';put(f,bp,old)
    assert get(f,path)==old,'CONCURRENT_CHANGE'
    put(f,path,out)
    try:
     st,fin,b,h=public(url)
     assert st==200 and fin==url and ('id="'+MARK+'"').encode() in b,'PUBLIC_MARKER_MISSING'
    except Exception:
     assert get(f,path)==out;put(f,path,old);raise
    row.update(status='published',path=path,backup=bp,sha256=hashlib.sha256(out).hexdigest())
   except Exception as e:row['reason']=str(e)
   print(json.dumps(row,ensure_ascii=False),flush=True)
  # Submit only URLs verified after this publication. Reuse the publicly verified key.
  try:
   key=get(f,'/public_html/indexnow-key.txt').decode().strip();assert re.fullmatch('[A-Za-z0-9-]{8,128}',key)
   keyurl=ROOT+key+'.txt';assert public(keyurl)[2].decode().strip()==key
   urls=[x['url'] for x in report if x['status']=='published' and x['url'].startswith(ROOT)]
   if urls:
    req=urllib.request.Request('https://api.indexnow.org/indexnow',data=json.dumps({'host':'www.arquindex.com.br','key':key,'keyLocation':keyurl,'urlList':urls}).encode(),headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=30) as r:print('INDEXNOW_SUBMISSION_HTTP',r.status,flush=True)
  except Exception as e:print('INDEXNOW_PENDING',str(e),flush=True)
 Path('publish-report').mkdir(exist_ok=True)
 Path('publish-report/blocos-aeo-20261022.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print('PUBLISHED',sum(x['status']=='published' for x in report),'OF',len(report),flush=True)
if __name__=='__main__':main()
