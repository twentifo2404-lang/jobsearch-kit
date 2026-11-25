# Job applications: shared rules for every agent (Claude, Codex, …)

One or more AI agents apply for jobs on behalf of the person who owns this folder. This file is how they stay out of each other's way, so no job gets applied to twice.

**Start every session by reading `HANDOFF.md`.** It holds this person's goal, skip rules, confirmed screening answers and which CV to use. If `HANDOFF.md` doesn't exist yet, stop and run the `jobsearch-setup` skill (or ask the user to) before applying anywhere.

## Files

All paths are relative to this folder. If your session runs somewhere else, `cd` here first. On Windows, if `python3` isn't found, use `python` or `py` instead in every command below.

| File | What it is |
|---|---|
| `HANDOFF.md` | Goal, skip rules, confirmed screening answers, CVs, account notes. The person's own rules. |
| `application_log.csv` | **The one log.** Every application, skip and failure by any agent. The `agent` column says who did it. |
| `claims.csv` | Short-lived "I'm applying to this right now" locks. Don't edit by hand. |
| `jobs.py` | The only way to read and write the two CSVs above. |
| `recruiter_contacts.csv` | Optional: recruiter and HR contacts per application. |
| `cv/` | The person's CVs, cover letters and transcripts. |
| `candidates/<name>/` | Optional: a second person sharing this folder (see below). |

Don't keep a separate log anywhere else.

## The 3-step routine (required for every job)

```bash
# 1. Before you even shortlist it
python3 jobs.py check "<job link>" --employer "<company>" --role "<job title>"

# 2. Right before opening the application form
python3 jobs.py claim "<job link>" --employer "<company>" --role "<job title>" --agent claude   # or --agent codex

# 3. Right after it is sent, or when you decide to skip it or it fails
python3 jobs.py log --agent claude --employer "<company>" --role "<job title>" \
  --location "<city>" --link "<job link>" --cv "<CV file>" \
  --status "SUBMITTED (LinkedIn)" --notes "<screening answers you gave, salary, anything odd>"
```

**What the exit codes mean**

| Code | Meaning | What to do |
|---|---|---|
| 0 | CLEAR | Go ahead. |
| 1 | ALREADY IN LOG | Don't apply. |
| 2 | CLAIMED by another agent right now | Leave it to them. |
| 3 | Same employer, or a similar role, already logged | Read both ads. If it's really a different job, use `claim --force`. If it's the same job on another site (job board vs LinkedIn vs the company site), don't apply. |

**Other routine rules**
- Log skips and failures too, so the other agent doesn't redo the work: `--status "SKIPPED - needs 3 yrs"`, `--status "NOT SUBMITTED - site error"`.
- If you claim a job and then don't apply, release it: `python3 jobs.py release "<link>" --agent claude`.
- Claims expire after 3 hours.
- `python3 jobs.py claims` lists what's in progress. `python3 jobs.py recent 20` shows the latest log rows.

## A second person in the same folder

If two people share one computer (for example a couple), the second one gets their own folder `candidates/<name>/` with their own `HANDOFF.md`, CVs and log. Add `--candidate <name>` to **every** `jobs.py` command for them. Never mix up their CVs, answers or accounts. `python3 jobs.py candidates` lists who's set up.

## Rules that apply to every agent
- **Never invent anything.** Qualifications, work history, screening answers: only what `HANDOFF.md` or the CV clearly supports. For experience or skill questions, answer "Yes" only when the CV clearly backs it; otherwise "No" or "No experience".
- **A question `HANDOFF.md` doesn't cover:** ask the user, then add the answer to `HANDOFF.md` (with the date) so the other agent uses it too.
- **Follow the skip rules in `HANDOFF.md`.** Log every skip with its reason.
- **Check which account is signed in** (LinkedIn, job boards, email) before each application. If the browser has someone else's account active, stop and tell the user.
- **Never type passwords, ID/passport numbers or bank details.** The user types those. Creating an account on a careers site is fine once the user has said so; they type the password.
- **Ticking consent or terms boxes:** ask the user first, unless they already approved it for that batch.
- **Never send messages or emails to recruiters** without the user's OK on that message.
- **Don't upload documents that contain ID numbers** (transcripts often do) without the user's OK for that application.
- **Quality over volume.** Read the whole ad before applying. A wrong answer on a form costs more than a skipped job.
