"""Quality gate for this existing-first editorial draft. No network or publication."""
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path


class MainContent(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.text = []
        self.sources = []
        self.headings = []
        self.faq = 0
        self._heading = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "div" and attrs.get("id") == "guarda-conteudo-principal":
            self.depth = 1
        elif self.depth and tag == "div":
            self.depth += 1
        if tag == "a" and attrs.get("href", "").startswith("https://www.gov.br/"):
            self.sources.append(attrs["href"])
        if self.depth and tag == "h3":
            self._heading = True
        if self.depth and tag == "summary":
            self.faq += 1

    def handle_endtag(self, tag):
        if self.depth and tag == "div":
            self.depth -= 1
        if tag == "h3":
            self._heading = False

    def handle_data(self, data):
        if self.depth:
            self.text.append(data)
        if self._heading:
            self.headings.append(data)


def validate(path):
    data = Path(path).read_bytes()
    html = data.decode("utf-8")
    parser = MainContent()
    parser.feed(html)
    words = re.findall(r"\b[\w]+(?:[-’'][\w]+)*\b", " ".join(parser.text))
    # Only text in the identified principal body counts: no menus, contact,
    # source list, author/date boilerplate, HTML comments or JSON-LD.
    assert len(words) >= 3000, f"Minimum 3000; received {len(words)}"
    assert parser.faq >= 6
    assert len(parser.headings) >= 15
    assert "Exemplo hipotético" in html
    assert "16 de outubro de 2026" in html
    assert "14 de setembro de 2026" in html
    assert len(parser.sources) >= 3
    assert not re.search(r"<h1\b|<script\b|<iframe\b", html, re.I)
    assert "WhatsApp (31) 97363-2725" in html
    assert "comercial@arquindex.com.br" in html
    return {"words_main": len(words), "faq_answers": parser.faq,
            "sections": len(parser.headings), "sha256": hashlib.sha256(data).hexdigest(),
            "count_scope": "#guarda-conteudo-principal only",
            "state": "draft_validated_not_published"}


if __name__ == "__main__":
    print(json.dumps(validate(Path(__file__).with_name("guarda-documental.html")),
                     ensure_ascii=False, indent=2))
