import {mkdtemp, writeFile, readFile, rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
const run = promisify(execFile);

/** Run in a restricted worker/container. Input type/size, concurrency and resource
 * limits must be enforced by the host. Arguments are fixed; no shell interpolation.
 * OCRmyPDF output-type=pdfa requests conversion, not independent certification.
 */
export function ocrProcessor({pdfa = false, language = 'por', validatePdfa} = {}) {
  if (!/^[a-z]{3}(\+[a-z]{3})*$/.test(language)) throw new TypeError('Invalid OCR language');
  return async bytes => {
    const dir = await mkdtemp(join(tmpdir(), 'capture-ocr-'));
    try {
      const source = join(dir, 'source.pdf'), output = join(dir, 'output.pdf');
      await writeFile(source, bytes, {mode: 0o600});
      await run('ocrmypdf', ['--skip-text', '--jobs', '1', '--language', language,
        '--output-type', pdfa ? 'pdfa-2' : 'pdf', source, output], {timeout: 180000, maxBuffer: 1024 * 1024});
      const result = await readFile(output);
      const text = await run('pdftotext', [output, '-'], {timeout: 30000, maxBuffer: 8 * 1024 * 1024});
      if (!text.stdout.trim()) throw new Error('Searchable OCR text absent; manual review required');
      const validation = pdfa ? await validatePdfa?.(result) : {validator: 'pdftotext', searchableText: true};
      if (pdfa && (validation?.valid !== true || !validation.validator)) throw new Error('Independent PDF/A validation required');
      return {bytes: result, validation};
    } finally { await rm(dir, {recursive: true, force: true}); }
  };
}
