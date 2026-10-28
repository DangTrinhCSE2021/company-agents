# Workflow

```
Client ─► Director ─► reception ──► ticket in open/
                         │
             open questions? ── yes ─► Director asks Client ─► reception updates ticket
                         │ no
          Director assigns ─► secretary: open/ → in-progress/, board, minutes
                         │
          Director delegates ─► engineer works in projects/<slug>/, logs to ticket
                         │
          Director reviews against acceptance criteria
                 │ fails                     │ passes
       back to engineer with feedback    secretary: → done/, board, minutes
                                              │
                                    Director reports to Client
```

## Ticket lifecycle

| Status        | Folder                      | Who moves it |
|---------------|-----------------------------|--------------|
| open          | `office/tickets/open/`        | reception creates |
| in-progress   | `office/tickets/in-progress/` | secretary |
| done          | `office/tickets/done/`        | secretary |

## Conventions

- Ticket file: `T-NNNN-short-slug.md`, IDs never reused.
- Dates: `YYYY-MM-DD`.
- One project folder per product/effort in `projects/`; many tickets can share one.
- Dropping a text file into `office/inbox/` is the same as telling the Director.
