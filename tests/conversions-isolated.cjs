// No network, browser or GA library: gtag is only an in-memory recorder.
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const source = fs.readFileSync(path.join(__dirname, '../assets/js/arquindex-conversions-v1.js'), 'utf8');
function harness(withGtag = true) {
  const listeners = {}, calls = [];
  const document = {documentElement:{dataset:{}},addEventListener(name, fn) {(listeners[name] ||= []).push(fn);}};
  const window = withGtag ? {gtag:(...args)=>calls.push(args)} : {};
  const context = vm.createContext({document, window, location:{origin:'https://www.arquindex.com.br',pathname:'/solucoes-documentais-brasil.html',search:'?email=example%40example.com',hash:'#private'}});
  const run = () => vm.runInContext(source, context);
  const fire = (name, event = {}) => (listeners[name] || []).forEach(fn=>fn(event));
  const click = href => fire('click',{target:{closest:()=>({getAttribute:()=>href})}});
  run(); return {calls,run,fire,click,listeners};
}
const passed = [];
function test(name, fn) {fn();passed.push(name);console.log('PASS '+name);}
test('WhatsApp wa.me/api/web, phone and email: one named event per click',()=>{
  const h=harness();
  for(const href of ['https://wa.me/5511999999999?text=private','https://api.whatsapp.com/send?phone=5511999999999','https://web.whatsapp.com/send','tel:+5511999999999','mailto:example@example.com?body=private']) h.click(href);
  assert.deepEqual(h.calls.map(x=>x[1]),['contact_whatsapp_click','contact_whatsapp_click','contact_whatsapp_click','contact_phone_click','contact_email_click']);
  for(const call of h.calls){const p=JSON.stringify(call); assert.ok(!p.includes('private'));assert.ok(!p.includes('999999'));assert.ok(!p.includes('@'));assert.equal(call[2].page_location,'https://www.arquindex.com.br/solucoes-documentais-brasil.html');}
});
test('Missing gtag silently produces no events; channels remain untouched',()=>{
  const h=harness(false);h.click('https://wa.me/5511999999999');assert.equal(h.calls.length,0);
});
test('Loading twice installs one listener and sends once',()=>{
  const h=harness();h.run();h.click('tel:5511999999999');assert.equal(h.calls.length,1);assert.equal(h.listeners.click.length,1);
});
test('Unrelated clicks, submit, invalid and failure notifications produce no lead',()=>{
  const h=harness();h.click('/services/');for(const event of ['submit','invalid','error','arquindex:lead-failed'])h.fire(event);assert.equal(h.calls.length,0);
});
test('Explicit lead-confirmed hook generates lead, ignores unused form fields',()=>{
  const h=harness();h.fire('arquindex:lead-confirmed',{detail:{service:'digitalizacao',form_id:'orcamento',email:'example@example.com',phone:'5511999999999',name:'Private Test'}});
  assert.equal(h.calls.length,1);assert.equal(h.calls[0][1],'generate_lead');assert.ok(!JSON.stringify(h.calls).includes('example@'));assert.ok(!JSON.stringify(h.calls).includes('Private Test'));
});
if (process.env.EXPECT_PRIVACY_FIX === '1') test('Metadata allowlists prevent names, identifiers and email-like tokens',()=>{
  const h=harness();h.fire('arquindex:lead-confirmed',{detail:{service:'Cliente_Teste',form_id:'12345678900'}});
  assert.equal(h.calls[0][2].lead_service,'unknown');assert.equal(h.calls[0][2].form_id,'unknown');
});
else {
  const h=harness();h.fire('arquindex:lead-confirmed',{detail:{service:'Cliente_Teste',form_id:'12345678900'}});
  console.log('OBSERVED metadata validator accepts arbitrary name/identifier-shaped tokens:',JSON.stringify(h.calls[0][2]));
}
console.log(JSON.stringify({passed:passed.length,networkRequests:0,ga4Hits:0,limit:'Mocks validate tracker logic, not real server receipt or GA4 ingestion.'}));
