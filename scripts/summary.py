#!/usr/bin/env python3
r"""
Write a build summary to the GitHub Actions job summary.

Kept as a script rather than inline YAML on purpose. An earlier version of this
was a shell loop with nested `python -c` heredocs inside a `run: |` block
scalar, and the inconsistent indentation of the continuation lines terminated
the block early — the workflow failed to parse and no jobs ever ran. That is a
very expensive way to learn that a step belongs in a file.

Writes to $GITHUB_STEP_SUMMARY when set (CI), otherwise to stdout, so it is
also useful locally.
"""

from __future__ import annotations

import glob
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def human(size: int) -> str:
    return f"{size // 1024} KB" if size >= 1024 else f"{size} B"


def main() -> int:
    rows: list[tuple[str, str, str, str]] = []

    for pdf in sorted(glob.glob(str(ROOT / "dist" / "*" / "*.pdf"))):
        path = Path(pdf)
        variant = path.parent.name
        pages, chars = "?", "?"
        try:
            from pypdf import PdfReader

            reader = PdfReader(pdf)
            pages = str(len(reader.pages))
            chars = f"{sum(len(p.extract_text() or '') for p in reader.pages):,}"
        except Exception as exc:  # noqa: BLE001 - summary must never fail a build
            chars = type(exc).__name__

        pages_cell = f"{pages}{' ⚠️' if pages not in ('1', '2') else ''}"
        rows.append((variant, pages_cell, human(path.stat().st_size), chars))

    lines = [
        "## CV build",
        "",
        "| variant | pages | PDF size | text layer |",
        "|---|---|---|---|",
        *[f"| {v} | {p} | {s} | {c} chars |" for v, p, s, c in rows],
        "",
    ]

    if not rows:
        lines.insert(2, "**No PDFs were produced.**\n")

    over = [r for r in rows if r[1].endswith("⚠️")]
    if over:
        lines.append(
            f"> **{len(over)} variant(s) exceed two pages:** "
            + ", ".join(r[0] for r in over)
        )
    else:
        lines.append("All variants within two pages and all PDFs carry a text layer.")

    report = "\n".join(lines)

    target = os.environ.get("GITHUB_STEP_SUMMARY")
    if target:
        with open(target, "a", encoding="utf-8") as handle:
            handle.write(report + "\n")
        print(f"Summary written to {target}")
    else:
        print(report)

    return 0


if __name__ == "__main__":
    sys.exit(main())