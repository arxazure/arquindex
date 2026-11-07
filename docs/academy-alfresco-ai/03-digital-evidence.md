# Laboratory 2 — SHA-256 and reproducible file inventories

SHA-256 detects changes in file bytes; **it does not alone establish document authorship, authenticity or a forensic chain of custody**.

Save this as `manifest.py`:

```python
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json, sys

def digest(path):
    h = sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1048576), b""):
            h.update(chunk)
    return h.hexdigest()

root = Path(sys.argv[1]).resolve()
if not root.is_dir():
    raise SystemExit("Folder not found")
files = [
    {"path": p.relative_to(root).as_posix(),
     "bytes": p.stat().st_size, "sha256": digest(p)}
    for p in sorted(root.rglob("*"))
    if p.is_file() and p.name != "manifest.json"
]
result = {"created_utc": datetime.now(timezone.utc).isoformat(),
          "algorithm": "SHA-256", "files": files}
(root / "manifest.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Audited {len(files)} files")
```

## Test
```bash
mkdir sample
printf 'Synthetic test\n' > sample/demo.txt
python manifest.py sample
```
Modify `demo.txt`, run again and compare its hash with the previous manifest. Do not overwrite earlier evidence manifests in a real investigation.

## Required production controls
Record acquisition authorization, custodians, transfers, timestamps, access records and protected storage. Separate source files from OCR derivatives, validate cryptographic signatures where appropriate, and preserve immutable logs.

**Exercise:** Does a changed hash after OCR prove tampering? **Answer:** No. OCR output is a derivative whose bytes may legitimately differ. Record both source and derivative hashes.

[Academy index](README.md) · [ECM AI architecture](01-alfresco-ai.md) · [API lab](02-fastapi-postgresql.md)
