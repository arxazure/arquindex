const SOURCE = "https://arquindex-gestao-documental.arquindex.chatgpt.site";
const BASE_PATH = "/gestao-documental";
const CANONICAL_BASE = "https://www.arquindex.com.br" + BASE_PATH;
const TEXT_TYPES = ["text/", "application/xml", "application/json", "application/javascript", "image/svg+xml"];
const ROUTE_PREFIXES = [
  "_next", "api", "autores", "blog", "brasil", "cidades", "comparativo", "conhecimento",
  "feed.xml", "favicon.svg", "glossario", "llms-full.txt", "llms.txt", "manifest.webmanifest",
  "orcamento", "privacidade", "robots.txt", "setores", "solucoes",
  "a948be82c7824bc989f2c5dd0f071bea.txt"
];

function rewriteText(input) {
  const marker = "__ARQUINDEX_REPLICA_CANONICAL_BASE__";
  let output = input.replaceAll(SOURCE + "/", marker).replaceAll(SOURCE, CANONICAL_BASE);
  // Match complete route segments: /brasil must not match /brasilia (issue #69).
  for (const prefix of ROUTE_PREFIXES) {
    const escaped = prefix.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    output = output.replace(new RegExp("/" + escaped + "(?=[/\"'?#<\\s]|$)", "g"), BASE_PATH + "/" + prefix);
  }
  return output
    .replace(/((?:href|src|action)=["'])\/(?!\/)/gi, "$1" + BASE_PATH + "/")
    .replaceAll('codex-preview" content="development', 'codex-preview" content="production')
    .replace(/(?:\/gestao-documental){2,}(?=\/|[\"'?#]|$)/g, BASE_PATH)
    .replaceAll(marker, CANONICAL_BASE + "/");
}

function isText(type) {
  return TEXT_TYPES.some((prefix) => type.includes(prefix));
}

export async function serveReplica(req, res) {
  const local = new URL(req.url, "http://localhost");
  if (local.pathname !== BASE_PATH && !local.pathname.startsWith(BASE_PATH + "/")) return false;
  if (!["GET", "HEAD"].includes(req.method || "GET")) {
    res.writeHead(405, { "content-type": "text/plain; charset=utf-8", "allow": "GET, HEAD" });
    res.end("Method not allowed");
    return true;
  }
  // Recover legacy malformed links without changing existing canonical URLs.
  // For example: /gestao-documental/gestao-documental/blog -> /gestao-documental/blog.
  if (local.pathname === BASE_PATH + BASE_PATH || local.pathname.startsWith(BASE_PATH + BASE_PATH + "/")) {
    const normalized = BASE_PATH + local.pathname.slice((BASE_PATH + BASE_PATH).length);
    res.writeHead(301, { "location": normalized + local.search, "cache-control": "public, max-age=3600" });
    res.end();
    return true;
  }
  const upstreamPath = local.pathname.slice(BASE_PATH.length) || "/";
  const upstream = new URL(SOURCE + upstreamPath);
  upstream.search = local.search;
  try {
    const response = await fetch(upstream, {
      redirect: "follow",
      headers: { "user-agent": req.headers["user-agent"] || "ArquindexReplica/1.0" },
      signal: AbortSignal.timeout(30000)
    });
    const contentType = response.headers.get("content-type") || "application/octet-stream";
    const headers = {
      "content-type": contentType,
      "cache-control": response.headers.get("cache-control") || (isText(contentType) ? "public, max-age=300" : "public, max-age=86400"),
      "x-robots-tag": "index, follow, max-snippet:-1, max-image-preview:large",
      "x-arquindex-replica": "chatgpt-sites"
    };
    let body;
    if (isText(contentType)) body = rewriteText(await response.text());
    else body = Buffer.from(await response.arrayBuffer());
    res.writeHead(response.status, headers);
    res.end(req.method === "HEAD" ? undefined : body);
  } catch (error) {
    res.writeHead(502, { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" });
    res.end("<!doctype html><html lang=\"pt-BR\"><meta charset=\"utf-8\"><title>Arquindex</title><h1>Conteúdo temporariamente indisponível</h1><p>Acesse o <a href=\"/\">site principal da Arquindex</a> ou fale pelo <a href=\"https://wa.me/5531973632725\">WhatsApp</a>.</p></html>");
  }
  return true;
}
