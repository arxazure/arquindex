import {S3Client, PutObjectCommand, GetObjectCommand} from '@aws-sdk/client-s3';
import {mkdir, open, readFile} from 'node:fs/promises';
import {resolve, dirname} from 'node:path';

export function tenantKey(tenantId, key) {
  if (typeof tenantId !== 'string' || !/^[A-Za-z0-9_-]{1,100}$/.test(tenantId)) throw new TypeError('Invalid tenant');
  if (typeof key !== 'string' || !key.startsWith(tenantId + '/capture/') ||
      !/^[A-Za-z0-9_/-]+$/.test(key) || key.includes('//')) throw new Error('Object outside tenant');
  return key;
}

// The bucket must be private. Never returns public or presigned URLs.
// Conditional PUT prevents accidental overwrite, not privileged deletion/WORM.
export function r2Storage({tenantId, bucket, endpoint, credentials}) {
  if (!bucket || new URL(endpoint).protocol !== 'https:') throw new TypeError('Private bucket and HTTPS endpoint required');
  const client = new S3Client({region: 'auto', endpoint, credentials, maxAttempts: 3});
  return {
    async putImmutable(key, bytes) {
      await client.send(new PutObjectCommand({Bucket: bucket, Key: tenantKey(tenantId, key),
        Body: bytes, ContentType: 'application/octet-stream', IfNoneMatch: '*'}));
    },
    async get(key) {
      const response = await client.send(new GetObjectCommand({Bucket: bucket, Key: tenantKey(tenantId, key)}));
      return Buffer.from(await response.Body.transformToByteArray());
    },
    close() { client.destroy(); }
  };
}

// For local integration/isolated staging on a private persistent volume.
// root must be application-owned (no untrusted filesystem writers/symlinks).
export function fileStorage({root, tenantId}) {
  const path = key => resolve(root, tenantKey(tenantId, key));
  return {
    async putImmutable(key, bytes) {
      const target = path(key);
      await mkdir(dirname(target), {recursive: true, mode: 0o700});
      const file = await open(target, 'wx', 0o600);
      try { await file.writeFile(bytes); await file.sync(); } finally { await file.close(); }
      const dir = await open(dirname(target), 'r');
      try { await dir.sync(); } finally { await dir.close(); }
    },
    get(key) { return readFile(path(key)); }
  };
}
