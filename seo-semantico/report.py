#!/usr/bin/env python3
"""Convert read-only audit JSON to prioritized, reviewable Markdown."""
import json
import sys
from pathlib import Path

PRIORITY = {
 "noindex": "CRITICAL",
 "missing_canonical": "HIGH",
 "missing_title": "HIGH",
 "h1_count": "MEDIUM",
 "missing_description": "MEDIUM",
 "thin_content_review": "REVIEW",
}
def render(data):
 rows=data.get("results",[])
 lines=["# Arquindex SEO diagnostic", "", "This report is read-only and does not submit URLs to search engines.", "",
        f"Audited URLs: {len(rows)}", ""]
 for row in rows:
  lines.extend([f"## {row['url']}", ""])
  if row.get("error"):
   lines.extend([f"- Availability error: {row['error']}", "- Priority: **CRITICAL — investigate hosting/network**", ""])
   continue
  lines.append(f"- HTTP: {row.get('status','unknown')} | Final URL: {row.get('final_url','unknown')}")
  lines.append(f"- Title: {row.get('title','(none)')}")
  lines.append(f"- Canonical: {row.get('canonical') or '(missing)'}")
  issues=row.get("issues",[])
  lines.extend(["- Findings: "+(", ".join(PRIORITY.get(i,"REVIEW")+": "+i for i in issues) if issues else "no basic issues detected"),
                "- Note: automated diagnostics do not prove indexing or Google rankings.", ""])
 return "\n".join(lines)+"\n"
def main():
 if len(sys.argv)!=3:raise SystemExit("Usage: report.py audit.json report.md")
 data=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
 Path(sys.argv[2]).write_text(render(data),encoding="utf-8")
if __name__=="__main__":main()
