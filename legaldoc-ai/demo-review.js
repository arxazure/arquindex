// Browser-only demonstration. No upload, storage or legal certification.
const btn=document.getElementById('analyze-demo');
btn.addEventListener('click',()=>{
 const source=document.getElementById('doc-text').value;
 const out=document.getElementById('analysis-results');
 out.replaceChildren();
 const list=[
  ['Campo variável',/\{\{\s*[A-Za-z][A-Za-z0-9_]*\s*\}\}/g],
  ['Pendente de preenchimento',/\b(?:PENDENTE|A PREENCHER|TBD)\b/gi],
  ['CNPJ (conferir)',/\b\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}\b/g],
  ['Data (conferir)',/\b\d{2}\/\d{2}\/\d{4}\b/g]
 ];
 let count=0;
 for(const [label,re] of list){const found=[...source.matchAll(re)];if(!found.length)continue;count+=found.length;const p=document.createElement('p');p.textContent=label+': '+found.length+' ocorrência(s)';out.appendChild(p);}
 const summary=document.createElement('p');summary.className='status';summary.textContent=count?count+' ocorrência(s) identificada(s). Conferência humana obrigatória.':'Nenhuma ocorrência reconhecida pela triagem básica. Isso não indica aprovação.';out.prepend(summary);
});

document.getElementById('compare-docs').addEventListener('click',()=>{
 const oldLines=document.getElementById('before-text').value.replace(/\r\n/g,'\n').split('\n');
 const newLines=document.getElementById('after-text').value.replace(/\r\n/g,'\n').split('\n');
 const target=document.getElementById('compare-results');target.replaceChildren();
 if(oldLines.length>300||newLines.length>300){target.textContent='Limite de 300 linhas por texto.';return;}
 const m=oldLines.length,n=newLines.length;
 const dp=Array.from({length:m+1},()=>new Uint16Array(n+1));
 for(let i=m-1;i>=0;i--)for(let j=n-1;j>=0;j--)dp[i][j]=oldLines[i]===newLines[j]?dp[i+1][j+1]+1:Math.max(dp[i+1][j],dp[i][j+1]);
 let i=0,j=0,adds=0,removes=0;
 const list=document.createElement('ul');
 while(i<m||j<n){
  if(i<m&&j<n&&oldLines[i]===newLines[j]){i++;j++;continue;}
  let label,line;
  if(j<n&&(i===m||dp[i][j+1]>=dp[i+1][j])){label='Incluída';line=newLines[j++];adds++;}
  else{label='Removida';line=oldLines[i++];removes++;}
  const item=document.createElement('li');item.textContent=label+': '+line.slice(0,240);list.appendChild(item);
 }
 const p=document.createElement('p');p.className='status';p.textContent='Resultado: '+adds+' linha(s) incluída(s), '+removes+' linha(s) removida(s). Revisão humana necessária.';target.append(p,list);
});
