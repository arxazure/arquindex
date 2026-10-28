import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fork } from 'node:child_process';
import { once } from 'node:events';
import { serveReplica } from '../replica-proxy.js';

const { paths } = JSON.parse(readFileSync(new URL('./fixtures/regional-city-paths.json', import.meta.url)));
const source = 'https://arquindex-gestao-documental.arquindex.chatgpt.site';
const origin = 'https://www.arquindex.com.br';
const base = '/gestao-documental';
const brasilia = '/brasil/centro-oeste/df/brasilia';
const html = (path) => `<html><head><link rel="canonical" href="${source}${path}"><meta name="robots" content="index,follow"></head><body><main><h1>Gestão documental</h1><a href="${path}">Cidade</a><script type="application/ld+json">${JSON.stringify({url: source + path})}</script></main></body></html>`;
async function request(path, body, type = 'text/html', method = 'GET', status = 200) {
  const oldFetch = globalThis.fetch;
  globalThis.fetch = async (url) => {
    assert.equal(new URL(url).origin, source);
    return new Response(body, {status, headers: {'content-type': type}});
  };
  const res = {writeHead(status, headers) {this.status = status; this.headers = headers;}, end(body) {this.body = body;}};
  try {
    assert.equal(await serveReplica({url: base + path, method, headers: {}}, res), true);
    return res;
  } finally { globalThis.fetch = oldFetch; }
}

test('all 500 inventory paths retain one self canonical, internal links, H1 and robots', async () => {
  assert.equal(paths.length, 500);
  assert.equal(new Set(paths).size, 500);
  for (const path of paths) {
    const res = await request(path, html(path));
    assert.equal(res.status, 200);
    assert.deepEqual([...res.body.matchAll(/<link rel="canonical" href="([^"]+)"/g)].map(m => m[1]), [origin + base + path], path);
    assert.ok(res.body.includes(`href="${base}${path}"`), path);
    assert.ok(res.body.includes(`"url":"${origin}${base}${path}"`), path);
    assert.equal((res.body.match(/<h1>/g) || []).length, 1);
    assert.ok(res.body.includes('<meta name="robots" content="index,follow">'));
    assert.doesNotMatch(res.headers['x-robots-tag'], /noindex/);
    assert.equal(res.body.slice(res.body.indexOf('<body>')).replaceAll(base, '').replaceAll(origin, source), html(path).slice(html(path).indexOf('<body>')));
  }
});

test('relative and public absolute Brasília canonical are also safe', async () => {
  for (const canonical of [brasilia, origin + brasilia, origin + base + brasilia]) {
    const res = await request(brasilia, `<link rel="canonical" href="${canonical}">`);
    const expected = (canonical.startsWith('/') ? '' : origin) + base + brasilia;
    assert.equal(res.body, `<link rel="canonical" href="${expected}">`);
  }
});

test('city sitemap preserves all locations and XML structure without adding routes', async () => {
  const xml = `<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${paths.map(p => `<url><loc>${source}${p}</loc></url>`).join('')}</urlset>`;
  const res = await request('/sitemap-cidades.xml', xml, 'application/xml');
  assert.equal(res.body, xml.replaceAll(source, origin + base));
  assert.equal((res.body.match(/<loc>/g) || []).length, 500);
});

test('complete route segments still rewrite, similar slugs and filename suffixes do not', async () => {
  const body = '<a href="/brasil">Brasil</a><a href="/blog?tag=1">Blog</a><a href="/api/quote">API</a><script src="/_next/static/a.js"></script><a href="/blogueiros">Autoria</a><a href="/robots.txt.bak">Backup</a>';
  const res = await request(brasilia, body);
  for (const path of ['/brasil', '/blog?tag=1', '/api/quote', '/_next/static/a.js', '/blogueiros', '/robots.txt.bak']) assert.ok(res.body.includes(`="${base}${path}"`), path);
  assert.doesNotMatch(res.body, /gestao-documental\/gestao-documental/);
});

test('noindex meta, non-200 status and HEAD behavior are preserved', async () => {
  const body = '<meta name="robots" content="noindex,follow"><h1>Revisão</h1>';
  assert.ok((await request(brasilia, body)).body.includes('content="noindex,follow"'));
  assert.equal((await request(brasilia, body, 'text/html', 'GET', 404)).status, 404);
  assert.equal((await request(brasilia, body, 'text/html', 'HEAD')).body, undefined);
});

test('real router: malformed Brasília redirects once to existing 200 URL; no IndexNow', async (t) => {
  const child = fork(new URL('../server.js', import.meta.url), [], {
    execArgv: ['--import', new URL('./fixtures/replica-upstream.mjs', import.meta.url).href],
    env: {...process.env, PORT: '0', NODE_ENV: 'test', INDEXNOW_KEY: '', INDEXNOW_AUTO_SUBMIT: 'false'},
    stdio: ['ignore', 'ignore', 'pipe', 'ipc']
  });
  let stderr = ''; child.stderr.on('data', b => {stderr += b;});
  t.after(async () => { child.kill(); await once(child, 'exit'); });
  const [message] = await Promise.race([once(child, 'message'), once(child, 'exit').then(() => {throw new Error(stderr);}), new Promise((_, reject) => {const timer = setTimeout(() => reject(new Error('Server timeout: ' + stderr)), 10000); timer.unref();})]);
  const local = `http://127.0.0.1:${message.port}`;
  const bad = base + '/brasil/centro-oeste/df/gestao-documental/brasilia';
  for (const method of ['GET', 'HEAD']) {
    const redirect = await fetch(local + bad + '?utm_source=test', {method, redirect: 'manual'});
    assert.equal(redirect.status, 301);
    assert.equal(redirect.headers.get('location'), base + brasilia + '?utm_source=test');
    const final = await fetch(local + redirect.headers.get('location'), {method, redirect: 'manual'});
    assert.equal(final.status, 200);
    assert.equal(final.headers.get('location'), null);
    const body = await final.text();
    if (method === 'HEAD') assert.equal(body, '');
    else {
      assert.ok(body.includes(`rel="canonical" href="${origin}${base}${brasilia}"`));
      assert.equal((body.match(/<h1>/g) || []).length, 1);
      assert.doesNotMatch(body, /noindex/);
    }
  }
  const sitemap = await fetch(local + base + '/sitemap-cidades.xml');
  const xml = await sitemap.text();
  assert.equal(sitemap.status, 200);
  assert.ok(xml.includes(`<loc>${origin}${base}${brasilia}</loc>`));
  assert.ok(!xml.includes(bad));
});
