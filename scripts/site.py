#!/usr/bin/env python3
r"""
Generate a static landing page for GitHub Pages.

Replaces the Jekyll site from the previous setup. Two jobs:

  1. Give one URL that lists every variant, so a recruiter who follows your
     LinkedIn banner can see the full set instead of a single CV.
  2. Make the unfinished state obvious. Each variant is labelled with its count
     of unresolved [ADD: ...] placeholders, so the site cannot quietly imply a
     finished document when it is not one.

Self-contained output: one HTML file, no external assets, no JS frameworks.
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
OUT = DIST / "site"

PLACEHOLDER = re.compile(r"\[ADD[^]]*\]|\[RESOLVE[^]]*\]", re.IGNORECASE)

LANGUAGE_LABEL = {"en": "English", "de": "Deutsch"}
LANGUAGE_ORDER = {"en": 0, "de": 1}


def count_placeholders(cv_yaml: Path) -> int:
    data = yaml.safe_load(cv_yaml.read_text(encoding="utf-8")) or {}
    blob = yaml.safe_dump(data.get("cv", {}), allow_unicode=True)
    return len(PLACEHOLDER.findall(blob))


def collect() -> list[dict]:
    variants = []
    for directory in sorted(DIST.iterdir()):
        if not directory.is_dir() or directory.name == "site":
            continue
        composed = directory / "cv.yaml"
        if not composed.exists():
            continue

        data = yaml.safe_load(composed.read_text(encoding="utf-8")) or {}
        cv = data.get("cv", {})
        lang = cv.get("language", "")
        if not lang:
            # The locale lives outside `cv`; fall back to the file path.
            lang = "de" if "_DE" in directory.name else "en"

        files = []
        for suffix, label in (("pdf", "PDF"), ("docx", "DOCX"), ("html", "HTML")):
            matches = sorted(directory.glob(f"*.{suffix}"))
            if matches:
                files.append((label, matches[0].name))

        slug = directory.name
        variants.append(
            {
                "dir": slug,
                "lang": lang,
                "name": cv.get("headline") or slug.replace("_", " "),
                "files": files,
                "open": count_placeholders(composed),
            }
        )

    variants.sort(key=lambda v: (LANGUAGE_ORDER.get(v["lang"], 9), v["dir"]))
    return variants


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Thomas Heinz — Curriculum Vitae</title>
<meta name="description" content="CV variants for Thomas Heinz, Director-level
Solutions Engineering, Identity and Security, Central and Eastern Europe.">
<style>
  :root {{ --navy:#003865; --ink:#1a1a1a; --muted:#666; --line:#e2e6ea; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",
         Roboto,"Helvetica Neue",Arial,sans-serif; color:var(--ink); }}
  .wrap {{ max-width:760px; margin:0 auto; padding:48px 24px 80px; }}
  h1 {{ color:var(--navy); font-size:2rem; margin:0 0 4px; letter-spacing:-.01em; }}
  .sub {{ color:var(--muted); margin:0 0 32px; }}
  h2 {{ color:var(--navy); font-size:1.05rem; text-transform:uppercase;
        letter-spacing:.08em; margin:36px 0 12px; font-weight:600; }}
  .card {{ border:1px solid var(--line); border-radius:8px; padding:18px 20px;
           margin-bottom:12px; }}
  .card h3 {{ margin:0 0 10px; font-size:1rem; font-weight:600; }}
  .links a {{ display:inline-block; margin-right:10px; padding:5px 12px;
              border:1px solid var(--navy); border-radius:5px; color:var(--navy);
              text-decoration:none; font-size:.85rem; }}
  .links a:hover {{ background:var(--navy); color:#fff; }}
  .note {{ font-size:.82rem; color:var(--muted); margin-top:8px; }}
  .warn {{ background:#fff8e6; border:1px solid #f0d9a0; border-radius:6px;
           padding:10px 12px; font-size:.82rem; color:#6b5310; margin-top:10px; }}
  footer {{ margin-top:48px; padding-top:20px; border-top:1px solid var(--line);
            font-size:.85rem; color:var(--muted); }}
  footer a {{ color:var(--navy); }}
</style>
</head>
<body>
<div class="wrap">
  <h1>Thomas Heinz</h1>
  <p class="sub">Director-level Solutions Engineering — Identity &amp; Security,
     Central &amp; Eastern Europe</p>

{body}

  <footer>
    Built from a single YAML source with
    <a href="https://github.com/rendercv/rendercv">RenderCV</a>. Every PDF on this
    page is real vector text, not an image — these CVs parse correctly in applicant
    tracking systems.<br>
    <a href="{site}">thomasheinz.net</a> ·
    <a href="https://www.linkedin.com/in/thomas-heinz/">LinkedIn</a> ·
    <a href="{repo}">Source repository</a>
  </footer>
</div>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", default="https://thomasheinz.net")
    parser.add_argument("--repo", default="https://github.com/TomTomNavigator/online-cv")
    args = parser.parse_args()

    if not DIST.exists():
        sys.exit("error: dist/ not found — run scripts/build.py first")

    variants = collect()
    if not variants:
        sys.exit("error: no built variants found in dist/")

    chunks = []
    for lang in sorted({v["lang"] for v in variants}, key=lambda l: LANGUAGE_ORDER.get(l, 9)):
        chunks.append(f"<h2>{html.escape(LANGUAGE_LABEL.get(lang, lang))}</h2>")
        for variant in [v for v in variants if v["lang"] == lang]:
            links = "".join(
                f'<a href="{variant["dir"]}/{html.escape(filename)}">{label}</a>'
                for label, filename in variant["files"]
            )
            warning = ""
            if variant["open"]:
                warning = (
                    f'<div class="warn">{variant["open"]} placeholder(s) still to '
                    "be filled in — check REVIEW.md.</div>"
                )
            chunks.append(
                '  <div class="card">\n'
                f'    <h3>{html.escape(variant["name"])}</h3>\n'
                f'    <div class="links">{links}</div>\n'
                f'    {warning}\n'
                "  </div>"
            )

    OUT.mkdir(parents=True, exist_ok=True)
    page = PAGE.format(body="\n".join(chunks), site=args.site, repo=args.repo)
    (OUT / "index.html").write_text(page, encoding="utf-8")

    # Copy the rendered artifacts up one level so the variant links resolve.
    # PDFs and DOCX are included deliberately: a reader who lands on the page
    # should be able to download the actual document without cloning the repo.
    for directory in DIST.iterdir():
        if not directory.is_dir() or directory.name == "site":
            continue
        target = OUT / directory.name
        target.mkdir(parents=True, exist_ok=True)
        for rendered in directory.glob("*.html"):
            shutil.copy2(rendered, target / rendered.name)
        for pattern in ("*.pdf", "*.docx"):
            for rendered in directory.glob(pattern):
                shutil.copy2(rendered, target / rendered.name)

    total_open = sum(v["open"] for v in variants)
    print(f"Wrote {OUT / 'index.html'} — {len(variants)} variants, "
          f"{total_open} placeholders remaining")
    return 0


if __name__ == "__main__":
    sys.exit(main())