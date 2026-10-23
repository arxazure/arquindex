import ftplib
import hashlib
import io
import json
import os
import posixpath
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup

STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
TODAY = "2026-10-23"
HOST = "acervos-medico-baixada-fluminense.arquindex.com.br"
FILE = "o-que-e.html"
URL = "https://" + HOST + "/" + FILE
MARKER = "arquindex-pdf-extenso-20261023"
EXPECTED_TITLE = "Acervos Médicos: Organização, Guarda e Acesso | Arquindex"
EXPECTED_H1 = "Como organizar e controlar grandes acervos médicos"

STYLE = """
<style id="arquindex-pdf-extenso-style-20261023">
#arquindex-pdf-extenso-20261023{max-width:1120px;margin:38px auto;padding:30px;border:1px solid #d6e0ee;border-radius:18px;background:#fff;color:#13243b;box-sizing:border-box;line-height:1.65}
#arquindex-pdf-extenso-20261023 h2,#arquindex-pdf-extenso-20261023 h3{color:#0b3d91;line-height:1.25}
#arquindex-pdf-extenso-20261023 .aq-direct{font-size:1.08rem;padding:18px 20px;border-left:5px solid #087f73;background:#eef8f6}
#arquindex-pdf-extenso-20261023 table{width:100%;border-collapse:collapse;margin:20px 0}
#arquindex-pdf-extenso-20261023 th,#arquindex-pdf-extenso-20261023 td{border:1px solid #d6e0ee;padding:12px;text-align:left;vertical-align:top}
#arquindex-pdf-extenso-20261023 th{background:#eaf0f8}
#arquindex-pdf-extenso-20261023 .aq-note{padding:16px 18px;background:#fff8e6;border:1px solid #ecd797;border-radius:10px}
#arquindex-pdf-extenso-20261023 .aq-example{padding:18px;background:#f4f7fc;border-radius:12px}
#arquindex-pdf-extenso-20261023 .aq-sources{font-size:.94rem;color:#42536b}
@media(max-width:760px){#arquindex-pdf-extenso-20261023{margin:24px 14px;padding:20px}#arquindex-pdf-extenso-20261023 .aq-table-wrap{overflow-x:auto}#arquindex-pdf-extenso-20261023 th,#arquindex-pdf-extenso-20261023 td{min-width:160px}}
</style>
"""

