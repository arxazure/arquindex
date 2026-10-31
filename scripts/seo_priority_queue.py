#!/usr/bin/env python3
"""Rank read-only SEO findings for human review; does not change pages."""
import argparse
import csv
import json
from pathlib import Path

WEIGHTS = {
    "canonical_count_0": 80, "canonical_count_2": 80,
    "canonical_not_absolute_https": 85,
    "noindex_review": 70, "missing_title": 55,
    "missing_meta_description": 30, "structured_data_review": 20,
    "author_attribution_review": 15, "cross_property_links_review": 10,
    "outside_arq_domain": 90, "invalid_absolute_https_loc": 85,
    "invalid_xml_or_file": 95, "duplicate_loc": 25,
    "sitemap_over_50000_urls": 65,
}
def weight(issue):
    if issue.startswith("canonical_count_"): return 80
    if issue.startswith("h1_count_"): return 40
    if issue.startswith("invalid_xml_or_file:"): return 95
    return WEIGHTS.get(issue, 25)

def prioritize(html_report, sitemap_report):
    queue = []
    for page in html_report.get("pages", []):
        issues = page.get("issues", page.get("errors", []))
        if issues:
            queue.append({"kind": "html", "source": page.get("path", ""),
                          "issues": issues, "priority": max(map(weight, issues))})
    for item in sitemap_report.get("inventories", []):
        issues = item.get("issues", [])
        if issues:
            queue.append({"kind": "sitemap", "source": item.get("file", ""),
                          "issues": issues, "priority": max(map(weight, issues))})
    queue.sort(key=lambda a: (-a["priority"], a["kind"], a["source"]))
    return {"scope": "static_repository_only", "count": len(queue),
            "queue": queue, "limitations": [
                "Scores are internal triage weights, not Google metrics.",
                "No live HTTP, DNS, Search Console or conversion measurement.",
                "Review each finding before editing or publishing."]}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--html", default="seo-report/authority-preflight.json")
    p.add_argument("--sitemaps", default="seo-report/sitemap-preflight.json")
    p.add_argument("--out", default="seo-report/priority-queue.json")
    p.add_argument("--csv", default="seo-report/priority-review.csv")
    args = p.parse_args()
    html = json.loads(Path(args.html).read_text(encoding="utf-8"))
    sitemap = json.loads(Path(args.sitemaps).read_text(encoding="utf-8"))
    result = prioritize(html, sitemap)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    csv_path = Path(args.csv)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "priority", "kind", "source", "issues", "classification", "decision",
            "owner", "verified_live_url", "evidence", "reviewed_at"])
        writer.writeheader()
        for item in result["queue"]:
            writer.writerow({"priority": item["priority"], "kind": item["kind"],
                "source": item["source"], "issues": "; ".join(item["issues"]),
                "classification": "UNREVIEWED", "decision": "", "owner": "",
                "verified_live_url": "", "evidence": "", "reviewed_at": ""})
    print(json.dumps({"findings": result["count"], "output": str(out), "csv": str(csv_path)}))
if __name__ == "__main__":
    main()
