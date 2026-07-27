---
name: test-case-doc
description: Author a Given/When/Then (Gherkin) test-case document from acceptance criteria and a PRD, acting as a senior SDET — derives positive/negative/edge/configuration cases with full AC↔TC traceability, per-case preconditions, test data, Playwright tags, calculation blocks, and an open-questions log, then creates OR updates it as a Confluence page. Use whenever the user asks to write/draft test cases, a test plan, a QA test-case document, or a Gherkin/BDD scenario doc from an AC file (.feature), a PRD, a Jira epic, or a Jira backlog/board — and whenever they ask to publish or update such a doc in Confluence. Organization-agnostic — resolves the site/cloudId/space at runtime.
---

# Test-Case Document

Author a rigorous **Given/When/Then test-case document** from acceptance criteria (AC) and a PRD, then (optionally) create or update it as a Confluence page. The output mirrors the canonical QA artifact shape: header → AC reference → open items → test data → traceability summary → test cases grouped by actor → open PM questions. This skill is **organization-agnostic** — it hardcodes no site, cloudId, or space.

## Your role

**Act as a senior SDET / QA engineer.** Apply real test-design judgment, not template-filling:

- **Every test case traces to an AC.** If you can't name the AC (or explicit PRD rule) a case verifies, don't write it. Conversely, every AC must be covered by ≥1 case — surface any AC with no test.
- **Derive, don't invent.** Test cases come from what the AC/PRD *states*. Behaviour the source doesn't specify is **not** a passing/failing assertion — it is an **Open Item** or an **Open PM Question**. Never fabricate expected results, formulas, thresholds, credentials, or test data.
- **Cover each AC from multiple angles.** For each AC derive the positive (happy-path) case, then the negative and edge cases the AC implies (see Test-design techniques). A one-case-per-AC document is usually under-tested.
- **Be honest about gaps.** Anything blocked, ambiguous, or awaiting a PM/eng answer is written with its assertion marked `TBD — do not execute until confirmed`, logged in Open Items, and rolled up into Open PM Questions. This is the single most important discipline.

## Resolve your Atlassian config

Get the site + cloudId (and later the space/project) in this order:

1. **Workspace template first.** If your project knowledge includes an account
   template (e.g. Hypefast's `hypefast-atlassian` skill in the companion
   `projects` repo), use the site, cloudId, space IDs, and Jira project/board
   list it records — skip discovery.
