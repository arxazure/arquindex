import os,io,ftplib,datetime,posixpath,urllib.request,xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE='https://www.arquindex.com.br/'
PAGE='riscos-documentais-engenharia.html'
URL=BASE+PAGE
ASSETS='campanha-engenharia-2026'
OUT=Path(os.environ.get('CAMPAIGN_OUTPUT','campaign-output'));OUT.mkdir(exist_ok=True)
slides=[('GUIA PARA GESTORES','O custo invisível do caos documental','Quatro riscos para engenharia, mineração e construção civil.'),('RISCO 01','Manutenção sem a informação necessária','Manuais e desenhos dispersos dificultam o planejamento e a consulta técnica.'),('RISCO 02','Auditorias com evidências incompletas','Registros sem classificação e origem clara aumentam o esforço de resposta.'),('RISCO 03','Revisões conflitantes','Uma pasta cheia de arquivos não informa qual versão está aprovada para uso.'),('RISCO 04','Entrega documental com lacunas','Sem índice e conferência, certificados e registros podem ficar fora do conjunto final.'),('PRÓXIMO PASSO','Organize antes de precisar','A Arquindex estrutura acervos e Databooks conforme o projeto. Solicite uma avaliação.')]
fontpaths=['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
def font(size,bold=False): return ImageFont.truetype(fontpaths[int(bold)],size)
def wrap(draw,text,f,width):
    lines=[];line=''
    for w in text.split():
        trial=(line+' '+w).strip()
        if draw.textlength(trial,font=f)>width and line:lines.append(line);line=w
        else:line=trial
    if line:lines.append(line)
    return '\n'.join(lines)
files={}
for n,(tag,title,body) in enumerate(slides,1):
    im=Image.new('RGB',(1080,1350),'#112d43');d=ImageDraw.Draw(im)
    d.rectangle((0,0,22,1350),fill='#31d2ad');d.text((80,74),'ARQUINDEX',font=font(44,True),fill='white')
    d.text((80,150),'GESTÃO DOCUMENTAL • DATABOOKS',font=font(24),fill='#a9c5d2')
    d.rounded_rectangle((80,260,450,322),radius=14,fill='#31d2ad');d.text((100,275),tag,font=font(24,True),fill='#112d43')
    titletext=wrap(d,title,font(70,True),900)
    d.multiline_text((80,370),titletext,font=font(70,True),fill='white',spacing=17)
    box=d.multiline_textbbox((80,370),titletext,font=font(70,True),spacing=17)
    yy=max(735,box[3]+70)
    d.multiline_text((80,yy),wrap(d,body,font(37),900),font=font(37),fill='#d3e7ef',spacing=15)
    d.line((80,1150,1000,1150),fill='#537387',width=2)
    d.text((80,1190),'www.arquindex.com.br',font=font(28),fill='#31d2ad')
    d.text((900,1190),f'{n}/6',font=font(28,True),fill='white')
    b=io.BytesIO();im.save(b,format='JPEG',quality=93);files[f'{ASSETS}/risco-{n:02d}.jpg']=b.getvalue()
body='''<p class="eyebrow">ENGENHARIA • MINERAÇÃO • CONSTRUÇÃO CIVIL</p><h1>Quatro riscos do caos documental na engenharia</h1><p class="lead">Uma planta sem revisão identificada, um certificado fora do Databook ou um manual difícil de localizar podem comprometer a resposta da equipe. A organização do acervo faz parte do planejamento da operação.</p><p><a class="button" href="https://wa.me/5531973632725?text=Gostaria%20de%20avaliar%20meu%20acervo%20t%C3%A9cnico">Solicitar avaliação do acervo técnico</a></p><img class="cover" src="/campanha-engenharia-2026/risco-01.jpg" alt="Quatro riscos documentais para engenharia, mineração e construção civil" width="1080" height="1350"><p>A informação técnica acompanha o ciclo de vida de obras, equipamentos e instalações. Seu valor depende também de contexto: origem, projeto, disciplina, revisão e condições de uso. Reunir documentos em uma pasta é apenas uma etapa; conferir a completude e identificar a versão aplicável são tarefas diferentes.</p><h2>1. Manutenção sem a informação necessária</h2><p>Manuais, desenhos técnicos e registros de inspeção dispersos dificultam a preparação de uma intervenção. A equipe pode precisar consultar várias fontes para entender qual documento corresponde ao equipamento e à configuração instalada.</p><p>Comece identificando os equipamentos críticos e os documentos necessários para cada consulta. Classifique o conjunto com identificadores consistentes e preserve a relação entre documento, equipamento e projeto. A digitalização precisa manter legíveis linhas, números e carimbos.</p><h2>2. Auditorias com evidências incompletas</h2><p>Uma solicitação de auditoria exige reunir evidências pertinentes e verificar sua origem. Quando o acervo não tem índice ou os registros estão fragmentados, a busca e a conferência demandam mais esforço. As consequências dependem das obrigações e do contexto de cada operação.</p><p>Um inventário de documentos recebidos, uma lista de pendências e critérios de aceite ajudam a acompanhar a completude do conjunto. O projeto deve definir quem confere, quem aprova e como são registradas as exceções.</p><h2>3. Revisões conflitantes de projetos</h2><p>Arquivos com nomes semelhantes podem representar versões diferentes. Uma data de modificação não substitui, por si só, o controle de revisão e aprovação. Também é necessário distinguir o histórico preservado dos documentos liberados para o uso pretendido.</p><p>Defina campos para código, revisão, status e responsável pela aprovação. Em um GED/ECM, permissões e fluxos devem refletir essas decisões. O sistema auxilia o controle; os critérios e responsabilidades precisam ser estabelecidos pela organização.</p><h2>4. Entrega documental com lacunas</h2><p>Na conclusão de uma obra ou fornecimento, certificados, relatórios e desenhos precisam compor o conjunto acordado. A montagem do Databook exige comparar os documentos disponíveis com o índice e com os requisitos contratuais do projeto.</p><p>Registre o que foi recebido, o que está pendente e o que precisa de correção. A entrega final deve permitir reconhecer a estrutura, localizar cada item e consultar os documentos na sequência definida. Não existe um índice universal adequado a todos os contratos.</p><h2>Campos úteis para estruturar o acervo</h2><div class="table"><table><tr><th>Campo</th><th>Aplicação</th><th>Exemplo fictício</th></tr><tr><td>Projeto e área</td><td>Relacionar documento à instalação</td><td>Projeto Alfa / Utilidades</td></tr><tr><td>Equipamento</td><td>Apoiar consulta por ativo</td><td>Bomba B-014</td></tr><tr><td>Disciplina</td><td>Organizar o conteúdo técnico</td><td>Mecânica</td></tr><tr><td>Código e revisão</td><td>Distinguir versões</td><td>DES-014 / Rev. 03</td></tr><tr><td>Status</td><td>Identificar a condição de uso</td><td>Em análise / Aprovado</td></tr><tr><td>Fornecedor e tipo</td><td>Localizar registros relacionados</td><td>Fornecedor exemplo / Certificado</td></tr></table></div><h2>Como a Arquindex pode apoiar</h2><p>A Arquindex atua em organização, digitalização e estruturação de acervos e Databooks empresariais. O escopo pode contemplar preparação física, captura, OCR, classificação, indexação e conferência, conforme as características do acervo e os critérios de aceite acordados.</p><ol><li><strong>Levantamento:</strong> identificar volume, formatos, estado físico, finalidade e necessidades de consulta.</li><li><strong>Estrutura:</strong> definir índice, campos, nomenclatura e responsabilidades de conferência.</li><li><strong>Processamento:</strong> organizar e digitalizar conforme os requisitos definidos.</li><li><strong>Conferência:</strong> avaliar legibilidade, sequência, indexação e pendências.</li><li><strong>Entrega:</strong> disponibilizar o conjunto e seus registros conforme o escopo contratado.</li></ol><h2>OCR e preparação do acervo para IA</h2><p>O OCR acrescenta texto pesquisável, mas pode apresentar erros. Números, identificadores e documentos degradados exigem atenção na validação. Antes de considerar busca semântica ou um assistente com RAG, é necessário avaliar texto, metadados, versões, permissões e fontes de resposta.</p><p>A preparação documental e a implantação de uma solução de IA são escopos distintos. Um piloto deve usar perguntas representativas e conferir as respostas contra os documentos de origem, respeitando os acessos autorizados.</p><h2>Perguntas frequentes</h2><details><summary>Qual deve ser o índice de um Databook?</summary><p>O índice depende dos requisitos do projeto, do contrato e do destinatário. Deve ser definido e conferido com os responsáveis pelo aceite.</p></details><details><summary>Digitalizar permite eliminar os originais?</summary><p>Não automaticamente. A destinação exige avaliação documental e jurídica, incluindo temporalidade, valor histórico e regras aplicáveis. O Decreto 10.278/2020 prevê condições e distinções conforme o contexto de uso.</p></details><details><summary>A pesquisa por OCR encontra tudo?</summary><p>Não há garantia universal. O resultado depende da qualidade e do conteúdo do original, do processamento e da conferência dos campos necessários.</p></details><details><summary>Como solicitar uma avaliação?</summary><p>Informe o setor, os tipos documentais, o volume aproximado e a finalidade de uso. Documentos confidenciais devem ser compartilhados somente pelo canal e com as condições de segurança acordados.</p></details><section class="cta"><h2>Organize antes de precisar</h2><p>Converse com a Arquindex sobre seu acervo técnico, documentação de obra ou Databook. Atendimento a partir de Belo Horizonte, conforme escopo e disponibilidade.</p><a class="button" href="https://wa.me/5531973632725?text=Gostaria%20de%20avaliar%20meu%20acervo%20t%C3%A9cnico">Falar com a Arquindex</a></section><h2>Continue a leitura</h2><ul><li><a href="/montagem_databook_organizar.html">Montagem e organização de Databooks</a></li><li><a href="/digitalizacao-com-ocr.html">Digitalização com OCR</a></li><li><a href="/">Serviços da Arquindex</a></li><li><a href="https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10278.htm">Decreto 10.278/2020 — texto oficial</a></li></ul>'''
page='''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Quatro riscos documentais na engenharia | Arquindex</title><meta name="description" content="Entenda quatro riscos de acervos técnicos desorganizados e como estruturar Databooks, plantas, revisões e certificados com a Arquindex."><meta name="robots" content="index,follow"><link rel="canonical" href="'''+URL+'''"><meta property="og:type" content="article"><meta property="og:title" content="Quatro riscos do caos documental na engenharia"><meta property="og:description" content="Rastreabilidade de documentos para engenharia, mineração e construção civil."><meta property="og:url" content="'''+URL+'''"><meta property="og:image" content="'''+BASE+ASSETS+'''/risco-01.jpg"><style>*{box-sizing:border-box}body{margin:0;font:18px/1.75 system-ui,sans-serif;color:#183247;background:#fff}header,footer{background:#112d43;color:white;padding:22px 6%}header a,footer a{color:white}main{max-width:1000px;padding:45px 24px;margin:auto}h1{font-size:clamp(2.1rem,5vw,3.6rem);line-height:1.12}h2{line-height:1.3;color:#075f6a;margin-top:42px}.eyebrow{font-size:14px;font-weight:700;color:#08766a}.lead{font-size:23px}.button{display:inline-block;padding:14px 22px;background:#08755f;color:white;text-decoration:none;border-radius:9px}.cover{float:right;width:235px;height:auto;margin:20px 0 24px 28px;border-radius:10px}a{color:#075c89}table{border-collapse:collapse;width:100%;font-size:16px}td,th{border:1px solid #cedbe2;padding:12px;text-align:left}.table{overflow:auto}th,.cta{background:#eff7f6}.cta{padding:24px;border-radius:12px}details{padding:15px 0;border-bottom:1px solid #ccd8de}summary{font-weight:bold;cursor:pointer}@media(max-width:600px){.cover{float:none;width:100%;max-width:360px;margin:10px 0}.lead{font-size:20px}}</style></head><body><header><a href="/">ARQUINDEX</a> · Gestão documental e digitalização</header><main>'''+body+'''</main><footer>Arquindex · Belo Horizonte/MG · <a href="/">Site principal</a></footer></body></html>'''
files[PAGE]=page.encode()
for name,data in files.items():
    path=OUT/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
if os.environ.get('PUBLISH_CAMPAIGN')!='true':
    print('LOCAL_READY',len(files));raise SystemExit(0)
assert os.environ.get('FTP_PASSWORD'),'FTP_PASSWORD ausente'
f=ftplib.FTP(os.environ['FTP_HOST'],timeout=45);f.login(os.environ['FTP_USERNAME'],os.environ['FTP_PASSWORD']);f.cwd('public_html')
root=f.pwd();parent=posixpath.dirname(root.rstrip('/'));assert parent and parent!=root
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
backup=parent+'/backup-campanha-engenharia-'+stamp
f.mkd(backup)
def read(name):
    b=bytearray()
    try:f.retrbinary('RETR '+name,b.extend)
    except ftplib.error_perm as e:
        if str(e).startswith('550'):return None
        raise
    return bytes(b)
NS='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',NS)
original={};changes=dict(files)
sitemap=read('sitemap.xml')
assert sitemap,'sitemap.xml ausente'
tree=ET.fromstring(sitemap)
if tree.tag=='{'+NS+'}sitemapindex':
    smname='sitemap-campanha-engenharia.xml';sm=ET.Element('{'+NS+'}urlset');el=ET.SubElement(sm,'{'+NS+'}url');ET.SubElement(el,'{'+NS+'}loc').text=URL
    changes[smname]=ET.tostring(sm,encoding='utf-8',xml_declaration=True)
    if BASE+smname not in [x.text for x in tree.iter('{'+NS+'}loc')]:
        el=ET.SubElement(tree,'{'+NS+'}sitemap');ET.SubElement(el,'{'+NS+'}loc').text=BASE+smname
        changes['sitemap.xml']=ET.tostring(tree,encoding='utf-8',xml_declaration=True)