SECTION = """
<section id="arquindex-pdf-extenso-20261023" aria-labelledby="pdf-extenso-title">
<h2 id="pdf-extenso-title">PDF extenso: capacidade de entrada não substitui conferência</h2>
<p class="aq-direct"><strong>Resposta direta:</strong> aceitar um PDF com muitas páginas é apenas uma condição técnica de entrada. Uma entrega documental útil depende também de legibilidade, ordem, identificação, campos definidos, tratamento de exceções, segurança, amostragem e critérios de aceite. Para comparar propostas, a organização deve pedir uma amostra verificável e descrever o resultado esperado antes do processamento integral.</p>

<h3>O que mudou no mercado em outubro de 2026</h3>
<p>A documentação do Microsoft Azure Content Understanding registrou, em outubro de 2026, o aumento do limite padrão da análise assíncrona de arquivos PDF e TIFF de 300 para 2.000 páginas, mantendo cinco páginas para a análise síncrona. Esse dado ajuda a compreender a evolução das ferramentas de análise documental, mas não demonstra, isoladamente, precisão, custo, prazo ou adequação a um acervo específico.</p>
<p class="aq-note"><strong>Limite desta referência:</strong> o Azure Content Understanding é citado como fonte técnica de mercado. Esta página não afirma que ele integra automaticamente o serviço da Arquindex, que dados médicos serão enviados a esse ambiente ou que a Arquindex oferece o limite de 2.000 páginas. Tecnologia, hospedagem, localização dos dados, subcontratação e responsabilidades precisam constar da proposta e do contrato aplicáveis.</p>

<h3>Antes do orçamento: descreva o arquivo e a entrega</h3>
<p>Um orçamento comparável começa pela descrição do acervo. Quantidade de páginas é importante, porém insuficiente. Dois PDFs com o mesmo tamanho podem exigir tratamentos muito diferentes: um pode conter texto digital uniforme; outro pode reunir imagens inclinadas, páginas de tamanhos variados, carimbos, manuscritos, anexos, documentos duplicados e folhas sem identificação. Em acervos médicos, também é necessário delimitar quem autoriza o tratamento, quem pode consultar o material e como serão protegidos os dados pessoais.</p>
<div class="aq-table-wrap">
<table>
<thead><tr><th>Item para informar</th><th>Pergunta prática</th><th>Entregável ou evidência esperada</th></tr></thead>
<tbody>
<tr><td>Volume e estrutura</td><td>Quantos arquivos e páginas existem? Há prontuários, exames, laudos e anexos no mesmo PDF?</td><td>Inventário de entrada, identificação do lote e registro de quantidade.</td></tr>
<tr><td>Condição dos originais</td><td>Há páginas tortas, rasgadas, claras, escuras, manuscritas ou com frente e verso?</td><td>Amostra representativa e regra para documentos que não atingirem o padrão.</td></tr>
<tr><td>Ordem documental</td><td>O arquivo precisa permanecer integral ou ser separado por paciente, episódio, tipo e data?</td><td>Regra de agrupamento, nomenclatura e relatório de exceções.</td></tr>
<tr><td>OCR e campos</td><td>É suficiente tornar o PDF pesquisável ou será necessário extrair nome, data, número e tipo documental?</td><td>Lista de campos, formato de saída e amostra com valores conferidos.</td></tr>
<tr><td>Qualidade</td><td>Como páginas ausentes, duplicadas, ilegíveis ou fora de ordem serão identificadas?</td><td>Critérios de inspeção, taxa de amostragem, registro de não conformidades e retrabalho.</td></tr>
<tr><td>Segurança</td><td>Quem acessará os dados e por quanto tempo cópias temporárias serão mantidas?</td><td>Perfis de acesso, registro de movimentação, retenção e descarte acordados.</td></tr>
<tr><td>Entrega</td><td>Qual sistema receberá os documentos e os índices?</td><td>PDF, PDF/A quando previsto, planilha ou integração definida e teste de importação.</td></tr>
</tbody>
</table>
</div>

<h3>Fluxo técnico recomendado para PDFs grandes</h3>
<ol>
<li><strong>Inventariar e preservar a entrada.</strong> O lote deve receber um identificador, contagem inicial e registro de origem. Se houver transferência física, a cadeia de movimentação precisa indicar coleta, responsáveis, volumes e recebimento.</li>
<li><strong>Selecionar uma amostra difícil.</strong> A amostra deve incluir documentos legíveis e problemáticos. Testar somente páginas perfeitas produz uma avaliação otimista e não revela como o processo lida com carimbos, manuscritos, cortes, tabelas ou mistura de tipos.</li>
<li><strong>Definir a unidade documental.</strong> Antes de separar, é preciso estabelecer quando começa e termina um prontuário, ficha, exame ou relatório. Páginas sem nome não devem ser deslocadas automaticamente para outro paciente apenas porque o reconhecimento não encontrou um identificador.</li>
<li><strong>Configurar captura, OCR e indexação.</strong> Resolução, cor, orientação, idioma, campos, nomenclatura e formato precisam corresponder ao uso posterior. OCR melhora a pesquisa, mas não transforma automaticamente todo texto reconhecido em dado validado.</li>
<li><strong>Processar com rastreabilidade.</strong> Arquivos recusados, páginas com baixa confiança, exceções de ordem e campos ausentes devem gerar registros próprios. Reprocessar sem registrar o motivo dificulta auditoria e aceite.</li>
<li><strong>Conferir e entregar.</strong> A organização deve receber os arquivos, índices, relatório de qualidade e lista de pendências. O teste final precisa reproduzir tarefas reais: pesquisar um termo, localizar um paciente autorizado, abrir o documento correto e verificar ordem e legibilidade.</li>
</ol>

<h3>Falhas que precisam de regra antes do processamento</h3>
<p><strong>Página sem identificação:</strong> manter a relação com as páginas vizinhas até que uma nova identificação confiável seja encontrada pode ser mais seguro do que criar um paciente ou documento por inferência. A regra exata depende da composição do acervo e deve ser validada em amostra.</p>
<p><strong>Nomes parecidos:</strong> similaridade textual ajuda, mas não deve ser o único critério para unir registros. Quando permitido pelo escopo, data de nascimento, número interno ou outro identificador pode apoiar a conferência. Dados usados nessa validação continuam sujeitos aos controles de acesso e finalidade.</p>
<p><strong>Texto reconhecido incorretamente:</strong> qualidade de imagem, fonte, idioma, carimbos e manuscritos influenciam o OCR. O projeto deve indicar quais campos terão conferência, quais tolerâncias serão aceitas e como divergências serão devolvidas para revisão.</p>
<p><strong>Arquivo parcialmente processado:</strong> interrupção, limite técnico ou formato incompatível não pode resultar em entrega silenciosamente incompleta. O lote precisa registrar quantidade recebida, processada, recusada e pendente.</p>
<p><strong>Página duplicada ou fora de ordem:</strong> a automação pode sinalizar padrões, mas o critério de remoção e reorganização deve ser aprovado. Em documentos multipágina, excluir ou mover uma folha sem verificar contexto pode alterar o sentido do registro.</p>

<h3>Segurança e dados médicos</h3>
<p>Prontuários e documentos de saúde podem conter dados pessoais sensíveis. O projeto deve identificar as posições de controlador e operador para cada operação, as instruções documentadas, os usuários autorizados, a finalidade, o ambiente de processamento, os prazos de retenção e o procedimento para incidentes. A demonstração pública ou comercial deve usar material fictício ou adequadamente anonimizado; nomes de pacientes e informações clínicas reais não devem ser usados para ilustrar capacidade técnica sem fundamento e autorização apropriados.</p>
<p>A escolha entre processamento local, servidor dedicado, nuvem contratada ou combinação de ambientes não deve ser feita apenas pelo tamanho do arquivo. Requisitos de integração, residência dos dados, cópias temporárias, logs, criptografia, continuidade e eliminação precisam ser comparados. A Arquindex define a arquitetura e os controles conforme o escopo aprovado; esta página não substitui análise jurídica, de segurança ou médica da organização contratante.</p>

<h3>Exemplo hipotético de aplicação</h3>
<div class="aq-example">
<p><strong>Cenário ilustrativo, não case de cliente:</strong> uma instituição possui PDFs extensos formados por fichas clínicas, exames e avaliações. Antes do lote completo, seleciona uma amostra com documentos nítidos, páginas inclinadas, anexos sem nome e pacientes com nomes semelhantes. O aceite exige preservar documentos multipágina, tornar o conteúdo pesquisável, registrar páginas sem identificação e entregar um relatório com arquivos processados, pendências e itens enviados para revisão.</p>
<p>O resultado não é avaliado apenas pela abertura do PDF. A equipe autorizada verifica se a busca encontra termos reais, se cada página permanece vinculada ao paciente correto, se a ordem definida foi mantida e se os arquivos recusados estão listados. Somente depois dessa conferência o padrão é aplicado ao restante do acervo.</p>
</div>

<h3>Perguntas práticas</h3>
<p><strong>Um PDF com 2.000 páginas sempre pode ser processado?</strong><br>Não. O número citado é um limite padrão de um serviço específico em análise assíncrona. Formato, tamanho em bytes, versão da API, configuração, região, qualidade e demais quotas também podem interferir. O fornecedor deve testar a amostra e informar a arquitetura efetivamente proposta.</p>
<p><strong>OCR elimina a revisão humana?</strong><br>Não necessariamente. OCR torna texto pesquisável e pode apoiar extração, mas campos críticos, documentos ruins e decisões de agrupamento podem exigir conferência. A proposta deve dizer o que será revisado e o que será entregue apenas como reconhecimento automático.</p>
<p><strong>Como comparar dois orçamentos?</strong><br>Compare preparação, unidade documental, campos, OCR, amostragem, retrabalho, segurança, formato de entrega, logística e tratamento de exceções. Um valor por página sem essas definições pode representar escopos diferentes.</p>
<p><strong>É permitido usar prontuários reais em uma prova de conceito?</strong><br>A decisão depende da finalidade, dos papéis dos agentes, das instruções e das medidas aplicáveis. Como prática prudente, prefira documentos fictícios ou anonimizados sempre que eles forem suficientes para o teste e restrinja acesso ao material autorizado.</p>
<p><strong>Capacidade de entrada comprova qualidade?</strong><br>Não. Capacidade indica quanto o sistema aceita em determinada operação. Qualidade precisa ser demonstrada por resultados conferidos, critérios de aceite, tratamento de falhas e evidências de entrega.</p>

<h3>Como solicitar uma avaliação técnica</h3>
<p>Para delimitar o escopo, informe volume aproximado, tipos documentais, condição das imagens, cidade de origem, necessidade de coleta, regra de separação, campos desejados, formato de entrega, prazo e ambiente autorizado. A Arquindex pode avaliar uma amostra e propor digitalização, OCR, indexação, organização e integração de acordo com os requisitos confirmados.</p>
<p><a href="https://www.arquindex.com.br/digitalizacao.html">Conheça a digitalização de documentos</a> · <a href="https://www.arquindex.com.br/digitalizacao-prontuarios-medicos.html">Veja a digitalização de prontuários</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_vertical&amp;utm_campaign=arq081_pdf_extenso_20261023">Solicite uma avaliação do acervo</a></p>

<p class="aq-sources"><strong>Fontes consultadas e data:</strong> Microsoft Learn, “What’s new in Azure Content Understanding”, seção de outubro de 2026, consultada em 23/10/2026; Microsoft Learn, quotas e limites do serviço; ANPD, materiais para agentes de tratamento; Lei nº 13.709/2018. As recomendações de inventário, amostra e aceite desta seção são orientação editorial da Arquindex e não são atribuídas à Microsoft ou à ANPD.</p>
<ul class="aq-sources">
<li><a href="https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/whats-new">Microsoft Learn — novidades do Content Understanding</a></li>
<li><a href="https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/service-limits">Microsoft Learn — quotas e limites</a></li>
<li><a href="https://www.gov.br/anpd/pt-br/centrais-de-conteudo/documentos-tecnicos-orientativos">ANPD — documentos técnicos e orientativos</a></li>
<li><a href="https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm">Lei Geral de Proteção de Dados Pessoais</a></li>
</ul>
<p class="aq-sources">Autoria: Equipe técnica Arquindex. Atualizado em 23/10/2026.</p>
</section>
"""

