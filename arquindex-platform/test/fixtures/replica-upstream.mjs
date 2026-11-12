// Synthetic upstream for the real Railway router. Never contacts a live service.
import http from 'node:http';
import { readFileSync } from 'node:fs';
const source = 'https://arquindex-gestao-documental.arquindex.chatgpt.site';
const { paths } = JSON.parse(readFileSync(new URL('./regional-city-paths.json', import.meta.url)));
const listen = http.Server.prototype.listen;
http.Server.prototype.listen = function (...args) {
  this.once('listening', () => process.send?.({port: this.address().port}));
  return listen.apply(this, args);
};
globalThis.fetch = async (input) => {
  const url = new URL(input);
  if (url.origin !== source) throw new Error('Unexpected outbound request: ' + url.origin);
  if (url.pathname === '/sitemap-cidades.xml') return new Response(`<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${paths.map(p => `<url><loc>${source}${p}</loc></url>`).join('')}</urlset>`, {headers: {'content-type': 'application/xml'}});
  if (!paths.includes(url.pathname)) throw new Error('Unexpected upstream path');
  return new Response(`<html><head><link rel="canonical" href="${source}${url.pathname}"><meta name="robots" content="index,follow"></head><body><main><h1>Gestão documental</h1></main></body></html>`, {headers: {'content-type': 'text/html'}});
};
