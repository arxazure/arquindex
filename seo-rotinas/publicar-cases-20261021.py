#!/usr/bin/env python3
"""Atualização não destrutiva da vitrine Arquindex, com backup e verificação pública."""
import ftplib, hashlib, html, io, json, os, re, socket, ssl, time, urllib.request
from datetime import datetime, timezone
from bs4 import BeautifulSoup

BASE_URL="https://www.arquindex.com.br/"
PATH="clientes-cases/index.html"
MARKER="arquindex-cases-autorizados-20261021"
STAMP=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
CASES=[
 ("Drogaria Araújo","Digitalização e processamento de cupons de venda e formulários da Farmácia Popular.","assets/arquindex-restored/editorial-digitalizacao.webp","/digitalizacao.html"),
 ("Drogaria Araújo","Digitalização de documentos do Departamento Pessoal.","assets/arquindex-restored/editorial-digitalizacao.webp","/gestao_de_colaboradores_documentos.html"),
 ("CBMM","Digitalização de Databooks de engenharia e acervo técnico.","images/editorial-citygusa.webp","/montagem_databook_organizar.html"),
 ("Belocal — Grupo Lhoist","Digitalização do acervo técnico de plantas de engenharia da fábrica e de manutenção.","images/editorial-lhoist.webp","/digitalizacao.html"),
 ("Cemig Igarapé","Digitalização do acervo técnico de manutenção da planta.","images/editorial-petrobras.webp","/digitalizacao.html"),
 ("Catta Preta Advogados","Virtualização do acervo de processos jurídicos.","images/editorial-cimcop.webp","/digitalizacao.html"),
 ("Tereza Mafra Advocacia","Virtualização do acervo de processos jurídicos.","images/editorial-superconcreto.webp","/digitalizacao.html"),
]
def sha(b):return hashlib.sha256(b).hexdigest()
def get(ftp,p):
    b=io.BytesIO();ftp.retrbinary("RETR "+p,b.write);return b.getvalue()
def put(ftp,p,b):ftp.storbinary("STOR "+p,io.BytesIO(b))
def fetch(url):
    req=urllib.request.Request(url+"?casescheck="+str(int(time.time())),headers={"User-Agent":"ArquindexCasesCheck/1.0","Cache-Control":"no-cache"})
    with urllib.request.urlopen(req,timeout=30) as r:return r.status,r.url,r.headers,r.read()
def make_block():
    rows=[]
    for name,desc,img,link in CASES:
        name,desc,img,link=map(lambda x:html.escape(x,quote=True),(name,desc,img,link))
        rows.append(f'<article class="arq-case-card"><img src="/{img}" width="460" height="180" loading="lazy" decoding="async" alt="Imagem editorial ilustrativa sobre documentação empresarial; não representa instalações de {name}"><div class="arq-case-content"><h3>{name}</h3><p>{desc}</p><a href="{link}">Conheça o serviço relacionado →</a><small>Imagem editorial ilustrativa, não é fotografia do cliente.</small></div></article>')
    return f'''
<!-- BEGIN {MARKER} -->
<section id="{MARKER}" aria-labelledby="arq-cases-heading">
  <style>
  #{MARKER}{{max-width:1200px;margin:2rem auto;padding:1.5rem 1rem;color:#182c41}}
  #{MARKER} h2{{color:#07365b;font-size:clamp(1.5rem,3vw,2.1rem);margin:0 0 1rem}}
  #{MARKER} .arq-case-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,270px),1fr));gap:1rem;margin-top:1.5rem}}
  #{MARKER} .arq-case-card{{background:#fff;border:1px solid #d6e0e9;border-radius:12px;overflow:hidden;box-shadow:0 5px 18px rgba(0,32,64,.08)}}
  #{MARKER} .arq-case-card img{{display:block;width:100%;height:175px;object-fit:cover;background:#e6eef5}}
  #{MARKER} .arq-case-content{{padding:1rem 1.1rem}}
  #{MARKER} .arq-case-content h3{{font-size:1.1rem;color:#07365b;margin:0 0 .7rem}}
  #{MARKER} .arq-case-content p{{line-height:1.55;margin:0 0 .8rem}}
  #{MARKER} .arq-case-content a{{color:#075a9b;text-decoration:underline;text-underline-offset:3px;font-weight:650}}
  #{MARKER} .arq-case-content small{{display:block;color:#5b6b7c;margin-top:.8rem}}
  </style>
  <h2 id="arq-cases-heading">Mais projetos de digitalização, RH, engenharia e acervos jurídicos</h2>
  <p>Projetos informados e autorizados para divulgação pela Arquindex. As descrições resumem o escopo dos serviços sem expor informações confidenciais, quantidades ou resultados não verificados.</p>
  <div class="arq-case-grid">{''.join(rows)}</div>
  <p style="margin-top:1.3rem">Precisa organizar um acervo semelhante? <a href="https://www.arquindex.com.br/">Conheça a Arquindex</a> ou fale pelo <a href="https://wa.me/5531973632725">WhatsApp (31) 97363-2725</a> e <a href="mailto:comercial@arquindex.com.br">comercial@arquindex.com.br</a>.</p>
</section>
<!-- END {MARKER} -->'''
def patch(original):
    text=original.decode("utf-8")
    soup=BeautifulSoup(text,"html.parser")
    assert soup.find("main"),"MAIN_MISSING"
    assert len(soup.find_all("h1"))==1,"H1_UNEXPECTED"
    assert soup.find(string=re.compile("Experiências com clientes",re.I)),"CASES_HEADING_MISSING"
    assert soup.find(string=re.compile("Abordagens",re.I)),"ABORDAGENS_MISSING"
    block=make_block()
    if f'<!-- BEGIN {MARKER} -->' in text:
        pattern=r'<!-- BEGIN '+MARKER+r' -->.*?<!-- END '+MARKER+r' -->'
        text,count=re.subn(pattern,lambda _:block,text,count=1,flags=re.S)
        assert count==1,"MARKER_REPLACE_FAILED"
    else:
        # Inserir antes da seção de Abordagens, sem alterar conteúdo existente.
        heading=re.search(r'<h2\b[^>]*>\s*Abordagens\s*</h2>',text,re.I)
        assert heading,"ABORDAGENS_HEADING_NOT_FOUND"
        sections=list(re.finditer(r'<section\b[^>]*>',text[:heading.start()],re.I))
        assert sections,"SECTION_NOT_FOUND"
        at=sections[-1].start()
        text=text[:at]+block+"\n"+text[at:]
    after=BeautifulSoup(text,"html.parser")
    assert len(after.select("#"+MARKER))==1,"DUPLICATE_BLOCK"
    assert len(after.select("#"+MARKER+" .arq-case-card"))==7,"SEVEN_PROJECTS_REQUIRED"
    assert len(after.find_all("h1"))==1,"H1_CHANGED"
    assert [str(x) for x in soup.find_all("script")]==[str(x) for x in after.find_all("script")],"SCRIPTS_CHANGED"
    assert [str(x) for x in soup.find_all("form")]==[str(x) for x in after.find_all("form")],"FORMS_CHANGED"
    assert soup.h1.get_text(" ",strip=True)==after.h1.get_text(" ",strip=True),"H1_TEXT_CHANGED"
    return text.encode("utf-8")
