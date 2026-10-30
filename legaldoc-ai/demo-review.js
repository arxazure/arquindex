// Browser-only demonstration. No upload, storage or legal certification.
const btn=document.getElementById('analyze-demo');
btn.addEventListener('click',()=>{
 const source=document.getElementById('doc-text').value;
 const out=document.getElementById('analysis-results');
 out.replaceChildren();
 const list=[
  ['Campo variável',/\\{\\{\\s*[A-Za-z][A-Za-z0-9_]*\\s*\\}\\}/g],
  ['Pendente de preenchimento',/\\b(?:PENDENTE|A PREENCHER|TBD)\\b/gi],
  ['CNPJ (conferir)',/\\b\\d{2}\\.\\d{3}\\.\\d{3}\\/\\d{4}-\\d{2}\\b/g],
  ['Data (conferir)',/\\b\\d{2}\\/\\d{2}\\/\\d{4}\\b/g]
 ];
 let count=0;
 for(const [label,re] of list){const found=[...source.matchAll(re)];if(!found.length)continue;count+=found.length;const p=document.createElement('p');p.textContent=label+': '+found.length+' ocorrência(s)';out.appendChild(p);}
 const summary=document.createElement('p');summary.className='status';summary.textContent=count?count+' ocorrência(s) identificada(s). Conferência humana obrigatória.':'Nenhuma ocorrência reconhecida pela triagem básica. Isso não indica aprovação.';out.prepend(summary);
});
