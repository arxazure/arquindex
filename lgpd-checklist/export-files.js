import PDFDocument from 'pdfkit';
import ExcelJS from 'exceljs';
import {Document, Packer, Paragraph, TextRun, HeadingLevel} from 'docx';

const plain=v=>String(v??'').replace(/[\u0000-\u001f]/g,' ').trim();
const fileName=s=>plain(s).normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-zA-Z0-9_-]+/g,'-').slice(0,65)||'arquivo';
const safeCell=v=>{let s=plain(v);return /^[=+@\-\t\r]/.test(s)?"'"+s:s;};

export async function sendExport(req,res,company,rows,definitions){
 const format=req.query.format, section=req.query.section||'all';
 if(!['pdf','xlsx','docx'].includes(format))return res.status(400).json({error:'Formato invalido'});
 if(section!=='all'&&!definitions[section])return res.status(400).json({error:'Secao invalida'});
 if(format==='docx'&&section!=='policy')return res.status(400).json({error:'Word disponivel para politicas'});
 const selected=rows.filter(r=>section==='all'||r.section===section);
 const basename=fileName(company.payload.company_name)+'-'+fileName(section);
 res.setHeader('Cache-Control','no-store');
 res.setHeader('X-Content-Type-Options','nosniff');
 if(format==='xlsx'){
  const wb=new ExcelJS.Workbook();wb.creator='Arquindex LGPD Checklist';
  const groups=Object.groupBy(selected,r=>r.section);
  for(const [key,items] of Object.entries(groups)){
   const sheet=wb.addWorksheet((definitions[key]?.label||key).slice(0,31).replace(/[\\/*?:\[\]]/g,''));
   const fields=Object.keys(definitions[key]?.fields||{});
   sheet.addRow(['ID','Data de criacao','ID vinculo',...fields.map(k=>definitions[key].fields[k])]);
   sheet.getRow(1).font={bold:true};sheet.views=[{state:'frozen',ySplit:1}];
   for(const r of items)sheet.addRow([r.id,r.created_at?.toISOString?.()||String(r.created_at||''),r.parent_id||'',...fields.map(k=>safeCell(r.payload?.[k]))]);
   sheet.columns.forEach(c=>{c.width=29;});
   sheet.autoFilter={from:'A1',to:{row:1,column:fields.length+3}};
  }
  if(!Object.keys(groups).length)wb.addWorksheet('Sem registros').addRow(['Nenhum registro cadastrado']);
  res.type('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
  res.attachment(basename+'.xlsx');return res.end(await wb.xlsx.writeBuffer());
 }
 if(format==='docx'){
  const children=[new Paragraph({text:'Politicas e termos - '+plain(company.payload.company_name),heading:HeadingLevel.TITLE})];
  for(const r of selected){
   children.push(new Paragraph({text:plain(r.payload.name),heading:HeadingLevel.HEADING_1}));
   children.push(new Paragraph({children:[new TextRun({text:'Status: '+plain(r.payload.status||'Rascunho'),bold:true})]}));
   for(const line of String(r.payload.text||'').split(/\r?\n/))children.push(new Paragraph({text:line||' '}));
  }
  const buffer=await Packer.toBuffer(new Document({sections:[{children}]}));
  res.type('application/vnd.openxmlformats-officedocument.wordprocessingml.document');
  res.attachment(basename+'.docx');return res.end(buffer);
 }
 res.type('application/pdf');res.attachment(basename+'.pdf');
 const doc=new PDFDocument({size:'A4',margin:48,info:{Title:'LGPD - '+plain(company.payload.company_name),Author:'Arquindex'}});
 doc.pipe(res);doc.fontSize(18).text('LGPD - '+plain(company.payload.company_name));doc.moveDown();
 for(const r of selected){
  const d=definitions[r.section];doc.fontSize(13).text((d?.label||r.section)+' - '+plain(r.payload?.[d?.name]||r.payload?.name),{underline:true});doc.moveDown(.4);
  for(const [key,label] of Object.entries(d?.fields||{})){const value=plain(r.payload?.[key]);if(!value)continue;doc.fontSize(9).text(label+': '+value);doc.moveDown(.3);}
  doc.moveDown();
 }
 doc.end();
}