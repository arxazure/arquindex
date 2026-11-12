import test from 'node:test';
import assert from 'node:assert/strict';
import {professionalDocx} from '../export-files.js';
import {buildProfessionalReport,reportHtml,reportPdf} from '../professional-reports.js';
const company={company_name:'Empresa Teste',company_cnpj:'00.000.000/0001-00',company_dpo:'DPO Teste',company_email:'privacidade@example.test'};
const records=[
 {id:'u1',section:'branch',parent_id:'c1',payload:{name:'Matriz'}},
 {id:'d1',section:'department',parent_id:'u1',payload:{name:'Departamento Pessoal'}},
 {id:'p1',section:'process',parent_id:'d1',payload:{name:'Gestão de dossiês de colaboradores',purpose:'Cumprimento de obrigações trabalhistas',legal_basis:'Art. 7, II - obrigação legal',data_categories:'Dados cadastrais e dados de saúde',data_subjects:'Colaboradores',origin:'Documentos físicos',storage:'Alfresco',sharing:'Medicina do Trabalho',international_transfer:'Não informado',retention:'Tabela de temporalidade',security:'Controle de acesso',responsible:'Responsável teste'}},
 {id:'r1',section:'risk',parent_id:'p1',payload:{name:'Acesso indevido',probability:'2',impact:'4',mitigation:'Revisão de permissões'}},
 {id:'w1',section:'website',payload:{name:'Site',url:'https://example.test',collection:'Formulário de contato',cookies:'A verificar'}}
];
test('ROPA respects linked department and all process fields',()=>{
 const r=buildProfessionalReport('ropa',records,company,new Date('2026-11-11T12:00:00Z'));
 const text=r.blocks.map(x=>x.text||x.label||JSON.stringify(x.rows||[])).join(' ');
 for(const expected of ['Departamento Pessoal','Gestão de dossiês','Medicina do Trabalho','Tabela de temporalidade','Acesso indevido','Matriz']) assert.ok(text.includes(expected),expected);
 assert.equal(r.processCount,1);
});
test('Privacy report includes website and purpose and remains draft',()=>{
 const r=buildProfessionalReport('privacy',records,company,new Date('2026-11-11T12:00:00Z'));
 const html=reportHtml(r);
 for(const expected of ['Empresa Teste','Cumprimento de obrigações','Formulário de contato','RASCUNHO']) assert.ok(html.includes(expected),expected);
});
test('PDF has valid signature, pages and final cross reference',()=>{
 const r=buildProfessionalReport('ropa',records,company,new Date('2026-11-11T12:00:00Z'));
 const pdf=reportPdf(r);
 assert.ok(pdf.subarray(0,8).toString().startsWith('%PDF-1.4'));
 assert.ok(pdf.toString('latin1').includes('startxref'));
 assert.ok(pdf.toString('latin1').includes('%%EOF'));
});
test('Missing data is never invented',()=>{
 const r=buildProfessionalReport('privacy',[],{company_name:'Empresa sem mapa'});
 assert.ok(r.issues.includes('processos de tratamento não cadastrados'));
 assert.ok(reportHtml(r).includes('Não há processos de tratamento mapeados'));
});

test('All seven report types produce complete structured chapters and editable DOCX',()=>{
 for(const type of ['privacy','ropa','risk','incident','audit','cookies','training']){
  const report=buildProfessionalReport(type,records,company,new Date('2026-11-11T12:00:00Z'));
  assert.ok(report.blocks.some(b=>b.kind==='section'));
  assert.ok(report.blocks.some(b=>b.kind==='title'));
  const docx=professionalDocx(report);
  assert.equal(docx.subarray(0,2).toString(),'PK');
  assert.ok(docx.length>1500);
 }
});
test('Company phone and sensitive-data classification survive in ROPA',()=>{
 const companyWithPhone={...company,company_phone:'(31) 3333-4444'};
 const modified=records.map(x=>x.id==='p1'?{...x,payload:{...x.payload,data_type_classification:'Sensível',process_operators:'Operador Teste'}}:x);
 const report=buildProfessionalReport('ropa',modified,companyWithPhone);
 const html=reportHtml(report);
 for(const word of ['3333-4444','Sensível','Operador Teste']) assert.ok(html.includes(word));
});
