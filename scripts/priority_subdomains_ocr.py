#!/usr/bin/env python3
"""Generate three differentiated commercial OCR sites for HomeHost deployment."""
from pathlib import Path
from html import escape
from datetime import date

ROOT = Path("seo-priority-ocr")
SITES = {
 "digitalizar-ocr-especializada": {
  "title":"Digitalização especializada com OCR para empresas",
  "city":"Brasil",
  "intro":"A Arquindex oferece projetos de digitalização especializada com reconhecimento óptico de caracteres, organização de documentos, indexação e arquivos pesquisáveis. O dimensionamento leva em conta volume, conservação, segurança e finalidade de uso.",
  "bullets":["Diagnóstico de acervos e estimativa de volumes","Preparação, digitalização e controle de qualidade","OCR pesquisável e indexação por metadados","Entrega organizada e política de acesso conforme projeto"],
  "faq":[("Qual é a diferença entre digitalização e OCR?","A digitalização produz a imagem do documento. O OCR reconhece caracteres para facilitar a pesquisa; documentos críticos ainda precisam de conferência."),("Posso enviar documentos confidenciais?","Os requisitos de confidencialidade, tratamento de dados e acesso são definidos no escopo e no contrato."),("Como funciona o orçamento?","O valor depende de páginas, formato, estado de conservação, indexação, logística e prazo.")],
 },
 "solucoes-ocr-sp": {
  "title":"Soluções de OCR e digitalização documental em São Paulo",
  "city":"São Paulo",
  "intro":"Empresas em São Paulo podem consultar a Arquindex para projetos de OCR, digitalização e organização de documentos. O atendimento e a logística são avaliados conforme local do acervo, quantidade e requisitos do projeto; não há afirmação de escritório local.",
  "bullets":["Análise da logística para acervos empresariais em São Paulo","Digitalização de contratos, dossiês e documentos administrativos","OCR e entrega de PDFs pesquisáveis","Indexação, conferência e integração documental sob escopo"],
  "faq":[("A Arquindex possui escritório em São Paulo?","A sede da Arquindex fica em Belo Horizonte; projetos em São Paulo dependem de análise de escopo e disponibilidade."),("OCR elimina revisão humana?","Não. A conferência pode ser necessária em documentos degradados e informações críticas."),("Como solicitar orçamento em SP?","Informe município, volume aproximado, tipos de documento e prazo desejado.")],
 },
 "digitalizar-ocr-bh": {
  "title":"Digitalização com OCR em Belo Horizonte para empresas",
  "city":"Belo Horizonte",
  "intro":"Em Belo Horizonte, a Arquindex desenvolve projetos de digitalização com OCR para transformar documentos físicos em arquivos pesquisáveis, organizados e aptos a rotinas empresariais, mediante escopo e critérios de qualidade definidos.",
  "bullets":["Avaliação do acervo e dos documentos por departamento","Digitalização com parâmetros de qualidade acordados","OCR, PDF pesquisável e identificação por metadados","Opções de organização e gestão documental"],
  "faq":[("Quanto custa digitalizar documentos em BH?","O preço depende do volume, da preparação, do OCR, da indexação, da logística e do prazo. Solicite proposta com dados do acervo."),("O papel pode ser eliminado após a digitalização?","Não automaticamente. A destinação depende da legislação e da tabela de temporalidade aplicável."),("A Arquindex atende outras cidades da RMBH?","A viabilidade de coleta e execução é avaliada conforme o município e o escopo.")],
 }
}


