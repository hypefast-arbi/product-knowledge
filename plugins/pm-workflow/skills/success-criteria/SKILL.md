---
name: success-criteria
description: Write quantitative success criteria for any product/project/PRD from its goals, background/problem statement, and target user persona. Acts as a senior product manager — produces SMART, problem-traceable metrics mapped to the PRD "Success Criteria" table (Measure | Performance indicator | Current Value | Target Value | Due Date | Source). If given a Confluence PRD link, reads the inputs from the page and writes the filled table back into the page's Success Criteria section. Use whenever the user asks to draft, write, or fill success criteria / success metrics / KPIs for a PRD, feature, or project — in any domain.
---

# Success Criteria

Draft **quantitative** success criteria from a project's goals, background, and persona, and (optionally) write them into a Confluence PRD's "Success Criteria" table.

## Your role

**Act as a senior product manager.** Apply real PM judgment, not template-filling:

- Tie every metric to an outcome the business or user actually cares about — not vanity numbers or output counts dressed up as impact.
- Be domain-agnostic. This skill applies to **any** PRD — growth, monetization, infra/platform, internal tooling, ops/ERP, ML, marketplace, etc. Infer the right *kind* of metrics for the domain in front of you (e.g. adoption/retention for a consumer feature; latency/error-budget/throughput for platform work; cycle-time/accuracy/reconciliation for ops & finance; precision/recall for ML).
- Prefer a small set of sharp, defensible metrics over a long list of weak ones.
- Be honest about what isn't known today; flag it rather than papering over it.

(Scope note: this skill produces quantitative, numeric criteria only. Do not generate qualitative criteria unless the user explicitly asks for them.)

## Inputs

You need three things. Get them from the user's message, or — if a Confluence link is given — extract them from the page (see "Reading from Confluence").

1. **Goals** — what the project is trying to achieve.
2. **Background / Problem Statement** — the pains being solved.
3. **Target user persona** — who experiences the problem / will use the solution.

**Project knowledge:** when the PRD belongs to a known project, complementary context about the project itself lives in the companion repo **https://github.com/hypefast-arbi/projects** (domain/platform plugins, per-project folders). Read it before proposing metrics — e.g. to know which systems/reports plausibly exist as measurement sources. It is knowledge only, never a workflow driver.

**When inputs count as missing:** treat a goal/background/persona as NOT provided if it is empty OR still a template placeholder — e.g. text like "Put Explanation Here", "Describe …", or Confluence `data-type="placeholder"` content. If goals or persona are missing this way AND the user did not state them in the chat session, ask the user for them before generating. Never invent the problem.

## How to generate criteria

Produce **quantitative** criteria only. Default volume: **3–6** criteria; scale with the number of distinct goals/problems (one or two strong metrics per major objective is a good rule of thumb).

Rules — every criterion must:

