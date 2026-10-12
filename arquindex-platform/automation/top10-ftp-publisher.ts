import * as ftp from "basic-ftp@5.0.5";

function safe(x:any){ return String(x ?? "").replace(/\r?\n/g," "); }

async function connectHost(host:string){
  const client = new ftp.Client(15000);
  client.ftp.verbose = false;
  try {
    await client.access({
      host,
      user: Bun.env.FTP_USER!,
      password: Bun.env.FTP_PASSWORD!,
      secure: true,
      secureOptions: {servername:'h59.servidorhh.com',rejectUnauthorized:true}
    });
    const pwd = await client.pwd();
    const root = await client.list();
    let publicHtml:any[] = [];
    try {
      await client.cd("public_html");
      publicHtml = await client.list();
    } catch {}
    return {
      ok:true,
      host,
      pwd,
      root:root.map(x=>({name:x.name,type:x.type,size:x.size,modifiedAt:x.modifiedAt?.toISOString?.() ?? null})),
      public_html:publicHtml.map(x=>({name:x.name,type:x.type,size:x.size,modifiedAt:x.modifiedAt?.toISOString?.() ?? null}))
    };
  } catch(e:any) {
    return {ok:false,host,error:safe(e?.message||e)};
  } finally {
    client.close();
  }
}

