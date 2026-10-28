import test from 'node:test';import assert from 'node:assert/strict';import {sha256,nextState,fillTemplate} from './workflow.js';
test('fluxo permite revisao e bloqueia atalhos',()=>{assert.equal(nextState('DRAFT','submit'),'REVIEW');assert.equal(nextState('REVIEW','approve'),'APPROVED');assert.throws(()=>nextState('DRAFT','approve'));assert.throws(()=>nextState('ARCHIVED','revise'));});
test('modelo coleta campos ausentes sem inventar valores',()=>{assert.deepEqual(fillTemplate('CNPJ: {{cnpj}}; Nome: {{nome}}',{cnpj:'00.000.000/0001-00'}),{rendered:'CNPJ: 00.000.000/0001-00; Nome: {{nome}}',missing:['nome']});});
test('hash de conteudo e deterministico',()=>{assert.equal(sha256('abc'),'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad');});
