import ftplib, hashlib, io, json, os, posixpath, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from bs4 import BeautifulSoup

STAMP = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
TARGETS = [
    dict(
        id='ARQ-028', host='instalacao-lgpd-sp.arquindex.com.br', file='empresas.html',
        slug='como-criar-inventario-de-dados-pessoais', article='Como criar inventário de dados pessoais',
        canonical='https://instalacao-lgpd-sp.arquindex.com.br/empresas.html?post=como-criar-inventario-de-dados-pessoais',
        section='''<section class="aq-aeo-answer" data-aq-aeo="ARQ-028"><h2>Como iniciar o inventário de dados pessoais e definir responsáveis?</h2><p><strong>Resposta direta:</strong> comece pelos processos de negócio, nomeie um responsável por cada fluxo e registre finalidade, titulares, categorias de dados, origem, repositórios, acessos, compartilhamentos, retenção e descarte. O DPO pode coordenar o método, mas a validação precisa envolver os donos dos processos.</p><table><thead><tr><th>Etapa</th><th>Evidência mínima</th></tr></thead><tbody><tr><td>Escopo</td><td>Processos prioritários, unidades envolvidas e responsáveis nomeados</td></tr><tr><td>Levantamento</td><td>Entrevistas confrontadas com formulários, sistemas, arquivos físicos e contratos</td></tr><tr><td>Validação</td><td>Finalidade, base legal, acesso, compartilhamentos, retenção e riscos revisados</td></tr><tr><td>Manutenção</td><td>Gatilhos de atualização para novos sistemas, fornecedores e mudanças de processo</td></tr></tbody></table><p>O artigo 37 da LGPD prevê registro das operações de tratamento. A matriz deve refletir o fluxo real, inclusive documentos em papel e cópias fora dos sistemas centrais.</p><p><a href="https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm#art37">LGPD — artigo 37</a> · <a href="https://www.arquindex.com.br/lgpd-consultoria.html">Consultoria de adequação LGPD</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=artigo&amp;utm_campaign=arq028_inventario_20261020">Definir escopo do inventário</a></p></section>'''
    ),
    dict(
        id='ARQ-031', host='software-reconhecimento-texto-documentos-digitalizados.arquindex.com.br', file='guia-completo.html',
        slug='incineracao-de-documentos-sem-risco-juridico', article='Incineração de documentos sem risco jurídico',
        canonical='https://software-reconhecimento-texto-documentos-digitalizados.arquindex.com.br/guia-completo.html?post=incineracao-de-documentos-sem-risco-juridico',
        section='''<section class="aq-aeo-answer" data-aq-aeo="ARQ-031"><h2>O que verificar antes de autorizar a destruição de documentos?</h2><p><strong>Resposta direta:</strong> identifique a série documental, confirme o prazo de guarda e a ausência de bloqueio jurídico, obtenha autorização formal, registre o lote, preserve a cadeia de custódia e exija evidência da destruição. Digitalizar não autoriza automaticamente eliminar o original.</p><table><thead><tr><th>Controle</th><th>Registro recomendado</th></tr></thead><tbody><tr><td>Elegibilidade</td><td>Tipo documental, período, tabela de temporalidade e fundamento da decisão</td></tr><tr><td>Autorização</td><td>Responsável, data, lote e eventuais exceções preservadas</td></tr><tr><td>Custódia</td><td>Coleta, transporte, acesso e recebimento rastreáveis</td></tr><tr><td>Encerramento</td><td>Método aplicado, quantidade e certificado ou termo do lote</td></tr></tbody></table><p>A LGPD admite conservação em hipóteses específicas após o término do tratamento. Por isso, privacidade, obrigações legais, prazos prescricionais e valor arquivístico devem ser avaliados antes da eliminação.</p><p><a href="https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm#art16">LGPD — artigo 16</a> · <a href="https://www.arquindex.com.br/guarda_de_documentos.html">Guarda e gestão documental</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=artigo&amp;utm_campaign=arq031_descarte_20261020">Avaliar o acervo</a></p></section>'''
    ),
    dict(
        id='ARQ-033', host='digitalizar-arquivos-bh.arquindex.com.br', file='index.html', slug=None,
        canonical='https://digitalizar-arquivos-bh.arquindex.com.br/',
        section='''<section class="aq-aeo-answer" data-aq-aeo="ARQ-033"><h2>Como preparar documentos para digitalização em Belo Horizonte e conferir a entrega?</h2><p><strong>Resposta direta:</strong> separe uma amostra representativa, inventarie caixas e séries documentais, defina resolução, cor, OCR, indexação, formato de entrega, acessos e critérios de aceite antes de estimar prazo e custo. A conferência deve provar completude, legibilidade e recuperação pelo índice acordado.</p><table><thead><tr><th>Fase</th><th>Decisão prática</th></tr></thead><tbody><tr><td>Amostra</td><td>Selecionar documentos de RH, contratos e áreas técnicas com exceções reais</td></tr><tr><td>Preparação</td><td>Quantificar, ordenar, retirar grampos e registrar documentos frágeis ou sigilosos</td></tr><tr><td>Captura</td><td>Definir 300 dpi quando adequado, cor, verso, OCR e tratamento de páginas em branco</td></tr><tr><td>Aceite</td><td>Testar busca, vínculo entre imagem e índice, completude, acesso e cópia de segurança</td></tr></tbody></table><p>Os requisitos do Decreto nº 10.278/2020 devem ser avaliados conforme o tipo documental e a finalidade. A decisão sobre descarte do papel exige análise própria; não decorre apenas da existência do arquivo digital.</p><p><a href="https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/decreto/d10278.htm">Decreto nº 10.278/2020</a> · <a href="https://www.arquindex.com.br/digitalizacao-documentos-belo-horizonte.html">Digitalização de documentos em Belo Horizonte</a> · <a href="https://www.arquindex.com.br/solicitar-proposta-contratacao.html?utm_source=site&amp;utm_medium=pagina_local&amp;utm_campaign=arq033_bh_20261020">Solicitar avaliação do lote</a></p></section>'''
    )
]

