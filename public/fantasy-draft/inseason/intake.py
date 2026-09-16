#!/usr/bin/env python3
"""Turn a transcribed screenshot into a roster or waiver file the weekly engine can read.

You paste names, one per line, exactly as they read on the ESPN page. This resolves each one
against data/players.json with the same forgiving match the draft app uses ("J. Chase",
"Gibbs", "Ja'Marr Chase / CIN WR" all land), writes a small JSON, and shouts about anything
it could not place so a transcription slip never becomes a silent wrong recommendation.

    python3 intake.py roster  < roster.txt   > roster.json
    python3 intake.py waivers < waivers.txt  > waivers.json

Roster lines may carry a slot prefix so the engine knows your current lineup:
    QB  Justin Herbert
    RB  Chase Brown
    FLEX DeVonta Smith
    BE  Rome Odunze
Lines without a prefix are treated as bench. K and D/ST are kept as-is (they are outside the
scored player pool); write them as "K Harrison Butker" or "DST Steelers".
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAYERS = HERE.parent / "data" / "players.json"
SLOTS = {"QB", "RB", "WR", "TE", "FLEX", "BE", "BN", "IR", "K", "DST", "D/ST"}


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    s = s.lower().replace("'", "").replace(".", "").replace("-", " ")
    s = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b", "", s)
    return re.sub(r"[^a-z0-9 ]", " ", s).strip()


WEEKLY = HERE.parent / "data" / "weekly_2026.json"


def load_players():
    """The draft model's 253 players, plus everyone nflverse has a 2026 stat line or injury row
    for. Waiver-wire breakouts are usually rookies and backups the draft model never scored;
    they still resolve here so the weekly engine can project them from this season's usage."""
    data = json.load(open(PLAYERS))
    players = list(data["players"] if isinstance(data, dict) else data)
    seen = {norm(p["name"]) + "|" + p["pos"] for p in players}
    if WEEKLY.exists():
        wk = json.load(open(WEEKLY))
        for g, p in wk.get("players", {}).items():
            key = norm(p["name"]) + "|" + p["pos"]
            if key in seen or p["pos"] not in ("QB", "RB", "WR", "TE"):
                continue
            seen.add(key)
            players.append({"id": "gsis:" + g, "name": p["name"], "pos": p["pos"], "team": p.get("team"),
                            "bye": None, "comp": 999 + len(players)})
    return players


def clean_line(line):
    """Strip bullets, pick numbers, '(DET RB)' tails and 'Name / TEAM POS' tails."""
    s = re.sub(r"^[\s*•\-–]+", " ", line)
    s = s.split("/")[0]
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"^\s*(?:r?\d+\s*[.):\-]?\s*)+", " ", s, flags=re.I)
    return s.strip()


def hit(p, toks):
    """Every token of the player's name must be claimed by a DIFFERENT typed token.

    One-to-one matters: with 'B. Hall' the initial 'b' must not be allowed to satisfy both
    'brock' and 'bowers'. Longer name tokens are matched first so an initial is spent on the
    surname-shaped word last, not first.
    """
    nt = sorted((t for t in norm(p["name"]).split() if t), key=len, reverse=True)
    pool = list(toks)
    for w in nt:
        found = None
        for i, t in enumerate(pool):
            if t == w or (len(t) > 1 and (w.startswith(t) or t.startswith(w))) or (len(t) == 1 and w.startswith(t)):
                found = i
                break
        if found is None:
            return False
        pool.pop(found)
    return True


def match(name, players, slot=None):
    q = norm(clean_line(name))
    toks = [t for t in q.split() if t]
    if not toks:
        return None, []
    exact = [p for p in players if norm(p["name"]) == q]
    if exact:
        return exact[0], []
    cands = [p for p in players if hit(p, toks)]
    if not cands:
        cands = [p for p in players if q in norm(p["name"])]
    # a line filed under RB / WR / TE / QB almost certainly is one; prefer that position
    if slot in ("QB", "RB", "WR", "TE"):
        same = [p for p in cands if p["pos"] == slot]
        if same:
            cands = same
    cands.sort(key=lambda p: p["comp"])
    return (cands[0] if cands else None), cands[1:4]


def parse(lines, players):
    out, problems = [], []
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        slot, rest = None, line
        head = line.split(None, 1)
        if head and head[0].upper().replace("/", "") in {s.replace("/", "") for s in SLOTS} and len(head) > 1:
            slot, rest = head[0].upper().replace("D/ST", "DST"), head[1]
        if slot in ("K", "DST"):
            out.append({"name": rest.strip(), "pos": slot, "slot": slot, "id": None, "team": None, "bye": None})
            continue
        p, alts = match(rest, players, slot)
        if not p:
            problems.append(f"NO MATCH: {raw.strip()!r}")
            continue
        entry = {"id": p["id"], "name": p["name"], "pos": p["pos"], "team": p["team"], "bye": p["bye"],
                 "slot": slot or "BE", "as_typed": rest.strip()}
        if alts and norm(p["name"]) != norm(clean_line(rest)):
            entry["alternatives"] = [a["name"] for a in alts]
        out.append(entry)
    return out, problems


def main():
    kind = sys.argv[1] if len(sys.argv) > 1 else "roster"
    players = load_players()
    entries, problems = parse(sys.stdin.read().splitlines(), players)
    seen, dupes = set(), []
    for e in entries:
        key = e["id"] or e["name"]
        if key in seen:
            dupes.append(e["name"])
        seen.add(key)
    result = {"kind": kind, "count": len(entries), "players": entries}
    json.dump(result, sys.stdout, indent=1)
    print(file=sys.stdout)
    for pr in problems:
        print("!! " + pr, file=sys.stderr)
    for d in dupes:
        print("!! DUPLICATE: " + d, file=sys.stderr)
    ambiguous = [e for e in entries if e.get("alternatives")]
    for e in ambiguous:
        print(f"?? {e['as_typed']!r} -> {e['name']}  (could also be: {', '.join(e['alternatives'])})", file=sys.stderr)
    if problems:
        sys.exit(2)


if __name__ == "__main__":
    main()
