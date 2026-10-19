#!/usr/bin/env python3
"""Existing-first SEO improvement: guarded, idempotent, fully reversible FTP deploy."""
import ftplib
import io
import os
import re
import sys
import ssl
import time
import urllib.request
from datetime import datetime, timezone

BASE = "https://www.arquindex.com.br/"
FTP_HOST = os.getenv("FTP_HOST", "")
FTP_USER = os.getenv("FTP_USERNAME", "")
FTP_PASSWORD = os.getenv("FTP_PASSWORD", "")
MARKER = "arquindex-seo-existing-first-20261018"
ANCHOR = re.compile(r"(<h2\b[^>]*>\s*Escolha o servi(?:ç|&ccedil;)o para sua necessidade\s*</h2>)", re.I)
CONTENT = {
    "guarda_de_documentos.html": """<!-- arquindex-seo-existing-first-20261018:guarda -->
<section id="guarda-documental-orcamento" aria-labelledby="guarda-orcamento-titulo" style="max-width:1040px;margin:2rem auto;padding:1.4rem;border:1px solid #dbe5ec;border-radius:12px">
<h2 id="guarda-orcamento-titulo">Quanto custa a guarda de documentos empresariais em Belo Horizonte?</h2>
<p>O custo da guarda de documentos depende da quantidade de caixas, da necessidade de inventário, da organização inicial e da frequência de consultas e movimentações. Coleta, acondicionamento, digitalização sob demanda e prazos de atendimento são definidos conforme o escopo. Por isso, comparar somente a mensalidade por caixa pode esconder custos de acesso e de recuperação. A Arquindex avalia o acervo e prepara uma proposta comercial adequada ao uso de cada departamento.</p>
<h3>O que avaliar antes de contratar a guarda física</h3>
<ul>
<li><strong>Inventário e rastreabilidade:</strong> identificação de caixas e tipos documentais, unidade de origem, período e responsáveis autorizados.</li>
<li><strong>Coleta e logística:</strong> conferência de volumes, protocolos de retirada, condições de transporte, devoluções e registro de movimentações.</li>
<li><strong>Consulta documental:</strong> definir quando a equipe precisa do original, quando uma cópia digital atende e como solicitar a localização.</li>
<li><strong>Temporalidade e destinação:</strong> revisar prazos de guarda e regras aplicáveis; digitalizar não significa autorizar descarte automático.</li>
</ul>
<h3>Guarda de arquivos com digitalização e OCR</h3>
<p>Empresas que consultam contratos, dossiês de colaboradores, documentos fiscais e registros técnicos podem combinar a guarda física com <a href="/digitalizacao.html">digitalização empresarial</a>, <a href="/digitalizacao-com-ocr.html">OCR para pesquisa</a> e <a href="/gestao_documental_documentos.html">classificação e gestão documental</a>. A decisão entre digitalizar todo o acervo ou apenas documentos demandados considera custo, prazo, risco e frequência de consulta.</p>
<h3>Perguntas frequentes sobre guarda de documentos</h3>
<details><summary>Como pedir um orçamento de guarda documental?</summary><p>Informe cidade, número aproximado de caixas, tipos documentais, necessidade de coleta, periodicidade de consultas e eventual digitalização. Uma amostragem ajuda a dimensionar o projeto.</p></details>
<details><summary>A guarda de documentos inclui digitalização?</summary><p>São serviços diferentes e complementares. A proposta especifica se haverá captura, OCR, indexação e entrega digital, além do armazenamento físico.</p></details>
<details><summary>É possível consultar um documento guardado?</summary><p>A forma de consulta, os usuários autorizados e os prazos de atendimento devem constar do contrato. Para consultas frequentes, vale avaliar digitalização sob demanda.</p></details>
<p><strong>ARQUINDEX - Gestão Documental e Digitalização.</strong> Site: <a href="https://www.arquindex.com.br/">www.arquindex.com.br</a>. Orçamentos: <a href="https://wa.me/5531973632725?text=Quero%20orcamento%20de%20guarda%20documental">WhatsApp (31) 97363-2725</a> ou <a href="mailto:comercial@arquindex.com.br">comercial@arquindex.com.br</a>.</p>
</section>
<!-- /arquindex-seo-existing-first-20261018:guarda -->""",
    "digitalizacao-com-ocr.html": """<!-- arquindex-seo-existing-first-20261018:ocr -->
<section id="ocr-empresarial-orcamento" aria-labelledby="ocr-orcamento-titulo" style="max-width:1040px;margin:2rem auto;padding:1.4rem;border:1px solid #dbe5ec;border-radius:12px">
<h2 id="ocr-orcamento-titulo">OCR para empresas: como avaliar preço, qualidade e indexação</h2>
<p>OCR é o reconhecimento de caracteres em imagens digitalizadas. O resultado pode permitir pesquisar termos dentro de PDFs, mas não garante, por si só, a correção de nomes, valores, datas e identificadores. Em projetos empresariais, o orçamento considera número de páginas, qualidade dos originais, idioma, tipos documentais e regras de indexação. A Arquindex pode combinar <a href="/digitalizacao.html">digitalização e OCR</a> com critérios de aceite definidos antes do processamento.</p>
<h3>Diferença entre PDF pesquisável e indexação de documentos</h3>
<p>O PDF pesquisável preserva a imagem e inclui texto para busca. A indexação utiliza campos estruturados, como tipo documental, funcionário, contrato, setor, data ou número de processo. Quando o cliente precisa localizar rapidamente o documento correto, a revisão de campos críticos costuma ser tão importante quanto a camada de texto.</p>
<h3>Checklist para solicitar orçamento de OCR</h3>
<ul>
<li>Informe o volume estimado de páginas, formatos físicos e condições de leitura.</li>
<li>Indique se deseja PDF/A, PDF pesquisável, extração de dados ou cadastro de metadados.</li>
<li>Liste os campos críticos que devem ser conferidos e os critérios de aceite.</li>
<li>Defina a entrega: pastas organizadas, <a href="/gestao_documental_documentos.html">sistema de gestão documental</a> ou outro repositório.</li>
</ul>
<p>Para projetos sujeitos aos requisitos de digitalização do Decreto 10.278/2020, a análise técnica também deve considerar os requisitos aplicáveis de formato, metadados e integridade. Veja a <a href="https://www.gov.br/conarq/pt-br/legislacao-arquivistica/decretos-federais/decreto-no-10-278-de-18-de-marco-de-2020" rel="noopener">referência oficial do CONARQ</a>. A digitalização não autoriza descarte indiscriminado dos originais.</p>
<p><strong>ARQUINDEX - Gestão Documental e Digitalização.</strong> <a href="https://www.arquindex.com.br/">www.arquindex.com.br</a> | <a href="https://wa.me/5531973632725?text=Quero%20orcamento%20de%20OCR">WhatsApp (31) 97363-2725</a> | <a href="mailto:comercial@arquindex.com.br">comercial@arquindex.com.br</a>.</p>
</section>
<!-- /arquindex-seo-existing-first-20261018:ocr -->"""
}

