import test from 'node:test';
import assert from 'node:assert/strict';
import {createInviteToken,validateInviteToken,inviteDigest} from './invite-security.js';
test('random invitation token is hashed and expires after 48h',()=>{
 const start=new Date('2026-11-04T12:00:00Z'),inv=createInviteToken(start);
 assert.equal(inv.token.length,43);
 assert.equal(inv.tokenHash,inviteDigest(inv.token));
 assert.notEqual(inv.token,inv.tokenHash);
 assert.equal(validateInviteToken({...inv,usedAt:null,now:new Date('2026-11-05T12:00:00Z')}),true);
 assert.equal(validateInviteToken({...inv,usedAt:null,now:new Date('2026-11-07T12:00:00Z')}),false);
 assert.equal(validateInviteToken({...inv,usedAt:'2026-11-04T13:00:00Z',now:start}),false);
 assert.equal(validateInviteToken({...inv,token:inv.token.slice(0,-1)+'x',usedAt:null,now:start}),false);
});
