# Sub-skill: Acceptance Criteria

Produce the `Acceptance Criteria` cell for one requirement row. Acceptance criteria are the QA contract: each scenario must be **verifiable by a tester with no further questions**.

## Format — Gherkin scenario blocks

Write criteria as one or more scenario blocks following exactly this template:

```gherkin
# Comment Logging Out as a current user
Scenario : A current user clicks the logout button
Given I am on the /landing page or related url
When I click on the Logout button
    And I click on the Confirm Logout button
Then I should see the “Sign In Page” or “Sign Up Page”
```

Template rules:

- `# Comment <behavior title>` — one comment line above each scenario naming the behavior being tested, phrased as *\<doing the thing\> as \<the actor\>*.
- `Scenario : <short sentence>` — the concrete situation: actor + trigger action.
- `Given` — the starting state: the page/menu the actor is on (use the route or menu path, e.g. `/landing page or related url`, `Purchase → Orders → RFQ`) and any preconditions (role, existing record, document state). Chain extra preconditions with indented `And` lines.
- `When` — the action(s) the actor takes, in order. Each additional action is an indented `    And` line under the `When`.
- `Then` — the observable result: what the actor sees (page/screen shown, message, status/state change, record created, notification sent). Chain extra results with indented `And` lines.
- First-person voice (`I am`, `I click`, `I should see`) for human actors; for system actors use the system as subject (`Given a validated reception exists in Jubelio … Then Odoo should …`).
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

- **Observable results only.** `Then I should see the PO status change to "Confirmed"` is testable; `Then it works correctly` is not.
- **Every scenario traces to the story and its journey step(s).** Don't smuggle new scope into scenarios — if a needed behavior has no story, propose the story instead.
- **Never invent business rules.** Thresholds, approval sequences, calculation formulas, and field lists come from the PRD/SOP or from the user. If a scenario needs a rule the source doesn't state, mark the value `(assumed — confirm)` or write `<TBD — confirm with author>`.
- **Platform criteria** — when a platform skill is loaded (e.g. Odoo), express pages, buttons, objects, and states in the platform's real terms per that skill; keep this same scenario-block template.
