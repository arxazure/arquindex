"""Fetch real Search Console data via Google OAuth refresh token in GitHub Actions.
Required GitHub secrets: GSC_CLIENT_ID, GSC_CLIENT_SECRET, GSC_REFRESH_TOKEN.
No synthetic rows, no credentials written to disk.
"""
import os,json,datetime,urllib.request,urllib.parse,sys
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


def authorized_property(site):
    if site.get('permissionLevel') not in ('siteOwner', 'siteFullUser', 'siteRestrictedUser'):
        return False
    value = site.get('siteUrl', '')
    if value.startswith('sc-domain:'):
        host = value[len('sc-domain:'):].lower()
    else:
        parsed = urllib.parse.urlsplit(value)
        if parsed.scheme not in ('http', 'https') or parsed.username or parsed.password:
            return False
        host = (parsed.hostname or '').lower()
    return host == 'arquindex.com.br' or host.endswith('.arquindex.com.br')


def main():
    missing=[x for x in ('GSC_CLIENT_ID','GSC_CLIENT_SECRET','GSC_REFRESH_TOKEN') if not os.environ.get(x, "").strip()]
    if missing:
        raise RuntimeError('GSC_NOT_CONFIGURED: missing GitHub Actions secrets '+', '.join(missing))
    try:
        token=oauth_token()
    except Exception as error:
        raise RuntimeError('GSC_OAUTH_FAILED: HTTP '+str(getattr(error, 'code', 'n/a'))) from None
    try:
        sites=request_json('https://www.googleapis.com/webmasters/v3/sites',token=token).get('siteEntry',[])
    except Exception as error:
        raise RuntimeError('GSC_PROPERTY_LIST_FAILED: HTTP '+str(getattr(error, 'code', 'n/a'))) from None
    allowed=sorted({s['siteUrl'] for s in sites if authorized_property(s)})
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
                # Do not replace prior verified data with a partial or empty success.
                # Exception bodies can contain sensitive data; report only type and HTTP status.
                raise RuntimeError('GSC_PROPERTY_READ_FAILED: '+site+'; '+type(e).__name__+'; HTTP '+str(getattr(e, 'code', 'n/a'))) from None
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
    if not allrows:
        raise RuntimeError('GSC_EMPTY_RESULT: prior verified data preserved; review property and date range')
    output={'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'start_date':start.isoformat(),'end_date':end.isoformat(),'source':'Google Search Console API OAuth','properties':property_reports,'rows':allrows}
    p=Path(__file__).with_name('gsc-real.json')
    temp=p.with_suffix('.json.tmp')
    temp.write_text(json.dumps(output,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    temp.replace(p)
    print('GSC properties:',len(property_reports),'rows:',len(allrows))
def run():
    diagnostic = {'platform': 'gsc', 'collection': 'failed', 'source': 'Google Search Console API OAuth',
                  'publication': 'not_attempted', 'indexation': 'not_verified'}
    try:
        main()
        diagnostic.update(collection='completed', code='GSC_COLLECTED')
        return 0
    except Exception as error:
        missing = [key for key in ('GSC_CLIENT_ID', 'GSC_CLIENT_SECRET', 'GSC_REFRESH_TOKEN')
                   if not os.getenv(key, '').strip()]
        known = ('GSC_NOT_CONFIGURED', 'GSC_OAUTH_FAILED', 'GSC_PROPERTY_LIST_FAILED', 'GSC_PROPERTY_READ_FAILED', 'GSC_NO_VERIFIED_ARQUINDEX_PROPERTIES', 'GSC_EMPTY_RESULT')
        code = str(error).split(':', 1)[0]
        diagnostic.update(code=code if code in known else 'GSC_COLLECTION_FAILED',
                          missing=missing, error_type=type(error).__name__,
                          http_status=getattr(error, 'code', None),
                          previous_data='preserved' if Path(__file__).with_name('gsc-real.json').exists() else 'not_available')
        return 2 if missing else 1
    finally:
        directory = Path('artifacts/gsc')
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'status.json').write_text(json.dumps(diagnostic) + '\n', encoding='utf-8')
        print(json.dumps(diagnostic))


if __name__=='__main__':sys.exit(run())
