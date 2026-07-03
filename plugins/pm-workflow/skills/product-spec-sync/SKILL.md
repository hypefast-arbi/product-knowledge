---
name: product-spec-sync
description: Move a Jira epic's stories and their Gherkin acceptance criteria (drafted in a Confluence PRD's requirement table) into a "product-spec"-style repo — a Gherkin .feature-file catalog generated into a static site (epics/<EPIC>/acceptance-criteria.feature + a feature registry + a build script). Use whenever the user asks to move/sync/import a Jira epic (or its ACs) into product-spec, add an epic to the AC catalog, turn a PRD's requirement table into product-spec Gherkin, or update the AC catalog after a PRD's requirement table is approved. Assumes the Jira epic + stories already exist and the PRD's Acceptance Criteria column is already in Gherkin (see the jira-create-ticket and requirement-table skills for those prerequisites) — this skill only moves what already exists into the repo. Repo-agnostic: reads the target repo's own README/CONTRIBUTING/AGENTS.md fresh every run rather than hardcoding its rules.
---

# Sync a Jira epic + PRD acceptance criteria into product-spec

Move one Jira epic's worth of work — its child Stories and the Gherkin acceptance
criteria already drafted for them in a PRD — into a "product-spec"-style repo: a
Gherkin `.feature`-file catalog (one file per epic) that a `build.py` renders into a
static MkDocs site. This skill is the last step of a chain: `jira-create-ticket`
creates the epic/stories, `requirement-table` drafts each story's Acceptance
Criteria cell as Gherkin, and **this skill** moves that already-drafted content into
the repo in the shape its own rules require.

**One-directional.** This skill only reads Jira/Confluence and writes to the repo.
It never edits the Jira issues or the PRD, and — unless the user explicitly asks —
it never pushes or opens a PR. Local commit only.

## Preconditions — check before starting

1. **The Jira epic and its child Stories already exist.** Confirm with a JQL query
   (`parent = <EPIC-KEY> ORDER BY key ASC`, see Step 2). If the epic has no
   children yet, stop and point the user at `jira-create-ticket`'s bulk-story flow
   instead of inventing stories here.
2. **The PRD's requirement table already has Gherkin ACs.** Fetch the PRD page and
   check its "Description of the User Flows" (or equivalent) table's Acceptance
   Criteria column actually contains `Scenario: ... Given ... When ... Then ...`
   text, not prose. If it's still prose, stop and point the user at
   `requirement-table` to draft the ACs first — don't draft Gherkin from scratch
   here, that's that skill's job and doing it here risks two skills disagreeing on
   house style.
3. **You can identify the target repo.** See "Resolve the target repo" below.

If any precondition fails, say so and ask how the user wants to proceed rather than
guessing or partially completing the move.

## Resolve the target repo

This skill is repo-agnostic — it hardcodes no path. Resolve the repo in this order:

1. **Workspace template first.** If a project-knowledge companion repo has an
   account/workspace template (e.g. Hypefast's `hypefast-repos` skill in the
   `projects` repo's `hypefast-workspace` plugin), use the path/remote/git-workflow
   it records — including whether the repo requires a PR (never push straight to
   its default branch if so).
2. **Otherwise ask** — a local clone path or a git remote to clone.
3. **Re-verify with `git remote -v`** in the resolved local clone before assuming
   a template entry is still accurate — it can drift (e.g. a repo moving host or
   org) without the template being updated.

Once resolved, treat its `README.md`, `CONTRIBUTING.md`, and `AGENTS.md` (if
present) as the **live source of truth for its rules** — read them fresh every run.
Do not rely on this skill's memory of a past run's rules; the repo's own docs can
change independently of this skill.

## Step 1 — Read the repo's own rules

Read (in this order) `README.md`, `CONTRIBUTING.md`, and `AGENTS.md` at the repo
root. You're looking for, at minimum:

- The canonical AC file path pattern (e.g. `epics/<EPIC>/acceptance-criteria.feature`)
- Tag conventions and cardinality (an id tag, bare feature tags validated against a
  registry file, status tags like draft/replaced/removed)
- The status lifecycle and its default (usually "no tag = live")
- The feature registry file (e.g. `features.yml`) and its schema
- Build/validate/test commands and what "clean" looks like
- Git workflow rules (branch-only, PR required, what never gets committed —
  usually a gitignored generated output directory)

Confirm your read of these back to yourself before drafting — this skill has no
opinion of its own on repo rules; the target repo's docs always win.

## Step 2 — Fetch the epic's Stories from Jira

```
searchJiraIssuesUsingJql(cloudId, jql: "parent = <EPIC-KEY> ORDER BY key ASC",
                          fields: ["summary", "status", "issuetype"], maxResults: 100)
```

This can return a large payload that gets persisted to a tool-result file instead
of shown inline. **Don't read that file with the Read tool** (it's typically one
giant minified JSON line — line-based reading won't paginate it usefully). Parse it
with a script instead:

- No `jq` on Windows by default. Use PowerShell `Get-Content -Raw | ConvertFrom-Json`
  or a small Node script — either works, pick whichever is already warmed up in the
  session.
- Extract just `key`, `fields.summary`, `fields.issuetype.name`, `fields.status.name`
  per issue. That's all this skill needs from Jira.

## Step 3 — Fetch the PRD and extract the requirement table

Fetch the PRD page (`getConfluencePage`, `contentFormat: "markdown"` — cheaper than
HTML for reading). This is also often large enough to persist to a file; save its
`content.nodes[0].body` to a scratch `.md` file (PowerShell `ConvertFrom-Json` +
`Set-Content`) rather than paging through the tool result.

**Locate the table robustly.** Don't search for a specific *end* heading by text —
a table's Description cells can contain prose that mentions a later section's name
verbatim (this bites you: e.g. a cell saying "...feed this into the List of Access
Restrictions section" will false-match a `.includes("List of Access Restrictions")`
search long before the real heading). Instead:

1. Find the **start**: the line that IS the heading (`startsWith`, not `includes`,
   e.g. `l.startsWith('### **Description of the User Flows**')`).
2. From there, collect every subsequent line that starts with `|` — a markdown
   table's rows are contiguous; the first line that stops starting with `|` is the
   natural end of the table. This needs no knowledge of what section follows.

The reusable parser at `scripts/parse-requirement-table.js` does this. See
[references/gherkin-parsing-notes.md](references/gherkin-parsing-notes.md) for the
exact splitting approach it uses to turn each row's Acceptance Criteria cell (one
string containing 1–N concatenated `Scenario: ...` blocks) into structured
Gherkin, and for a Windows Gherkin-parser gotcha you need to know before adding any
per-scenario comment.

