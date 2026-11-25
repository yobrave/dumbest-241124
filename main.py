"""Dumbest Thing Your Agent Did Today: one-line entry exporter."""
import os
import pathlib
import sys

GATE_MAX = 200
ENTRY = pathlib.Path(__file__).resolve().parent / "entry.txt"
TAG = "dmb4-dumbest-r4"


def main():
    line = ENTRY.read_text(encoding="utf-8").strip()
    if len(line) < 1 or len(line) > GATE_MAX:
        sys.exit("gate: length out of range")
    outdir = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "entry.txt").write_text(line + "\n", encoding="utf-8", newline="\n")
    print('{"status":"pass","tag":"%s","len":%d,"max":%d}' % (TAG, len(line), GATE_MAX))


main()
