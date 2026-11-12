"use strict";
const test=require("node:test"),assert=require("node:assert/strict");
const {createIndex}=require("./index"),{toJson,toCsv,toAlto,toPageXml}=require("./export");
const fixture=()=>createIndex({tenantId:"lab",documentId:"synthetic-1",imageSha256:"b".repeat(64),synthetic:true,tokens:[{box:[10,20,30,12],hypotheses:[{text:"A&B <teste>",probability:0.8},{text:"A&B",probability:0.2}]}]});
test("JSON retains alternatives and image hash",()=>{const x=JSON.parse(toJson(fixture()));assert.equal(x.tokens[0].hypotheses.length,2);assert.equal(x.imageSha256,"b".repeat(64));});
test("CSV includes selected confidence and coordinates",()=>{const x=toCsv(fixture());assert.match(x,/0\.8/);assert.match(x,/10/);});
test("ALTO escapes special characters",()=>{const x=toAlto(fixture());assert.match(x,/A&amp;B &lt;teste&gt;/);assert.doesNotMatch(x,/CONTENT="A&B/);});
test("PAGE XML includes image and word polygon",()=>{const x=toPageXml(fixture());assert.match(x,/10,20 40,20 40,32 10,32/);assert.match(x,/A&amp;B &lt;teste&gt;/);});
test("export refuses untrusted non-synthetic object",()=>assert.throws(()=>toCsv({tokens:[],imageSha256:"b".repeat(64)}),/INVALID_SYNTHETIC_INDEX/));
