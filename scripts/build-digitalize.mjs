import {mkdirSync,writeFileSync} from 'node:fs';
import {digitalizePaths,renderDigitalize} from './digitalize-pages.mjs';
const base='https://www.arquindex.com.br';
for(const p of digitalizePaths){const out='digitalize-output'+p;mkdirSync(out,{recursive:true});writeFileSync(out+'index.html',renderDigitalize(p,base).body);}
writeFileSync('digitalize-output/digitalize/sitemap.xml',renderDigitalize('/digitalize/sitemap.xml',base).body);
console.log('Geradas',digitalizePaths.length,'paginas');
