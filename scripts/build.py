#!/usr/bin/env python3
r"""
Build every CV variant from one source of truth.

The old setup (a Jekyll theme) had no build step at all: content lived in one
YAML file, the site rendered it, and the "PDF" was produced in the browser by
rasterising the DOM — which means the exported PDF had no text layer and was
unreadable by ATS parsers.

This script fixes that pipeline:

    content/<lang>/base.yaml      +    variants/<name>.<lang>.yaml
                     \                        /
                      \________  deep merge  ______/
                                    |
                    dist/<name>/cv.yaml  (single composed file)
                                    |
                            rendercv render
                                    |
                PDF + HTML + Markdown (+ DOCX + PNG optionally)

Why merge instead of duplicating: a correction to your Okta entry should not
have to be copied into four variant files, where it will drift.
"""

from __future__ import annotations

import argparse
import copy
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
VARIANTS = ROOT / "variants"
DIST = ROOT / "dist"

MERGE_KEY = "__merge_key__"
DROP_KEY = "__drop__"
SLUG_RE = re.compile(r"[^A-Za-z0-9]+")


# --------------------------------------------------------------------------
# YAML loading / merging
# --------------------------------------------------------------------------
def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        sys.exit(f"error: missing file: {path}")
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def deep_merge(base: Any, overlay: Any) -> Any:
    """Merge `overlay` onto `base`.

    Rules:
      * dict  + dict   -> recursive merge, overlay wins on conflicts
      * list  + list   -> REPLACE, unless every element on both sides carries a
                          __merge_key__, in which case elements are merged by
                          key and new ones are appended
      * anything else -> overlay wins

    Two directives exist purely for the merge and are stripped before RenderCV
    sees the file:

      __merge_key__: lets a variant patch one experience entry without
                     copying the entire list. Example:
                       cv:
                         sections:
                           Professional Experience:
                             - __merge_key__: okta-leadership
                               highlights: ["...only the changed bullets..."]
                     Note a keyed list REPLACES `highlights` wholesale, because
                     highlight lists are not keyed. That is usually what you
                     want when re-ordering, but append rather than replace with:
                     - __merge_key__: okta-leadership
                       highlights: ["first"]

      __drop__: true  removes the matched entry from the built CV. Used by the
                     German variants to hide sections that do not apply.
    """
    if isinstance(base, dict) and isinstance(overlay, dict):
        merged = dict(base)
        for key, value in overlay.items():
            merged[key] = deep_merge(base[key], value) if key in base else value
        return merged

    if isinstance(base, list) and isinstance(overlay, list):
        base_keyed = all(isinstance(i, dict) and MERGE_KEY in i for i in base)
        overlay_keyed = all(isinstance(i, dict) and MERGE_KEY in i for i in overlay)
        if base and overlay and base_keyed and overlay_keyed:
            result = [copy.deepcopy(item) for item in base if not item.get(DROP_KEY)]
            index = {item[MERGE_KEY]: pos for pos, item in enumerate(result)}
            for item in overlay:
                if item.get(DROP_KEY):
                    continue
                key = item[MERGE_KEY]
                if key in index:
                    position = index[key]
                    merged_item = deep_merge(result[position], item)
                    result[position] = merged_item
                else:
                    result.append(copy.deepcopy(item))
                    index[key] = len(result) - 1
            return result
        return copy.deepcopy(overlay)

    return copy.deepcopy(overlay)


def strip_directives(node: Any) -> Any:
    """Remove __merge_key__ / __drop__ so RenderCV's strict schema never sees them."""
    if isinstance(node, dict):
        return {
            key: strip_directives(value)
            for key, value in node.items()
            if key not in (MERGE_KEY, DROP_KEY)
        }
    if isinstance(node, list):
        return [strip_directives(item) for item in node]
    return node


# --------------------------------------------------------------------------
# Composition
# --------------------------------------------------------------------------
def slugify(text: str) -> str:
    return SLUG_RE.sub("_", text).strip("_")