# Additional high-impression domains. Each landing page has a distinct search intent.
SITES.update({
 "digitalizar-ocr-empresas":{
  "title":"OCR corporativo: digitalização e pesquisa de documentos",
  "city":"Brasil",
  "intro":"O OCR corporativo facilita a localização de documentos digitalizados em acervos empresariais. A Arquindex combina diagnóstico de tipos documentais, captura, reconhecimento de caracteres, nomenclatura, indexação e controle de qualidade conforme regras estabelecidas no projeto.",
  "bullets":["Inventário dos dossiês, contratos e documentos administrativos","Definição de campos para pesquisa e metadados","Digitalização com OCR e revisão de amostras","Entrega estruturada para gestão eletrônica de documentos"],
  "faq":[("Como pesquisar documentos após o OCR?","O projeto pode entregar PDFs pesquisáveis e índices por metadados, conforme as necessidades de localização."),("É possível processar lotes grandes?","O prazo e a estratégia de processamento são definidos após avaliar volume, formatos e qualidade do acervo."),("O OCR reconhece escrita à mão?","A precisão varia conforme a caligrafia e o material, exigindo testes e conferência quando necessário.")]
 },
 "digitalizacao-ocr-empresas":{
  "title":"Digitalização de documentos com OCR para empresas",
  "city":"Brasil",
  "intro":"Digitalizar documentos empresariais requer mais do que fotografar páginas. Um projeto consistente organiza a preparação, a captura, o reconhecimento textual, a indexação, a conferência e a entrega conforme o destino do acervo e suas obrigações de guarda.",
  "bullets":["Separação e preparo dos originais para captura","Critérios definidos para resolução e legibilidade","OCR pesquisável, nomenclatura e organização de arquivos","Conferência, segurança e rastreabilidade do processo"],
  "faq":[("Qual formato recebo?","PDF pesquisável e demais formatos são definidos na proposta e conforme a finalidade de uso."),("Digitalização certificada é igual a OCR?","Não. OCR permite pesquisa de texto; requisitos legais de digitalização são adicionais e dependem do caso."),("Posso integrar os arquivos a um GED?","A organização por metadados pode ser planejada para facilitar a importação no sistema escolhido.")]
 },
 "arquivo":{
  "title":"Organização e gestão de arquivos físicos empresariais",
  "city":"Belo Horizonte",
  "intro":"A gestão de arquivos empresariais começa pela localização confiável dos documentos. A Arquindex apoia inventário, identificação de caixas, classificação, definição de acesso, temporalidade e integração com serviços de guarda e digitalização.",
  "bullets":["Inventário por caixas, setores e séries documentais","Identificação de responsabilidades e frequência de consultas","Classificação e temporalidade conforme critérios aplicáveis","Planejamento de guarda, digitalização e destinação segura"],
  "faq":[("Como começar a organizar o arquivo morto?","Faça o levantamento das caixas e dos tipos documentais, defina prioridades de consulta e valide critérios de classificação."),("Toda caixa pode ser eliminada após o prazo?","Não. Prazos, suspensões de descarte e requisitos jurídicos precisam ser verificados antes da destinação."),("É possível solicitar documentos guardados?","As modalidades de consulta e recuperação são definidas em contrato e inventário do acervo.")]
 },
 "digitalizacao-exin-bh":{
  "title":"Digitalização empresarial e proteção de dados em Belo Horizonte",
  "city":"Belo Horizonte",
  "intro":"A digitalização de documentos em Belo Horizonte precisa equilibrar produtividade, qualidade documental e proteção de dados pessoais. A Arquindex avalia controles de acesso, tratamento de informações, OCR e indexação de acordo com a sensibilidade do acervo.",
  "bullets":["Mapeamento de documentos e categorias de informação","Definição de operadores, acessos e controles de confidencialidade","Digitalização, OCR e indexação segundo o escopo","Procedimentos de entrega segura e retenção documental"],
  "faq":[("Digitalizar documentos garante conformidade à LGPD?","Não. A conformidade envolve base legal, transparência, segurança, retenção e governança além da digitalização."),("Quais cuidados adotar com prontuários?","São necessários controles específicos de acesso, sigilo, retenção e regras setoriais aplicáveis."),("A Arquindex realiza diagnóstico do projeto?","O escopo e os controles são avaliados antes da proposta de serviço.")]
 },
 "digitalizar-arquivos-rj":{
  "title":"Digitalização e organização de arquivos corporativos no Rio de Janeiro",
  "city":"Rio de Janeiro",
  "intro":"Organizações no Rio de Janeiro podem consultar a Arquindex para projetos de digitalização e organização de arquivos físicos e eletrônicos. A execução e a logística de coleta dependem da análise de escopo, cidade, volume e requisitos de segurança; a empresa não declara escritório local.",
  "bullets":["Levantamento de volume, localidade e tipos documentais","Planejamento de transporte ou processamento conforme viabilidade","Digitalização com OCR e indexação quando contratados","Entrega com estrutura de arquivos e critérios de aceite"],
  "faq":[("Há coleta de documentos no Rio de Janeiro?","A possibilidade de coleta é avaliada conforme endereço, volume e condições do projeto."),("Qual é o prazo de execução?","Depende da quantidade de páginas, da preparação e do nível de indexação."),("Como solicitar orçamento?","Informe município, estimativa de caixas ou páginas e tipos de documentos.")]
 },
 "digitalizar-arquivos-sp":{
  "title":"Digitalização de arquivos empresariais em São Paulo",
  "city":"São Paulo",
  "intro":"A Arquindex avalia demandas de digitalização de arquivos de empresas de São Paulo, com foco em preparação, reconhecimento textual, organização documental e entrega pesquisável. Atendimento fora de Belo Horizonte sujeito a escopo e viabilidade logística.",
  "bullets":["Diagnóstico dos arquivos por setor ou unidade","Definição de padrões de digitalização e identificação","OCR e indexação de documentos conforme contrato","Conferência e entrega para arquivo digital ou GED"],
  "faq":[("Vocês digitalizam arquivos empresariais em SP?","Projetos em São Paulo são avaliados individualmente conforme volume, escopo e logística."),("Posso digitalizar só parte do arquivo?","Sim, é possível dimensionar um lote piloto ou uma série documental específica."),("O arquivo digitalizado substitui o original?","A validade e a destinação dependem do regime jurídico e dos requisitos técnicos aplicáveis.")]
 }
})

