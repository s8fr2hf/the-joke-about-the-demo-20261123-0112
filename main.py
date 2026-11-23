#!/usr/bin/env python3
"""Write the demo joke to the output directory.

Reads ``entry.txt`` sitting next to this script, validates it (UTF-8,
one line, 1-280 Unicode code points, not only whitespace), and writes it
to ``$MAKEFUN_OUTPUT_DIR/entry.txt`` (default ``/output``).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

MAX_CODE_POINTS = 280


def fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 1


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    source = script_dir / "entry.txt"
    try:
        text = source.read_text(encoding="utf-8")
    except FileNotFoundError:
        return fail(f"{source} not found")
    except UnicodeDecodeError:
        return fail("entry.txt is not valid UTF-8")

    joke = text[:-1] if text.endswith("\n") else text

    if not joke or joke.isspace():
        return fail("entry.txt is empty or only whitespace")
    if "\n" in joke or "\r" in joke:
        return fail("entry.txt must be exactly one line")
    if any(ord(ch) < 0x20 and ch not in "\t" for ch in joke):
        return fail("entry.txt contains a control character")
    if len(joke) > MAX_CODE_POINTS:
        return fail(
            f"entry.txt is {len(joke)} code points, over the "
            f"{MAX_CODE_POINTS} limit"
        )

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    if not out_dir.is_absolute():
        # A relative output dir is resolved against the script's
        # directory, never the caller's working directory.
        out_dir = script_dir / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "entry.txt").write_text(joke, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
