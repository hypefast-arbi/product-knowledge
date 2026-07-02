# Sub-skill: Acceptance Criteria

Produce the `Acceptance Criteria` cell for one requirement row. Acceptance criteria are the QA contract: each scenario must be **verifiable by a tester with no further questions**.

## Format — Gherkin scenario blocks (mandatory template)

Write criteria as one or more scenario blocks following exactly this template:

```gherkin
Scenario: User can sync the latest data of all customers - sync data
Given that a salesperson is on the sales app
And theyre on the customer tab
When they click sync data
Then get the latest customer data from Jubelio and Jurnal
And update the last time sync
```

Template rules:

- `Scenario: <what the user can do> - <short action label>` — a capability statement ("User can …", "System can …") followed by a hyphen and a 2–4 word label for the action being tested.
- `Given that <actor> is on <place/state>` — the starting point: the concrete actor role (a salesperson, a procurement ops, a finance AP officer) and where they are (app, page, menu path, or document state). Additional preconditions each go on their own `And` line directly below.
- `When they <action>` — the trigger action, third person. Additional chained actions each on their own `And` line.
- `Then <observable result>` — what happens: data shown/created/updated, state change, screen shown, notification sent. Additional results each on their own `And` line.
- All lines start at column 0 — `And` lines are NOT indented.
- Third-person voice throughout (`a salesperson … they … them`), never first person. For system-actor stories the system is the subject (`Given that a validated reception exists in Jubelio … Then Odoo creates …`).
- One scenario tests one path. Don't fold the happy path and a rejection path into one scenario — write two.

Typical volume: 2–6 scenarios per story — fewer usually means the story is under-specified, more means the story should probably be split.

## Coverage checklist

For every story, walk this list and write a scenario for each item that applies:

1. **Happy path** — the journey step succeeds; name the resulting state/screen/record/notification in the `Then`.
2. **State transition** — when the flow is a document lifecycle, assert the from→to state and who/what triggers it.
3. **Validation / negative** — required fields, invalid input, or acting out of sequence is rejected with visible feedback.
4. **Permission** — who can and explicitly who canNOT perform the action, when the story involves roles or restrictions.
5. **Edge cases the source states** — partial quantities, zero/duplicate cases, boundary values from the SOP.
6. **Hand-off** — the next actor in the journey is notified / can see what they need.
7. **Data outcome** — for calculation or sync stories: the exact figures/records created, and what they must reconcile to.

Skip checklist items that genuinely don't apply — don't pad.

## Rules

- **Observable results only.** `Then the PO status changes to "Confirmed"` is testable; `Then it works correctly` is not.
- **Every scenario traces to the story and its journey step(s).** Don't smuggle new scope into scenarios — if a needed behavior has no story, propose the story instead.
- **Never invent business rules.** Thresholds, approval sequences, calculation formulas, and field lists come from the PRD/SOP or from the user. If a scenario needs a rule the source doesn't state, mark the value `(assumed — confirm)` or write `<TBD — confirm with author>`.
- **Platform criteria** — when a platform skill is loaded (e.g. Odoo), express pages, buttons, objects, and states in the platform's real terms per that skill; keep this same scenario-block template.