def page(slug, data):
 host=f"{slug}.arquindex.com.br"
 url=f"https://{host}/"
 title=escape(data["title"])
 desc=escape(data["intro"][:155],quote=True)
 import json
 schema={"@context":"https://schema.org","@type":"Service","name":data["title"],"provider":{"@type":"Organization","name":"Arquindex","url":"https://www.arquindex.com.br/"},"areaServed":data["city"]}
 bullets="".join(f"<li>{escape(x)}</li>" for x in data["bullets"])
 faqs="".join(f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q,a in data["faq"])
 return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} | Arquindex</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}"><meta name="robots" content="index,follow,max-image-preview:large"><style>body{{margin:0;font:17px/1.7 system-ui,Arial;color:#173047;background:#fff}}header,footer{{background:#123550;color:white;padding:22px 6%}}a{{color:#075c88}}header a,footer a{{color:white}}main{{max-width:1060px;margin:auto;padding:25px 5%}}h1{{font-size:clamp(2rem,5vw,3.2rem);line-height:1.2}}section{{padding:20px 0;border-bottom:1px solid #dce5e9}}.hero{{background:#ecf5f7;border-radius:14px;padding:26px}}.cta{{display:inline-block;background:#08694d;color:#fff;padding:12px 20px;border-radius:8px;text-decoration:none;font-weight:700}}nav a{{display:inline-block;margin:6px 16px 6px 0}}details{{padding:12px;border-bottom:1px solid #ddd}}summary{{cursor:pointer;font-weight:600}}</style><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head><body><header><strong>ARQUINDEX</strong> · <a href="https://www.arquindex.com.br/">Portal principal</a></header><main><section class="hero"><h1>{title}</h1><p>{escape(data["intro"])}</p><a class="cta" href="https://wa.me/5531973632725?text=Ol%C3%A1%20Arquindex%2C%20quero%20or%C3%A7amento%20de%20OCR">Solicitar orçamento pelo WhatsApp</a></section><section><h2>Etapas e entregas do projeto</h2><p>O levantamento inicial define o escopo, os tipos de documentos, os critérios de conferência, o tratamento de dados, os prazos e o formato de entrega. Cada acervo exige uma proposta técnica compatível com seus riscos e objetivos.</p><ul>{bullets}</ul><p>O reconhecimento de texto facilita a busca, mas não substitui verificações humanas quando a qualidade do original ou a criticidade dos dados exige precisão adicional.</p></section><section><h2>Como contratar</h2><p>Informe a quantidade aproximada de páginas ou caixas, o tipo documental, a cidade, a necessidade de coleta, o nível de indexação e o prazo pretendido. A Arquindex poderá avaliar o serviço de digitalização, OCR e gestão documental de forma integrada.</p><a class="cta" href="https://www.arquindex.com.br/">Conhecer a Arquindex</a></section><section><h2>Serviços complementares</h2><nav aria-label="Serviços relacionados"><a href="https://www.arquindex.com.br/digitalizacao-com-ocr.html">Digitalização com OCR</a><a href="https://www.arquindex.com.br/guarda_de_documentos.html">Guarda documental</a><a href="https://www.arquindex.com.br/gestao_documental_documentos.html">Gestão documental</a><a href="https://www.arquindex.com.br/lgpd-consultoria.html">LGPD</a></nav></section><section><h2>Perguntas frequentes</h2>{faqs}</section></main><footer>Arquindex — Gestão documental e digitalização · <a href="https://www.arquindex.com.br/">www.arquindex.com.br</a></footer></body></html>"""

def main():
 for slug,data in SITES.items():
  root=ROOT/(slug+".arquindex.com.br")
  root.mkdir(parents=True,exist_ok=True)
  host=slug+".arquindex.com.br"
  (root/"index.html").write_text(page(slug,data),encoding="utf-8")
  (root/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: https://{host}/sitemap.xml\n",encoding="utf-8")
  (root/"sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://{host}/</loc></url></urlset>\n',encoding="utf-8")
  print(host,"PAGE_GENERATED",len(data["faq"]),"FAQs")
if __name__=="__main__":
 main()
