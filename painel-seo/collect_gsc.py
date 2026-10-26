"""Fetch real Search Console data via Google OAuth refresh token in GitHub Actions.
Required GitHub secrets: GSC_CLIENT_ID, GSC_CLIENT_SECRET, GSC_REFRESH_TOKEN.
No synthetic rows, no credentials written to disk.
"""
import os,json,datetime,urllib.request,urllib.parse
from pathlib import Path

def request_json(url, payload=None, token=None):
    data=json.dumps(payload).encode() if payload is not None else None
    headers={'Accept':'application/json','User-Agent':'Arquindex-GSC-GitHub/1.0'}
    if data is not None: headers['Content-Type']='application/json'
    if token: headers['Authorization']='Bearer '+token
    with urllib.request.urlopen(urllib.request.Request(url,data=data,headers=headers),timeout=35) as response:
        return json.load(response)

def oauth_token():
    params=urllib.parse.urlencode({
      'client_id':os.environ['GSC_CLIENT_ID'],
      'client_secret':os.environ['GSC_CLIENT_SECRET'],
      'refresh_token':os.environ['GSC_REFRESH_TOKEN'],
      'grant_type':'refresh_token'
    }).encode()
    with urllib.request.urlopen(urllib.request.Request('https://oauth2.googleapis.com/token',data=params),timeout=35) as response:
        return json.load(response)['access_token']

def main():
    missing=[x for x in ('GSC_CLIENT_ID','GSC_CLIENT_SECRET','GSC_REFRESH_TOKEN') if not os.environ.get(x)]
    if missing:
        raise RuntimeError('GSC_NOT_CONFIGURED: missing GitHub Actions secrets '+', '.join(missing))
    token=oauth_token()
    sites=request_json('https://www.googleapis.com/webmasters/v3/sites',token=token).get('siteEntry',[])
    allowed=[s['siteUrl'] for s in sites if s.get('permissionLevel') not in ('siteUnverifiedUser',) and ('arquindex.com.br' in s.get('siteUrl',''))]
    today=datetime.date.today()
    end=today-datetime.timedelta(days=3)
    start=end-datetime.timedelta(days=27)
    allrows=[]
    property_reports=[]
    for site in allowed:
        endpoint='https://www.googleapis.com/webmasters/v3/sites/'+urllib.parse.quote(site,safe='')+'/searchAnalytics/query'
        count=0
        for offset in range(0,25000,2500):
            body={'startDate':start.isoformat(),'endDate':end.isoformat(),'dimensions':['query','page'],'rowLimit':2500,'startRow':offset,'type':'web'}
            try: response=request_json(endpoint,body,token)
            except Exception as e:
                print('Could not read property '+site+': '+str(e)[:180])
                break
            rows=response.get('rows',[])
            for r in rows:
                keys=r.get('keys',[])
                if len(keys)<2:continue
                allrows.append({'property':site,'query':keys[0],'page':keys[1],'clicks':r.get('clicks',0),'impressions':r.get('impressions',0),'ctr':r.get('ctr',0),'position':r.get('position',0)})
            count+=len(rows)
            if len(rows)<2500:break
        property_reports.append({'property':site,'rows':count})
    if not allowed:
        raise RuntimeError('GSC_NO_VERIFIED_ARQUINDEX_PROPERTIES: check OAuth authorization and Search Console access')
    output={'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'start_date':start.isoformat(),'end_date':end.isoformat(),'source':'Google Search Console API OAuth','properties':property_reports,'rows':allrows}
    p=Path(__file__).with_name('gsc-real.json')
    p.write_text(json.dumps(output,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    print('GSC properties:',len(property_reports),'rows:',len(allrows))
if __name__=='__main__':main()
