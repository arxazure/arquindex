from pathlib import Path
import runpy, textwrap, subprocess, json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
R=Path(__file__).resolve().parents[1]
x=runpy.run_path(str(R/'scripts/build-design-20261025.py')); DATA=x['DATA'];A=x['assets'];S=x['SOURCES']
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('D',font));pdfmetrics.registerFont(TTFont('DB',bold))
NAVY=HexColor('#052b4d');GREEN=HexColor('#138412');BLUE=HexColor('#006ba7')
def line(c,txt,x,y,width=82,size=11,color=NAVY,leading=17):
 c.setFillColor(color);c.setFont('D',size)
 for p in txt.split('\n'):
  for s in textwrap.wrap(p,width=width):c.drawString(x,y,s);y-=leading
 return y
for slug,title,headline,desc,benefits,steps,criteria,faq,art in DATA:
 path=A/f'manual-{slug}.pdf';c=canvas.Canvas(str(path),pagesize=(595,842));c.setTitle('Manual técnico: '+title);c.setAuthor('Arquindex')
 pages=[('Fluxo e responsabilidades',list(enumerate(steps,1))),('Critérios de aceite e checklist',list(enumerate(criteria,1))),('Contratação e referências',[])]
 for n,(section,rows) in enumerate(pages,1):
  c.setFillColor(NAVY);c.rect(0,735,595,107,fill=1,stroke=0);c.setFillColor(white);c.setFont('DB',24);c.drawString(42,797,'ARQUINDEX');c.setFont('D',10);c.drawString(42,774,'GESTÃO DOCUMENTAL E SOLUÇÕES ECM')
  y=line(c,title,42,706,width=43,size=21,leading=28);y-=22;c.setFillColor(GREEN);c.setFont('DB',15);c.drawString(42,y,section);y-=32
  if n==1:y=line(c,desc,42,y,width=78);y-=16
  for i,text in rows:
   c.setFillColor(BLUE);c.setFont('DB',13);c.drawString(42,y,f'{i:02d}');y=line(c,text,77,y,width=71);y-=30
  if n==1:
   y=line(c,'Responsáveis no projeto',42,y,width=70,size=13);y-=10
   y=line(c,'Cliente: aprova escopo, índices, acessos e critérios de aceite. Arquindex: executa as atividades contratadas e registra pendências. A aprovação técnica e a decisão sobre retenção e destinação permanecem com os responsáveis designados.',42,y,width=80)
  elif n==2:
   y=line(c,'Antes de contratar',42,y,width=70,size=13);y-=12
   for t in ['Informar volume, cidade, formatos e prazo pretendido.','Definir frequência de consulta, usuários e restrições de acesso.','Aprovar critérios de conferência e tratamento de divergências.','Definir logística, responsabilidades e condições de devolução.']:
    y=line(c,'[  ] '+t,42,y,width=78);y-=12
  else:
   for q,a in faq:
    y=line(c,q,42,y,width=68,size=12);y-=5;y=line(c,a,42,y,width=80);y-=22
   y=line(c,'Atendimento',42,y,width=70,size=13);y-=10
   y=line(c,'Belo Horizonte e região metropolitana. Projetos nas capitais sob avaliação técnica e logística. Nenhuma localidade citada indica unidade física da Arquindex.',42,y,width=80);y-=20
   for t,u in S:
    y=line(c,t,42,y,width=80,size=9,leading=13);c.linkURL(u,(42,y,553,y+15),relative=0);y-=15
   y=line(c,'A aplicação de normas depende do contexto. Digitalização não autoriza descarte automático. Não há certificação ou chancela da ANPD ou do CONARQ.',42,y,width=85,size=9,leading=13)
  c.setFillColor(NAVY);c.rect(0,0,595,46,fill=1,stroke=0);c.setFillColor(white);c.setFont('D',9);c.drawString(42,27,'www.arquindex.com.br  |  (31) 97363-2725');c.drawRightString(553,27,f'25/10/2026  •  {n}/3');c.showPage()
 c.save()
 # Video tutorial consists of an editorial briefing and four process steps, with matching captions.
 work=R/'campanhas/design-20261025/video-work'/slug;work.mkdir(parents=True,exist_ok=True)
 scenes=[(title,desc)]+[(f'Etapa {i+1}',s) for i,s in enumerate(steps)]
 vtt=['WEBVTT','']
 for i,(heading,body) in enumerate(scenes):
  doc=work/f'frame-{i}.pdf';v=canvas.Canvas(str(doc),pagesize=(960,540));v.setFillColor(NAVY);v.rect(0,0,960,540,fill=1,stroke=0)
  v.setFillColor(white);v.setFont('DB',26);v.drawString(48,480,'Arquindex');v.setFont('D',12);v.drawRightString(912,480,'VÍDEO EXPLICATIVO')
  y=line(v,heading,48,395,width=39,size=31,color=white,leading=39)
  line(v,body,48,y-25,width=69,size=21,color=white,leading=31)
  v.setFillColor(GREEN);v.rect(0,0,960,67,fill=1,stroke=0);v.setFillColor(white);v.setFont('DB',17);v.drawString(48,27,'www.arquindex.com.br');v.drawRightString(912,27,'WhatsApp (31) 97363-2725');v.save()
  subprocess.run(['pdftoppm','-scale-to','960','-singlefile','-png',str(doc),str(work/f'frame-{i}')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  vtt.extend([f'00:00:{i*6:02d}.000 --> 00:00:{(i+1)*6:02d}.000',heading+'. '+body,''])
 (A/f'{slug}.vtt').write_text('\n'.join(vtt),encoding='utf-8')
 concat=work/'frames.txt';concat.write_text(''.join(f"file '{work/f'frame-{i}.png'}'\nduration 6\n" for i in range(5))+f"file '{work/'frame-4.png'}'\n")
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-vf','fps=12,format=yuv420p','-c:v','libx264','-preset','fast','-crf','25','-movflags','+faststart','-t','30',str(A/f'{slug}.mp4')],check=True)
 print('MEDIA_OK',slug,flush=True)
