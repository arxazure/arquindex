import test from 'node:test';
import assert from 'node:assert/strict';
import {inflateRawSync} from 'node:zlib';
import {excelExport} from '../export-files.js';

function unpack(buffer){
 const result=new Map();
 let i=0;
 while(i+30<=buffer.length && buffer.readUInt32LE(i)===0x04034b50){
  const method=buffer.readUInt16LE(i+8);
  const size=buffer.readUInt32LE(i+18);
  const nameSize=buffer.readUInt16LE(i+26);
  const extraSize=buffer.readUInt16LE(i+28);
  const name=buffer.subarray(i+30,i+30+nameSize).toString('utf8');
  const start=i+30+nameSize+extraSize;
  const content=buffer.subarray(start,start+size);
  result.set(name,(method===8?inflateRawSync(content):content).toString('utf8'));
  i=start+size;
 }
 return result;
}
const make=(section,name,probability,impact)=>({
 id:section+'-'+name,section,parent_id:null,created_at:'2026-10-28',updated_at:'2026-10-28',
 payload:{name,probability,impact}
});
test('Excel exports risk grade and severity colors without inventing missing assessments',()=>{
 const bytes=excelExport([
  make('risk','baixo','1','4'),
  make('risk','moderado','3','3'),
  make('risk','alto','4','4'),
  make('risk','critico','5','5'),
  make('risk','pendente','A avaliar','A avaliar')
 ]);
 const entries=unpack(bytes);
 assert.ok(entries.has('xl/styles.xml'));
 const xml=entries.get('xl/worksheets/sheet1.xml');
 const styles=entries.get('xl/styles.xml');
 assert.match(xml,/pontuacao_risco/);
 assert.match(xml,/grau_risco/);
 for(const grade of ['Baixo','Moderado','Alto','Critico','Nao avaliado'])assert.ok(xml.includes(grade));
 for(const color of ['FFDCFCE7','FFFEF9C3','FFFFEDD5','FFFEE2E2','FFE5E7EB'])assert.ok(styles.includes(color));
 assert.match(xml,/autoFilter/);
 assert.match(xml,/t="inlineStr"/);
 assert.match(xml,/s="6"/);
});
test('Excel never combines different companies when input was tenant scoped',()=>{
 const bytes=excelExport([make('system','Repositorio empresa A')]);
 const text=[...unpack(bytes).values()].join(' ');
 assert.match(text,/Repositorio empresa A/);
 assert.doesNotMatch(text,/Repositorio empresa B/);
});
