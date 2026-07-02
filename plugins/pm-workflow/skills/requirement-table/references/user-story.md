# Sub-skill: User Story

Produce the `User Story` cell (and its module tag) for one requirement row.

## Format

```
As a <persona/actor>, I want to <capability>, so that <outcome that serves a stated goal>.
```

- **Persona** comes from the PRD's Target Customer Persona or the actors named in the SOP flows (e.g. brand manager, procurement ops, finance AP officer, merchandiser, legal officer). Use the role name the PRD uses — don't rename roles.
- **System actors are allowed** for automation requirements: "As a <system> I want to <automated behavior>, so that <outcome>" (e.g. auto-validation, syncs, calculations, access restrictions). Use them only when no human is the actor.
- **Outcome** must be a benefit, not a restatement of the capability. If you can't articulate why the actor wants it, the story probably isn't real — check the flow again or ask.

## Quality bar (INVEST, applied)

- **Independent enough to schedule** — a story that can't be built without another names that dependency in its Description, not in the story sentence.
- **Negotiable** — describe the need, not the UI. "I want to be notified" is a story; "I want a red toast in the top-right" is not.
- **Valuable** — traces to the Problem Statement or a goal. If a seed story from Solution Overview doesn't trace, ask the author rather than silently dropping it.
- **Estimable & Small** — one capability per story. Split when a story hides several verbs with different actors, permissions, or acceptance criteria (e.g. "create and approve and export" → 3 stories). Merge when a fragment can't be tested alone.
- **Testable** — if you can't imagine its acceptance criteria, rewrite it.

## Working from the Solution Overview seed list

When the PRD's Solution Overview already lists stories:

- Keep the author's intent and actor; fix only grammar, ambiguity, and INVEST violations. Note every substantive change to the user during review.
- Keep the author's module tag unless it's clearly wrong; with a platform skill loaded, translate the tag to the platform's real module/app name.
- Don't add new stories beyond the seed list + what the SOP flows clearly require. New stories you infer from flows get flagged `(new — derived from <flow name>)` for the author to accept.

## Module tag

One or more module names, `+`-separated when a story genuinely spans modules (e.g. `Purchase + Accounting`). Use the PRD's taxonomy, or the platform skill's mapping when one is loaded.
