import {open} from 'node:fs/promises';

/** Import only a file finalized by the producer (e.g. atomic rename from .tmp).
 * Does not install a Windows scanner driver/watcher or delete/move originals.
 * Host binds filePath to an allowlisted private input root and trusted job.
 */
export async function receiveFinalizedFile(service, {filePath, metadata, origem, publicBody = false,
  channel = 'watched_folder', maxBytes = 100 * 1024 * 1024}) {
  const file = await open(filePath, 'r');
  try {
    const before = await file.stat();
    if (!before.isFile() || before.size < 1 || before.size > maxBytes) throw new Error('Invalid finalized file');
    const bytes = await file.readFile();
    const after = await file.stat();
    if (before.size !== after.size || before.mtimeMs !== after.mtimeMs || before.ctimeMs !== after.ctimeMs) {
      throw new Error('Input changed during read; finalize producer file first');
    }
    return service.receive({bytes, metadata, origem, publicBody, channel});
  } finally { await file.close(); }
}
