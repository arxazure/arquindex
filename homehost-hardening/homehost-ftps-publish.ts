// Homehost FTPS publisher: explicit, reviewed manifest only. Default DRY RUN.
// Run in Bun with basic-ftp dependency. Never store credentials in GitHub.
import * as ftp from "basic-ftp@5.0.5";
import {Readable, Writable} from "node:stream";
import {readFile} from "node:fs/promises";
import {lookup} from "node:dns/promises";
import {createHash} from "node:crypto";
const manifestPath = process.argv[2];
if (!manifestPath) throw Error("Usage: bun run homehost-ftps-publish.ts manifest.json");
const manifest = JSON.parse(await readFile(manifestPath,"utf8"));
if (manifest.schemaVersion !== 1 || manifest.host !== "www.arquindex.com.br" || !Array.isArray(manifest.files)) throw Error("Invalid manifest");
if (manifest.files.length > 1000) throw Error("Batch too large");
const dryRun = process.env.FTPS_APPLY !== "true";
const host=process.env.FTP_HOST_PRIMARY, user=process.env.FTP_USER, password=process.env.FTP_PASSWORD;
if (!host || !user || !password) throw Error("Missing FTP environment");
const certHost=process.env.FTP_TLS_SERVERNAME || "h59.servidorhh.com";
const [a,b]=await Promise.all([lookup(host,{all:true}),lookup(certHost,{all:true})]);
if (!a.some(x=>b.some(y=>x.address===y.address))) throw Error("FTPS endpoint does not match TLS certificate host");
const client=new ftp.Client(25000); client.ftp.verbose=false;
const hash=b=>createHash("sha256").update(b).digest("hex");
async function get(remote){let size=0;const chunks=[];await client.downloadTo(new Writable({write(chunk,_e,cb){size+=chunk.length;if(size>1024*1024)return cb(Error("Existing file too large"));chunks.push(Buffer.from(chunk));cb();}}),remote);return Buffer.concat(chunks);}
const results=[];
try {
 await client.access({host,user,password,secure:true,secureOptions:{servername:certHost,rejectUnauthorized:true}});
 await client.cd("public_html");
 const root=await client.pwd();
 const files=new Set();
 for (const item of manifest.files) {
  const path=item.path;
  if (typeof path!=="string" || path.startsWith("/") || path.includes("..") || !/^(?:[a-z0-9-]+\/)*[a-z0-9-]+(?:\.html|\/index\.html)$/.test(path) || !/^[a-f0-9]{64}$/.test(item.sha256) || files.has(path)) throw Error("Unsafe or duplicate path: "+path);
  files.add(path);
  if (typeof item.content!=="string" || Buffer.byteLength(item.content)>200000 || hash(Buffer.from(item.content))!==item.sha256) throw Error("Content checksum mismatch: "+path);
  const parts=path.split("/"); const name=parts.pop(); const dir=parts.join("/");
  await client.cd(root);
  let exists=true;
  try {if(dir)await client.cd(dir);} catch {exists=false;}
  let current=null;
  if(exists){const entry=(await client.list()).find(x=>x.name===name);if(entry)current=await get(name);}
  if(current){results.push({path,status:hash(current)===item.sha256?"unchanged":"conflict-existing"});continue;}
  if(dryRun){results.push({path,status:exists?"would-create":"would-create-directories"});continue;}
  await client.cd(root);
  if(dir) await client.ensureDir(root+"/"+dir);
  const tmp="."+name+".arquindex-upload";
  await client.uploadFrom(Readable.from([Buffer.from(item.content)]),tmp);
  if(hash(await get(tmp))!==item.sha256)throw Error("Upload checksum mismatch: "+path);
  await client.rename(tmp,name);
  results.push({path,status:"uploaded"});
 }
} finally {client.close();}
console.log(JSON.stringify({dryRun,files:results.length,results},null,2));