2. **Otherwise discover.** `getAccessibleAtlassianResources` returns your
   accessible site(s) and cloudId; `getConfluenceSpaces(cloudId, keys:"<KEY>")`
   resolves a space key → spaceId (don't list all spaces); `getVisibleJiraProjects`
   resolves a project.
3. **If ambiguous** (more than one site, or none given), ask the user.

These tools are deferred — load what you need first with `ToolSearch`, e.g.
`select:mcp__claude_ai_Atlassian_Rovo__getConfluencePage,mcp__claude_ai_Atlassian_Rovo__updateConfluencePage,mcp__claude_ai_Atlassian_Rovo__createConfluencePage,mcp__claude_ai_Atlassian_Rovo__searchJiraIssuesUsingJql,mcp__claude_ai_Atlassian_Rovo__getJiraIssue`.

## Inputs

You need these; get them from the user's prompt, an attached/opened file, or a Confluence/Jira link/board. Ask only for what's genuinely missing.

1. **AC source** (required) — the acceptance criteria. May be:
   - a `.feature` / Gherkin file (e.g. an epic file in a **product-spec-style AC-catalog repo** — see "Reading from a product-spec repo" below — or any standalone `.feature` file),
   - a Confluence AC page or PRD's requirement table (see `requirement-table`/`success-criteria` skills for how that table is drafted),
   - a Jira epic, a single story, or an **entire board/backlog** (fetch via the Atlassian MCP — see below),
   - or ACs pasted in chat.
2. **PRD source** (recommended) — for context, flows, test data, and calculation rules. A Confluence PRD link, a `docs/prd/*.md`, or pasted text.
3. **Feature name** — short label used in the title, IDs, and Playwright tags (e.g. `Customer Organization` → `CUSTORG`). When covering multiple stories/tickets at once, this is usually the epic or board name.
4. **App + URL** — the system under test and its (staging) URL, for the header block.

**When an input counts as missing:** treat an AC/PRD as NOT provided if it is empty or still a template placeholder (`Put Explanation Here`, `Describe …`, Confluence `data-type="placeholder"`). If the AC source is missing, **stop and ask** — you cannot write grounded test cases without it. Never invent the acceptance criteria.

### Reading the AC/PRD from a source
- **Open/attached `.feature` file** → read it directly; each `Scenario`/`Scenario Outline` and its `Given/When/Then` steps are your raw material and often map 1:1 to an AC ID.
- **Confluence page** → extract the page ID (numeric URL segment, or the tiny-link code) and `getConfluencePage(cloudId, pageId, contentFormat:"html")`. Image-only sections can't be read (the MCP returns HTML only, not text inside screenshots) — ask the user to paste that content rather than guessing.
- **Jira epic/story/board** → see "Covering a whole epic or backlog" below.

### Reading from a product-spec-style AC-catalog repo
If the AC source is (or should be) tracked in a "product-spec"-style repo — a Gherkin `.feature`-file catalog, one file per epic, typically at `epics/<EPIC>/acceptance-criteria.feature` (this is what the sibling `product-spec-sync` skill writes) — that file **is** the authoritative AC list. Read it directly rather than re-deriving ACs from Jira/PRD prose when both exist; if it disagrees with the PRD/Jira, flag the conflict as an Open Item rather than silently picking one.

### Covering a whole epic or backlog
When the user asks to cover **all stories under an epic** or **an entire board/backlog** (not a single AC file):
1. Confirm the project + board with the workspace template, or resolve with `getVisibleJiraProjects`.
2. Enumerate the stories with `searchJiraIssuesUsingJql`, e.g. `project = <KEY> AND issuetype = Story ORDER BY Rank ASC` (add `AND parent = <EPIC-KEY>` to scope to one epic, or a status filter if the user wants only backlog/unstarted items). Ask maxResults ≥ story count; this can be a large payload — if it gets persisted to a tool-result file, parse it programmatically (don't page through it with Read) and extract only `key`, `fields.summary`, `fields.description`, `fields.status.name`.
3. For each story, pull its **acceptance criteria** — from the story's own description/AC field if it has Gherkin, or from the PRD requirement table row that produced it, or from the product-spec repo if this epic has already been synced there (check first — don't re-derive ACs that already exist as Gherkin).
4. Treat each story as one **Section** in the output (grouped by actor is still the primary grouping *within* a story's cases, but the AC Reference table and traceability summary should additionally show which Jira story each AC/case came from — add a `Story` column to both).
5. Any story with **no usable AC/description** (empty, placeholder, or purely technical with no user-facing behaviour to assert) is not silently skipped — list it in Open Items as "no AC available — needs PM input" and omit it from the traceability count rather than inventing behaviour for it.

### Grounding in domain knowledge
When the feature touches Odoo/ERP behaviour, invoke the relevant `odoo-*` functional skills (from the companion `projects` repo's `odoo-erp` plugin, if installed) to ground preconditions and expected results in how the module actually works — don't assume ERP semantics. If the ACs themselves need shoring up first, that's a job for the `requirement-table` / `odoo-requirement-table` skills, not this one.

## How to author the test cases

### Test-design techniques (how to reach good coverage)
For each AC, systematically derive cases:

- **Equivalence partitioning** — one representative case per class of equivalent inputs (don't test five values from the same class).
- **Boundary values** — test at and around limits (0, 1, max, max+1, empty, min length).
- **Positive vs negative** — the happy path *and* the rejection/blocked path. Access-control and scoping ACs almost always need a negative "cannot see / cannot access" case.
- **Edge cases** — the messy real-world combinations the AC implies (cross-org, revocation, duplicate match, empty state, concurrent state).
- **Configuration cases** — where behaviour is driven by a backend flag/grant/toggle, test that changing the config takes effect.
- **Decision tables / state transitions** — when an outcome depends on a combination of conditions, enumerate the combinations rather than testing one.

Scale the volume to the ACs — a small feature may be a dozen cases; a scoping/permissions feature is typically 30–40; a whole backlog spans many sections. Prefer sharp, traceable cases over padding.

### Test types
Label every case one of: **Positive**, **Negative**, **Edge Case**, **Configuration** (combine when apt, e.g. `Negative / Edge Case`).

### Per-test-case fields (every case has all of these)
| Field | Rule |
| --- | --- |
| **ID** | `TC-<FEATURE>-NNN`, zero-padded, sequential (e.g. `TC-CUSTORG-001`). Stable — never renumber on edit; append new IDs. |
| **Title** | One line, states the behaviour verified. |
| **Preconditions** | The exact state needed (who is logged in, what data must exist). Reference named test-data accounts, not fabricated ones. |
| **Test Type** | Positive / Negative / Edge Case / Configuration. |
| **Playwright Tag** | `@<feature>-<short-slug>`, kebab-case, unique per case (e.g. `@custorg-pusat-aocaov`). This is the automation hook. |
| **AC Reference** | The AC ID(s) this case verifies. Mandatory — a case with no AC ref is not allowed. |
| **Story** | (When covering a Jira epic/backlog) the Jira key this case traces back to. |
| **Test Data** | (When needed) specific keywords/values the step uses; capture live values at execution time rather than fabricating. |
| **Scenario** | The `Given … And … When … Then … And …` steps. Keep it declarative and executable. |
| **Calculation** | (When the assertion is a computed value) see below. |
| **Expected Result** | The single, checkable outcome. If unknown/blocked, write `TBD — do not execute until <who> confirms <what>` and log it. |
| **Execution Result** | Status (Not Run / Passed / Failed / Blocked), Executed By, Execution Date, Defect link, and free-text Actual Result. Always present but empty (`Status: Not Run`) when a case is first authored — filled in later per "Recording execution results" below. |

Group cases into **`Section N — Actor: <role>`** blocks (or, when covering a whole epic/backlog, **`Section N — <Story key>: <Story title>`**, with actor sub-groupings inside if a story spans several). One grouping per section, in a sensible order.

### Calculation blocks
When an Expected Result is a computed figure (an average, total, rounding, currency format), add a **Calculation** block instead of a bare number:
- **Formula** — the exact expression (numerator/denominator, what's included/excluded).
- **Rounding / format** — e.g. 2 decimals, IDR (`Rp 1.234.567,89`).
- **Input values** — say "capture at execution time" rather than inventing figures.
- If the formula is not confirmed by the PRD/PM, write `Formula: TBD — do not assert exact value until confirmed` and note the known constraints only.

### The surrounding sections (assemble in this order)
1. **Header block** — Feature/Epic, App, URL, **AC Source**, **PRD Source**, Model = `Given / When / Then`, Created (today's date), Status = `Not Executed`.
2. **AC Reference** table — every AC ID + description (+ Story column if epic/backlog scope), verbatim from the source.
3. **Open Items** — a dated log of anything not covered and *why*: `TBD`, `Resolved <date>`, `Skipped per instruction`, `No AC available`. This is the assumptions ledger; it makes the reasoning auditable.
4. **Test Data** — the accounts/entities/mappings the cases reference; a note that login credentials are substituted at execution time. Only real, provided data.
5. **Summary / traceability matrix** — one row per case: `TC ID | Title | Type | (Story |) AC Ref`. This is the coverage view.
6. **Test cases**, grouped by section (above).
7. **Open PM/Eng Questions** — blocking questions rolled up: `# | Question | Related AC/Story | Why it's blocking`.

### Traceability self-check (before presenting)
- Every AC in the reference table appears in ≥1 case's **AC Reference** → list any uncovered AC.
- Every case's **AC Reference** points to a real AC in the table → no orphan cases.
- Every story you enumerated (epic/backlog scope) appears in the summary at least once, or is explicitly logged in Open Items as "no AC available."
- Every blocked/TBD case is in **Open Items** *and* **Open PM Questions**.
State this coverage check to the user explicitly.

## Output & review

**Always present the drafted document to the user for review first** (as Markdown in chat — tables for AC reference / summary, then the cases), **before** writing anything to Confluence. Call out: the coverage check, every TBD/blocked case, and every place you'd otherwise have had to assume. Get an explicit go-ahead before publishing.

## Confluence — create & update

Uses the Atlassian Rovo MCP tools. Resolve `cloudId` per "Resolve your Atlassian config" above.

- **Title convention:** `[Test Cases] <Feature/Epic Name>`.
- **Location:** if the user gives a page/parent URL, use it directly (page ID = the numeric segment, or the tiny-link code after `/x/`). If they give only a space, resolve `spaceId` via `getConfluenceSpaces(cloudId, keys:"<KEY>")` (or the workspace template) and create at the space root. If neither, ask.

### Confluence HTML dialect (important — do not use storage-format macros)
The `contentFormat:"html"` body for these tools is **HTML+**, not Confluence storage XML — `<ac:structured-macro>` is rejected. Use plain HTML plus these `data-type` attributes:
- Panels: `<div data-type="panel-info|panel-warning|panel-note|panel-success|panel-error"><p>text</p></div>`
- Status lozenge: `<span data-type="status" data-color="green|red|yellow|blue|neutral|purple">Label</span>`
- Code block: standard `<pre><code class="language-gherkin">...</code></pre>` (no macro needed)
- Table of contents / other native macros: `<div data-type="extension" data-extension-key="toc" data-extension-type="com.atlassian.confluence.macro.core" data-parameters="{}"></div>`
- Expand/collapsible: `<details><summary>Title</summary><p>content</p></details>`
- Tables: standard `<table><thead>...` plus `data-colwidth`/cell `data-background` as needed.

The reusable building blocks (header info panel, AC-reference table, open-items table, test-data table, traceability table, a single test-case block, open-questions table) — all in this dialect — live in `references/confluence-blocks.html`. Read that file and assemble the body from its snippets, one test-case block per case, rather than improvising the structure.

### Create a new page
The body can be large (a few dozen cases, more for a whole backlog). To keep the bulky HTML out of your main context, **delegate the assembly + create call to a subagent** (`Agent`, `subagent_type: "general-purpose"`) once the user has approved the draft — mirroring the `confluence-create-page` PRD path. Give the subagent a self-contained prompt: the approved case data, the **absolute path** to `references/confluence-blocks.html` (resolve it yourself first — the subagent can't resolve a relative path against this skill), the resolved `cloudId`/`spaceId`/`parentId`/`title`, and instructions to return **only** the page title, ID, and `_links.webui`. For a small doc (a handful of cases) it's fine to call `createConfluencePage` inline.

`createConfluencePage(cloudId, spaceId, parentId?, title, contentFormat:"html", body, status:"current")`.

### Update an existing page
1. `getConfluencePage(cloudId, pageId, contentFormat:"html")` — one fetch.
2. Modify **only** the sections that changed:
   - **New cases** → append test-case blocks and add their rows to the traceability table + AC-reference coverage.
   - **Changed expected results / status** → edit only those cells.
   - **Resolved TBDs** → update the Open Items and Open PM Questions tables.
   - Preserve every other section byte-for-byte, and **never renumber existing TC IDs**.
3. `updateConfluencePage(cloudId, pageId, contentFormat:"html", body:<full modified body>, includeBody:false)`. **Do not pass a `title` parameter unless the user explicitly asked for a rename** — omitting it leaves the existing title untouched; passing any value (even one meant to be a no-op restatement) risks the model substituting a wrong/hallucinated title. This has actually happened (a real page's title was clobbered to an unrelated value during an unrelated body edit) — treat title as a field you touch only on explicit request.
4. Confirm via the returned incremented `version.number`; give the user the URL. If you did check the response and the title looks different from what you expect, say so immediately rather than assuming it's fine.

### Large, hand-retyped bodies risk silent corruption
When a subagent (or you) must edit a large existing body by reading it, mentally editing a spot in the middle, and resubmitting the whole string, there is real risk of transcription drift over tens of thousands of characters — a subagent doing exactly this on this skill's first real page caught and fixed one typo via a post-write diff, but also separately mis-set the title (caught only because the user was told the resulting title and it didn't match). Mitigations:
- Prefer **not re-typing the full body from memory** — fetch it once, and where your tooling allows it, treat the fetched value as an opaque string you slice/splice (e.g. string find-and-insert-after) rather than reproducing it token-by-token.
- After any large-body update, **do a structural self-check** before reporting success: counts of key markers (number of `<h2>` test-case headings, number of a newly-inserted block, the title, any distinctive header text) should match expectations. Don't rely solely on the tool's returned `version.number` as proof the content is correct — it only proves *a* write happened, not that the write was faithful.
- If anything about reproducing a large body verbatim feels risky, say so and stop rather than guessing.

### Token thrift (Confluence)
`updateConfluencePage` has no partial update — it needs the **entire** body, which is large, and re-emitting it on write is expensive **output**. So:
- **Reuse the body already in context** — don't re-fetch before writing if you fetched it this session.
- **Don't fetch "to be safe"** — rely on the version number / conflict error.
- **Skip the post-write verification fetch** — the incremented `version.number` confirms the write.
- Set `includeBody:false` so the response doesn't echo the body back.
- Net target: **one full-body read + one full-body write** per run.

### Preserve, don't clobber
Before updating, read the current page. If it has author/QA-written content you didn't generate (executed results, defect links, manual notes), **preserve it** — append or edit surgically, and ask before overwriting anything a human added. If the page is currently empty (a fresh page created for this purpose), just write the full document.

## Recording execution results

A separate, later workflow from authoring: the user (or you, on their behalf) reports that some test cases were run, and you update **only** those cases' **Execution Result** block — status, executed by, date, defect link, actual result — on the already-published page.

1. Get from the user, per case: which TC ID(s), the outcome (Passed/Failed/Blocked), who ran it and when (default to today/the user if unstated but confirm), the actual result observed, and a defect link/key if Failed.
2. `getConfluencePage(cloudId, pageId, contentFormat:"html")` — one fetch.
3. For each named TC ID, find its block and edit **only** its Execution Result table + Actual Result paragraph:
   - `Status` → the matching status lozenge: Passed = `data-color="green"`, Failed = `data-color="red"`, Blocked = `data-color="yellow"`, Not Run = `data-color="neutral"`.
   - Fill `Executed By`, `Execution Date`, `Defect` (issue key/link if any), and the `Actual Result` paragraph.
   - Do not touch that case's Preconditions/Gherkin/Expected Result, or any other case, section, or table on the page.
4. Roll up the header panel's overall **Status** lozenge from the aggregate of all 36 (or however many) cases' Execution Result statuses: any `Failed` → header `Failed` (red); else any case still `Not Run` → header `In Progress` (yellow); else all `Passed`/`Blocked` with none `Not Run` → header `Passed` (green) if all Passed, otherwise `Blocked` (yellow). State the computed rollup to the user rather than silently deciding if it's ambiguous (e.g. a mix of Blocked and Passed with no Failed).
5. `updateConfluencePage(cloudId, pageId, contentFormat:"html", body:<full modified body>, includeBody:false)` — same token-thrift rules as an update (one read, one write, `includeBody:false`, no verification re-fetch).
6. Report back: which TC IDs were updated, their new statuses, and the new overall header status.

For a small number of cases (a handful), do this inline. For updating many cases at once (a full execution pass), delegate to a subagent the same way as a large create/update — give it the exact TC ID → result mapping and the resolved cloudId/pageId, and have it return only the updated TC IDs + new `version.number`.

## Report back
Give the user: the page title, space/parent, page ID, and URL (`_links.webui` prefixed with the site's wiki base, `https://<your-site>.atlassian.net/wiki`). For a delegated create, relay these from the subagent's result.

## Guardrails
- Never write to Confluence without showing the draft and getting an explicit go-ahead.
- Never fabricate ACs, expected results, formulas, thresholds, test data, or credentials — flag them as TBD/Open Items instead.
- Every test case must trace to an AC; every AC must be covered or explicitly listed as a gap. When covering a backlog, every story must appear or be logged as "no AC available."
- Never renumber existing TC IDs on update; append.
- Don't touch page sections you didn't generate without asking.
- Never use `<ac:structured-macro>`/storage XML in the Confluence body — see the HTML dialect section above.
- Never change a page's title on an update unless the user explicitly asked for a rename — omit the `title` parameter entirely rather than restating the existing one.
- After any large-body update, self-check the result structurally (marker counts, title) before reporting success — don't treat a returned `version.number` alone as proof the write was faithful.