STYLE = '''<style id="arquindex-aeo-20261020">.aq-aeo-answer{max-width:1120px;margin:36px auto;padding:28px;border:1px solid #d9e2ef;border-radius:16px;background:#fff;color:#0c1b33}.aq-aeo-answer h2{color:#0b3d91}.aq-aeo-answer table{width:100%;border-collapse:collapse;margin:18px 0}.aq-aeo-answer th,.aq-aeo-answer td{padding:12px;border:1px solid #d9e2ef;text-align:left;vertical-align:top}.aq-aeo-answer th{background:#eaf0f8}@media(max-width:760px){.aq-aeo-answer{margin:24px 16px;padding:20px}.aq-aeo-answer table{display:block;overflow-x:auto}.aq-aeo-answer th,.aq-aeo-answer td{min-width:145px}}</style>'''
WIDGET = Path('conteudo/publicacao/_atendimento-flutuante.html').read_text('utf-8')

def get(ftp, path):
    data = bytearray(); ftp.retrbinary('RETR ' + path, data.extend); return bytes(data)

def put_atomic(ftp, path, data, label):
    directory, name = posixpath.dirname(path), posixpath.basename(path)
    temp = directory + '/.tmp-' + name + '-' + label
    ftp.storbinary('STOR ' + temp, io.BytesIO(data)); assert get(ftp, temp) == data
    try: ftp.delete(path)
    except ftplib.error_perm as exc:
        if not str(exc).startswith('550'): raise
    ftp.rename(temp, path); assert get(ftp, path) == data

def mkdir(ftp, path):
    current = ftp.pwd()
    try:
        ftp.cwd('/')
        for part in path.strip('/').split('/'):
            if not part: continue
            try: ftp.mkd(part)
            except ftplib.error_perm as exc:
                if not str(exc).startswith('550'): raise
            ftp.cwd(part)
    finally: ftp.cwd(current)

def locate(ftp, base, target):
    for root in [base + '/subdominios/' + target['host'], base + '/' + target['host'], '/subdominios/' + target['host'], '/' + target['host']]:
        path = root + '/' + target['file']
        try:
            data = get(ftp, path)
            if b'<html' in data.lower(): return path, data
        except ftplib.all_errors: pass
    raise RuntimeError('TARGET_NOT_FOUND ' + target['id'])

def public(url):
    sep = '&' if '?' in url else '?'
    req = urllib.request.Request(url + sep + 'verify=' + STAMP, headers={'User-Agent':'ArquindexSEO/1.0','Cache-Control':'no-cache'})
    with urllib.request.urlopen(req, timeout=40) as response: return response.status, response.read(6000000)

def dynamic_transform(target, original):
    text = original.decode('utf-8')
    marker = 'arquindex-aeo-' + target['id'].lower() + '-20261020'
    assert marker not in text, 'ALREADY_UPDATED ' + target['id']
    payload = json.dumps({k:target[k] for k in ['slug','article','canonical','section']}, ensure_ascii=False)
    js = f'''<script id="{marker}">(function(c){{function apply(){{if(new URLSearchParams(location.search).get("post")!==c.slug)return;var blog=document.getElementById("soro-blog");if(!blog)return;var article=Array.from(blog.querySelectorAll("h1")).find(function(h){{return h.textContent.trim()===c.article;}});if(!article)return;Array.from(document.querySelectorAll("h1")).forEach(function(h){{if(h===article||blog.contains(h))return;var p=document.createElement("p");p.className=(h.className?h.className+" ":"")+"aq-context-title";p.innerHTML=h.innerHTML;h.replaceWith(p);}});var cans=Array.from(document.querySelectorAll('link[rel="canonical"]'));var can=cans.shift();if(!can){{can=document.createElement("link");can.rel="canonical";document.head.appendChild(can);}}can.href=c.canonical;cans.forEach(function(x){{x.remove();}});if(!document.querySelector('[data-aq-aeo="{target['id']}"]'))article.closest("article,section,div").insertAdjacentHTML("beforeend",c.section);}}function start(){{apply();new MutationObserver(apply).observe(document.documentElement,{{childList:true,subtree:true}});}}if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start,{{once:true}});else start();}})({payload});</script>'''
    pos = text.lower().rindex('</body>')
    return (text[:pos] + STYLE + js + '\n' + text[pos:]).encode('utf-8')

