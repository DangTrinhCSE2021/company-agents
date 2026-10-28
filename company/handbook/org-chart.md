# Org chart

```
                Client (you)
                    │
                Director  ── main Claude session, defined by CLAUDE.md
          ┌─────────┼──────────┐
     Reception  Secretary   Engineer   ── subagents in .claude/agents/
```

| Role      | Owns                               | Writes to                          | Model   |
|-----------|------------------------------------|------------------------------------|---------|
| Director  | Decisions, delegation, review      | nothing directly                   | session |
| Reception | Intake, ticket quality             | `office/tickets/open/`, `inbox/`   | haiku   |
| Secretary | Ticket status, board, minutes      | `office/` (records only)           | haiku   |
| Engineer  | Technical work                     | `projects/`, own ticket's Work log | inherit |

Why the Director is the main session: only the main session can delegate to
subagents and talk to the Client, so the role that coordinates must live there.