export default {
  async fetch(req:Request) {
    const u = new URL(req.url);
    if (u.pathname === "/health") return Response.json({ok:true});
    if (u.pathname !== "/probe") return new Response("Not found",{status:404});
    if (req.headers.get("x-maintenance-key") !== Bun.env.MAINTENANCE_KEY) return new Response("Forbidden",{status:403});
    const hosts = [Bun.env.FTP_HOST_PRIMARY, Bun.env.FTP_HOST_FALLBACK].filter(Boolean) as string[];
    const results = [];
    for (const h of hosts) results.push(await connectHost(h));
    return Response.json({results});
  }
};
// One-shot publication of the approved, pinned Arquindex batch. No credential export.
import {Readable,Writable} from 'node:stream';
import {lookup} from 'node:dns/promises';
const batchSha='897b968d1ada329cbaae6a39783abbc437d4f4cd';
const batchOrigin='https://raw.githubusercontent.com/arxazure/arquindex/'+batchSha+'/arquindex-platform/top10-public/';
const batchMarker='/backups/top10-'+batchSha+'-tls-v2.json';
function digest(data:Uint8Array){return crypto.subtle.digest('SHA-256',data).then(v=>Array.from(new Uint8Array(v)).map(n=>n.toString(16).padStart(2,'0')).join(''));}
async function downloadFtp(client:any,path:string,limit=400000){let size=0;const chunks:Buffer[]=[];const sink=new Writable({write(chunk,_enc,done){size+=chunk.length;if(size>limit)return done(Error('FTP download exceeds limit'));chunks.push(Buffer.from(chunk));done();}});await client.downloadTo(sink,path);return Buffer.concat(chunks);}
async function publicBody(url:string){const r=await fetch(url,{signal:AbortSignal.timeout(20000),redirect:'error'});if(!r.ok)throw Error('HTTP '+r.status+' for published URL');return new Uint8Array(await r.arrayBuffer());}
async function publishTop10Batch(){
 if(await Bun.file(batchMarker).exists()){console.log('TOP10_BATCH already attempted; no automatic replay');return;}
 const report:any={batchSha,startedAt:new Date().toISOString(),uploaded:0,verified:0,state:'attempting'};
 await Bun.write(batchMarker,JSON.stringify(report));
 const client=new ftp.Client(25000);client.ftp.verbose=false;
 try{
  const manifest=await fetch(batchOrigin+'manifest.json',{signal:AbortSignal.timeout(20000)}).then(r=>{if(!r.ok)throw Error('Pinned manifest not available');return r.json();});
  if(manifest.domain!=='https://www.arquindex.com.br'||manifest.basePath!=='/top10'||manifest.files.length!==118)throw Error('Batch scope mismatch');
  for(const f of manifest.files)if(!/^(?:(?:guias|artigos)\/[a-z0-9-]+\.html|index\.html|sitemap\.xml|top10[a-z0-9]+\.txt)$/.test(f.path)||!/^\w{64}$/.test(f.sha256)||f.bytes>100000)throw Error('Invalid manifest entry');
  if(!Bun.env.FTP_HOST_PRIMARY||!Bun.env.FTP_USER||!Bun.env.FTP_PASSWORD)throw Error('Existing FTP environment incomplete');
  // Require authenticated TLS; do not downgrade to plaintext or ignore certificate errors.
  const certificateHost='h59.servidorhh.com';
  const [targetAddresses,certificateAddresses]=await Promise.all([lookup(Bun.env.FTP_HOST_PRIMARY,{all:true}),lookup(certificateHost,{all:true})]);
  if(!targetAddresses.some(a=>certificateAddresses.some(b=>a.address===b.address)))throw Error('Certificate host DNS does not match configured FTP endpoint');
  await client.access({host:Bun.env.FTP_HOST_PRIMARY,user:Bun.env.FTP_USER,password:Bun.env.FTP_PASSWORD,secure:true,secureOptions:{servername:certificateHost,rejectUnauthorized:true}});
  await client.cd('public_html');
  const root=await client.pwd();const listing=await client.list();
  const index=listing.find((f:any)=>['index.html','index.php','index.htm'].includes(f.name));
  if(!index)throw Error('Business root index not found');
  const home=(await downloadFtp(client,index.name)).toString('utf8');
  const canonical=(home.match(/<link\b[^>]*>/gi)||[]).some(tag=>/rel=["']canonical["']/i.test(tag)&&/href=["']https:\/\/(?:www\.)?arquindex\.com\.br\/["']/i.test(tag));
  if(!canonical)throw Error('Root does not confirm Arquindex canonical; no file written');
  const base=root.replace(/\/$/,'')+'/top10';
  for(const f of manifest.files){
   const r=await fetch(batchOrigin+f.path,{signal:AbortSignal.timeout(20000)});if(!r.ok)throw Error('Source unavailable: '+f.path);
   const bytes=new Uint8Array(await r.arrayBuffer());if(bytes.length!==f.bytes||await digest(bytes)!==f.sha256)throw Error('Source integrity mismatch: '+f.path);
   const slash=f.path.lastIndexOf('/');const dir=slash<0?base:base+'/'+f.path.slice(0,slash);const name=f.path.slice(slash+1);
   await client.ensureDir(dir);const existing=(await client.list()).find((x:any)=>x.name===name);
   if(existing){if(await digest(await downloadFtp(client,name,100000))!==f.sha256)throw Error('Existing file conflict: '+f.path);}
   else {const temp='.'+name+'.top10-upload';await client.uploadFrom(Readable.from([Buffer.from(bytes)]),temp);if(await digest(await downloadFtp(client,temp,100000))!==f.sha256)throw Error('Upload verification failed');await client.rename(temp,name);report.uploaded++;}
  }
  client.close();
  for(const f of manifest.files){const body=await publicBody(manifest.domain+'/top10/'+f.path);if(await digest(body)!==f.sha256)throw Error('Public integrity mismatch: '+f.path);report.verified++;}
  report.state='published';report.hub=manifest.domain+'/top10/index.html';report.sitemap=manifest.domain+'/top10/sitemap.xml';
  const urlList=manifest.pages.map((p:any)=>manifest.domain+'/top10/'+p.path);
  const response=await fetch('https://api.indexnow.org/indexnow',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({host:'www.arquindex.com.br',key:manifest.key,keyLocation:manifest.domain+'/top10/'+manifest.key+'.txt',urlList}),signal:AbortSignal.timeout(20000)});
  report.indexNow={status:response.status,count:urlList.length,accepted:[200,202].includes(response.status),indexed:false};
 }catch(e:any){report.state=report.state==='published'?'published_indexnow_pending':'blocked';let message=String(e?.message||e).slice(0,350);for(const key of ['FTP_PASSWORD','FTP_USER','MAINTENANCE_KEY'])if(Bun.env[key])message=message.replaceAll(Bun.env[key]!, '[redacted]');report.error=message;}
 finally{client.close();report.finishedAt=new Date().toISOString();await Bun.write(batchMarker,JSON.stringify(report));console.log('TOP10_BATCH_RESULT '+JSON.stringify(report));}
}
publishTop10Batch().catch(()=>console.error('TOP10_BATCH fatal error; inspect marker, no automatic replay'));
