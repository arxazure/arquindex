#!/usr/bin/env python3
"""Generate 56 local landing pages, DNS inventory and a sitemap without touching production."""
from pathlib import Path
import html, json, re, xml.etree.ElementTree as ET
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]/"restauracao-56"
CITIES={"bh":"Belo Horizonte","betim":"Betim","contagem":"Contagem","novalima":"Nova Lima"}
PREFIXES=["digitalizacaodedocumentos","guardadocumental","gestaodocumental","incineracaodedocumentos","escaneardocumentos","alfresco","consultorialgpd","adequacaolgpd","dpo","canaldedenunciaslgpd","ecm","escanearprontuariomedico","escaneardossiefuncionario","digitalizacaodepartamentopessoal"]
LABELS=["Digitalização de documentos","Guarda documental","Gestão documental","Destinação segura de documentos","Escaneamento de documentos","Alfresco ECM","Consultoria LGPD","Adequação à LGPD","DPO terceirizado","Canal de denúncias e privacidade","Gestão eletrônica ECM","Digitalização de prontuários médicos","Digitalização de dossiês de funcionários","Digitalização para departamento pessoal"]
def hostname(prefix,city):
    if prefix in ("consultorialgpd","adequacaolgpd","canaldedenunciaslgpd","escaneardossiefuncionario","digitalizacaodepartamentopessoal"):
        return prefix+("" if city=="bh" else "-"+city)+".arquindex.com.br"
    if city=="bh":
        return prefix+("embh" if prefix not in ("dpo","ecm") else "embh")+".arquindex.com.br" if prefix not in ("escaneardossiefuncionario",) else prefix+".arquindex.com.br"
    join="em" if prefix not in ("dpo","ecm") else "em"
    return prefix+join+city+".arquindex.com.br"
def main():
    ROOT.mkdir(exist_ok=True)
    urls=[]; records=[]
    for city,place in CITIES.items():
        for prefix,label in zip(PREFIXES,LABELS):
            host=hostname(prefix,city)
            # BH special legacy names (without 'em' for consultoria, etc.) already handled
            title=f"{label} em {place} | Arquindex"
            description=f"Conheça soluções de {label.lower()} para empresas de {place} e região. Solicite uma avaliação técnica à Arquindex."
            url=f"https://{host}/"
            canonical=f"https://www.arquindex.com.br/atendimento/{city}/{prefix}/"
            structured=json.dumps({"@context":"https://schema.org","@type":"Service","name":label,"areaServed":{"@type":"City","name":place},"provider":{"@type":"Organization","name":"Arquindex","url":"https://www.arquindex.com.br/"}},ensure_ascii=False)
            body=f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><meta name="description" content="{html.escape(description)}"><link rel="canonical" href="{canonical}"><script type="application/ld+json">{structured}</script><style>body{{margin:0;font:18px/1.6 system-ui;color:#18324a;background:#f6f9fc}}header,main,footer{{padding:24px max(20px,calc((100% - 1000px)/2))}}header{{background:#102f4c;color:white}}a{{color:#087b9b}}header a{{color:white}}main{{background:white}}h1{{font-size:clamp(28px,5vw,46px);line-height:1.15}}.cta{{display:inline-block;padding:14px 22px;background:#087b9b;color:white;border-radius:8px;text-decoration:none}}footer{{font-size:14px}}</style></head><body><header><a href="https://www.arquindex.com.br/">Arquindex — Soluções em Gestão Documental</a></header><main><h1>{html.escape(label)} em {html.escape(place)}</h1><p>{html.escape(description)}</p><h2>Como funciona</h2><p>A Arquindex avalia o volume, os tipos documentais, as exigências de segurança, a organização e os formatos de entrega para apresentar uma proposta adequada. O escopo e os prazos dependem do diagnóstico.</p><h2>Atendimento empresarial</h2><p>Solicite informações sobre metodologia, confidencialidade, rastreabilidade e condições comerciais para sua operação.</p><a class="cta" href="https://wa.me/5531973632725?text={quote('Olá, gostaria de orçamento para '+label+' em '+place)}">Solicitar orçamento pelo WhatsApp</a><p><a href="https://www.arquindex.com.br/">Conheça todos os serviços da Arquindex</a></p></main><footer>Arquindex Gestão Documental — Atendimento mediante avaliação de escopo.</footer></body></html>"""
            dest=ROOT/"paginas"/host/"index.html";dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(body,encoding="utf-8")
            records.append({"hostname":host,"cidade":place,"servico":label,"canonical":canonical,"dns":"PENDENTE","tls":"PENDENTE","deploy":"PENDENTE"})
            urls.append(canonical)
    assert len(records)==56 and len({x["hostname"] for x in records})==56
    (ROOT/"inventario.json").write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")
    ns="http://www.sitemaps.org/schemas/sitemap/0.9";ET.register_namespace("",ns)
    root=ET.Element("{%s}urlset"%ns)
    for url in urls: ET.SubElement(ET.SubElement(root,"{%s}url"%ns),"{%s}loc"%ns).text=url
    ET.ElementTree(root).write(ROOT/"sitemap-local.xml",encoding="utf-8",xml_declaration=True)
    print(f"PASS: {len(records)} páginas; {len(urls)} URLs canônicas; nenhum DNS alterado")
if __name__=="__main__": main()
