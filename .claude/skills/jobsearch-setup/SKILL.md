---
name: jobsearch-setup
description: First-time setup for this job-application folder. Interviews the user about their target roles, skip rules and screening answers, reads their CVs, and writes HANDOFF.md. Use when HANDOFF.md is missing, when the user says "set me up", "onboard me", or wants to add a second person (partner, sibling) to the folder.
---

# Job search setup

Goal: end with a complete `HANDOFF.md` (built from `HANDOFF.template.md`) that any agent can apply from without guessing.

## 1. Check the folder
- Run `python3 --version` (needs 3.8+). If missing, tell the user how to install Python and stop.
- Is this for the main person or a second person? For a second person, pick a short lowercase name (e.g. `sam`); their files go in `candidates/<name>/` and every `jobs.py` command for them takes `--candidate <name>`.
- If `HANDOFF.md` already exists for that person, ask whether to update it or start over. Never overwrite it without a yes.

## 2. Read the CVs
- Ask the user to put their CV PDFs in `cv/` (or `candidates/<name>/cv/`). Read each one fully.
- From the CVs, pre-fill everything you can: name, qualification, grades, experience with dates, software, languages, links. Show the user what you pulled and ask them to correct it.
- Note any document that shows an ID or passport number, so agents ask before uploading it.

## 3. Interview the user
Ask in small batches (3–5 questions at a time, using AskUserQuestion where the options are clear). Cover every section of `HANDOFF.template.md`:
1. **Goal:** target roles, seniority, locations (remote?), minimum and expected salary, which job sites to use.
2. **Skip rules:** industries they won't work in, languages they don't speak, max years of experience asked for, minimum pay, anything else that's a deal-breaker.
3. **Screening answers:** work rights, notice period, transport, travel/relocation, licences, shift work, background checks, employment status, last salary, and whether to answer gender/ethnicity/DOB or ask each time.
4. **CV choice:** which CV for which kind of role.
5. **Accounts:** the email used to apply, and whether anyone else's accounts are signed in on this browser.

Rules while interviewing:
- Only write what the user actually said or the CV shows. If they're unsure, write "ask me" for that item.
- Don't ask for passwords, ID numbers or bank details, and don't write them in any file.

## 4. Write HANDOFF.md
- Copy `HANDOFF.template.md` to `HANDOFF.md` (or `candidates/<name>/HANDOFF.md`), fill every `<…>` placeholder, delete lines that don't apply, and put today's date in the title.
- Read it back to the user in a short summary and fix anything they flag.

## 5. Smoke-test the log
```bash
python3 jobs.py check "https://example.com/job/123" --employer "Test Co" --role "Test"   # expect CLEAR
python3 jobs.py recent
```
(Add `--candidate <name>` for a second person.) Don't log the test job.

## 6. Hand over
Tell the user setup is done and that they can start applying with the `apply-jobs` skill (or by asking "apply for jobs"). Remind them:
- They type every password and approve every consent box and recruiter message.
- They should keep their browser signed in to the right accounts (Claude in Chrome extension installed).
