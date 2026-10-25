import { timingSafeEqual } from 'node:crypto';

const hub = 'https://capture-hub-production.up.railway.app';
export const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const number = value => typeof value === 'number' && Number.isFinite(value);
export function compare(current, previous, lowerIsBetter = false) {
  if (!number(current) || !number(previous)) return {color:'gray', text:'Sem dados comparáveis', delta:null, percent:null};
  const delta = current - previous;
  const percent = previous === 0 ? null : delta / Math.abs(previous) * 100;
  if (!delta) return {color:'gray', text:'Sem alteração', delta, percent};
  const improved = lowerIsBetter ? delta < 0 : delta > 0;
  return {color:improved ? 'green' : 'red', text:improved ? 'Melhoria' : 'Queda', delta, percent};
}
const record = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const textOrMissing = value => value == null || typeof value === 'string';
const numericOrMissing = value => value == null || number(value);
const validDay = value => typeof value === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(value) && Number.isFinite(Date.parse(value)) && new Date(value).toISOString().slice(0,10) === value;
const validPeriod = p => record(p) && validDay(p.start) && validDay(p.end) && p.start <= p.end;
export function validSnapshot(s) {
  if (!record(s) || s.schemaVersion !== 1 || typeof s.collectedAt !== 'string' || !/^\d{4}-\d{2}-\d{2}T.*(?:Z|[+-]\d{2}:\d{2})$/.test(s.collectedAt) || !Number.isFinite(Date.parse(s.collectedAt)) || !Array.isArray(s.metrics) || !textOrMissing(s.freshnessNote)) return false;
  const fields = {
    metrics: ['label','source','unit','deltaUnit','note'],
    sources: ['name','account','availability','period','comparison','receivedAt','freshness'],
    channels: ['name','account','read','write','pending'],
    pages: ['page'], receipts: ['channel','state','url','id','note']
  };
  for (const [key, strings] of Object.entries(fields)) {
    const rows = s[key];
    if (rows === undefined) continue;
    if (!Array.isArray(rows) || !rows.every(row => record(row) && strings.every(field => textOrMissing(row[field])))) return false;
  }
  if (!s.metrics.every(m => numericOrMissing(m.current) && numericOrMissing(m.previous) && (m.lowerIsBetter === undefined || typeof m.lowerIsBetter === 'boolean'))) return false;
  if (!(s.pages || []).every(p => ['clicks','impressions','position'].every(k => numericOrMissing(p[k])))) return false;
  if (s.queue !== undefined && (!record(s.queue) || !Object.values(s.queue).every(v => v === null || typeof v === 'string' || typeof v === 'boolean' || number(v)))) return false;
  if (s.periods !== undefined && (!record(s.periods) || !validPeriod(s.periods.current) || !validPeriod(s.periods.previous))) return false;
  return true;
}
const dayLabel = value => value.split('-').reverse().join('/');
const periodLabel = p => `${dayLabel(p.start)}–${dayLabel(p.end)}`;
const comparisonLabel = snapshot => snapshot.periods
  ? `${periodLabel(snapshot.periods.current)} versus ${periodLabel(snapshot.periods.previous)}.`
  : 'Períodos da comparação não informados no snapshot; confira os períodos por fonte abaixo.';
const fmt = (value, unit = '') => number(value) ? value.toLocaleString('pt-BR', {maximumFractionDigits:unit === '%' ? 2 : 2}) + escapeHtml(unit) : 'Sem dados';
const date = value => { const d = new Date(value); return Number.isFinite(d.getTime()) ? d.toLocaleString('pt-BR', {timeZone:'America/Sao_Paulo'}) : 'Não informada'; };
const link = (url, label) => {try {const u = new URL(url); if (['http:','https:'].includes(u.protocol)) return `<a href="${escapeHtml(u.href)}" rel="noopener noreferrer">${escapeHtml(label)}</a>`;}catch{} return escapeHtml(label);};
const css = `:root{color-scheme:dark;font:16px system-ui;background:#091425;color:#eef3fa}*{box-sizing:border-box}body{margin:0}header,main{max-width:1240px;margin:auto;padding:28px 24px}header{border-bottom:1px solid #31425b}h1{font-size:32px;margin:8px 0}h2{margin-top:36px;font-size:23px}h3{margin:0 0 12px;font-size:18px}p{line-height:1.6}.muted,small{color:#b9c4d3}a{color:#9bcfff;overflow-wrap:anywhere}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:14px}.card,.notice{background:#14233a;border:1px solid #33465e;border-radius:12px;padding:20px}.value{font-size:32px;font-weight:750;margin:12px 0}.green{color:#72e6af}.red{color:#ffa2a2}.gray{color:#bcc3ce}.pill{display:inline-block;border:1px solid currentColor;border-radius:8px;padding:4px 8px;font-weight:600}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:12px;text-align:left;border-bottom:1px solid #33465e;vertical-align:top}th{color:#bacbe0}.table{overflow:auto}details{margin:18px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}footer{margin:30px 0;font-size:14px}.notice{border-left:4px solid #9bcfff}nav{display:flex;gap:20px;flex-wrap:wrap}summary{cursor:pointer}@media(max-width:600px){header,main{padding:20px 14px}h1{font-size:27px}.value{font-size:28px}td,th{padding:8px}}`;

