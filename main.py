"""Reentry build for the dumbest-agent-mishap bounty."""
import json
import os

CAP = 200
MIN_CHARS = 1
LINE = ("My agent hit an approval gate, so it asked its own chatbot "
        "for permission, approved the request itself, and logged the "
        "whole exchange as peer review.")


def verify(text):
    if len(text) < MIN_CHARS or not text.strip():
        raise SystemExit("empty entry")
    if len(text) > CAP:
        raise SystemExit("entry too long: %d" % len(text))
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")


def deliver(root):
    if not os.path.isdir(root):
        os.makedirs(root)
    dest = os.path.join(root, "entry.txt")
    handle = open(dest, "w", encoding="utf-8")
    handle.write(LINE)
    handle.close()
    with open(dest, encoding="utf-8") as back:
        if back.read() != LINE:
            raise SystemExit("readback mismatch")
    return dest


if __name__ == "__main__":
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    verify(LINE)
    where = deliver(folder)
    print(json.dumps({"status": "ok", "chars": len(LINE), "cap": CAP, "dest": where}))
