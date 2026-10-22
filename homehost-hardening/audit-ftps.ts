// Read-only inventory of Homehost public_html for Search Console URL exports.
// Usage: bun run homehost-hardening/audit-ftps.ts urls.json > audit.json
// Input: JSON array of URLs, or {urls:[{url:"https://..."}]}.
import * as ftp from "basic-ftp@5.0.5";
import {readFile} from "node:fs/promises";
import {lookup} from "node:dns/promises";
const input=JSON.parse(await readFile(process.argv[2],"utf8"));
const items=Array.isArray(input)?input:input.urls;
if(!Array.isArray(items))throw Error("Expected URL array");
const host=process.env.FTP_HOST_PRIMARY,user=process.env.FTP_USER,password=process.env.FTP_PASSWORD;
if(!host||!user||!password)throw Error("Missing FTP environment");
const tlsHost=process.env.FTP_TLS_SERVERNAME||"h59.servidorhh.com";
const [a,b]=await Promise.all([lookup(host,{all:true}),lookup(tlsHost,{all:true})]);
if(!a.some(x=>b.some(y=>x.address===y.address)))throw Error("FTP DNS does not match TLS server");
const client=new ftp.Client(30000);client.ftp.verbose=false;
const results=[], cache=new Map();
try {
 await client.access({host,user,password,secure:true,secureOptions:{servername:tlsHost,rejectUnauthorized:true}});
 await client.cd("public_html");
 const root=await client.pwd();
 async function listing(dir){
  if(cache.has(dir))return cache.get(dir);
  try{await client.cd(root);if(dir)await client.cd(dir);const list=await client.list();cache.set(dir,list);return list;}
  catch(e){cache.set(dir,null);return null;}
 }
 for(const item of items){
  const raw=typeof item==="string"?item:item.url;
  if(typeof raw!=="string")continue;
  let url;try{url=new URL(raw);}catch{results.push({url:raw,status:"invalid-url"});continue;}
  if(!["arquindex.com.br","www.arquindex.com.br"].includes(url.hostname)){results.push({url:raw,status:"other-host"});continue;}
  let path;try{path=decodeURIComponent(url.pathname);}catch{results.push({url:raw,status:"invalid-path"});continue;}
  if(path.includes("..")||path.includes("\\")||!/^\/[a-zA-Z0-9_./%-]*$/.test(path)){results.push({url:raw,status:"unsafe-path"});continue;}
  const bits=path.split("/").filter(Boolean);
  const ext=bits.length?bits[bits.length-1].split(".").pop().toLowerCase():"";
  if(["bak","py","sql","env","log","zip","json","xlsx","csv","txt","php"].includes(ext)){results.push({url:raw,status:"internal-or-non-html-review"});continue;}
  const isDir=path.endsWith("/")||!bits[bits.length-1]?.includes(".");
  const parent=(isDir?bits:bits.slice(0,-1)).join("/");
  const entries=await listing(parent);
  if(!entries){results.push({url:raw,status:"directory-missing-or-inaccessible",ftpPath:"public_html/"+parent});continue;}
  const candidates=isDir?["index.html","index.php","index.htm"]: [bits[bits.length-1]];
  const found=entries.find(e=>candidates.includes(e.name));
  results.push({url:raw,status:found?"ftp-file-present":"ftp-file-missing",ftpPath:"public_html/"+(parent?parent+"/":"")+(found?.name||candidates[0]),bytes:found?.size??null});
 }
}finally{client.close();}
const summary=Object.fromEntries([...new Set(results.map(x=>x.status))].map(s=>[s,results.filter(x=>x.status===s).length]));
console.log(JSON.stringify({checkedAt:new Date().toISOString(),summary,results},null,2));
