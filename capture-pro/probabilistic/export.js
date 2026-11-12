"use strict";
// Pure exporters for synthetic probabilistic index. No I/O or remote API calls.
function xml(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&apos;");}
function assertIndex(index){if(!index||index.synthetic!==true||!Array.isArray(index.tokens)||!/^[a-f0-9]{64}$/i.test(index.imageSha256||""))throw Error("INVALID_SYNTHETIC_INDEX");}
function best(t){return t.validated?.text??t.hypotheses.reduce((a,b)=>b.probability>a.probability?b:a).text;}
function toJson(index){assertIndex(index);return JSON.stringify({schemaVersion:index.schemaVersion,documentId:index.documentId,imageSha256:index.imageSha256,tokens:index.tokens.map((t,i)=>({index:i,box:t.box??null,selectedText:best(t),hypotheses:t.hypotheses,validated:t.validated??null}))},null,2);}
function toCsv(index){assertIndex(index);const q=s=>'"'+String(s??"").replace(/"/g,'""')+'"';return ["token_index,selected_text,confidence,x,y,width,height",...index.tokens.map((t,i)=>[i,best(t),t.validated?1:Math.max(...t.hypotheses.map(h=>h.probability)),...(t.box??["","","",""])].map(q).join(","))].join("\n");}
function toAlto(index,{imageWidth=1000,imageHeight=1000}={}){
 assertIndex(index);if(![imageWidth,imageHeight].every(n=>Number.isSafeInteger(n)&&n>0))throw Error("INVALID_DIMENSIONS");
 const strings=index.tokens.map((t,i)=>{const b=t.box??[0,i*20,0,0];return '<String ID="s'+i+'" CONTENT="'+xml(best(t))+'" HPOS="'+b[0]+'" VPOS="'+b[1]+'" WIDTH="'+b[2]+'" HEIGHT="'+b[3]+'" WC="'+(t.validated?1:Math.max(...t.hypotheses.map(h=>h.probability)))+'"/>';}).join("");
 return '<?xml version="1.0" encoding="UTF-8"?>\n<alto xmlns="http://www.loc.gov/standards/alto/ns-v4#"><Description><MeasurementUnit>pixel</MeasurementUnit></Description><Layout><Page WIDTH="'+imageWidth+'" HEIGHT="'+imageHeight+'"><PrintSpace><TextBlock><TextLine>'+strings+'</TextLine></TextBlock></PrintSpace></Page></Layout></alto>';
}
function toPageXml(index,{imageFilename="synthetic.png",imageWidth=1000,imageHeight=1000}={}){
 assertIndex(index);if(![imageWidth,imageHeight].every(n=>Number.isSafeInteger(n)&&n>0))throw Error("INVALID_DIMENSIONS");
 const words=index.tokens.map((t,i)=>{const [x,y,w,h]=t.box??[0,i*20,0,0];const points=[x+","+y,(x+w)+","+y,(x+w)+","+(y+h),x+","+(y+h)].join(" ");return '<Word id="w'+i+'"><Coords points="'+points+'"/><TextEquiv><Unicode>'+xml(best(t))+'</Unicode></TextEquiv></Word>';}).join("");
 return '<?xml version="1.0" encoding="UTF-8"?>\n<PcGts xmlns="http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15"><Page imageFilename="'+xml(imageFilename)+'" imageWidth="'+imageWidth+'" imageHeight="'+imageHeight+'"><TextRegion id="r1"><TextLine id="l1">'+words+'</TextLine></TextRegion></Page></PcGts>';
}
module.exports={toJson,toCsv,toAlto,toPageXml};