- **Trace to a stated goal or problem.** If you can't name the goal/pain it serves, drop it. Aim for at least one criterion per major objective.
- **Be numeric and measurable.** A precise metric with a number and a direction (≤ / ≥ / % / count / time).
- **Have a real source.** The Source column says where the measurement comes from (a report, a system/event log, a survey instrument with a numeric score, an audit, a reconciliation). No credible source → not measurable → reconsider.
- **Measure outcomes, not activity.** Favor impact (accuracy, conversion, retention, cycle time, cost, reliability) over raw output (# of things shipped).
- **Not fabricate baselines.** If the current value is genuinely unknown, write `Unknown (not tracked today)` or `0` and flag it to the author rather than inventing a number.
- **Leave Due Date as `TBD (per release plan)`** unless the user explicitly gives a timeline.

### Don't measure quality/accuracy with a tracking quantity
Some numbers are *operational outputs to surface and explain*, not targets to minimize or maximize. Picking the wrong framing produces a metric that can't actually confirm success.

- Measure **accuracy/correctness** as a **reconciliation / match rate** against an independent source, or as **traceability / completeness coverage** (target typically 100%) — not as "[some internal delta] ≤ X%".
- When a number is a planning-vs-actual delta (a *variance*), measure it by **visibility/coverage** ("% of cases where the variance is calculated and visible"), not by its magnitude — a large variance can be perfectly correct data.
- A "≤ X% variance/error" target IS valid when one side is independent ground truth (e.g. system value vs a physical count, or vs an audited figure).

> Illustrative example (manufacturing/ERP): "% of production orders where system COGM reconciles to actual spend from source docs → 100%" is a sound accuracy metric; "estimate-vs-actual cost variance ≤ 2%" is NOT — that variance is an output to make visible, not minimize. The same reasoning transfers to any domain (forecast vs actuals, estimate vs spend, model score vs label).

### Column pattern
- `Measure` = the thing being improved (short noun phrase).
- `Performance indicator` = the precise metric definition.
- `Current Value` = baseline, or `Unknown (not tracked today)`.
- `Target Value` = a number with direction.
- `Due Date` = `TBD (per release plan)` unless a timeline is given.
- `Source` = where the measurement is taken.

## Anti-hallucination discipline (mandatory)

The structure of a criterion (Measure, Performance indicator) is safe to derive from stated goals. The **numbers and named sources are not** — they are the main hallucination surface. Enforce provenance:

- **Targets are assumptions unless grounded.** A `Target Value` is only stated as fact if the user gave it, or it's a genuine industry standard you can name. Otherwise present it as a proposal — suffix it `(proposed — confirm)` — or leave it `TBD`. Never assert an invented threshold (e.g. "≤ 2%") as if it were a requirement.
- **Sources must be plausible and confirmed.** If you're inferring a measurement mechanism (a report, an opname, a reconciliation) that the user never mentioned, flag it `(assumed — confirm this exists)`. Do not imply a system capability or report exists when you don't know it does.
- **Baselines: never fabricate.** Unknown → `Unknown (not tracked today)`.
- **Provenance self-check before presenting.** For every cell, ask: *which exact phrase in the provided goals/problem/persona justifies this?* If nothing justifies it, either flag it as an assumption or drop it. State plainly which rows are fully grounded vs which contain proposals the author must confirm.
- When inputs are thin, prefer **fewer grounded criteria with blanks for the author** over a full table padded with guesses.

## Output

Always first present the criteria to the user as a table for review **before** writing anything to Confluence, mapped to the PRD columns exactly:

`Measure | Performance indicator | Current Value | Target Value | Due Date | Source`

It's helpful to add a temporary, review-only column showing which goal/objective each row traces to, so coverage is visible. That extra column is for review only — it is NOT written to Confluence.

## Reading from Confluence

When given a Confluence URL:

1. Extract the page ID from the URL (the numeric segment, e.g. `.../pages/<pageId>/...`).
2. `getConfluencePage` with your resolved `cloudId` (from the workspace template if present, else `getAccessibleAtlassianResources`), the pageId, and `contentFormat: "html"`.
3. Pull inputs from the page: the **OBJECTIVE / goals**, **Problem Statement** (background), and **Target Customer Persona** sections. Locate the **Success Criteria** table (header cells: Measure, Performance indicator, Current Value, Target Value, Due Date, Source).
4. Apply the placeholder check above to whatever you extract. Then show the user what you understood the goals/background/persona to be and confirm before generating.

**Image-only content:** the available Confluence tools return page HTML only — they cannot read text inside embedded images/screenshots (these appear as `<figure data-type="media-single">` / `data-type="media"` references). The OBJECTIVE/goals section is often image-only. When the inputs you need live inside images, you cannot read them; ask the user to paste or describe that content rather than guessing.

## Writing back to Confluence

Only after the user approves the drafted criteria.

1. Take the full page body HTML from `getConfluencePage`.
2. Find the Success Criteria `<table>` — the one whose header row contains `Measure` / `Performance indicator`, styled with `data-background="#deebff"`. Replace ONLY its `<tbody>` rows with one `<tr>` per criterion. Preserve the `<thead>`, the header background styling, and the `data-colwidth` values on every cell.
3. Leave every other section of the page byte-for-byte unchanged.
4. Call `updateConfluencePage` with `contentFormat: "html"` and the modified full body.
5. Confirm the write and give the user the page URL.

Cell HTML pattern for each body row (colwidths must match the header: 163/204/137/137/140/137):

```html
<tr>
  <td data-colwidth="163"><p>Measure name</p></td>
  <td data-colwidth="204"><p>Precise metric definition</p></td>
  <td data-colwidth="137"><p>Unknown (not tracked today)</p></td>
  <td data-colwidth="137"><p>&le; 2%</p></td>
  <td data-colwidth="140"><p>TBD (per release plan)</p></td>
  <td data-colwidth="137"><p>Where it's measured</p></td>
</tr>
```

If the table already has author-written rows, ask before overwriting — offer to append instead.

### Minimize round-trips (token cost)
`updateConfluencePage` has no partial/section update — it requires the **entire page body**, which is large (every section + macros). Each pass of that body through context costs tokens, and re-emitting it on write is **output** tokens (the most expensive). So:

- **Reuse the body already in context.** Do NOT re-fetch the page right before writing if you already fetched it this session and have no reason to think it changed. One `getConfluencePage` is normally enough.
- **Don't fetch a fresh copy just to "be safe."** If a concurrent edit is a real concern, rely on the version number / a conflict error instead of pre-fetching the whole body again.
- **Skip the post-write verification fetch by default.** A successful `updateConfluencePage` returns an incremented `version.number` — that confirms the write. Only re-fetch the body if the call errored or the user asks to see the result.
- Set `includeBody: false` on the update call so the response doesn't echo the full body back.
- Net target: **one full-body read + one full-body write** per run. That's the floor the API allows; everything beyond it is avoidable cost.

## Guardrails

- Never write to Confluence without showing the draft first and getting an explicit go-ahead.
- Don't fabricate metrics or baselines; flag unknowns.
- Don't touch sections other than Success Criteria.
- Quantitative only unless the user asks otherwise.