## Step 4 — Propose the feature-tag taxonomy (pause here for review)

Every bare `@<feature>` tag in the target repo must resolve to an entry in its
feature registry (e.g. `features.yml`). For a new epic you'll usually need to
propose **new** feature entries — this is a judgment call, not mechanical, so:

1. Read [references/feature-taxonomy.md](references/feature-taxonomy.md) for how
   to group stories into features (prefer the PRD's own named flows/SOPs when it
   has them; fall back to the Module column) and when to cross-tag a story under
   two features.
2. Build a compact **Story → feature tag(s)** table and a **new feature registry
   entries** draft (name + one-line description each).
3. **Show both to the user and get explicit confirmation before writing anything.**
   A wrong taxonomy call written straight to the repo means a follow-up PR just to
   fix grouping — cheaper to catch it here. Also confirm the status-tag call now
   (see Step 5) in the same review pass so there's one approval round-trip, not two.

## Step 5 — Draft tag conventions

Unless the target repo's own status lifecycle says otherwise:

- **Every AC in a not-yet-shipped epic gets the repo's "not live yet" tag** (e.g.
  `@draft`) — whole epic, not per-story, even if some child Stories happen to be
  Done in Jira. The site should never report unbuilt behavior as current. Only
  drop the tag epic-wide once the epic actually ships, per the repo's own
  golden-rule-style immutability constraint (if it has one) — that's a separate,
  later edit, not part of this sync.
- **One continuous AC-id counter across the whole epic file**, not restarted per
  story — match whatever numbering scheme the repo's existing epic files already
  use (check a real example file, don't assume).
- **Add a traceability comment pointing at the originating Story** if the repo's
  CONTRIBUTING allows a trailing ticket comment. Place it exactly where
  [references/gherkin-parsing-notes.md](references/gherkin-parsing-notes.md) says
  it's safe for the repo's Gherkin parser — a naive placement can silently corrupt
  a rendered title instead of failing loud, so verify empirically for a new repo/
  parser combination rather than assuming this note's placement always transfers.

## Step 6 — Generate, review, then write

Run `scripts/parse-requirement-table.js` (or the equivalent for the target repo's
exact table schema) with the confirmed feature map to produce the draft
`.feature` file text and the feature-registry diff. Show the user:

- Scenario/AC count and per-story breakdown
- A couple of sample rendered scenarios (not necessarily all of them)
- The feature-registry diff

Get a go-ahead, then write the `.feature` file and the feature-registry file to
disk.

## Step 7 — Build, test, verify

Run the repo's own build/validate/test commands (from Step 1) and confirm a clean
result — no warnings, all tests passing. Then spot-check the generated output for
the new epic (epic page, one or two AC hub pages, and the features index) to
confirm the status/feature tags rendered as intended. **Never commit the generated
output directory** — it's gitignored for a reason.

On Windows specifically, see
[references/gherkin-parsing-notes.md](references/gherkin-parsing-notes.md) for two
build-environment gotchas (a `python`/`python3` PATH shim that doesn't resolve, and
a console-encoding crash in tools that print a `→`-style arrow) that look like
content bugs but aren't.

## Step 8 — Commit locally, stop before push

Stage only the new/changed spec files (the `.feature` file, the feature registry) —
never the generated output. Follow the repo's own git workflow rules from Step 1
(branch requirement, commit message style). **Commit locally and stop.** Do not
push and do not open a PR unless the user explicitly asks for it in this
conversation — treat each request as scoped to itself, not standing permission for
future syncs.

## Step 9 — Report back

Summarize: files changed, total AC/scenario count, build+test result, and any
judgment calls made (taxonomy, draft tagging, comment placement) so the user can
course-correct before this reaches a PR.

## Quick reference

```
# 1. Confirm epic's stories
searchJiraIssuesUsingJql(cloudId, jql: "parent = <EPIC-KEY> ORDER BY key ASC", fields: [...])

# 2. Fetch PRD, extract requirement table
getConfluencePage(cloudId, pageId, contentFormat: "markdown")
node scripts/parse-requirement-table.js <prd-body.md> <EPIC-KEY> <feature-map.json> [--no-draft]

# 3. Build + validate (target repo's own commands — example, confirm against its README)
python3 build.py   # or: py build.py   (Windows, no python3 on PATH)
python3 -m pytest

# 4. Commit locally only
git add epics/<EPIC>/acceptance-criteria.feature features.yml
git commit -m "..."   # never push without being asked
```
