#!/usr/bin/env python3
"""Offline Ahrefs 4XX canonical triage; no website or DNS writes."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

def choose(row, names):
    folded = {k.strip().lower().replace(" ", "").replace("_", ""): v for k, v in row.items() if k}
    return next((folded[n] for n in names if folded.get(n)), "")

def classify(page, canonical, status):
    p, c = urlsplit(page), urlsplit(canonical)
    if not page or not canonical:
        return "missing_evidence"
    if c.scheme not in ("http", "https") or not c.netloc:
        return "invalid_canonical"
    if p.hostname != c.hostname:
        return "cross_host_manual_review"
    if c.scheme != "https":
        return "http_canonical_review"
    if status and status.isdigit() and 400 <= int(status) <= 499:
        return "canonical_4xx_confirm_in_live"
    return "verify_live_status"

def analyze(rows):
    findings = []
    for row in rows:
        page = choose(row, ("url", "pageurl", "sourceurl", "page"))
        canon = choose(row, ("canonical", "canonicalurl", "canonicaltarget", "canonicalhref"))
        status = choose(row, ("canonicalhttpcode", "canonicalstatus", "targetstatus", "httpcode", "statuscode"))
        # Generic httpCode often refers to the source URL, not target. Never claim target status from it.
        explicit_target = choose(row, ("canonicalhttpcode", "canonicalstatus", "targetstatus"))
        status = explicit_target or ""
        classification = classify(page, canon, status)
        findings.append({"page":page, "canonical":canon, "target_http_status_from_export":status, "category":classification, "host":urlsplit(page).hostname or "", "review_status":"UNVERIFIED_LIVE", "suggested_action":"Confirm source/target GET, redirects, indexability and HomeHost origin before edit"})
    return {"count":len(findings), "by_category":dict(sorted(Counter(x["category"] for x in findings).items())), "by_host":dict(sorted(Counter(x["host"] for x in findings).items())), "findings":findings,
            "limitations":["Export alone does not establish current live HTTP status, canonical target or hosting origin.",
                           "The Ahrefs 556 figure is audit occurrences and may not be 556 unique URLs.",
                           "Never rewrite canonical, sitemap, DNS, FTP or submit indexing automatically."]}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True, help="Ahrefs CSV exported with URL and canonical columns")
    ap.add_argument("--out", type=Path, default=Path("seo-report/canonical-4xx-triage.json"))
    args = ap.parse_args()
    if not args.input.is_file():
        ap.error("export not found")
    with args.input.open(encoding="utf-8-sig", newline="") as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames:
            ap.error("missing CSV headers")
        report=analyze(list(reader))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"rows":report["count"],"categories":report["by_category"],"output":str(args.out)},ensure_ascii=False))
if __name__ == "__main__":
    main()
