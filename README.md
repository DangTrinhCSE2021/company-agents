# Agent Company

A company run entirely by Claude agents: a Director (the main session) delegating to
Reception, Secretary and Engineer subagents, with all records kept as files.

## Start working

```
cd agent-company
claude
```

Then just tell the Director what you need, e.g. *"Build a CLI that converts CSV to JSON."*
Ask *"What's on the board?"* any time for status.

## Where to change things

| To change…                         | Edit                                   |
|------------------------------------|----------------------------------------|
| How the Director behaves           | `CLAUDE.md`                            |
| A staff member's job               | `.claude/agents/<role>.md`             |
| The process / conventions          | `company/handbook/workflow.md`         |
| Ticket format                      | `company/templates/ticket.md` (+ secretary's board format) |
| Add or remove a role               | `company/handbook/hiring.md`           |

Records (`office/`) and deliverables (`projects/`) are data — safe to archive or clear
without touching how the company works.