def connect():
    if not all((FTP_HOST, FTP_USER, FTP_PASSWORD)):
        raise RuntimeError("Missing required FTP environment variables")
    ftp = ftplib.FTP_TLS(context=ssl.create_default_context(), timeout=35)
    ftp.connect(FTP_HOST, 21)
    ftp.login(FTP_USER, FTP_PASSWORD)
    ftp.prot_p()  # Require encrypted data transfers. Never disable certificate verification.
    return ftp

def read(ftp, name):
    data = bytearray()
    ftp.retrbinary("RETR " + name, data.extend)
    return bytes(data)

def write(ftp, name, data):
    ftp.storbinary("STOR " + name, io.BytesIO(data))

def backup_dir(ftp, public_dir):
    ftp.cwd(public_dir)
    ftp.cwd("..")
    try:
        ftp.cwd("seo-backups")
    except ftplib.error_perm:
        ftp.mkd("seo-backups")
        ftp.cwd("seo-backups")
    subdir = "existing-first-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    ftp.mkd(subdir)
    ftp.cwd(subdir)
    return ftp.pwd()

def patch(name, original):
    try:
        html = original.decode("utf-8")
        encoding = "utf-8"
    except UnicodeDecodeError:
        html = original.decode("latin-1")
        encoding = "latin-1"
    if MARKER + ":" in html:
        return original, False
    if "<html" not in html.lower() or "</body" not in html.lower():
        raise RuntimeError("Not a complete HTML page: " + name)
    modified, hits = ANCHOR.subn(lambda match: CONTENT[name] + "\n" + match.group(1), html, count=1)
    if hits != 1:
        raise RuntimeError("Expected content insertion anchor not found: " + name)
    data = modified.encode(encoding)
    if data == original:
        raise RuntimeError("No change: " + name)
    return data, True

