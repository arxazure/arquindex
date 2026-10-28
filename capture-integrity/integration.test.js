import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp, readFile, rm, writeFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {PGlite} from '@electric-sql/pglite';
import pg from 'pg';
import {captureService} from './service.js';
import {fileStorage, tenantKey} from './storage.js';
import {checksum} from './decreto-10278.js';
import {ocrProcessor} from './processing.js';
import {veraPdfValidator} from './verapdf.js';
const run = promisify(execFile);
const metadata = {assunto:'Teste', autor:'Emitente ficticio', dataDigitalizacao:'2026-10-27T10:00:00-03:00',
  localDigitalizacao:'BH', responsavelDigitalizacao:'Operador ficticio', titulo:'Teste', tipoDocumental:'Teste'};

test('SQL persistence, tenant boundaries, rollback, append-only audit and storage readback', async t => {
  const root = await mkdtemp(join(tmpdir(), 'capture-integration-'));
  // TEST_DATABASE_URL must point to an EMPTY, DISPOSABLE database, never production.
  let embedded;
  let pool;
  if (process.env.TEST_DATABASE_URL) {
    pool = new pg.Pool({connectionString:process.env.TEST_DATABASE_URL});
  } else {
    embedded = new PGlite(join(root, 'postgres'));
    const query = async (sql, params) => {
      const r = await embedded.query(sql, params);
      return {...r, rowCount: r.rows.length || r.affectedRows || 0};
    };
    pool = {query, async connect() { return {query, release() {}}; }};
  }
  try {
    for (const file of ['schema.sql', '002-append-only.sql']) {
      const sql = await readFile(new URL(file, import.meta.url), 'utf8');
      if (embedded) await embedded.exec(sql); else await pool.query(sql);
    }
    const storage = fileStorage({root, tenantId:'company-a'});
    const service = captureService({pool, storage, identity:{tenantId:'company-a',actorId:'operator-a',canCapture:true}});
    const other = captureService({pool, storage:fileStorage({root, tenantId:'company-b'}),
      identity:{tenantId:'company-b',actorId:'operator-b',canCapture:true}});
    const bytes = Buffer.from('original fixture');
    const received = await service.receive({bytes, metadata, origem:'scanner', channel:'scanner'});
    const id = received.documentoId;
    await t.test('committed bytes and descriptive metadata survive database reopen', async () => {
      if (embedded) { await embedded.close(); embedded = new PGlite(join(root, 'postgres')); }
      assert.deepEqual(await service.readVersion(id, 1), bytes);
      const doc = await pool.query('SELECT metadata,metadata_valid FROM capture_integrity_documents WHERE tenant_id=$1 AND document_id=$2',['company-a',id]);
      assert.equal(doc.rows[0].metadata.autor, metadata.autor);
      assert.equal(doc.rows[0].metadata_valid, true);
      assert.equal(received.hash, checksum(bytes).valor);
    });
    await t.test('other tenant cannot read, process, or use another object prefix', async () => {
      await assert.rejects(other.readVersion(id, 1), /not found in tenant/);
      let called = false;
      await assert.rejects(other.process({documentId:id, sourceVersion:1, stage:'ocr', processor:async()=>{called=true;}}), /not found/);
      assert.equal(called,false);
      assert.throws(()=>tenantKey('company-b',`company-a/capture/${id}/received`), /outside tenant/);
      assert.throws(()=>captureService({pool,storage,identity:{tenantId:'company-a',actorId:'a',canCapture:false}}), /permission/);
    });
    await t.test('OCR output becomes a new hash and preserves source version', async () => {
      // This subtest checks orchestration; real OCR is tested separately below.
      const result = await service.process({documentId:id,sourceVersion:1,stage:'ocr',
        processor:async()=>({bytes:Buffer.from('derived fixture')})});
      assert.equal(result.version, 2);
      assert.notEqual(result.hash, received.hash);
      assert.deepEqual(await service.readVersion(id, 1), bytes);
      const audit = await pool.query("SELECT details FROM capture_integrity_audit WHERE tenant_id=$1 AND document_id=$2 AND action='version_added'",['company-a',id]);
      assert.equal(audit.rows[0].details.sourceVersion, 1);
    });
    await t.test('unvalidated PDF/A cannot become a committed PDF/A version', async () => {
      await assert.rejects(service.process({documentId:id, sourceVersion:2, stage:'pdfa',
        processor:async()=>({bytes:Buffer.from('not a validated PDF/A')})}), /validation evidence/);
      const rows = await pool.query("SELECT * FROM capture_integrity_versions WHERE stage='pdfa'");
      assert.equal(rows.rowCount,0);
    });
    await t.test('immutable objects, version records and audit reject mutation', async () => {
      await assert.rejects(storage.putImmutable(`company-a/capture/${id}/received`,bytes), /EEXIST/);
      await assert.rejects(pool.query('UPDATE capture_integrity_versions SET stage=$1 WHERE document_id=$2',['changed',id]), /append-only/);
      await assert.rejects(pool.query('DELETE FROM capture_integrity_audit WHERE document_id=$1',[id]), /append-only/);
    });
    await t.test('failed DB transaction leaves no partial document and preserves object', async () => {
      const bad = {...metadata,identificadorDigital:id};
      // A fresh storage root allows the duplicate DB key to be exercised.
      const retryStore = fileStorage({root:join(root,'retry'),tenantId:'company-a'});
      const retry = captureService({pool,storage:retryStore,identity:{tenantId:'company-a',actorId:'a',canCapture:true}});
      await assert.rejects(retry.receive({bytes,metadata:bad,origem:'scanner',channel:'upload'}), /duplicate key/);
      assert.deepEqual(await retryStore.get(`company-a/capture/${id}/received`),bytes);
      const count = await pool.query('SELECT count(*) AS n FROM capture_integrity_documents');
      assert.equal(Number(count.rows[0].n),1);
    });
    await t.test('storage corruption is detected and audited before processing', async () => {
      await writeFile(join(root,`company-a/capture/${id}/received`),'tampered');
      await assert.rejects(service.readVersion(id,1),/integrity failed/);
      const rows = await pool.query("SELECT * FROM capture_integrity_audit WHERE action='integrity_failed'");
      assert.equal(rows.rowCount,1);
    });
    await t.test('real raster PDF -> OCR -> SQL version -> readback', {skip:!process.env.CAPTURE_REAL_OCR}, async t => {
      const fixture = join(root, 'scan.pdf');
      await run('python', ['-c',
        'from PIL import Image,ImageDraw,ImageFont; import sys; im=Image.new("RGB",(1800,1100),"white"); d=ImageDraw.Draw(im); f=ImageFont.truetype("DejaVuSans.ttf",65); d.text((100,200),"ARQUINDEX TEST DOCUMENT 2026",font=f,fill="black"); im.save(sys.argv[1],"PDF",resolution=200)', fixture]);
      const raw = await readFile(fixture);
      const doc = await service.receive({bytes:raw,metadata,origem:'importado_fisico',channel:'upload'});
      const result = await service.process({documentId:doc.documentoId,sourceVersion:1,stage:'ocr',processor:ocrProcessor({language:'eng'})});
      assert.equal(result.version,2);
      assert.notEqual(result.hash, doc.hash);
      assert.deepEqual(await service.readVersion(doc.documentoId,1),raw);
      const output = await service.readVersion(doc.documentoId,2);
      const searchable = join(root,'searchable.pdf'); await writeFile(searchable,output);
      const text = await run('pdftotext',[searchable,'-']);
      assert.match(text.stdout.replace(/\s+/g,' '),/ARQUINDEX TEST DOCUMENT 2026/);
      // Real PDF/A conversion is invoked, but lack of an independent validator
      // must fail closed and must not register a PDF/A version.
      await assert.rejects(service.process({documentId:doc.documentoId,sourceVersion:2,stage:'pdfa',
        processor:ocrProcessor({pdfa:true,language:'eng'})}), /Independent PDF\/A validation required/);
      const versions = await pool.query('SELECT stage FROM capture_integrity_versions WHERE document_id=$1 ORDER BY version_number',[doc.documentoId]);
      assert.deepEqual(versions.rows.map(r=>r.stage),['recebido','ocr']);
      await t.test('independent veraPDF validation gates persisted PDF/A version', {skip:!process.env.CAPTURE_VERAPDF}, async()=>{
        const validate=veraPdfValidator({executable:process.env.CAPTURE_VERAPDF,flavour:'2b'});
        assert.equal((await validate(output)).valid,false);
        const pdfa=await service.process({documentId:doc.documentoId,sourceVersion:2,stage:'pdfa',
          processor:ocrProcessor({pdfa:true,language:'eng',validatePdfa:validate})});
        assert.equal(pdfa.version,3);
        const stored=await service.readVersion(doc.documentoId,3);
        const proof=await validate(stored);assert.equal(proof.valid,true);assert.equal(proof.sourceHash,pdfa.hash);
        const evidence=await pool.query("SELECT details FROM capture_integrity_audit WHERE document_id=$1 AND action='version_added' ORDER BY id DESC LIMIT 1",[doc.documentoId]);
        assert.equal(evidence.rows[0].details.evidence.validator,'veraPDF');
        assert.equal(evidence.rows[0].details.sourceVersion,2);
        assert.deepEqual(await service.readVersion(doc.documentoId,1),raw);
      });
    });
  } finally {
    if (embedded) await embedded.close(); else await pool.end();
    await rm(root,{recursive:true,force:true});
  }
});
