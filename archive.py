"""The archive of HelioField imagery: one day per Carrington rotation, kept
when it ages out of the daily site.

    python archive.py --out site

For each day of the daily site (sr-dash/heliofield-imagery) older than its
60-day window, of a rotation the archive does not hold yet, the day's images
and index are copied from that site's public files into site/days/<date>.
site/index.json lists the archived days and their rotations; the daily site
reads it to know which days are served from here, and lets those go.
Prints changed=true or changed=false (for the workflow).
"""

import argparse
import json
import time
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

RECENT = "https://sr-dash.github.io/heliofield-imagery/"
KEEP_DAYS = 60
UA = {"User-Agent": "heliofield-imagery-archive"}


def get(url: str) -> bytes:
    req = urllib.request.Request(f"{url}{'&' if '?' in url else '?'}t={int(time.time())}", headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=Path("site"))
    a = ap.parse_args()
    days_dir = a.out / "days"
    days_dir.mkdir(parents=True, exist_ok=True)
    idx_path = a.out / "index.json"
    idx = json.loads(idx_path.read_text()) if idx_path.exists() else {"dates": [], "cr": {}}
    recent = json.loads(get(RECENT + "index.json"))
    here = set(recent["dates"]) - set(recent.get("archived", []))
    cutoff = (date.fromisoformat(max(here)) - timedelta(days=KEEP_DAYS)).isoformat()
    held = set(idx["cr"].values())
    added = []
    for d in sorted(x for x in here if x < cutoff):
        day = json.loads(get(RECENT + f"days/{d}/index.json"))
        cr = day.get("cr")
        if cr is None or cr in held or d in idx["dates"]:
            continue
        out = days_dir / d
        out.mkdir(exist_ok=True)
        for p in day["panels"]:
            for f in p["files"].values():
                if f:
                    (out / f).write_bytes(get(RECENT + f"days/{d}/{f}"))
        (out / "index.json").write_text(json.dumps(day, indent=1))
        idx["dates"].append(d)
        idx["cr"][d] = cr
        held.add(cr)
        added.append(d)
        print(f"archived {d} (CR {cr})")
    if added:
        idx["dates"] = sorted(idx["dates"])
        idx["updated"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        idx["about"] = ("One day per Carrington rotation of HelioField imagery, kept when it ages out of the daily site "
                        "(https://sr-dash.github.io/heliofield-imagery/). Panels, files and credits as there.")
        idx_path.write_text(json.dumps(idx, indent=1))
    (a.out / ".nojekyll").write_text("")
    print(f"{len(added)} day(s) added; {len(idx['dates'])} in the archive")
    print(f"changed={'true' if added else 'false'}")


if __name__ == "__main__":
    main()
