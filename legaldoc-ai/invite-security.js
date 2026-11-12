// Invitation primitives for a future authenticated backend; never run on the public demo.
// Do not log raw tokens or expose token hashes to the client.
import {randomBytes,createHash,timingSafeEqual} from 'node:crypto';
const MAX_AGE_MS=48*60*60*1000;
export function inviteDigest(token){
 if(typeof token!=='string'||!/^[A-Za-z0-9_-]{43}$/.test(token))return null;
 return createHash('sha256').update('arquindex-invite-v1:'+token).digest('hex');
}
export function createInviteToken(now=new Date()){
 const token=randomBytes(32).toString('base64url');
 return {token,tokenHash:inviteDigest(token),expiresAt:new Date(now.getTime()+MAX_AGE_MS).toISOString()};
}
export function validateInviteToken({token,tokenHash,expiresAt,usedAt,now=new Date()}){
 const provided=inviteDigest(token);
 if(!provided||typeof tokenHash!=='string'||!strHex64(tokenHash))return false;
 if(usedAt||!Number.isFinite(new Date(expiresAt).getTime())||new Date(expiresAt).getTime()<=now.getTime())return false;
 return timingSafeEqual(Buffer.from(provided,'hex'),Buffer.from(tokenHash,'hex'));
}
function strHex64(x){return /^[a-f0-9]{64}$/i.test(x);}
