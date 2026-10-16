"""Install the versioned form in the publishing source and its legacy mirror."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'seo-regional/56-sites/guardadocumentalembh.arquindex.com.br/index.html'
MIRROR = ROOT / 'deploy/subdominios/guardadocumentalembh/index.html'
FRAGMENT = ROOT / 'scripts/templates/guarda-commercial-form.html'


def sync():
    page = SOURCE.read_text(encoding='utf-8')
    fragment = FRAGMENT.read_text(encoding='utf-8')
    page = re.sub(r'<!-- guarda-commercial-form:start -->.*?<!-- guarda-commercial-form:end -->\s*', '', page, flags=re.S)
    anchor = '</div><section><h2>Soluções corporativas e benefícios</h2>'
    assert anchor in page, 'Hero anchor changed: review placement before generating.'
    page = page.replace(anchor, '</div>' + fragment + '<section><h2>Soluções corporativas e benefícios</h2>', 1)
    page = re.sub(r'<a class="btn" href="https://wa.me/[^"<>]+">Solicitar orçamento pelo WhatsApp</a>', '<a class="btn" href="#orcamento">Solicitar orçamento</a>', page, count=1)
    assert page.count('id="commercial-form"') == 1
    SOURCE.write_text(page, encoding='utf-8')
    MIRROR.write_text(page, encoding='utf-8')


if __name__ == '__main__':
    sync()
