---
name: apply-jobs
description: Run a job-application session from this folder - search the job sites in HANDOFF.md, shortlist fitting jobs, and apply one by one with the jobs.py check/claim/log routine. Use when the user says "apply for jobs", "do a batch", "find me jobs", "run a JobStreet/LinkedIn search", or names a specific job link to apply to.
---

# Apply-jobs session

## Before starting
1. Read `AGENTS.md` and `HANDOFF.md` (for a second person: `candidates/<name>/HANDOFF.md`, and add `--candidate <name>` to every `jobs.py` command). If `HANDOFF.md` is missing, run `jobsearch-setup` instead.
2. Run `python3 jobs.py recent 20` and `python3 jobs.py claims` to see what's been done and what another agent is working on.
3. Ask the user how many applications this batch, which sites, and how recent (e.g. "posted in the last 3 days") if they haven't said.
4. In the browser, confirm the signed-in account on each job site belongs to this person.

## Search and shortlist
- Search each site with the roles and locations from `HANDOFF.md`.
- For each posting: open the full ad, check it against every skip rule, then run `jobs.py check`. Log skips right away with the reason (`--status "SKIPPED - <reason>"`).
- Show the user the shortlist (employer, role, location, salary if shown, link) before applying, unless they told you to go ahead without asking.

## Apply, one job at a time
1. `jobs.py claim` right before opening the form. Exit code not 0 means stop on this one (see AGENTS.md).
2. Pick the CV per `HANDOFF.md`. Fill the form only with answers from `HANDOFF.md` or the CV.
3. A question that isn't covered: pause and ask the user. Add their answer to `HANDOFF.md` with the date.
4. Passwords, ID numbers, consent/terms boxes and anything irreversible beyond the submit the user asked for: hand to the user.
5. After submitting: `jobs.py log` with the site in the status (e.g. `SUBMITTED (LinkedIn)`) and the screening answers you gave in `--notes`. If it failed or you stopped: log that, or `jobs.py release` the claim.

## End of session
- Add a dated "Session notes" entry to `HANDOFF.md`: applied (count + names), skipped (main reasons), waiting on the user (assessments, accounts to create, documents needed).
- Tell the user anything time-sensitive: online assessments, interview invites, deadlines.
