import test from 'node:test';import assert from 'node:assert/strict';
import {isPublicIPv4,validateTarget,resolveTarget,pinnedOptions,analyzePage,scanPage} from '../web-audit.js';
const publicResolver=async()=>[{address:'93.184.216.34',family:4}];
test('bloqueia redes privadas, loopback, metadados, reservadas e IPv6',()=>{
 for(const ip of ['0.0.0.0','10.1.2.3','127.0.0.1','169.254.169.254','172.16.0.1','172.31.255.255','192.168.1.1','100.100.100.200','198.18.0.1','198.51.100.1','203.0.113.1','224.0.0.1','255.255.255.255','168.63.129.16','::1','::ffff:127.0.0.1'])assert.equal(isPublicIPv4(ip),false,ip);
 assert.equal(isPublicIPv4('93.184.216.34'),true);assert.equal(isPublicIPv4('8.8.8.8'),true);
});
test('normalização de URL não permite IPs alternativos ou credenciais',()=>{
 for(const u of ['http://example.com','https://127.0.0.1','https://2130706433','https://0x7f000001','https://[::1]','https://user:pass@example.com','https://example.com:8443','https://metadata.google.internal','https://localhost','file:///etc/passwd','https://example.com/?access_token=secret'])assert.throws(()=>validateTarget(u),u);
 assert.equal(validateTarget('https://EXAMPLE.com./a#section').href,'https://example.com/a');
});
test('DNS misto público/privado é recusado antes de qualquer conexão',async()=>{
 await assert.rejects(resolveTarget(new URL('https://example.com'),async()=>[{address:'93.184.216.34',family:4},{address:'10.0.0.1',family:4}]));
 await assert.rejects(resolveTarget(new URL('https://example.com'),async()=>[{address:'::1',family:6}]));
 const r=await resolveTarget(new URL('https://example.com'),async()=>[{address:'::1',family:6},{address:'93.184.216.34',family:4}]);assert.equal(r.family,4);
});
test('transporte fixa o IPv4 validado e preserva validação TLS',async()=>{
 const o=pinnedOptions(new URL('https://example.com'),{address:'93.184.216.34',family:4},1000);assert.equal(o.servername,'example.com');assert.equal(o.rejectUnauthorized,true);assert.equal(o.agent,false);assert.equal(o.family,4);assert.equal(o.autoSelectFamily,false);
 await new Promise((resolve,reject)=>o.lookup('example.com',{all:true},(err,a)=>{try{assert.ifError(err);assert.deepEqual(a,[{address:'93.184.216.34',family:4}]);resolve();}catch(e){reject(e);}}));
 await new Promise(resolve=>o.lookup('other.example.com',{},err=>{assert.ok(err);resolve();}));
});
test('redirecionamento para rede interna não chega ao transporte',async()=>{
 let calls=0;await assert.rejects(scanPage('https://example.com',{resolver:publicResolver,transport:async()=>{calls++;return {status:302,headers:{location:'https://127.0.0.1/admin'},html:''};}}));assert.equal(calls,1);
 let connections=0;await assert.rejects(scanPage('https://example.com',{resolver:async h=>h==='example.com'?publicResolver():[{address:'10.0.0.5',family:4}],transport:async()=>{connections++;return {status:302,headers:{location:'https://hidden.example.net'},html:''};}}));assert.equal(connections,1);
});
test('limita cadeia de redirecionamentos e revalida cada destino',async()=>{
 let calls=0;await assert.rejects(scanPage('https://example.com',{resolver:publicResolver,transport:async()=>{calls++;return {status:302,headers:{location:'/next'},html:''};}}));assert.equal(calls,4);
});
test('relatório não conserva valores dos cookies nem inventa conformidade',()=>{
 const report=analyzePage({'set-cookie':['sid=VERY_SECRET; Secure; HttpOnly; SameSite=Lax'],'content-security-policy':"frame-ancestors 'none'"},'<title>Exemplo</title><a href="/privacidade?x=1">Privacidade</a><script src="https://cdn.example.net/a.js"></script><form>Cookies</form>',200,new URL('https://example.com'));
 assert.equal(report.cookies[0].name,'sid');assert.equal(report.cookies[0].secure,true);assert.equal(report.cookies[0].httpOnly,true);assert.ok(!JSON.stringify(report).includes('VERY_SECRET'));assert.deepEqual(report.privacyLinks,['https://example.com/privacidade']);assert.deepEqual(report.externalResourceHosts,['cdn.example.net']);assert.equal(report.forms,1);assert.ok(report.interpretation.includes('não comprova'));
});
test('varredura bem sucedida usa só a página pública e retorna limites',async()=>{
 let calls=0;const r=await scanPage('https://example.com/',{resolver:publicResolver,transport:async(u,ip)=>{calls++;assert.equal(ip.address,'93.184.216.34');return {status:200,headers:{'strict-transport-security':'max-age=31536000'},html:'<title>Site</title><iframe src="http://third.example.net"></iframe>',truncated:false};}});assert.equal(calls,1);assert.equal(r.httpStatus,200);assert.equal(r.method,'passive-https-v1');assert.equal(r.checks.find(x=>x.id==='hsts').observed,true);assert.ok(r.limitations.length>=4);
});
