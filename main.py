"""Dumbest Thing My Agent Did Today - one-line entry builder.

Reads the incident line, replays the gate (1..200 chars, single line,
no blank) and emits the artifact to the output directory.
"""
import json
import os
import sys

CAP = 200
FILE_NAME = "entry.txt"

ENTRY_LINE = "Today my agent squashed eleven commits into one called 'stuff', force-pushed to main, then opened an incident ticket asking who had force-pushed to main."


def guard(line):
    if not line.strip():
        sys.exit("gate: blank line")
    if len(line) > CAP:
        sys.exit("gate: %d chars over cap %d" % (len(line), CAP))
    for ch in "\n\r":
        if ch in line:
            sys.exit("gate: newline inside line")
    if "  " in line:
        sys.exit("gate: double space found")
    return len(line)


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, FILE_NAME), encoding="utf-8") as fh:
        body = fh.read().strip()
    if body != ENTRY_LINE:
        sys.exit("gate: entry.txt drifted from builder")
    size = guard(ENTRY_LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, FILE_NAME)
    with open(dest, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(ENTRY_LINE + "\n")
    print(json.dumps({"path": dest, "len": size, "cap": CAP}))


if __name__ == "__main__":
    main()
