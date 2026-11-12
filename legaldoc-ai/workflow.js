import {createHash} from 'node:crypto';
export const sha256 = value => createHash('sha256').update(value).digest('hex');
export const transitions = Object.freeze({
 DRAFT: Object.freeze({submit:'REVIEW'}),
 REVIEW: Object.freeze({approve:'APPROVED',reject:'REJECTED'}),
 REJECTED: Object.freeze({revise:'DRAFT'}),
 APPROVED: Object.freeze({prepare_signature:'SIGNATURE_PENDING'}),
 SIGNATURE_PENDING: Object.freeze({record_verified_signature:'SIGNED',cancel_signature:'APPROVED'}),
 SIGNED: Object.freeze({archive:'ARCHIVED'}),
 ARCHIVED: Object.freeze({})
});
export function nextState(current,action){
 const next=transitions[current]?.[action];
 if(!next)throw Object.assign(new Error('Transicao de estado nao permitida'),{status:409});
 return next;
}
export function fillTemplate(template,fields){
 if(typeof template!=='string'||!fields||typeof fields!=='object'||Array.isArray(fields))throw Error('Modelo ou campos invalidos');
 const missing=new Set();
 const rendered=template.replace(/{{\s*([A-Za-z][A-Za-z0-9_]{0,63})\s*}}/g,(match,key)=>{
  const value=fields[key];
  if(typeof value!=='string'&&typeof value!=='number'){missing.add(key);return match;}
  return String(value);
 });
 return {rendered,missing:[...missing]};
}
