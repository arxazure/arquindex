"""Resume the explicitly authorized remaining portals, preserving per-host evidence."""
import json,pathlib,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parents[2]
PORTALS=["arquivo-morto-seguro","guarda-rastreavel","descarte-documental","alfresco-implantacao","alfresco-manuais","ecm-custos","ia-documental-local","preservacao-digital","metadados-documentais","lgpd-registros","dpo-operacional","databooks-tecnicos","documentos-rh","auditoria-documental"]
DEST=ROOT/'publish-report/remaining-19'
DEST.mkdir(parents=True,exist_ok=True)
for slug in PORTALS:
 mode='verify' if slug=='arquivo-morto-seguro' else 'pilot'
 for attempt in range(4):
  print('AUTHORIZED_PORTAL',slug,'MODE',mode,'ATTEMPT',attempt+1,flush=True)
  code=subprocess.run([sys.executable,str(ROOT/'scripts/portais-tecnicos/publish.py'),'--mode',mode,'--portal',slug,'--approval','APPROVED:'+slug]).returncode
  source=ROOT/'publish-report/portais-tecnicos-20.json'
  report=json.loads(source.read_text())
  (DEST/(slug+'.json')).write_text(json.dumps(report,indent=2))
  if code==0:break
  results=report.get('results',[])
  if not results or results[-1].get('state')!='pending_dns_tls_or_public_qa' or results[-1].get('error') not in ('COMMUNICATION_DNS','COMMUNICATION_NETWORK','COMMUNICATION_TIMEOUT','COMMUNICATION_TLS'):
   sys.exit(code or 1)
  if attempt==3:sys.exit(code or 1)
  mode='verify'
  time.sleep(30)
 else:sys.exit(1)
print('AUTHORIZED_REMAINING_COMPLETE',len(PORTALS),flush=True)
