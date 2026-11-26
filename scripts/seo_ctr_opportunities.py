#!/usr/bin/env python3
"""Rank GSC page exports for CTR work. Offline; never changes production."""
import argparse
import csv
import json
from pathlib import Path
from urllib.parse import urlsplit

def number(value):
    s = str(value or "0").strip().replace("%", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0

def rank(rows, minimum=30):
    output = []
    for row in rows:
        folded = {k.lower().strip(): v for k, v in row.items() if k}
        page = folded.get("pages") or folded.get("page") or folded.get("página") or folded.get("url") or ""
        impressions = number(folded.get("impressions", folded.get("impressões")))
        clicks = number(folded.get("clicks", folded.get("cliques")))
        position = number(folded.get("position", folded.get("posição")))
        if not page.startswith("https://") or impressions < minimum or position <= 0:
            continue
        ctr = 100 * clicks / impressions
        # Rank opportunities in reachable positions, without claiming expected CTR.
        score = round(impressions * max(0, 0.04 - ctr / 100) * (1 if position <= 10 else 0.55 if position <= 20 else 0.15), 2)
        output.append({"url": page, "host": urlsplit(page).hostname, "clicks": clicks,
                       "impressions": impressions, "ctr_percent": round(ctr, 2),
                       "position": position, "priority_score": score})
    return sorted(output, key=lambda r: (-r["priority_score"], -r["impressions"], r["url"]))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("seo-report/ctr-opportunities.json"))
    parser.add_argument("--min-impressions", type=int, default=30)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    with args.input.open(encoding="utf-8-sig", newline="") as source:
        ranked = rank(csv.DictReader(source), args.min_impressions)
    result = {"source": str(args.input), "method": "heuristic prioritization, not predicted clicks",
              "rows_eligible": len(ranked), "opportunities": ranked[:args.limit],
              "note": "Compare by query, device and position before changing titles; export is not a full site index."}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"eligible": len(ranked), "selected": len(result["opportunities"]), "out": str(args.out)}))

if __name__ == "__main__":
    main()