def main():
    pw=os.environ.get("FTP_PASSWORD")
    assert pw,"FTP_PASSWORD_MISSING"
    host=(os.environ.get("FTP_TLS_HOST") or "h59.servidorhh.com").strip()
    remote=(os.environ.get("FTP_REMOTE_DIR") or "public_html").strip("/")
    assert re.fullmatch(r"[a-zA-Z0-9._-]+",remote),"UNSAFE_REMOTE_DIR"
    expected=set(socket.gethostbyname_ex("ftp.arquindex.com.br")[2])
    assert expected.intersection(socket.gethostbyname_ex(host)[2]),"HOSTING_IP_MISMATCH"
    ctx=ssl.create_default_context()
    ctx.minimum_version=ssl.TLSVersion.TLSv1_2
    with ftplib.FTP_TLS(timeout=50,context=ctx) as ftp:
        ftp.connect(host,21)
        assert ftp.sock.getpeername()[0] in expected,"UNEXPECTED_REMOTE_IP"
        ftp.auth()
        print("TLS_CERTIFICATE_VERIFIED",host)
        ftp.login("arquind2",pw)
        ftp.prot_p()
        ftp.cwd(remote)
        print("REMOTE_ROOT_CONFIRMED",ftp.pwd())
        before=get(ftp,PATH)
        assert b"arquindex" in before.lower(),"UNEXPECTED_DESTINATION"
        desired=patch(before)
        if desired==before:
            print("CASES_ALREADY_CURRENT",sha(desired))
        else:
            backup=PATH+".backup."+STAMP
            put(ftp,backup,before)
            assert get(ftp,backup)==before,"BACKUP_NOT_VERIFIED"
            assert get(ftp,PATH)==before,"CONCURRENT_CHANGE"
            print("BACKUP_VERIFIED",backup,sha(before))
            try:
                put(ftp,PATH,desired)
                assert get(ftp,PATH)==desired,"UPLOAD_VERIFY_FAILED"
                print("UPLOAD_VERIFIED",sha(desired))
            except Exception:
                if get(ftp,PATH)==desired:
                    put(ftp,PATH,before)
                    assert get(ftp,PATH)==before,"ROLLBACK_FAILED"
                raise
    url=BASE_URL+"clientes-cases/"
    for attempt in range(5):
        try:
            status,final,headers,body=fetch(url)
            assert status==200 and final.startswith(url),"PUBLIC_STATUS_OR_REDIRECT"
            assert MARKER.encode() in body,"PUBLIC_MARKER_MISSING"
            assert len(BeautifulSoup(body,"html.parser").select("#"+MARKER+" .arq-case-card"))==7,"PUBLIC_CARDS_MISSING"
            assert "noindex" not in headers.get("X-Robots-Tag","").lower(),"PUBLIC_NOINDEX"
            print("CASES_PUBLIC_HTTP200_CONTENT_VERIFIED",url,sha(body))
            return
        except Exception as exc:
            print("PUBLIC_RETRY",attempt+1,type(exc).__name__,str(exc)[:130])
            if attempt==4:raise
            time.sleep(8)
if __name__=="__main__":main()
