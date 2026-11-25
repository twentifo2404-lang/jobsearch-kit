#!/usr/bin/env python3
"""Shared job-application registry for every agent (Claude, Codex, ...) and the user.

Single source of truth: application_log.csv. Short-lived claims (so two agents
don't apply to the same job at once): claims.csv.

Usage
  python3 jobs.py check <link-or-text> [--employer E --role R]
      exit 0 = CLEAR, 1 = already in log, 2 = claimed by another agent right now,
      3 = possible duplicate (same employer / similar role)
  python3 jobs.py claim <link> --employer E --role R --agent claude|codex
      run right BEFORE opening the application form; fails (non-zero) if not clear
  python3 jobs.py log --agent A --employer E --role R --location L --link URL --cv CV --status S [--notes N]
      run right AFTER submitting (or skipping); also releases the claim
  python3 jobs.py release <link> --agent A      give up a claim without logging
  python3 jobs.py claims                         list active claims
  python3 jobs.py recent [N]                     show the last N log rows (default 15)
  python3 jobs.py candidates                     list the extra candidates set up here

Claims older than 3 hours are treated as expired.

Candidates
  Leave out --candidate (or pass --candidate me) for the main person: their log
  lives in this folder. For anyone else sharing this folder (a partner, a sibling),
  pass --candidate <name>: their files live in candidates/<name>/ and are created
  on first use. Duplicate checks only look at the chosen candidate's log, so two
  people can apply to the same job.
"""
import argparse, csv, datetime as dt, os, re, sys
from contextlib import contextmanager

try:  # macOS / Linux
    import fcntl

    def _lock(fh):
        fcntl.flock(fh, fcntl.LOCK_EX)

    def _unlock(fh):
        fcntl.flock(fh, fcntl.LOCK_UN)
except ImportError:  # Windows
    import msvcrt

    def _lock(fh):
        fh.seek(0)
        msvcrt.locking(fh.fileno(), msvcrt.LK_LOCK, 1)  # retries for ~10 s, then raises

    def _unlock(fh):
        fh.seek(0)
        msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 1)

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CANDIDATE = "me"
LOG = os.path.join(HERE, "application_log.csv")
CLAIMS = os.path.join(HERE, "claims.csv")
LOCK = os.path.join(HERE, ".jobs.lock")
LOG_HEADER = ["date", "employer", "role", "location", "link", "cv_used", "status", "notes", "agent"]
CLAIM_HEADER = ["claimed_at", "agent", "key", "employer", "role", "link"]
CLAIM_TTL = dt.timedelta(hours=3)


def candidate_dir(name):
    if name == DEFAULT_CANDIDATE:
        return HERE
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,30}", name):
        sys.exit(f"bad --candidate '{name}': use lowercase letters, digits, - or _")
    return os.path.join(HERE, "candidates", name)


