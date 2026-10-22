"""Print the clips that may be used today (none used in the last 30 days, by group).

Usage: python3 eligible.py YYYY-MM-DD [--tag TAG]
Prints one line per allowed clip: id | name | tags. Last line: COUNT <n>.
--tag limits the list to clips with that tag (coffee, writing, laptop, phone, rest, reading,
candle, flowers, food, time, making, workspace). Also prints TAGS: how many allowed clips each tag has.
Also: python3 eligible.py YYYY-MM-DD --check ID [ID ...]  -> prints OK or BLOCKED <id> and exits 1.
"""
import json, sys, datetime, os
here = os.path.dirname(os.path.abspath(__file__))
clips = json.load(open(os.path.join(here, "clips.json")))["clips"]
log = json.load(open(os.path.join(here, "log.json")))["log"]
today = datetime.date.fromisoformat(sys.argv[1])
group = {c["id"]: c["group"] for c in clips}
blocked = set()
for e in log:
    if (today - datetime.date.fromisoformat(e["date"])).days < 30:
        for i in e["clips"]:
            blocked.add(group.get(i, i))
if "--check" in sys.argv:
    bad = [i for i in sys.argv[sys.argv.index("--check") + 1:] if group.get(i, i) in blocked or i not in group]
    print("OK" if not bad else "BLOCKED " + " ".join(bad)); sys.exit(1 if bad else 0)
ok = [c for c in clips if c["group"] not in blocked]
from collections import Counter
print("TAGS", dict(Counter(x for c in ok for x in c.get("tags", []))))
if "--tag" in sys.argv:
    tag = sys.argv[sys.argv.index("--tag") + 1]
    ok = [c for c in ok if tag in c.get("tags", [])]
for c in ok:
    print(c["id"], "|", c["name"], "|", ",".join(c.get("tags", [])))
print("COUNT", len(ok))
