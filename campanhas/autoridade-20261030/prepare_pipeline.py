from pathlib import Path
R=Path(__file__).resolve().parents[2]
s=(R/'scripts/publicar-alfresco-automacao.py').read_text()
s=s.replace('alfresco-automacao-manifest.json','autoridade-20261030-manifest.json').replace('publish-report/alfresco-automacao','publish-report/autoridade-20261030').replace('sitemap-alfresco-automacao.xml','sitemap-autoridade-20261030.xml').replace('ARQ-ALFRESCO-AUTOMACAO-20261029','ARQ-AUTORIDADE-20261030').replace("'alfresco-automacao-'","'autoridade-20261030-'").replace("'2026-10-29'","'2026-10-30'")
start=s.index(' block=b\'');end=s.index(" NS='http://www.sitemaps.org",start)
s=s[:start]+''' targets={
  'guarda_de_documentos.html':('Guarda digital e recuperação dos documentos','guias/guarda-digital-documentos-seguranca/'),
  'alfresco-belo-horizonte/index.html':('Planeje metadados, permissões e automação no ECM','guias/alfresco-ecm-implantacao-e-automacao/'),
  'alfresco-cloud-ocr-ia/index.html':('Implantação e operação do ECM','guias/alfresco-ecm-implantacao-e-automacao/'),
  'consultoria-lgpd-belo-horizonte/index.html':('Como integrar LGPD aos documentos','guias/consultoria-lgpd-gestao-documental/'),
  'gestao-documental-belo-horizonte/index.html':('Classificação, eventos e temporalidade','guias/gestao-documental-classificacao-temporalidade/'),
  'index.html':('Gestão documental: conheça as soluções e os guias da Arquindex','gestao-documental-brasil/')}
 result['existing_pages_updated']=[]
 for p,(title,link) in targets.items():
  target='/public_html/'+p;old=get(f,target)
  if old is None:continue
  text=old.decode('utf-8')
  assert 'arquindex' in text.lower(),'UNEXPECTED_REMOTE_SITE'
  if 'id="arq-autoridade-20261030"' in text:continue
  block=('<section id="arq-autoridade-20261030" style="max-width:1080px;margin:24px auto;padding:24px;box-sizing:border-box"><h2>'+title+'</h2><p><a href="/'+link+'">Leia o guia prático</a> para planejar escopo, controles e critérios de aceite.</p><p>Atendimento: <a href="/atendimento/gestao-documental-rm-bh/">Região Metropolitana de Belo Horizonte</a> e <a href="/atendimento/gestao-documental-rm-sp/">Região Metropolitana de São Paulo</a>, conforme escopo e logística contratados.</p></section>')
  # Use a semantic closing anchor without assuming the checked-out root is the live site.
  m=re.search(r'</main\\s*>',text,re.I) or re.search(r'</body\\s*>',text,re.I)
  assert m,'HTML_INSERTION_ANCHOR_MISSING'
  planned[target]=(text[:m.start()]+block+text[m.start():]).encode()
  result['existing_pages_updated'].append(BASE+p)
''' +s[end:]
(R/'scripts/publicar-autoridade-20261030.py').write_text(s)
s=(R/'scripts/qa/alfresco-automacao.cjs').read_text().replace('alfresco-automacao-manifest.json','autoridade-20261030-manifest.json').replace('publish-report/alfresco-automacao','publish-report/autoridade-20261030').replace('sitemap-alfresco-automacao.xml','sitemap-autoridade-20261030.xml').replace('ARQ-ALFRESCO-AUTOMACAO-20261029','ARQ-AUTORIDADE-20261030')
# Resolve browser from setup rather than assume a runner-installed Chrome.
s=s.replace(",executablePath:'/usr/bin/google-chrome'",'')
(R/'scripts/qa/autoridade-20261030.cjs').write_text(s)
s=(R/'scripts/descobrir-alfresco-automacao.py').read_text().replace('publish-report/alfresco-automacao','publish-report/autoridade-20261030').replace('sitemap-alfresco-automacao.xml','sitemap-autoridade-20261030.xml')
(R/'scripts/descobrir-autoridade-20261030.py').write_text(s)