def use_candidate(name):
    global LOG, CLAIMS
    d = candidate_dir(name)
    LOG, CLAIMS = os.path.join(d, "application_log.csv"), os.path.join(d, "claims.csv")
    os.makedirs(d, exist_ok=True)
    if not os.path.exists(LOG):
        with open(LOG, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(LOG_HEADER)


# Words ignored when comparing employer names (company suffixes, filler).
STOP = {"sdn", "bhd", "berhad", "m", "the", "co", "company", "group", "of", "limited", "ltd", "llc", "gmbh",
        "inc", "corp", "corporation", "plc", "pte", "pty", "services", "service", "sb", "and", "malaysia",
        "singapore", "international", "holdings"}
# Words ignored when comparing role titles.
ROLE_STOP = {"the", "and", "of", "a", "an", "for", "in", "with", "to", "fresh", "grad", "graduate", "junior",
             "jr", "immediate", "vacancy", "urgent", "hiring", "position", "role", "remote", "hybrid"}


def now():
    return dt.datetime.now().replace(microsecond=0)


@contextmanager
def locked():
    with open(LOCK, "w") as fh:
        _lock(fh)
        try:
            yield
        finally:
            _unlock(fh)


def job_keys(text):
    """Stable IDs found in a link or free text."""
    t = text or ""
    keys = set()
    for m in re.finditer(r"jobstreet\.com(?:\.[a-z]{2})?/(?:[a-z-]+/)*job/(\d+)", t):
        keys.add("jobstreet:" + m.group(1))
    for m in re.finditer(r"linkedin\.com/jobs/view/(?:[^/\s]*-)?(\d{8,})", t):
        keys.add("linkedin:" + m.group(1))
    for m in re.finditer(r"currentJobId=(\d{8,})", t):
        keys.add("linkedin:" + m.group(1))
    for m in re.finditer(r"indeed\.com/\S*?jk=([0-9a-f]{16})", t):
        keys.add("indeed:" + m.group(1))
    for m in re.finditer(r"\b(JR\d{6,})\b", t, re.I):
        keys.add("workday:" + m.group(1).upper())
    for m in re.finditer(r"oraclecloud\.com/.*?/job/(\d+)", t):
        keys.add("oracle:" + m.group(1))
    for m in re.finditer(r"myworkdayjobs\.com/\S*?_(\w*R\d+)", t):
        keys.add("workday:" + m.group(1).upper())
    if not keys and re.match(r"https?://", t.strip()):
        keys.add("url:" + re.sub(r"[?#].*$", "", t.strip().lower()).rstrip("/"))
    return keys


def norm_employer(s):
    s = (s or "").lower()
    s = re.sub(r"\(.*?\)", " ", s)  # drop "(M)", "(client: ...)"
    return " ".join(w for w in re.findall(r"[a-z0-9]+", s) if w not in STOP)


def role_tokens(s):
    s = re.sub(r"\(.*?\)", " ", (s or "").lower())
    return {w for w in re.findall(r"[a-z0-9&]+", s) if w not in ROLE_STOP and len(w) > 1}


def similar_role(a, b):
    ta, tb = role_tokens(a), role_tokens(b)
    if not ta or not tb:
        return False
    return len(ta & tb) / len(ta | tb) >= 0.6


def read_log():
    if not os.path.exists(LOG):
        return []
    with open(LOG, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_claims():
    if not os.path.exists(CLAIMS):
        return []
    with open(CLAIMS, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    fresh = []
    for r in rows:
        try:
            if now() - dt.datetime.fromisoformat(r["claimed_at"]) < CLAIM_TTL:
                fresh.append(r)
        except Exception:
            pass
    return fresh


def write_claims(rows):
    with open(CLAIMS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CLAIM_HEADER)
        w.writeheader()
        w.writerows(rows)


def find(link, employer=None, role=None, agent=None):
    """Return (code, message). 0 clear, 1 in log, 2 claimed by other, 3 possible dup."""
    keys = job_keys(link)
    for r in read_log():
        rk = job_keys(r.get("link", "")) | job_keys(r.get("notes", ""))
        if keys & rk:
            return 1, f"ALREADY IN LOG: {r['date']} | {r['employer']} | {r['role']} | {r['status']} | by {r.get('agent') or '?'}"
    for c in read_claims():
        if c["key"] in keys and c["agent"] != agent:
            return 2, f"CLAIMED by {c['agent']} at {c['claimed_at']}: {c['employer']} | {c['role']}"
    if employer:
        ne = norm_employer(employer)
        same = [r for r in read_log() if ne and norm_employer(r["employer"]) == ne]
        if same:
            sim = [r for r in same if role and similar_role(role, r["role"])]
            hits = sim or same
            label = ("POSSIBLE DUPLICATE (same employer, similar role)" if sim else
                     "SAME EMPLOYER, different role - read both ads; use claim --force if it is a genuinely different job")
            return 3, label + ":\n  " + "\n  ".join(
                f"{r['date']} | {r['employer']} | {r['role']} | {r['link']} | {r['status']} | by {r.get('agent') or '?'}"
                for r in hits[-5:])
        for c in read_claims():
            if c["agent"] != agent and norm_employer(c["employer"]) == ne and (not role or similar_role(role, c["role"])):
                return 2, f"CLAIMED by {c['agent']} at {c['claimed_at']} (same employer/similar role): {c['employer']} | {c['role']}"
    if not keys and not employer:
        return 3, "No job ID found in that text; pass --employer and --role so a name match can be done."
    return 0, "CLEAR"


def main():
    cand = argparse.ArgumentParser(add_help=False)
    cand.add_argument("--candidate", default=argparse.SUPPRESS,
                      help=f"whose applications: {DEFAULT_CANDIDATE} (default) or a name under candidates/")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, parents=[cand])
    sub = p.add_subparsers(dest="cmd", required=True)
    _add = sub.add_parser
    sub.add_parser = lambda *x, **k: _add(*x, parents=[cand], **k)
    c = sub.add_parser("check"); c.add_argument("link"); c.add_argument("--employer"); c.add_argument("--role"); c.add_argument("--agent")
    cl = sub.add_parser("claim"); cl.add_argument("link"); cl.add_argument("--employer", required=True)
    cl.add_argument("--role", required=True); cl.add_argument("--agent", required=True)
    cl.add_argument("--force", action="store_true", help="claim despite a POSSIBLE DUPLICATE after reading both ads")
    lg = sub.add_parser("log")
    for a in ("agent", "employer", "role", "link", "status"):
        lg.add_argument("--" + a, required=True)
    lg.add_argument("--location", default=""); lg.add_argument("--cv", default=""); lg.add_argument("--notes", default="")
    lg.add_argument("--date", default=dt.date.today().isoformat())
    rl = sub.add_parser("release"); rl.add_argument("link"); rl.add_argument("--agent", required=True)
    sub.add_parser("claims")
    rc = sub.add_parser("recent"); rc.add_argument("n", nargs="?", type=int, default=15)
    sub.add_parser("candidates")
    a = p.parse_args()

    if a.cmd == "candidates":
        d = os.path.join(HERE, "candidates")
        names = sorted(n for n in os.listdir(d) if os.path.isdir(os.path.join(d, n))) if os.path.isdir(d) else []
        print("\n".join([DEFAULT_CANDIDATE + " (default)"] + names))
        sys.exit(0)

    who = getattr(a, "candidate", DEFAULT_CANDIDATE).lower()
    use_candidate(who)
    print(f"[candidate: {who}]", file=sys.stderr)

    with locked():
        if a.cmd == "check":
            code, msg = find(a.link, a.employer, a.role, a.agent)
            print(msg); sys.exit(code)

        if a.cmd == "claim":
            code, msg = find(a.link, a.employer, a.role, a.agent)
            if code in (1, 2) or (code == 3 and not a.force):
                print("NOT CLAIMED - " + msg); sys.exit(code)
            keys = job_keys(a.link) or {"name:" + norm_employer(a.employer) + "|" + " ".join(sorted(role_tokens(a.role)))}
            rows = [r for r in read_claims() if r["key"] not in keys]
            for k in keys:
                rows.append({"claimed_at": now().isoformat(), "agent": a.agent, "key": k,
                             "employer": a.employer, "role": a.role, "link": a.link})
            write_claims(rows)
            print(f"CLAIMED by {a.agent}: {a.employer} | {a.role}" + (" (forced past: " + msg + ")" if code == 3 else ""))
            sys.exit(0)

        if a.cmd == "log":
            if a.status.upper().startswith("SUBMITTED"):
                code, msg = find(a.link, None, None, a.agent)
                if code == 1:
                    print("NOT LOGGED - " + msg); sys.exit(1)
            with open(LOG, "a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([a.date, a.employer, a.role, a.location, a.link, a.cv, a.status, a.notes, a.agent])
            keys = job_keys(a.link)
            write_claims([r for r in read_claims() if r["key"] not in keys and not (
                r["agent"] == a.agent and norm_employer(r["employer"]) == norm_employer(a.employer)
                and similar_role(r["role"], a.role))])
            print(f"LOGGED: {a.employer} | {a.role} | {a.status}")
            sys.exit(0)

        if a.cmd == "release":
            keys = job_keys(a.link)
            rows = read_claims()
            keep = [r for r in rows if not (r["key"] in keys and r["agent"] == a.agent)]
            write_claims(keep)
            print(f"released {len(rows) - len(keep)} claim(s)")
            sys.exit(0)

        if a.cmd == "claims":
            rows = read_claims()
            print("\n".join(f"{r['claimed_at']} {r['agent']}: {r['employer']} | {r['role']} | {r['link']}" for r in rows)
                  or "no active claims")
            sys.exit(0)

        if a.cmd == "recent":
            for r in read_log()[-a.n:]:
                print(f"{r['date']} | {r.get('agent', '')} | {r['employer']} | {r['role']} | {r['status']}")
            sys.exit(0)


if __name__ == "__main__":
    main()
