from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import sys

BASE = Path("comparativos")
class Inspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.titles = 0
        self.h1 = 0
        self.canonicals = []
        self.descriptions = []
        self.robots = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title": self.titles += 1
        if tag == "h1": self.h1 += 1
        if tag == "link" and a.get("rel") == "canonical": self.canonicals.append(a.get("href", ""))
        if tag == "meta" and a.get("name") == "description": self.descriptions.append(a.get("content", ""))
        if tag == "meta" and a.get("name") == "robots": self.robots.append(a.get("content", ""))
        if tag == "a": self.links.append(a.get("href", ""))

def main():
    files = sorted(BASE.glob("**/index.html"))
    if not files: raise SystemExit("Nenhuma landing page encontrada")
    for file in files:
        html = file.read_text(encoding="utf-8")
        p = Inspector()
        p.feed(html)
        expected = "https://www.arquindex.com.br/" + file.parent.as_posix() + "/"
        errors = []
        if p.titles != 1: errors.append("title deve ser unico")
        if p.h1 != 1: errors.append("h1 deve ser unico")
        if p.canonicals != [expected]: errors.append("canonical divergente: " + str(p.canonicals))
        if len(p.descriptions) != 1 or not (70 <= len(p.descriptions[0]) <= 180): errors.append("description ausente ou fora da faixa")
        if not any("index" in x for x in p.robots): errors.append("robots index ausente")
        for link in p.links:
            if link.startswith("http") and urlparse(link).scheme != "https": errors.append("link nao HTTPS: " + link)
        if errors:
            print("FAIL", file, *errors, sep=" | ")
            return 1
        print("PASS", file, expected)
    return 0

if __name__ == "__main__":
    sys.exit(main())
