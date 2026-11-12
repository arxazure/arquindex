import {readFileSync,writeFileSync} from 'node:fs';
import {pathToFileURL} from 'node:url';
import {validSnapshot} from './server.mjs';
export function importSnapshot(input) {
  const snapshot=JSON.parse(input);
  if(!validSnapshot(snapshot)) throw Error('Invalid snapshot');
  return JSON.stringify(snapshot,null,2)+'\n';
}
if(process.argv[1] && import.meta.url===pathToFileURL(process.argv[1]).href){
  try {
    const [input,output]=process.argv.slice(2);
    if(!input || !output) throw Error();
    // Private local output only; never stdout, overwrite, network or deployment.
    writeFileSync(output,importSnapshot(readFileSync(input,'utf8')),{mode:0o600,flag:'wx'});
    process.stderr.write('Validated private file created. No provider was contacted.\n');
  }catch{process.stderr.write('Import failed: check arguments, schema and destination. No snapshot logged.\n');process.exitCode=1;}
}