export function render(snapshot) {
  const e = escapeHtml;
  const cards = (snapshot.metrics || []).map(m => {
    const c = compare(m.current, m.previous, m.lowerIsBetter);
    const change = c.delta === null ? '' : ` · ${c.delta > 0 ? '+' : ''}${fmt(c.delta, m.deltaUnit || m.unit || '')}`;
    const pct = c.percent === null ? (c.delta !== null && m.previous === 0 ? ' · base anterior zero; percentual indefinido' : '') : ` · ${c.percent > 0 ? '+' : ''}${fmt(c.percent, '%')}`;
    return `<article class="card"><h3>${e(m.label)}</h3><small>${e(m.source)}</small><div class="value">${fmt(m.current, m.unit)}</div><span class="pill ${c.color}">${e(c.text + change + pct)}</span><p>Anterior: ${fmt(m.previous, m.unit)}</p><small>${e(m.note || '')}</small></article>`;
  }).join('');
  const sources = (snapshot.sources || []).map(s => `<tr><td>${e(s.name)}<br><small>${e(s.account)}</small></td><td>${e(s.availability)}<br><small>${e(s.period)}<br>Comparação: ${e(s.comparison || 'Não disponível')}</small></td><td>${e(date(s.receivedAt))}<br><small>${e(s.freshness || 'Atualização do cache do provedor não informada')}</small></td></tr>`).join('');
  const channels = (snapshot.channels || []).map(c => `<tr><td>${e(c.name)}<br><small>${e(c.account)}</small></td><td>${e(c.read)}</td><td>${e(c.write)}</td><td>${e(c.pending)}</td></tr>`).join('');
  const pages = (snapshot.pages || []).map(p => `<tr><td>${link(p.page,p.page)}</td><td>${fmt(p.clicks)}</td><td>${fmt(p.impressions)}</td><td>${fmt(p.position)}</td></tr>`).join('');
  const publications = (snapshot.receipts || []).map(r => `<tr><td>${e(r.channel)}</td><td>${e(r.state)}</td><td>${link(r.url, r.id || 'Abrir recibo')}</td><td>${e(r.note)}</td></tr>`).join('');
  return `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Top10 Google — Arquindex</title><style>${css}</style></head><body><header><small>ARQUINDEX CAPTURE · PAINEL PRIVADO</small><h1>Top10 Google</h1><p>Presença digital com dados verificáveis</p><nav><a href="/admin">Sistemas</a><a href="/admin/top10/data">Dados e evidências em JSON</a><a href="/logout">Sair</a></nav></header><main><div class="notice"><strong>Instantâneo coletado em ${e(date(snapshot.collectedAt))} (Brasília).</strong><p>As consultas foram realizadas nos conectores autorizados. Este painel calcula os indicadores a cada acesso usando a última coleta armazenada; não há sincronização contínua. Recarregar a página não consulta os provedores. ${e(snapshot.freshnessNote)}</p></div><h2>Busca · comparação de períodos</h2><p>${e(comparisonLabel(snapshot))} Verde: melhoria. Vermelho: queda. Cinza: sem comparação ou sem alteração. Para posição média, um número menor é melhor; a variação percentual indica o movimento numérico.</p><div class="grid">${cards}</div><h2>Fontes e disponibilidade</h2><div class="table"><table><thead><tr><th>Origem e conta</th><th>Disponibilidade e período</th><th>Última consulta · Brasília</th></tr></thead><tbody>${sources}</tbody></table></div><h2>Páginas com cliques no Google</h2><p class="muted">Amostra das até 20 páginas com mais cliques entre as linhas retornadas para o período informado na fonte. Posição média agregada da página, sem recorte por cidade. Totais por propriedade vêm de consulta separada; não são somas desta tabela. Não comprova indexação atual.</p><div class="table"><table><thead><tr><th>Página</th><th>Cliques</th><th>Impressões</th><th>Posição média</th></tr></thead><tbody>${pages}</tbody></table></div><h2>Integrações de redes sociais</h2><p>Capacidade anunciada pelo conector e resultado observado são informações distintas. Nenhum teste de publicação foi enviado nesta implantação.</p><div class="table"><table><thead><tr><th>Canal / identidade</th><th>Leitura</th><th>Publicação disponível</th><th>Pendência observada</th></tr></thead><tbody>${channels}</tbody></table></div><h2>Recibos encontrados nos provedores</h2><div class="table"><table><thead><tr><th>Canal</th><th>Estado no provedor</th><th>ID / link</th><th>Evidência e limite</th></tr></thead><tbody>${publications}</tbody></table></div><h2>Fila existente · estados registrados</h2><p>${e(Object.entries(snapshot.queue || {}).map(([k,v])=>k+': '+v).join(' · '))}</p><p class="muted">Contagens do registro operacional, sem equiparar aceites ou estados desconhecidos a publicações visíveis. A fila e os agendamentos existentes foram preservados.</p><h2>Metas editoriais</h2><div class="grid"><div class="card"><h3>3 posts por canal/dia</h3><p>Meta planejada</p></div><div class="card"><h3>100 páginas SEO/GEO/AEO</h3><p>Planejadas no PR #36</p></div><div class="card"><h3>15 artigos</h3><p>Pautas planejadas no PR #36</p></div></div><h2>Ainda sem medição verificável</h2><p>Ranking por cidade, indexação atual por URL, leitura e scroll de artigos, conversões qualificadas e citações em respostas de IA: sem dados integrados. Tráfego de referência de IA não equivale a citações.</p><details><summary>Como conferir a coleta</summary><p>O JSON privado contém solicitações, contas, períodos e respostas das fontes utilizadas. Campos ausentes e consultas vazias permanecem sem valor; não são convertidos em zero.</p><p>${link('https://github.com/arxazure/arquindex/pull/36','Código e revisão no PR #36')}</p></details><footer>Somente leitura. A HomeHost permanece sem alterações, conforme issue #28. Dados armazenados fora do código público. Autenticação pelo Capture Hub.</footer></main></body></html>`;
}

