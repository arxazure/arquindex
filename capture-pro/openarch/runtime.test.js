"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const {spawnSync} = require("node:child_process");
// No installation or stack start. A missing real CLI is a skip, never a fake success.
const probe = spawnSync("openarch",["version","--output","json"],{encoding:"utf8",timeout:10000,maxBuffer:65536,
  env:{PATH:process.env.PATH,NO_COLOR:"1"}});
test("real OpenArch CLI 0.2.1 version",{skip:probe.error?.code === "ENOENT" ? "OpenArch CLI is not installed" : false},() => {
  assert.ifError(probe.error);
  assert.equal(probe.status,0);
  assert.match(probe.stdout,/0\.2\.1/);
});
test("real OpenArch stack integration",{skip:"Requires separately approved isolated stack; Docker and server unavailable"},() => {});
