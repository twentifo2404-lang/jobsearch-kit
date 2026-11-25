# Claude instructions for this folder

Read and follow AGENTS.md, then HANDOFF.md.

- If HANDOFF.md doesn't exist, run the `jobsearch-setup` skill first.
- To run an application session, use the `apply-jobs` skill.
- Other agents (such as Codex) may apply from this same log, so run `jobs.py check`, then `claim`, then `log` with `--agent claude` for every application.