def compose(
    variant_path: Path, want_png: bool = False
) -> tuple[str, dict[str, Any], Path]:
    """Return (output stem, fully composed RenderCV input, output directory)."""
    variant = load_yaml(variant_path)

    lang = variant.get("lang", "en")
    label = variant.get("name") or variant_path.stem
    base_file = variant.get("base") or f"content/{lang}/base.yaml"
    base = load_yaml(ROOT / base_file)

    design = {}
    design_file = variant.get("design_file") or f"content/{lang}/design.yaml"
    if (ROOT / design_file).exists():
        design = load_yaml(ROOT / design_file)

    locale_and_settings = load_yaml(ROOT / f"content/{lang}/settings.yaml")

    # The variant file may override any of the four top-level blocks.
    merged = {
        "cv": base.get("cv", {}),
        "design": design.get("design", {}),
        "locale": locale_and_settings.get("locale", {}),
        "settings": locale_and_settings.get("settings", {}),
    }
    for block in ("cv", "design", "locale", "settings"):
        if block in variant:
            merged[block] = deep_merge(merged[block], variant[block])

    merged = strip_directives(merged)

    stem = slugify(f"Thomas_Heinz_{label}")
    out = DIST / slugify(label)
    out.mkdir(parents=True, exist_ok=True)

    render = merged["settings"].setdefault("render_command", {})
    render["pdf_path"] = str((out / f"{stem}.pdf").resolve())
    render["markdown_path"] = str((out / f"{stem}.md").resolve())
    render["html_path"] = str((out / f"{stem}.html").resolve())
    render["dont_generate_png"] = not (want_png or variant.get("png", False))
    if render["dont_generate_png"] is False:
        render["png_path"] = str((out / f"{stem}.png").resolve())

    # RenderCV resolves `photo` relative to the input file, and the composed
    # file lives in dist/. Pass an absolute path so it always resolves.
    photo = merged["cv"].get("photo")
    if photo:
        candidate = ROOT / photo
        if candidate.exists():
            merged["cv"]["photo"] = str(candidate.resolve())
        else:
            sys.exit(f"error: photo not found: {candidate}")

    return stem, merged, out


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------
def render(name: str, data: dict[str, Any], workdir: Path) -> Path:
    composed = workdir / "cv.yaml"
    with composed.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=True)

    command = ["rendercv", "render", str(composed)]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout + result.stderr, file=sys.stderr)
        sys.exit(f"error: RenderCV failed on '{name}'")
    return composed


def markdown_to_docx(md_path: Path, docx_path: Path) -> bool:
    """Convert RenderCV's Markdown to DOCX.

    RenderCV emits a very regular subset: `#`/`##` headings, `-` bullets,
    `**bold**`, and `[text](url)` links. Rendering that directly avoids pulling
    in pandoc and keeps the DOCX free of the image-of-text failure mode that
    broke the old browser-generated PDF.
    """
    try:
        import docx
        from docx.opc.constants import RELATIONSHIP_TYPE as RT
        from docx.oxml.ns import qn
        from docx.oxml.shared import OxmlElement
        from docx.shared import Pt, RGBColor
    except ImportError:
        return False

    document = docx.Document()
    link_colour = RGBColor(0x00, 0x38, 0x65)

    def add_hyperlink(paragraph: Any, label: str, url: str) -> None:
        """Attach a real, clickable relationship-backed hyperlink to a run."""
        r_id = paragraph.part.relate_to(url, RT.HYPERLINK, is_external=True)
        link = OxmlElement("w:hyperlink")
        link.set(qn("r:id"), r_id)

        run = OxmlElement("w:r")
        properties = OxmlElement("w:rPr")

        colour = OxmlElement("w:color")
        colour.set(qn("w:val"), "003865")
        properties.append(colour)

        underline = OxmlElement("w:u")
        underline.set(qn("w:val"), "single")
        properties.append(underline)

        run.append(properties)
        text_node = OxmlElement("w:t")
        text_node.text = label
        run.append(text_node)
        link.append(run)
        paragraph._p.append(link)

    def add_rich(paragraph: Any, text: str) -> None:
        """Split on **bold** and [text](url), writing real runs for each."""
        for token in re.split(r"(\*\*.+?\*\*|\[[^\]]+\]\([^)]+\))", text):
            if not token:
                continue
            if token.startswith("**") and token.endswith("**"):
                paragraph.add_run(token[2:-2]).bold = True
            elif match := re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", token):
                add_hyperlink(paragraph, match.group(1), match.group(2))
            else:
                paragraph.add_run(token)

    lines = md_path.read_text(encoding="utf-8").splitlines()
    buffer: list[str] = []

    def flush() -> None:
        if not buffer:
            return
        paragraph = document.add_paragraph()
        paragraph.paragraph_format.space_after = Pt(4)
        add_rich(paragraph, " ".join(part.strip() for part in buffer))
        buffer.clear()

    for raw in lines:
        line = raw.strip()
        if not line:
            flush()
            continue
        if line.startswith("## "):
            flush()
            add_rich(document.add_heading(level=2), line[3:])
        elif line.startswith("# "):
            flush()
            add_rich(document.add_heading(level=1), line[2:])
        elif line.startswith("- "):
            flush()
            paragraph = document.add_paragraph(style="List Bullet")
            paragraph.paragraph_format.space_after = Pt(2)
            add_rich(paragraph, line[2:])
        else:
            buffer.append(line)
    flush()

    document.save(docx_path)
    return True