const headers = {'cache-control':'no-store, private','x-robots-tag':'noindex, nofollow','x-content-type-options':'nosniff','referrer-policy':'no-referrer','x-frame-options':'DENY','content-security-policy':"default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; frame-ancestors 'none'"};
export function authorized(req, secret) {
  if (!secret || secret.length < 32) return false;
  const actual = Buffer.from(req.headers.get('authorization') || '');
  const expected = Buffer.from('Bearer ' + secret);
  return actual.length === expected.length && timingSafeEqual(actual, expected);
}
export function handle(req, env) {
  const path = new URL(req.url).pathname;
  if (path === '/health') return Response.json({ok:true,version:'top10-verified-v1',mode:'connector-snapshot',publishingEnabled:false},{headers});
  if (path === '/') return new Response(null,{status:302,headers:{...headers,location:hub+'/admin/top10'}});
  if (!authorized(req,env.TOP10_INTERNAL_TOKEN)) return new Response('Acesso privado pelo Capture Hub.',{status:401,headers});
  if (req.method !== 'GET') return new Response('Somente leitura',{status:405,headers:{...headers,allow:'GET'}});
  if (!['/dashboard','/api/snapshot'].includes(path)) return new Response('Não encontrado',{status:404,headers});
  let snapshot;
  try {snapshot=JSON.parse(env.TOP10_SNAPSHOT_JSON || '');if(!validSnapshot(snapshot))throw Error();}
  catch {return new Response('Coleta verificada indisponível.',{status:503,headers});}
  if (path === '/api/snapshot') return Response.json(snapshot,{headers});
  return new Response(render(snapshot),{headers:{...headers,'content-type':'text/html; charset=utf-8'}});
}
if (globalThis.Bun && import.meta.main) Bun.serve({port:Number(Bun.env.PORT || 3000),fetch:req=>handle(req,Bun.env)});