def get(ftp, path):
    data = bytearray()
    ftp.retrbinary("RETR " + path, data.extend)
    return bytes(data)

def mkdir(ftp, path):
    old = ftp.pwd()
    try:
        ftp.cwd("/")
        for part in path.strip("/").split("/"):
            if not part:
                continue
            try:
                ftp.mkd(part)
            except ftplib.error_perm as exc:
                if not str(exc).startswith("550"):
                    raise
            ftp.cwd(part)
    finally:
        ftp.cwd(old)

def put(ftp, path, data, label):
    folder = posixpath.dirname(path)
    name = posixpath.basename(path)
    temp = folder + "/.tmp-" + name + "-" + label
    ftp.storbinary("STOR " + temp, io.BytesIO(data))
    assert get(ftp, temp) == data
    try:
        ftp.delete(path)
    except ftplib.error_perm as exc:
        if not str(exc).startswith("550"):
            raise
    ftp.rename(temp, path)
    assert get(ftp, path) == data

def locate(ftp, base):
    roots = [
        base + "/subdominios/" + HOST,
        base + "/" + HOST,
        "/subdominios/" + HOST,
        "/" + HOST,
    ]
    for root in roots:
        path = root + "/" + FILE
        try:
            data = get(ftp, path)
            if b"<html" in data.lower():
                return path, data
        except ftplib.all_errors:
            pass
    raise RuntimeError("TARGET_NOT_FOUND ARQ-081")