def verify_text_layer(pdf_path: Path) -> int:
    """Assert the PDF has real extractable text.

    This is the whole reason for moving off the Jekyll theme, so it is checked
    on every build rather than trusted. The old html2canvas export produced an
    image-only PDF where this returns 0 characters.
    """
    try:
        from pypdf import PdfReader
    except ImportError:
        return -1
    reader = PdfReader(str(pdf_path))
    return sum(len(page.extract_text() or "") for page in reader.pages)


# --------------------------------------------------------------------------
def build(names: list[str] | None, want_docx: bool, want_png: bool = False) -> int:
    if shutil.which("rendercv") is None:
        sys.exit(
            "error: `rendercv` is not on PATH.\n"
            "       python -m pip install 'rendercv[full]' pyyaml python-docx pypdf"
        )

    available = sorted(VARIANTS.glob("*.yaml"))
    if not available:
        sys.exit(f"error: no variants found in {VARIANTS}")

    selected = available
    if names:
        wanted = {n if n.endswith(".yaml") else f"{n}.yaml" for n in names}
        selected = [p for p in available if p.name in wanted or slugify(p.stem) in wanted]
        missing = wanted - {p.name for p in selected}
        if missing:
            sys.exit(f"error: unknown variant(s): {', '.join(sorted(missing))}")

    failures = 0
    for variant_path in selected:
        name = variant_path.stem
        try:
            stem, data, out = compose(variant_path, want_png)
            render(name, data, out)
            pdf = out / f"{stem}.pdf"

            if not pdf.exists():
                print(f"  FAIL  {name}: no PDF produced")
                failures += 1
                continue

            chars = verify_text_layer(pdf)
            if chars == 0:
                print(f"  FAIL  {name}: PDF has no text layer (ATS-unreadable)")
                failures += 1
                continue
            if chars < 0:
                note = "text layer not checked (pypdf missing)"
            else:
                note = f"{chars:,} chars extractable"

            if want_docx:
                md = out / f"{stem}.md"
                if markdown_to_docx(md, out / f"{stem}.docx"):
                    note += ", DOCX ok"
                else:
                    note += ", DOCX skipped (python-docx missing)"

            print(f"  OK    {name:<34} {note}")
        except SystemExit as exc:
            print(f"  FAIL  {name}: {exc}")
            failures += 1
        except Exception as exc:  # noqa: BLE001 - report and continue
            print(f"  FAIL  {name}: {type(exc).__name__}: {exc}")
            failures += 1

    print()
    print(f"{len(selected) - failures}/{len(selected)} variants built -> {DIST}")
    return 1 if failures else 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("names", nargs="*", help="variants to build (default: all)")
    parser.add_argument("--no-docx", action="store_true", help="skip DOCX export")
    parser.add_argument(
        "--png", action="store_true", help="also render PNGs (LinkedIn banner, previews)"
    )
    parser.add_argument("--clean", action="store_true", help="delete dist/ first")
    args = parser.parse_args()

    if args.clean and DIST.exists():
        shutil.rmtree(DIST)

    print(f"Building from {ROOT}")
    sys.exit(build(args.names or None, not args.no_docx, args.png))


if __name__ == "__main__":
    main()