# Sub-skill: Description

Produce the `Description` cell for one requirement row. The description gives a developer the context the story sentence and criteria can't carry — it answers *"where does this sit in the process, and what do I need to know to build it?"*

## Structure

Short paragraphs / compact bullets, in this order (include only what applies):

1. **Flow context** — which flow/SOP this belongs to and where: "Step 3–4 of the <flow name> journey: after <previous step>, before <next step>." Include the relevant journey steps (from the user-journey sub-skill) as a brief numbered sequence when the story covers several steps.
2. **Behavior detail** — the business rules, inputs/fields, and calculations the story needs, exactly as stated in the source. This is where SOP detail that doesn't fit a one-line criterion lives.
3. **Dependencies** — other stories that must exist first, integrations touched (name the external system), master data required.
4. **Boundaries** — what this story deliberately does NOT cover (points to the neighboring story or to Out of Scope).

## Rules

- **No new requirements.** Anything a tester must verify belongs in Acceptance Criteria; the description explains, it doesn't secretly extend. If writing the description surfaces a missing behavior, go back and add a criterion (or a story) instead.
- **Source-bound.** Field lists, formulas, and rules come from the PRD/SOP or the user; mark anything inferred `(assumed — confirm)`.
- **Self-contained.** A reader should not need to open the SOP to understand the row — but DO cite the source ("per <SOP name>") so they can go deeper.
- **Tight.** 3–8 lines is the normal range. If a description balloons, the story is too big — split it.
