import ftplib,io,os,urllib.request,hashlib
from PIL import Image,ImageDraw,ImageFont
URL="https://arquivo.arquindex.com.br/bh.html"
with urllib.request.urlopen(urllib.request.Request(URL,headers={"Cache-Control":"no-cache"}),timeout=40) as r:
 body=r.read().decode("utf-8");assert r.status==200
assert "Guarda de Documentos em BH: Consulta e Controle" in body
assert 'data-aq-aeo="ARQ-055"' in body or "data-aq-aeo='ARQ-055'" in body
print("DESTINATION_VERIFIED",URL)
im=Image.new("RGB",(1200,1200),"#f4f7fa");d=ImageDraw.Draw(im)
font="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
bold="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def text(x,y,t,size=32,color="#12384c",weight=False):d.text((x,y),t,font=ImageFont.truetype(bold if weight else font,size),fill=color)
d.rectangle((0,0,1200,180),fill="white")
with urllib.request.urlopen("https://www.arquindex.com.br/assets/arquindex-restored/arquindex-logo-oficial.webp",timeout=40) as r:logo=Image.open(io.BytesIO(r.read())).convert("RGBA")
logo.thumbnail((420,130));im.paste(logo,(70,25),logo)
text(70,225,"GUARDA DE DOCUMENTOS EM BH",29,weight=True)
text(70,292,"Consulta e controle",60,weight=True)
text(70,370,"Movimentação registrada, do pedido à devolução",30)
steps=[("01","Solicitar","Identifique caixa e documento"),("02","Autorizar","Confirme quem pode consultar"),("03","Retirar","Registre responsável e data"),("04","Devolver","Confira o retorno do material")]
for i,(n,t,sub) in enumerate(steps):
 y=475+i*133
 d.rounded_rectangle((70,y,1130,y+112),radius=22,fill="white",outline="#d9e2e8",width=2)
 d.ellipse((93,y+22,160,y+89),fill="#12384c")
 text(105,y+36,n,26,"white",True)
 text(190,y+18,t,33,weight=True);text(190,y+64,sub,25)
d.rectangle((0,1080,1200,1200),fill="#12384c")
text(70,1110,"Veja o roteiro: arquivo.arquindex.com.br/bh.html",26,"white")
b=io.BytesIO();im.save(b,"JPEG",quality=94);data=b.getvalue()
name="arq055-guarda-protocolo-20261021.jpg"
with ftplib.FTP_TLS(timeout=60) as f:
 f.connect("ftp.arquindex.com.br",21);f.login("arquind2",os.environ["FTP_PASSWORD"]);f.prot_p()
 def get(p):
  b=bytearray();f.retrbinary("RETR "+p,b.extend);return bytes(b)
 base=None
 for candidate in ["/public_html","/home/arquind2/public_html"]:
  try:
   if b"arquindex" in get(candidate+"/index.html").lower():base=candidate;break
  except ftplib.all_errors:pass
 assert base
 folder=base+"/assets/social-arq055"
 try:f.mkd(folder)
 except ftplib.error_perm as e:
  if not str(e).startswith("550"):raise
 path=folder+"/"+name
 try:old=get(path)
 except ftplib.error_perm:old=None
 if old is not None:assert old==data,"EXISTING_DIFFERENT_ASSET"
 else:f.storbinary("STOR "+path,io.BytesIO(data))
 assert get(path)==data
photo="https://www.arquindex.com.br/assets/social-arq055/"+name
with urllib.request.urlopen(photo,timeout=40) as r:assert r.status==200 and hashlib.sha256(r.read()).digest()==hashlib.sha256(data).digest()
print("IMAGE_PUBLIC_VERIFIED",photo,len(data),hashlib.sha256(data).hexdigest())
