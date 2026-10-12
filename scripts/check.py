#!/usr/bin/env python3
r"""
Pre-commit sanity check. Fast — no rendering, no network.

Catches the mistakes that are expensive to discover late:

  * YAML that does not parse (including the "bare [ADD: ...] opens a flow
    sequence" trap, which is the most common mistake in this repo)
  * A variant whose __merge_key__ does not exist in the base content, which
    would silently do nothing instead of failing
  * __merge_key__ collisions, which would make merges ambiguous
  * A missing or oversized photo
  * Leftover placeholders, reported as a count per variant

Run:  python scripts/check.py        (or: make check)
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
VARIANTS = ROOT / "variants"
MERGE_KEY = "__merge_key__"
PHOTO_MAX_BYTES = 4 * 1024 * 1024

errors: list[str] = []
warnings: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def warn(message: str) -> None:
    warnings.append(message)


def load(path: Path):
    try:
        with path.open(encoding="utf-8") as handle:
            return yaml.safe_load(handle)
    except yaml.YAMLError as exc:
        fail(f"{path.relative_to(ROOT)}: YAML parse error — {exc}")
        return None


def collect_keys(node, found: list[str]) -> None:
    if isinstance(node, dict):
        if MERGE_KEY in node:
            found.append(str(node[MERGE_KEY]))
        for value in node.values():
            collect_keys(value, found)
    elif isinstance(node, list):
        for item in node:
            collect_keys(item, found)


def count_placeholders(node) -> int:
    if isinstance(node, dict):
        return sum(count_placeholders(v) for v in node.values())
    if isinstance(node, list):
        return sum(count_placeholders(v) for v in node)
    if isinstance(node, str):
        return node.count("[ADD") + node.count("[RESOLVE")
    return 0


def main() -> int:
    # ---- content -----------------------------------------------------------
    base_keys: dict[str, list[str]] = {}
    for base in sorted(CONTENT.glob("*/base.yaml")):
        data = load(base)
        if data is None:
            continue
        keys: list[str] = []
        collect_keys(data.get("cv", {}), keys)
        duplicates = {k for k in keys if keys.count(k) > 1}
        if duplicates:
            fail(f"{base.relative_to(ROOT)}: duplicate {MERGE_KEY}: {sorted(duplicates)}")
        base_keys[base.parent.name] = keys
        print(f"  {base.relative_to(ROOT)}: {len(keys)} keyed entries, "
              f"{count_placeholders(data)} placeholders")

    # ---- photo -------------------------------------------------------------
    photo = ROOT / "assets" / "thomas.png"
    if not photo.exists():
        fail("assets/thomas.png is missing — the CV header needs it")
    elif photo.stat().st_size > PHOTO_MAX_BYTES:
        warn(f"assets/thomas.png is {photo.stat().st_size // 1024} KB; "
             "keep it well under 4 MB so the PDF stays small")

    # ---- variants ----------------------------------------------------------
    for variant_path in sorted(VARIANTS.glob("*.yaml")):
        variant = load(variant_path)
        if variant is None:
            continue
        lang = variant.get("lang", "en")
        if lang not in base_keys:
            fail(f"{variant_path.relative_to(ROOT)}: lang '{lang}' has no "
                 f"content/{lang}/base.yaml")
            continue

        keys: list[str] = []
        collect_keys(variant.get("cv", {}), keys)
        unknown = [k for k in keys if k not in base_keys[lang]]
        if unknown:
            fail(f"{variant_path.relative_to(ROOT)}: {MERGE_KEY} not present in "
                 f"content/{lang}/base.yaml: {sorted(set(unknown))} "
                 "(this overlay would silently do nothing)")

        design_file = ROOT / f"content/{lang}/design.yaml"
        if not design_file.exists():
            warn(f"content/{lang}/design.yaml missing — the {lang} build will "
                 "fall back to RenderCV defaults")

        print(f"  {variant_path.relative_to(ROOT)}: {len(keys)} patched entries, "
              f"{count_placeholders(variant)} placeholders")

    # ---- workflow ---------------------------------------------------------
    # A workflow that does not parse fails at run time with "0 jobs", which
    # looks like a platform outage and costs a slow debugging round trip. An
    # earlier version of build.yml had this exact bug: a `run: |` block scalar
    # whose continuation lines were under-indented, which silently terminated
    # the block and made the rest of the file unparseable.
    for workflow in sorted((ROOT / ".github" / "workflows").glob("*.y*ml")):
        if load(workflow) is not None:
            print(f"  {workflow.relative_to(ROOT)}: parses")

    # ---- report ------------------------------------------------------------
    for message in warnings:
        print(f"  warning: {message}")
    for message in errors:
        print(f"  ERROR:   {message}")

    if errors:
        print(f"\n{len(errors)} error(s).")
        return 1
    print("\nNo structural errors.")
    return 0


if __name__ == "__main__":
    sys.exit(main())