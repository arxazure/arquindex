#!/usr/bin/env python3
"""Compare Ahrefs issue exports with local SEO candidates; no site changes.

Input must have a URL column and an issue/type column.
Usage: python3 scripts/ahrefs_reconcile.py --ahrefs export.csv --candidates seo-report/ahrefs-review.csv
"""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

URL_HEADERS = ("url", "page url", "affected url", "page", "source url")
ISSUE_HEADERS = ("issue", "issue type", "type", "problem")
CANDIDATE_HEADERS = ("candidate_url", "issue")
ISSUE_TERMS = {
    "orphan": "orphan_within_scanned_files_review",
    "incoming internal": "orphan_within_scanned_files_review",
    "meta description": "meta_description_missing",
    "open graph": "open_graph_incomplete",
    "og tags": "open_graph_incomplete",
    "title too long": "title_over_60_characters_review",
    "multiple h1": "multiple_h1",
    "faqpage": "faq_schema_review_not_automatic",
    "faq page": "faq_schema_review_not_automatic",
}
# These Ahrefs issues are NOT established by the local static HTML inventory.
EXTERNAL_REVIEW = ("slow page", "indexnow", "referring domains", "word count")


def field(columns, aliases):
    lookup = {str(k).strip().lower().lstrip("\ufeff"): k for k in columns}
    for alias in aliases:
        if alias in lookup:
            return lookup[alias]
    return None


def normalize(url):
    """Only fold scheme/hostname case and fragment; preserve path and trailing slash."""
    try:
        p = urlsplit(str(url or "").strip())
        host = p.hostname
        port = p.port
    except ValueError:
        return None
    if p.scheme.lower() not in ("http", "https") or not host:
        return None
    host = host.lower()
    if port and port not in (80, 443):
        host += ":" + str(port)
    return urlunsplit((p.scheme.lower(), host, p.path or "/", p.query, ""))


def classify_issue(value):
    name = str(value).strip().lower()
    if any(term in name for term in EXTERNAL_REVIEW):
        return None
    for term, code in ISSUE_TERMS.items():
        if term in name:
            return code
    return None


def load_csv(path, required):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"{path}: CSV has no header")
        fields = [field(reader.fieldnames, aliases) for aliases in required]
        if any(f is None for f in fields):
            raise ValueError(f"{path}: required headers missing; found {reader.fieldnames}")
        return [tuple(row.get(col, "") for col in fields) for row in reader]


def reconcile(ahrefs, candidates):
    indexed = {}
    for url, issue in candidates:
        key = (normalize(url), issue.strip())
        if key[0]:
            indexed.setdefault(key, 0)
            indexed[key] += 1
    rows = []
    totals = Counter()
    for raw_url, raw_issue in ahrefs:
        url = normalize(raw_url)
        issue = classify_issue(raw_issue)
        if not url:
            status = "INVALID_URL"
        elif not issue:
            status = "MANUAL_REVIEW_EXTERNAL_OR_UNKNOWN_ISSUE"
        elif (url, issue) in indexed:
            status = "MATCH_REQUIRES_LIVE_VERIFICATION"
        else:
            status = "NO_EXACT_LOCAL_MATCH"
        totals[status] += 1
        rows.append({"ahrefs_url": raw_url, "ahrefs_issue": raw_issue,
                     "normalized_url": url or "", "mapped_candidate_issue": issue or "",
                     "local_matches": indexed.get((url, issue), 0),
                     "status": status,
                     "notes": "No site change; validate HTTP, canonical and deployed source before edits."})
    return {"scope": "CSV_RECONCILIATION_ONLY", "counts": dict(totals), "rows": rows,
            "limitations": [
                "Matching is exact and does not infer deployment or claim issue resolution.",
                "URL path, query and trailing slash are preserved to avoid false positives.",
                "Performance, backlinks, IndexNow and word-count issues require their original evidence.",
                "A matched candidate still requires live confirmation and editorial review."
            ]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ahrefs", type=Path, required=True)
    ap.add_argument("--candidates", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=Path("seo-report/ahrefs-reconciled.csv"))
    ap.add_argument("--json", type=Path, default=Path("seo-report/ahrefs-reconciled.json"))
    a = ap.parse_args()
    audit = load_csv(a.ahrefs, (URL_HEADERS, ISSUE_HEADERS))
    candidates = load_csv(a.candidates, (("candidate_url",), ("issue",)))
    result = reconcile(audit, candidates)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.json.parent.mkdir(parents=True, exist_ok=True)
    with a.out.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "ahrefs_url", "ahrefs_issue", "normalized_url", "mapped_candidate_issue",
            "local_matches", "status", "notes"])
        writer.writeheader()
        writer.writerows(result["rows"])
    a.json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(result["rows"]), "status": result["counts"],
                      "csv": str(a.out), "json": str(a.json)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
