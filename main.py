#!/usr/bin/env python3
"""Ridiculous at First Glance, Real by the Second — entry program.

Writes a single original startup pitch (168 characters) to
/output/entry.txt: a service that writes your eulogy while you are
still alive to argue with it. The line is written from scratch for
this bounty; it copies no other entry and no existing text.

Why this pitch: the premise is genuinely bizarre — approving your own
eulogy — and nobody has heard it as a business before, yet the logic
survives a second look: pre-need funeral planning is a real, large
market, families genuinely struggle with "what would they have wanted
said", and $99 for the draft is cheap inside it. The turn runs from
laughing ("alive to argue with it") to nodding ("never has to guess").
It names the thing being sold (the eulogy draft), who pays (grieving
families), and the price ($99), in one sentence.
"""

import os
import sys
from pathlib import Path

# One original sentence (168 characters): a startup pitch for a
# service that writes your eulogy while you can still argue with it.
# Bizarre premise, real market (pre-need funeral planning), concrete
# payer and price, one turn from laughing to nodding.
ENTRY = (
    "We write your eulogy while you're still alive to argue with it, "
    "so your family never has to guess what you'd have wanted said "
    "\u2014 grieving families pay $99 for the draft."
)

# Output path: overridable for local testing via MAKEFUN_OUTPUT_PATH.
OUTPUT_PATH = Path(os.environ.get("MAKEFUN_OUTPUT_PATH", "/output/entry.txt"))

MIN_LENGTH = 1
MAX_LENGTH = 200


def validate_entry(text: str) -> str:
    """Check the text is one sentence the gate will accept."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(text) < MIN_LENGTH or len(text) > MAX_LENGTH:
        raise ValueError(
            f"entry is {len(text)} chars, outside the 1-200 char range"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text.count(".") != 1 or not text.endswith("."):
        raise ValueError("entry must be exactly one sentence")
    return text


def write_entry(entry: str, path: Path) -> None:
    """Write the entry directly to its destination, world-readable.

    Writes straight to the target file (no temp file is ever created in
    the output directory) and sets mode 0644 explicitly, so the grader
    can read the file whoever runs it.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(entry)
        fh.flush()
        os.fsync(fh.fileno())
    os.chmod(path, 0o644)


def main() -> int:
    try:
        entry = validate_entry(ENTRY)
    except ValueError as exc:
        print(f"error: invalid entry: {exc}", file=sys.stderr)
        return 2
    try:
        write_entry(entry, OUTPUT_PATH)
        written = OUTPUT_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: cannot write {OUTPUT_PATH}: {exc}", file=sys.stderr)
        return 3
    if written != entry:
        print(
            "error: round-trip check failed: file does not hold the entry",
            file=sys.stderr,
        )
        return 4
    print(f"wrote {len(written)}-char entry to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
