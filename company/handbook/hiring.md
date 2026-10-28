# Hiring a new role

1. Copy `company/templates/agent.md` to `.claude/agents/<role>.md`.
2. Write a precise `description` — the Director chooses staff by it.
3. Grant the fewest `tools` the role needs. Use `model: haiku` for clerical work.
4. Add a **Report back** section so the Director gets a consistent summary.
5. Add the role to the Staff table in `CLAUDE.md` and to `org-chart.md`.
6. If the role changes the process, update `workflow.md`.
7. Restart the Claude session (or run `/agents`) so the new role is picked up.

Ideas for future hires: `qa` (tests and reviews engineer output), `researcher`
(web research, read-only), `writer` (docs and copy), `designer` (UI mock-ups).

Firing: delete the file in `.claude/agents/` and remove it from the tables above.