def verify_public(name, key):
    url = BASE + name
    req = urllib.request.Request(url, headers={"User-Agent": "ArquindexQualityCheck/2026-10-18", "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=30) as response:
        if response.status != 200 or response.geturl() != url:
            raise RuntimeError("Public HTTP status or URL mismatch for " + name)
        document = response.read(4_000_000).decode("utf-8", errors="replace")
    if key not in document or "www.arquindex.com.br" not in document or "comercial@arquindex.com.br" not in document:
        raise RuntimeError("New content not verified on public page " + name)

def main():
    ftp = connect()
    written = []
    original = {}
    try:
        ftp.cwd("public_html")
        public_dir = ftp.pwd()
        proposed = {}
        for name in CONTENT:
            original[name] = read(ftp, name)
            proposed[name], changed = patch(name, original[name])
            print("PREPARED", name, "changed=" + str(changed), flush=True)
        if not any(proposed[n] != original[n] for n in CONTENT):
            print("NOOP already present; no FTP modifications needed")
            return
        backup = backup_dir(ftp, public_dir)
        for name in CONTENT:
            write(ftp, name, original[name])
            if read(ftp, name) != original[name]:
                raise RuntimeError("Backup validation failed")
        print("BACKUP_VERIFIED outside_public_html", flush=True)
        ftp.cwd(public_dir)
        for name in CONTENT:
            if proposed[name] == original[name]:
                continue
            if read(ftp, name) != original[name]:
                raise RuntimeError("Concurrent modification detected: " + name)
            written.append(name)
            write(ftp, name, proposed[name])
            if read(ftp, name) != proposed[name]:
                raise RuntimeError("FTP write verification failed: " + name)
        ftp.quit()
        time.sleep(6)
        for name in written:
            for attempt in range(4):
                try:
                    verify_public(name, MARKER)
                    print("PUBLIC_HTTP_200_AND_CONTENT_CONFIRMED", BASE + name, flush=True)
                    break
                except Exception:
                    if attempt == 3:
                        raise
                    time.sleep(6)
        print("DEPLOY_SUCCESS", len(written), "existing URLs preserved", flush=True)
    except Exception as err:
        print("DEPLOY_FAILED", type(err).__name__, str(err)[:200], flush=True)
        if written:
            try:
                fresh = connect()
                fresh.cwd("public_html")
                for name in written:
                    write(fresh, name, original[name])
                fresh.quit()
                print("ROLLBACK_UPLOADED", len(written), flush=True)
            except Exception as rollback_error:
                print("ROLLBACK_FAILED", type(rollback_error).__name__, flush=True)
        sys.exit(1)
    finally:
        try:
            ftp.quit()
        except Exception:
            pass

if __name__ == "__main__":
    main()

