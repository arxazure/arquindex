import test from "node:test";
import assert from "node:assert/strict";
import { serveReplica } from "../replica-proxy.js";

function fakeResponse() {
  return {
    status: null,
    headers: null,
    body: null,
    writeHead(status, headers) { this.status = status; this.headers = headers; },
    end(body) { this.body = body; }
  };
}

test("legacy doubled prefix redirects to canonical single prefix", async () => {
  const res = fakeResponse();
  const handled = await serveReplica({
    url: "/gestao-documental/gestao-documental/blog/categoria/lgpd-governanca",
    method: "GET",
    headers: {}
  }, res);
  assert.equal(handled, true);
  assert.equal(res.status, 301);
  assert.equal(res.headers.location, "/gestao-documental/blog/categoria/lgpd-governanca");
});

test("legacy redirect keeps query string", async () => {
  const res = fakeResponse();
  await serveReplica({
    url: "/gestao-documental/gestao-documental/blog?utm_source=google",
    method: "GET",
    headers: {}
  }, res);
  assert.equal(res.status, 301);
  assert.equal(res.headers.location, "/gestao-documental/blog?utm_source=google");
});

test("normal non-replica paths are left to the main router", async () => {
  const res = fakeResponse();
  const handled = await serveReplica({ url: "/health", method: "GET", headers: {} }, res);
  assert.equal(handled, false);
  assert.equal(res.status, null);
});

test("unsafe methods are rejected, not redirected", async () => {
  const res = fakeResponse();
  const handled = await serveReplica({
    url: "/gestao-documental/gestao-documental/blog", method: "POST", headers: {}
  }, res);
  assert.equal(handled, true);
  assert.equal(res.status, 405);
  assert.equal(res.headers.allow, "GET, HEAD");
});
