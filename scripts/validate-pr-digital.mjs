import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const result = spawnSync(process.env.PYTHON || 'python3', [fileURLToPath(new URL('./validate-pr-digital.py', import.meta.url))], {stdio:'inherit'});
if (result.error) console.error(result.error.message);
process.exit(result.status ?? 1);
