import {mkdtemp,writeFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {checksum} from './decreto-10278.js';
const run=promisify(execFile);

/** Trusted worker configuration only: executable is never taken from an HTTP
 * request. Uses an independently installed veraPDF CLI, not a client verdict.
 * Report validation establishes a PDF/A profile result, not ICP-Brasil trust
 * or compliance of the physical scanning/metadata process as a whole.
 */
export function veraPdfValidator({executable='verapdf',flavour='2b'}={}) {
 if(!['1a','1b','2a','2b','2u','3a','3b','3u','4','4e','4f'].includes(flavour))throw new TypeError('Invalid PDF/A profile');
 return async bytes=>{
  if(!(bytes instanceof Uint8Array)||!bytes.byteLength)throw new TypeError('PDF bytes required');
  const dir=await mkdtemp(join(tmpdir(),'capture-verapdf-'));
  try {
   const source=join(dir,'candidate.pdf');await writeFile(source,bytes,{mode:0o600});
   let stdout,exitCode=0;
   try {({stdout}=await run(executable,['--format','json','--flavour',flavour,source],{timeout:180000,maxBuffer:16*1024*1024}));}
   catch(error){
    // veraPDF returns 1 for a completed, non-compliant result. Parse its
    // report but never turn a nonzero exit into a positive validation.
    if(error.code!==1||error.killed||error.signal||typeof error.stdout!=='string')throw new Error('Independent validator could not complete');
    stdout=error.stdout;exitCode=1;
   }
   const report=JSON.parse(stdout).report,jobs=report?.jobs,summary=report?.batchSummary;
   const validations=jobs?.[0]?.validationResult;
   const valid=exitCode===0&&Array.isArray(jobs)&&jobs.length===1&&summary?.totalJobs===1&&
    summary.failedParsingJobs===0&&summary.failedEncryptedJobs===0&&summary.veraExceptions===0&&summary.outOfMemory===0&&
    Array.isArray(validations)&&validations.length===1&&validations[0].jobEndStatus==='normal'&&validations[0].compliant===true;
   return {valid,validator:'veraPDF',version:report?.buildInformation?.releaseDetails?.find(v=>v.id==='apps')?.version||'unknown',
    profile:flavour,sourceHash:checksum(bytes).valor,reportHash:checksum(Buffer.from(stdout)).valor,
    failedChecks:validations?.[0]?.details?.failedChecks??null};
  } finally {await rm(dir,{recursive:true,force:true});}
 };
}
