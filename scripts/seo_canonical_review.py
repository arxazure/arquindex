#!/usr/bin/env python3
"""Offline Ahrefs 4XX canonical triage; no website or DNS writes."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

OFFICIAL_HOSTS = {"arquindex.com.br", "www.arquindex.com.br"}

def normalize_header(value):
    return "".join(char for char in value.lower() if char.isalnum())

def choose(row, names):
    folded = {normalize_header(k.strip()): v for k, v in row.items() if k}
    return next((folded[normalize_header(n)] for n in names
                 if folded.get(normalize_header(n))), "")

def parse_web_url(value):
    if not isinstance(value, str) or not value or value != value.strip():
        return None
    if any(ord(char) < 32 or char == "\\" for char in value):
        return None
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        port = parsed.port
    except ValueError:
        return None
    if (parsed.scheme not in ("http", "https") or not hostname
            or parsed.username is not None or parsed.password is not None):
        return None
    if port is not None and port != (443 if parsed.scheme == "https" else 80):
        return None
    return parsed

def classify(page, canonical, status):
    if not page or not canonical:
        return "missing_evidence"
    p, c = parse_web_url(page), parse_web_url(canonical)
    if not p:
        return "invalid_page_url"
    if not c:
        return "invalid_canonical"
    if p.hostname not in OFFICIAL_HOSTS:
        return "source_host_manual_review"
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
        canon = choose(row, ("canonical", "canonicalurl", "canonicaltarget",
                             "canonicalhref", "canonicalurltarget"))
        status = choose(row, ("canonicalhttpcode", "canonicalstatus",
                              "canonicalstatuscode", "targetstatus",
                              "targethttpcode", "targetstatuscode", "targethttpstatuscode",
                              "canonicalurlhttpcode", "canonicalurlstatuscode",
                              "canonicalurlhttpstatuscode", "canonicalhttpstatuscode",
                              "canonicaltargethttpcode", "canonicaltargethttpstatuscode",
                              "canonicaltargetstatuscode"))
        source_status = choose(row, ("sourcehttpcode", "sourcehttpstatuscode",
                                     "pagehttpcode", "pagehttpstatuscode"))
        classification = classify(page, canon, status)
        parsed_page = parse_web_url(page)
        findings.append({"page":page, "canonical":canon,
                         "source_http_status_from_export":source_status,
                         "target_http_status_from_export":status,
                         "category":classification,
                         "host":parsed_page.hostname if parsed_page else "",
                         "review_status":"UNVERIFIED_LIVE",
                         "suggested_action":"Confirm source/target GET, redirects, indexability and HomeHost origin before edit"})
    return {"count":len(findings), "by_category":dict(sorted(Counter(x["category"] for x in findings).items())), "by_host":dict(sorted(Counter(x["host"] for x in findings).items())), "findings":findings,
            "limitations":["Export alone does not establish current live HTTP status, canonical target or hosting origin.",
                           "The Ahrefs 556 figure is audit occurrences and may not be 556 unique URLs.",
                           "Never rewrite canonical, sitemap, DNS, FTP or submit indexing automatically."]}

def read_export(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("missing CSV headers")
        return analyze(list(reader))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True, help="Ahrefs CSV exported with URL and canonical columns")
    ap.add_argument("--out", type=Path, default=Path("seo-report/canonical-4xx-triage.json"))
    args = ap.parse_args()
    if not args.input.is_file():
        ap.error("export not found")
    try:
        report = read_export(args.input)
    except ValueError as exc:
        ap.error(str(exc))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"rows":report["count"],"categories":report["by_category"],"output":str(args.out)},ensure_ascii=False))
if __name__ == "__main__":
    main()