def update_webpage_schema(soup):
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = script.string or script.get_text()
        try:
            payload = json.loads(raw)
        except Exception:
            continue
        changed = False
        items = payload if isinstance(payload, list) else payload.get("@graph", [payload])
        for item in items:
            if isinstance(item, dict) and item.get("@type") == "WebPage":
                item["dateModified"] = TODAY
                changed = True
        if changed:
            script.string = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))

def transform(original):
    soup = BeautifulSoup(original.decode("utf-8"), "html.parser")
    assert soup.head and soup.body
    assert soup.title and soup.title.get_text(strip=True) == EXPECTED_TITLE
    h1s = soup.find_all("h1")
    assert len(h1s) == 1 and h1s[0].get_text(" ", strip=True) == EXPECTED_H1
    canonical = soup.find("link", rel=lambda value: value and "canonical" in value)
    assert canonical and canonical.get("href") == URL

    for old in soup.select("#" + MARKER + ", #arquindex-pdf-extenso-style-20261023"):
        old.decompose()
    soup.head.append(BeautifulSoup(STYLE, "html.parser"))
    fragment = BeautifulSoup(SECTION, "html.parser")
    anchor = soup.select_one('[data-aq-aeo="ARQ-081"]')
    if anchor:
        anchor.insert_before(fragment)
    else:
        footer = soup.find("footer")
        footer.insert_before(fragment) if footer else soup.body.append(fragment)
    update_webpage_schema(soup)

    output = str(soup).encode("utf-8")
    assert output.count(('id="' + MARKER + '"').encode()) == 1
    assert b"capacidade de entrada n\xc3\xa3o substitui confer\xc3\xaancia" in output
    return output

