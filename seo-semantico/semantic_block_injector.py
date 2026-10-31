#!/usr/bin/env python3
"""Create reviewed semantic HTML blocks in a separate staging directory only."""
import argparse, hashlib, html, json, re
from pathlib import Path

def block_html(identifier, info):
    def esc(x): return html.escape(str(x), quote=True)
    lines=[f"<!-- ARQ-SEMANTIC:{identifier}:START -->",
           f'<section class="arq-semantic" data-arq-semantic="{esc(identifier)}" aria-label="{esc(info["title"])}">',
           f'<h2>{esc(info["title"])}</h2>']
    lines.extend(f"<p>{esc(p)}</p>" for p in info.get("paragraphs",[]))
    if info.get("points"):
        lines+=["<ul>"]+[f"<li>{esc(s)}</li>" for s in info["points"]]+["</ul>"]
    for q in info.get("questions",[]):
        lines.append(f'<details><summary>{esc(q["question"])}</summary><p>{esc(q["answer"])}</p></details>')
    return "\n".join(lines+["</section>",f"<!-- ARQ-SEMANTIC:{identifier}:END -->"])

def inject(source, identifier, content):
    if not re.fullmatch(r"[a-z0-9_-]{1,64}", identifier):
        raise ValueError("Invalid block id")
    start=f"<!-- ARQ-SEMANTIC:{identifier}:START -->"
    end=f"<!-- ARQ-SEMANTIC:{identifier}:END -->"
    if source.count(start)!=1 or source.count(end)!=1 or source.index(start)>=source.index(end):
        raise ValueError("Exactly one correctly ordered marker pair is required")
    expr=re.compile(re.escape(start)+r".*?"+re.escape(end), re.S)
    return expr.sub(lambda _:block_html(identifier,content),source,count=1)

def process(config, root, staging, apply=False):
    root, staging=Path(root).resolve(),Path(staging).resolve()
    if root==staging or root in staging.parents and staging.name=="":raise ValueError("Invalid staging path")
    results=[]
    prepared=[]
    for target in config["targets"]:
        rel=Path(target["path"])
        if rel.is_absolute() or ".." in rel.parts or rel.suffix.lower() not in (".html",".htm"):
            raise ValueError("Unsafe relative HTML path")
        src=(root/rel).resolve()
        if not src.is_relative_to(root):raise ValueError("Outside source root")
        original=src.read_text(encoding="utf-8")
        revised=inject(original,target["block_id"],target["content"])
        prepared.append((rel,revised))
        results.append({"path":str(rel),"changed":original!=revised,
                        "source_sha256":hashlib.sha256(original.encode()).hexdigest(),
                        "staging_sha256":hashlib.sha256(revised.encode()).hexdigest()})
    staging.mkdir(parents=True,exist_ok=True)
    if apply:
        for rel,text in prepared:
            destination=staging/rel
            destination.parent.mkdir(parents=True,exist_ok=True)
            destination.write_text(text,encoding="utf-8")
    (staging/"semantic-changes.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
    return results

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--config",required=True);p.add_argument("--root",required=True)
    p.add_argument("--output",required=True);p.add_argument("--apply",action="store_true")
    a=p.parse_args()
    data=json.loads(Path(a.config).read_text(encoding="utf-8"))
    print(json.dumps(process(data,a.root,a.output,a.apply),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