def static_transform(target, original):
    soup = BeautifulSoup(original.decode('utf-8'), 'html.parser')
    assert soup.head and soup.body and soup.title and soup.find('h1')
    assert not soup.select('[data-aq-aeo="ARQ-033"]'), 'ALREADY_UPDATED ARQ-033'
    for canonical in soup.find_all('link', rel=lambda value: value and 'canonical' in value): canonical.decompose()
    soup.head.append(soup.new_tag('link', rel='canonical', href=target['canonical']))
    soup.head.append(BeautifulSoup(STYLE, 'html.parser'))
    for selector in ['#arq-floating-style','#arq-floating','#arq-floating-script','#arq-dedup-floats','.aq-brand-wa']:
        for node in soup.select(selector): node.decompose()
    for node in list(soup.find_all('script')):
        src=(node.get('src') or '').lower(); text=node.string or node.get_text() or ''
        if ('__arqWhatsappOptions' in text or 'whatsapp_replace_crisp/jquery.js' in src or 'whatsapp_replace_crisp/user_main.js' in src or 'watiwidget.js' in src): node.decompose()
    fragment=BeautifulSoup(WIDGET,'html.parser')
    for node in list(fragment.contents): soup.body.append(node)
    section = BeautifulSoup(target['section'], 'html.parser')
    footer = soup.find('footer')
    if footer: footer.insert_before(section)
    else: soup.body.append(section)
    rendered=str(soup)
    assert rendered.count('id="arq-floating"') == 1 and 'Conversar no chat' in rendered
    return str(soup).encode('utf-8')

with ftplib.FTP_TLS(timeout=60) as ftp:
    ftp.connect('ftp.arquindex.com.br', 21); ftp.login('arquind2', os.environ['FTP_PASSWORD']); ftp.prot_p(); ftp.set_pasv(True)
    base = None
    for candidate in ['/public_html','/home/arquind2/public_html']:
        try:
            if b'arquindex' in get(ftp, candidate + '/index.html').lower(): base = candidate; break
        except ftplib.all_errors: pass
    assert base, 'PUBLIC_ROOT_NOT_FOUND'
    records = []
    for target in TARGETS:
        path, original = locate(ftp, base, target)
        updated = dynamic_transform(target, original) if target['slug'] else static_transform(target, original)
        records.append((target, path, original, updated))
    backup = '/seo-backups/rodada-20261020-manha-' + STAMP
    mkdir(ftp, backup); ftp.storbinary('STOR ' + backup + '/.htaccess', io.BytesIO(b'Options -Indexes\nRequire all denied\n'))
    for target, path, original, updated in records:
        bpath = backup + '/' + target['id'].lower() + '-' + hashlib.sha256(path.encode()).hexdigest()[:12] + '.html'
        ftp.storbinary('STOR ' + bpath, io.BytesIO(original)); assert get(ftp, bpath) == original
        print('BACKUP_VERIFIED', target['id'], bpath, hashlib.sha256(original).hexdigest(), flush=True)
    written = []
    try:
        for target, path, original, updated in records: assert get(ftp, path) == original, 'CONCURRENT_CHANGE ' + target['id']
        for target, path, original, updated in records:
            put_atomic(ftp, path, updated, STAMP); written.append((path, original))
            print('FTP_PUBLISHED_VERIFIED', target['id'], hashlib.sha256(updated).hexdigest(), flush=True)
        for target, path, original, updated in records:
            url = target['canonical']; last = None
            for attempt in range(3):
                try:
                    status, body = public(url)
                    assert status == 200 and target['id'].encode() in body
                    assert b'id="arq-floating"' in body and b'arquindex-logo-oficial.webp' in body and b'noindex' not in body.lower()
                    print('PUBLIC_SOURCE_VERIFIED', target['id'], url, hashlib.sha256(body).hexdigest(), flush=True)
                    last = None; break
                except Exception as exc:
                    last = exc
                    if attempt < 2: time.sleep(5)
            if last: raise last
    except Exception:
        for path, original in reversed(written): put_atomic(ftp, path, original, 'rollback-' + STAMP)
        print('ROLLBACK_COMPLETED', flush=True); raise