def public(url):
    request = urllib.request.Request(
        url + ("&" if "?" in url else "?") + "verify=" + STAMP,
        headers={"User-Agent": "ArquindexSEO/1.0", "Cache-Control": "no-cache"},
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.status, response.read(12_000_000)

report_dir = Path("publish-report")
report_dir.mkdir(exist_ok=True)
report = {
    "date": TODAY,
    "id": "ARQ-081",
    "url": URL,
    "state": "started",
    "new_pages": 0,
    "updated_pages": 1,
    "published_pages": 0,
    "gsc_submitted": False,
    "indexnow_submitted": False,
}

with ftplib.FTP_TLS(timeout=60) as ftp:
    ftp.connect("ftp.arquindex.com.br", 21)
    ftp.login("arquind2", os.environ["FTP_PASSWORD"])
    ftp.prot_p()
    ftp.set_pasv(True)

    base = None
    for candidate in ["/public_html", "/home/arquind2/public_html"]:
        try:
            if b"arquindex" in get(ftp, candidate + "/index.html").lower():
                base = candidate
                break
        except ftplib.all_errors:
            pass
    assert base, "PUBLICATION_ROOT_NOT_CONFIRMED"

    page_path, original = locate(ftp, base)
    updated = transform(original)
    sitemap_path = posixpath.dirname(page_path) + "/sitemap.xml"
    old_sitemap = get(ftp, sitemap_path)

    backup = "/seo-backups/arq081-pdf-extenso-" + STAMP
    mkdir(ftp, backup)
    ftp.storbinary("STOR " + backup + "/.htaccess", io.BytesIO(b"Options -Indexes\nRequire all denied\n"))
    ftp.storbinary("STOR " + backup + "/o-que-e.html", io.BytesIO(original))
    ftp.storbinary("STOR " + backup + "/sitemap.xml", io.BytesIO(old_sitemap))
    assert get(ftp, backup + "/o-que-e.html") == original
    assert get(ftp, backup + "/sitemap.xml") == old_sitemap

    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", ns)
    root = ET.fromstring(old_sitemap)
    found = False
    for node in root:
        loc = node.find("{" + ns + "}loc")
        if loc is not None and (loc.text or "").rstrip("/") == URL.rstrip("/"):
            found = True
            lastmod = node.find("{" + ns + "}lastmod")
            if lastmod is None:
                lastmod = ET.SubElement(node, "{" + ns + "}lastmod")
            lastmod.text = TODAY
    assert found, "TARGET_NOT_IN_EXISTING_SITEMAP"
    new_sitemap = ET.tostring(root, encoding="utf-8", xml_declaration=True)

    wrote_page = False
    wrote_sitemap = False
    try:
        assert get(ftp, page_path) == original, "CONCURRENT_PAGE_CHANGE"
        assert get(ftp, sitemap_path) == old_sitemap, "CONCURRENT_SITEMAP_CHANGE"
        put(ftp, page_path, updated, STAMP)
        wrote_page = True
        if new_sitemap != old_sitemap:
            put(ftp, sitemap_path, new_sitemap, "sitemap-" + STAMP)
            wrote_sitemap = True

        time.sleep(3)
        status, body = public(URL)
        assert status == 200
        page = BeautifulSoup(body.decode("utf-8"), "html.parser")
        assert page.title and page.title.get_text(strip=True) == EXPECTED_TITLE
        assert len(page.find_all("h1")) == 1
        canonical = page.find("link", rel=lambda value: value and "canonical" in value)
        assert canonical and canonical.get("href") == URL
        assert page.select_one("#" + MARKER)
        assert b"noindex" not in body.lower()
        visible_words = len(page.get_text(" ", strip=True).split())
        assert visible_words >= 4300, visible_words

        sm_status, sm_body = public("https://" + HOST + "/sitemap.xml")
        assert sm_status == 200 and URL.encode() in sm_body and TODAY.encode() in sm_body

        report.update({
            "state": "published_verified",
            "published_pages": 1,
            "backup": backup,
            "page_path": page_path,
            "sitemap_path": sitemap_path,
            "page_sha256": hashlib.sha256(updated).hexdigest(),
            "public_sha256": hashlib.sha256(body).hexdigest(),
            "visible_words": visible_words,
            "http_status": status,
            "canonical": URL,
            "h1_count": 1,
            "noindex": False,
            "sitemap_http_status": sm_status,
            "sitemap_contains_url": True,
            "lastmod": TODAY,
        })
        print(json.dumps(report, ensure_ascii=False), flush=True)
    except Exception:
        if wrote_page:
            put(ftp, page_path, original, "rollback-" + STAMP)
        if wrote_sitemap:
            put(ftp, sitemap_path, old_sitemap, "rollback-sitemap-" + STAMP)
        report["state"] = "rollback_completed"
        (report_dir / "arq081-pdf-extenso-20261023.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print("ROLLBACK_COMPLETED", flush=True)
        raise

(report_dir / "arq081-pdf-extenso-20261023.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
)
