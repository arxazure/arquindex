#!/usr/bin/env python3
"""Prepara patches HTML E-E-A-T/AEO em cópias locais, sem FTP nem deploy."""
import argparse
import json
from pathlib import Path
from html.parser import HTMLParser

BLOCKS = {
 "digitalizacao": {
  "heading": "Como funciona a digitalização empresarial?",
  "answer": "A digitalização empresarial envolve preparação, captura, conferência e indexação dos documentos. Conforme o escopo, pode incluir OCR, PDF pesquisável e metadados. A conformidade com o Decreto 10.278/2020 depende dos requisitos aplicáveis; escanear não garante automaticamente equivalência jurídica.",
  "steps": ["Diagnóstico do acervo e critérios de aceite", "Preparação, captura e controle de qualidade", "Entrega organizada, conferência e rastreabilidade"],
  "faq": [("O OCR substitui a conferência?", "Não. Erros de reconhecimento exigem controles de qualidade compatíveis com o uso dos dados."), ("Quando guardar o original?", "A retenção depende do tipo documental, das obrigações legais e dos requisitos aplicáveis.")],
  "service": "Digitalização empresarial de documentos",
 },
 "guarda": {
  "heading": "Como funciona a guarda de documentos?",
  "answer": "A guarda documental organiza caixas e documentos com inventário, localização, autorização de acesso e controle de movimentações. Prazos de retenção e destinação dependem da classificação documental e das obrigações aplicáveis.",
  "steps": ["Inventário e identificação", "Custódia e localização controlada", "Consulta, devolução e destinação autorizada"],
  "faq": [("Como localizar uma caixa?", "Por meio de inventário e identificação definidos no contrato."), ("O descarte é automático?", "Não. Depende de avaliação de temporalidade, obrigações e autorização.")],
  "service": "Guarda e custódia documental",
 },
 "alfresco": {
  "heading": "O que considerar em um projeto GED/ECM Alfresco?",
  "answer": "Uma solução GED/ECM reúne documentos, metadados, permissões, pesquisa e fluxos. O custo e a arquitetura dependem de versão, edição, infraestrutura, integrações, segurança e sustentação contratadas.",
  "steps": ["Levantamento de requisitos e arquitetura", "Implantação, permissões e integrações", "Testes, backup, aceite e sustentação"],
  "faq": [("Alfresco é sempre gratuito?", "Não. Licenças, infraestrutura, implantação e operação variam conforme a solução."), ("Como validar a recuperação?", "Por testes documentados de restauração, acesso e integridade.")],
  "service": "Implantação e operação GED ECM Alfresco",
 },
 "lgpd": {
  "heading": "O que envolve uma consultoria LGPD?",
  "answer": "Um projeto LGPD mapeia tratamentos, avalia bases legais e riscos, define responsabilidades, controles e documentos e acompanha sua implementação. Modelos isolados não garantem conformidade.",
  "steps": ["Diagnóstico e inventário de tratamentos", "Avaliação de riscos, controles e responsabilidades", "Plano de ação, treinamento e acompanhamento"],
  "faq": [("Toda empresa precisa indicar encarregado?", "A obrigação e eventuais dispensas dependem das regras aplicáveis e da situação da organização."), ("O que é ROPA?", "É o registro das operações de tratamento de dados pessoais.")],
  "service": "Consultoria LGPD e governança de dados",
 },
 "ocr": {
  "heading": "Como tornar documentos pesquisáveis com OCR?",
  "answer": "OCR converte imagens de texto em caracteres pesquisáveis, mas pode errar nomes, números, tabelas e manuscritos. A qualidade depende da captura, idioma, processamento e revisão.",
  "steps": ["Avaliação de qualidade e legibilidade", "Reconhecimento de caracteres e indexação", "Amostragem, conferência e entrega"],
  "faq": [("OCR garante precisão total?", "Não. A precisão depende da origem e dos controles de revisão."), ("PDF pesquisável substitui o original?", "Não necessariamente. O uso e a retenção dependem do contexto documental.")],
  "service": "OCR e PDFs pesquisáveis",
 },
}
class Counter(HTMLParser):
 def __init__(self):
  super().__init__(); self.h1=0;self.canonicals=0;self.block=0;self.body=0
 def handle_starttag(self, tag, attrs):
  d=dict(attrs)
  if tag=="h1":self.h1+=1
  if tag=="link" and "canonical" in d.get("rel","").split():self.canonicals+=1
  if tag=="section" and d.get("id")=="aq-eeat-aeo":self.block+=1
  if tag=="body":self.body+=1

def esc(s):
 import html
 return html.escape(s,quote=True)
def make_block(item):
 steps="".join("<li>"+esc(x)+"</li>" for x in item["steps"])
 faq="".join("<h3>"+esc(q)+"</h3><p>"+esc(a)+"</p>" for q,a in item["faq"])
 return ('\n<section id="aq-eeat-aeo" aria-labelledby="aq-eeat-heading" class="aq-eeat-aeo">'
         '<h2 id="aq-eeat-heading">'+esc(item["heading"])+'</h2><p>'+esc(item["answer"])+'</p>'
         '<h3>Etapas e entregáveis</h3><ol>'+steps+'</ol><h2>Perguntas frequentes</h2>'+faq+
         '<p><strong>Transparência:</strong> etapas, entregáveis e condições finais são definidos em proposta e contrato. '
         'Solicite critérios de qualidade, confidencialidade e aceite aplicáveis ao seu projeto.</p></section>\n')
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--service",choices=BLOCKS,required=True)
 p.add_argument("--input",required=True,type=Path)
 p.add_argument("--output",required=True,type=Path)
 a=p.parse_args()
 if a.input.resolve()==a.output.resolve():p.error("Saída deve ser diferente da origem")
 html=a.input.read_text(encoding="utf-8")
 c=Counter();c.feed(html)
 if c.body!=1 or c.h1!=1 or c.canonicals!=1 or c.block: p.error("Pré-condição falhou: exige body/H1/canonical únicos e bloco ainda ausente")
 pos=html.lower().rfind("</main>")
 if pos<0:p.error("Sem </main> explícito: revisão manual obrigatória")
 result=html[:pos]+make_block(BLOCKS[a.service])+html[pos:]
 check=Counter();check.feed(result)
 if check.h1!=1 or check.canonicals!=1 or check.block!=1:p.error("Regressão estrutural")
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(result,encoding="utf-8")
 print(json.dumps({"status":"staged_only","service":a.service,"input":str(a.input),"output":str(a.output),"h1":check.h1,"canonical":check.canonicals,"eeat_block":check.block},ensure_ascii=False))
if __name__=="__main__":main()
