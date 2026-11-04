#!/usr/bin/env python3
"""Summarize read-only Arquindex semantic SEO audits without inventing rankings.

The inputs are diagnostic HTTP/HTML checks, not Search Console metrics.
No publishing, external requests, or secrets are required.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.parse import urlsplit

ISSUE_PRIORITY = {
    "noindex": "critical",
    "missing_title": "high",
    "missing_canonical": "high",
    "external_canonical_review": "high",
    "h1_count": "medium",
    "missing_description": "medium",
    "thin_content_review": "review",
}
ORDER = ("critical", "high", "medium", "review")


def summarize(document):
    rows = document.get("results")
    if not isinstance(rows, list):
        raise ValueError("Audit JSON must contain a results list")
    totals = Counter()
    issues = Counter()
    destinations = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        url = str(row.get("url", ""))
        host = urlsplit(url).hostname or "unknown"
        status = row.get("status")
        error = row.get("error")
        found = list(dict.fromkeys(row.get("issues") or []))
        rank = set()
        if error or not isinstance(status, int) or status >= 400:
            rank.add("critical")
            totals["unavailable"] += 1
        elif status >= 300:
            rank.add("medium")
            totals["redirect"] += 1
        elif status == 200:
            totals["http_200"] += 1
        for issue in found:
            issues[str(issue)] += 1
            rank.add(ISSUE_PRIORITY.get(issue, "review"))
        priority = next((p for p in ORDER if p in rank), "ok")
        totals[priority] += 1
        destinations.append({
            "url": url, "host": host, "http_status": status,
            "final_url": row.get("final_url"), "priority": priority,
            "issues": found, "error": error,
        })
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "audit_scope": "approved URLs in configured sites.txt only",
        "audited": len(destinations),
        "http_200": totals["http_200"],
        "unavailable": totals["unavailable"],
        "by_priority": {p: totals[p] for p in (*ORDER, "ok")},
        "issues": dict(issues.most_common()),
        "pages": destinations,
        "limitations": [
            "Read-only diagnostics; not an indexing or ranking measurement.",
            "No changes to live HTML, sitemaps, hosting, or Search Console.",
            "An HTTP 200 alone does not prove SEO correctness or indexability.",
        ],
    }


def markdown(summary):
    lines = [
        "# Arquindex | Saúde do SEO semântico", "",
        f"Data UTC: {summary['generated_at_utc']}",
        f"URLs verificadas: **{summary['audited']}**; HTTP 200: **{summary['http_200']}**; "
        f"indisponíveis: **{summary['unavailable']}**.", "",
        "| Prioridade | Páginas |", "|---|---:|",
    ]
    for p, count in summary["by_priority"].items():
        lines.append(f"| {p.upper()} | {count} |")
    lines.extend(["", "## Evidências por URL", ""])
    for page in summary["pages"]:
        details = ", ".join(page["issues"]) or "nenhuma falha básica detectada"
        lines.append(
            f"- **{page['priority'].upper()}**: {page['url']} "
            f"(HTTP {page['http_status'] if page['http_status'] is not None else 'indisponível'}). "
            f"{details}."
        )
    lines.extend([
        "", "## Próximas decisões", "",
        "1. Corrigir indisponibilidades, noindex e canonicals inconsistentes antes de expandir conteúdo.",
        "2. Revisar títulos, H1, descrições e páginas pouco informativas com equipe editorial.",
        "3. Cruzar página + consulta no GSC quando dados reais e credenciais estiverem disponíveis.",
        "4. Registrar revisões, origem de publicação, URL HTTP 200 e efeito medido antes de alegar melhoria.", "",
        "**Limite:** o relatório não mede indexação, posições nem conversões e não publica alterações.", "",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown", required=True)
    parser.add_argument("--github-summary")
    args = parser.parse_args()
    source = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = summarize(source)
    content = markdown(result)
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    Path(args.markdown).write_text(content, encoding="utf-8")
    if args.github_summary:
        with Path(args.github_summary).open("a", encoding="utf-8") as out:
            out.write(content + "\n")
    print(f"Semantic audit summary: {result['audited']} URLs; {result['unavailable']} unavailable")


if __name__ == "__main__":
    main()
