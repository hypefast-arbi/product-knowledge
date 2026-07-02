# Sub-skill: User Journey

Build the user journey for each flow. The journey is a **working artifact**: it is not a column of the table itself — it feeds the Acceptance Criteria and Description cells and is shown to the user during review so they can validate your understanding of the process.

## Source

Derive journeys from the PRD's **User Flows** section: the linked SOP/flow documents (often Google Docs — read them via Google Drive tools) and any flow diagrams described in text. One journey per flow (e.g. one for procurement, one for vendor payment, one for goods receipt) — NOT one per story. Stories then map to one or more steps of a journey.

If a flow document is unreadable (image-only, no access), ask the user to describe the flow. Never invent process steps.

## Format

Numbered steps, each with actor → action → system response:

```
Journey: <flow name> (source: <SOP doc title/link>)
1. <Actor> <does action> → system <responds/changes state>
2. ...
   ⤷ Exception: <condition> → <what happens instead> (step 2a)
```

- **Happy path first**, top to bottom, from the triggering event to the end state that delivers the outcome.
- **Exception paths** that the SOP mentions (rejection, partial receipt, validation failure, overdue) attach to the step where they branch. Only include exceptions the source states or the user confirms — flag inferred ones `(assumed — confirm)`.
- Name the **state of the key business object** at each step when the flow revolves around a document lifecycle (draft → submitted → approved → done). State transitions become natural acceptance criteria later.
- Note **hand-offs** explicitly (who is notified, what they receive) — hand-offs are where real processes break, so they must appear in acceptance criteria.

## Mapping stories to steps

After drafting a journey, annotate which story covers which step(s). This mapping is your completeness check:

- A journey step no story covers → missing story (propose it, flagged as derived).
- A story covering no step of any journey → either the journey source is incomplete or the story is scope creep; raise it with the user.

Show the journeys + mapping during the review phase, before the table is finalized.
