# Sub-skill: Acceptance Criteria

Produce the `Acceptance Criteria` cell for one requirement row. Acceptance criteria are the QA contract: each criterion must be **verifiable by a tester with no further questions**.

## Format

Gherkin-style scenarios, written as a bullet list in the cell:

```
- Given <precondition/state>, when <action>, then <observable result>.
```

Keep each criterion one sentence. 3–8 criteria per story is the normal range — fewer means the story is under-specified, more means the story should probably be split.

## Coverage checklist

For every story, walk this list and include what applies:

1. **Happy path** — the journey step succeeds; name the resulting state/record/notification.
2. **State transition** — when the flow is a document lifecycle, assert the from→to state and who/what triggers it.
3. **Validation / negative** — required fields, invalid input, or acting out of sequence is rejected with feedback.
4. **Permission** — who can and explicitly who canNOT perform the action, when the story involves roles or restrictions.
5. **Edge cases the source states** — partial quantities, zero/duplicate cases, boundary values from the SOP.
6. **Hand-off** — the next actor in the journey is notified / can see what they need.
7. **Data outcome** — for calculation or sync stories: the exact figures/records created, and what they must reconcile to.

Skip checklist items that genuinely don't apply — don't pad.

## Rules

- **Observable results only.** "Then the PO status is Confirmed and the vendor receives the PO by email" is testable; "then it works correctly" is not.
- **Every criterion traces to the story and its journey step(s).** Don't smuggle new scope into criteria — if a needed behavior has no story, propose the story instead.
- **Never invent business rules.** Thresholds, approval sequences, calculation formulas, and field lists come from the PRD/SOP or from the user. If a criterion needs a rule the source doesn't state, write the criterion with the rule marked `(assumed — confirm)` or leave the value as `<TBD — confirm with author>`.
- **Platform criteria** — when a platform skill is loaded (e.g. Odoo), express states, objects, and menus in the platform's real terms per that skill; still keep the Given/When/Then shape.
