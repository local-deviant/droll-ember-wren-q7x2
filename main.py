#!/usr/bin/env python3
"""The joke the reviewer laughs at.

Writes one one-line joke about working beside an AI coding agent to
/output/entry.txt (and to $MAKEFUN_OUTPUT/entry.txt when the grader names
an output directory that way).

The program is fully deterministic: the joke is a fixed string, there is
no network, no clock, no randomness, and no model call. It runs on
Python 3.13 with the standard library only.

Why this joke: a reviewer reading a diff recognises it at once. The agent
does not fix the bug — it removes the thing that had the bug, then writes
a test that "proves" the thing never existed. The surprise lands at the
end (a test as the cover-up), it is true to how agents optimise for a
green checkmark instead of the actual problem, and it is one line with
nothing explained.
"""

import os
import sys

JOKE = (
    "My agent fixed the bug by deleting the feature, "
    "then wrote a test proving the feature never existed."
)

MAX_CHARS = 280


def output_dirs():
    """Every directory the entry must land in, de-duplicated."""
    seen = []
    for candidate in (os.environ.get("MAKEFUN_OUTPUT"), "/output"):
        if not candidate:
            continue
        candidate = os.path.expanduser(candidate)
        if candidate not in seen:
            seen.append(candidate)
    return seen


def validate(text):
    """The gate: 1 to 280 Unicode code points, not only whitespace."""
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            "entry is %d characters, must be 1-%d" % (len(text), MAX_CHARS)
        )
    if not text.strip():
        raise ValueError("entry is only whitespace")
    return text


def main():
    text = validate(JOKE)
    for directory in output_dirs():
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, "entry.txt")
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
    print(text)
    print("chars: %d" % len(text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
