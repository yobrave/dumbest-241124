import json
import os

INCIDENT_CAP = 200


def incident():
    home = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(home, "entry.txt"), "rb") as handle:
        blob = handle.read()
    text = blob.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    rows = [row.strip() for row in text.split(b"\n") if row.strip()]
    payload = rows[0] if rows else b""
    line = payload.decode("utf-8")
    assert 1 <= len(line) <= INCIDENT_CAP, "mishap line is %d chars, cap %d" % (len(line), INCIDENT_CAP)
    drop_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    os.makedirs(drop_dir, exist_ok=True)
    drop = os.path.join(drop_dir, "entry.txt")
    with open(drop, "wb") as handle:
        handle.write(payload)
    with open(drop, "rb") as handle:
        assert handle.read() == payload, "the readback bytes moved"
    print(json.dumps({"pass": True, "n": len(line), "drop": drop}))


if __name__ == "__main__":
    incident()
