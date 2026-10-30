// Deterministic and explainable pre-review, not a legal opinion.
const patterns=[
 {key:'cnpj',label:'CNPJ',regex:/\b\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}\b/g},
 {key:'cpf',label:'CPF',regex:/\b\d{3}\.\d{3}\.\d{3}-\d{2}\b/g},
 {key:'date',label:'Data',regex:/\b\d{2}\/\d{2}\/\d{4}\b/g},
 {key:'variable',label:'Campo pendente',regex:/\{\{\s*[A-Za-z][A-Za-z0-9_]*\s*\}\}/g},
 {key:'placeholder',label:'Informacao a completar',regex:/\b(?:A PREENCHER|PENDENTE|TBD)\b/gi}
];
function validCnpj(raw){
 const n=raw.replace(/\D/g,'');
 if(n.length!==14||/^(\d)\1{13}$/.test(n))return false;
 for(let size=12;size<=13;size++){
  let weight=size===12?5:6,sum=0;
  for(let i=0;i<size;i++){sum+=Number(n[i])*weight;weight=weight===2?9:weight-1;}
  if(Number(n[size])!==((11-sum%11)%11)%10)return false;
 }
 return true;
}
export function analyzeDocumentText(input){
 if(typeof input!=='string'||input.length>200000)throw Error('Conteudo de documento invalido');
 const findings=[];
 for(const p of patterns){for(const match of input.matchAll(p.regex)){
  findings.push({type:p.key,label:p.label,excerpt:p.key==='cpf'?'[dado pessoal oculto]':match[0],offset:match.index,needsReview:p.key==='variable'||p.key==='placeholder'||(p.key==='cnpj'&&!validCnpj(match[0]))});
  if(findings.length>=100)break;
 }}
 findings.sort((a,b)=>a.offset-b.offset);
 return {length:input.length,findings:findings.slice(0,100),warnings:findings.filter(f=>f.needsReview).length,disclaimer:'Triagem automatizada: revisar dados, validade juridica, contexto, poderes e legislacao antes da aprovacao.'};
}