elif tree.tag=='{'+NS+'}urlset':
    if URL not in [x.text for x in tree.iter('{'+NS+'}loc')]:
        el=ET.SubElement(tree,'{'+NS+'}url');ET.SubElement(el,'{'+NS+'}loc').text=URL
        changes['sitemap.xml']=ET.tostring(tree,encoding='utf-8',xml_declaration=True)
else:raise RuntimeError('Tipo de sitemap inesperado')
home=read('index.html')
if home and PAGE.encode() not in home:
    text=home.decode('utf-8');assert '</body>' in text
    block='<aside style="max-width:1100px;margin:28px auto;padding:22px;background:#eef7f6"><h2>Engenharia, mineração e construção</h2><p>Conheça <a href="/'+PAGE+'">quatro riscos do caos documental e como estruturar seu acervo técnico</a>.</p></aside>'
    changes['index.html']=text.replace('</body>',block+'</body>',1).encode()
for n in changes:
    original[n]=read(n)
    if original[n] is not None:f.storbinary('STOR '+backup+'/'+n.replace('/','__'),io.BytesIO(original[n]))
try:f.mkd(ASSETS)
except ftplib.error_perm: f.cwd(ASSETS);f.cwd(root)
applied=[]
try:
    for n,data in changes.items():
        f.storbinary('STOR '+n,io.BytesIO(data));applied.append(n);assert read(n)==data
    for n in [PAGE]+[x for x in files if x.endswith('.jpg')]:
        req=urllib.request.Request(BASE+n,headers={'Cache-Control':'no-cache','User-Agent':'ArquindexCampaign/1.0'})
        with urllib.request.urlopen(req,timeout=40) as r:
            assert r.status==200;data=r.read()
            assert data==files[n], 'Conteudo publico divergente: '+n
        print('PUBLIC_VERIFIED',BASE+n,flush=True)
except Exception:
    for n in reversed(applied):
        if original[n] is None:f.delete(n)
        else:f.storbinary('STOR '+n,io.BytesIO(original[n]))
    raise
finally:f.quit()
print('CAMPAIGN_DEPLOYED',URL,flush=True)
