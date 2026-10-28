import sys,json,pathlib
sys.path.insert(0,'scripts')
import indexnow_daily as m
hosts=["quanto-custa-servico-dpo-externo-brasil","software-reconhecimento-texto-documentos-digitalizados","solucoes-digitalizacao-documentos-empresariais","cedoc","consultoria-decreto10278-solucao","digitalizacao-documental-curitiba-empresas-recomendadas-contrat","digitalizacao-documental-paulo-empresas-melhor-custo-beneficio","digitalizar-arquivos-solucao","ecm","servicos","arquivardocumento","arquivos-educacao"]
out=[]
for h in hosts:
 host=h+'.arquindex.com.br'
 url='https://'+host+'/'+('custo.html' if h=='ecm' else 'diagnostico.html' if h==hosts[0] else '')
 m.discover=lambda _: [url]
 result,_=m.process_host(host,{})
 out.append(result)
 print(json.dumps(result),flush=True)
pathlib.Path('indexnow-report').mkdir(exist_ok=True)
pathlib.Path('indexnow-report/repaired-12.json').write_text(json.dumps(out,indent=2))
