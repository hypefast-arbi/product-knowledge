---
name: jira-create-ticket
description: Create a new Jira issue (Task, Story, Bug, or Epic) via the Atlassian Rovo MCP server. Use whenever the user asks to create a Jira ticket/issue/story/task/bug/epic, add something to a backlog, file a new work item, or turn a PRD into an epic. Handles issue-type selection, field gathering, PRD-sourced epics (including the image-only OBJECTIVE gap), and linking a created epic back to its source PRD. Organization-agnostic — resolves the site/cloudId/project at runtime.

---

# Create a Jira Issue (Task / Story / Bug / Epic)

Create a new issue on a Jira site using the Atlassian Rovo MCP tools. A new issue
lands in the project backlog by default (no sprint assigned). This skill covers
both ordinary backlog items (Task/Story/Bug) and Epics — including epics sourced
from a Confluence PRD. It is **organization-agnostic** — it hardcodes no site,
cloudId, or project.

## Resolve your Atlassian config

Get the site + cloudId in this order:

1. **Workspace template first.** If your project knowledge includes an account
   template (e.g. Hypefast's `hypefast-atlassian` skill in the companion
   `projects` repo), use the site, cloudId, and project/board list it records —
   skip discovery.
2. **Otherwise discover.** `getAccessibleAtlassianResources` returns your
   site(s) and cloudId.
3. **If ambiguous** (more than one site, or none given), ask the user.

The create tool is `mcp__claude_ai_Atlassian_Rovo__createJiraIssue`. For epics
sourced from a PRD you also need the Confluence tools `getConfluencePage` /
`updateConfluencePage`. These tools are deferred — load what you need first with
`ToolSearch` (`select:mcp__claude_ai_Atlassian_Rovo__createJiraIssue` or add the
Confluence tools when doing PRD work).

## Resolve the project

Use the project the user names. If a workspace template lists known projects
(key + board), use it to recognize/confirm the target. Otherwise — or if the
user names a project not in the template — resolve/confirm it with
`mcp__claude_ai_Atlassian_Rovo__getVisibleJiraProjects` (use `searchString`), and
confirm the desired issue type is present in that project's `issueTypes`.

## Step 1 — Decide the issue type

Ask if the user didn't say, or infer from context:

| Issue type | When |
| --- | --- |
| **Task** | Default for generic work with no natural user-facing framing. |
| **Story** | A user-facing feature — has (or can be given) a "As a … I want … so that …" shape. |
| **Bug** | A defect. |
| **Epic** | A large PRD-level body of work that will be broken into stories/tasks. Almost always sourced from a Confluence PRD — see Step 2b. |

Use `AskUserQuestion` with Task / Story / Bug / Epic when ambiguous.

## Step 2a — Gather inputs for Task / Story / Bug

Ask **only** for what's missing — don't re-ask for anything already in the user's
prompt.

- **Title / Summary** — required, the only thing you genuinely need.
- **Description** — optional but recommended; offer to draft one if missing.
- Optional fields the user mentioned: assignee, labels, story points, parent
  epic, dates.

### Mapping "title" / "summary" / "description" → Jira fields

Jira has only **two** text fields: *Summary* (single-line title) and
*Description* (body). Users sometimes supply three labelled values — **title**,
**summary**, and **description**. Map them deterministically:

| User says | Goes to Jira field |
| --- | --- |
| **title** | `summary` (the Jira Summary field) |
| **summary** | first line of `description`, rendered **bold** as a lead-in |
| **description** | the rest of `description`, after a blank line |

So `title: TEST DESC / summary: xxxxxx / description: abc…` becomes:
- Jira **summary** = `TEST DESC`
- Jira **description** (markdown) = `**xxxxxx**\n\nabc…`

Rules:
- Title only, no summary/description → use it as Jira Summary, leave Description
  empty (or offer to draft one).
- Summary but no title → treat the summary as the title; don't create an empty
  title.
- Never silently drop any of the three values — everything typed must land in
  either Summary or Description.

### Fields reference (team-managed project example)

| Field | Required? | How to resolve |
| --- | --- | --- |
| Project | ✅ | Project key, e.g. `PROJ`. |
| Issue type | ✅ | `Task` / `Story` / `Bug`. |
| Summary | ✅ | The ticket title. |
| Description | optional | Free text / Markdown. |
| Assignee | optional | Resolve name → accountId with `lookupJiraAccountId`. |
| Labels | optional | Array of strings, e.g. `["backend","ai"]`. |
| Story point estimate | optional | `customfield_10016` (number). |
| Start date | optional | `customfield_10015` (YYYY-MM-DD). |
| Due date | optional | `duedate` (YYYY-MM-DD). |
| Parent (Epic) | optional | `parent` = epic issue key, e.g. `PROJ-12`. |

Other projects may expose different/extra fields (e.g. Priority) — check with
`getJiraIssueTypeMetaWithFields` if unsure.

## Step 2b — Gather inputs for Epic

- **From a Confluence PRD (common case):**
  - Fetch the page with `getConfluencePage` (`contentFormat: "markdown"`).
  - **Epic name** = the PRD page **title**, with any leading tag prefix like
    `[2026][PRD]` **stripped** — e.g. page title
    `[2026][PRD] Acme Billing Revamp` → epic summary
    `Acme Billing Revamp`. Keep the rest of the title as-is.
  - **Epic description** = the PRD's **OBJECTIVE** content.
    Some PRD templates render the OBJECTIVE goal statement as **images**,
    unreadable via API (your workspace template may flag this — e.g. Hypefast's
    `hypefast-atlassian` skill does). When that happens, the readable **Problem
    Statement** subsection just below it is usually the best textual proxy.
    Confirm with the user via `AskUserQuestion` before creating the issue
    (recommended option = Problem Statement text; other = user pastes the real
    objective). Never fetch external files/images to fill this gap — PRD page
    text only.
- **From the user directly:** use the given name/description as-is; still ask
  for whatever's missing.
- Confirm the target project/board and that `Epic` appears in its issue types.

## Step 2c — Deriving a title when the source has no title (e.g. bulk Stories from a PRD)

A PRD's user-story tables (Solution Overview, Description of the User Flows)
give the story sentence itself but rarely a short title. When asked to turn N
user stories into N Story tickets, derive each title like this:

1. **Prefer mining an existing scenario label.** If the row's Acceptance
   Criteria already has Gherkin scenarios in the
   `Scenario: <capability> - <label>` format (see
   [[gherkin-template-preference]]), the `<label>` segment after the dash is
   usually already a good short title — reuse it (capitalized) instead of
   inventing a new phrase. When extracting this with a script, require a
   space-hyphen-space separator (` - `), not a bare `-`, or the regex will
   false-match inside hyphenated words like "auto-validate".
2. **Otherwise, condense the "I want to …" clause** of the user story into a
   short imperative phrase (e.g. "As a merchandiser, I want to create a new BOM
   request…" → "Create BOM request").
3. **Disambiguate before finalizing.** Extracted/condensed titles frequently
   collide across rows (e.g. two different rows both reducing to "Create
   request", or a restriction row reducing to "Allowed role" regardless of
   which object it restricts). Scan the full title list for duplicates or
   vague titles and sharpen them using the row's Module/object
   (e.g. "Request production purchase order" vs. "Request raw material
   purchase order"; "Restrict BOM edit access" vs. "Restrict manufacturing
   order edit access").
4. **Show the full title list for confirmation** before bulk-creating —
   titles are inherently a judgment call, and creating dozens of tickets is
   costly to redo. A quick compact review table is enough; don't ask
   question-by-question for 30+ rows.
5. Unless told otherwise, the ticket **Description is the user-story sentence
   verbatim and nothing else** — no acceptance criteria, no bold lead-in, no
   extra commentary appended.

## Step 3 — Create the issue inline (single) or via a subagent (bulk)

For **one** issue, call the tool directly yourself — **do not delegate to a
subagent**. A subagent re-pays a fixed startup tax (its own system prompt +
reloading the ~50 Atlassian MCP tool schemas, ~14k tokens) to avoid the tool's
~750-token verbose response — a net loss for one-off issue creation. Inline is
the cheapest available method.

For a **batch** (e.g. N Stories generated from a PRD's user-story table), the
calculus flips: the subagent's fixed startup tax is paid once, while inlining
N calls yourself means N × ~750 tokens of verbose tool-response noise land in
your own context. Instead:
1. Build the finalized per-ticket data (title, description, assignee, any
   parent link) as a small script/JSON file — don't hand-construct it row by
   row in prose.
2. Delegate the whole batch to one subagent: "read this file, call
   `createJiraIssue` once per entry with these exact fields, continue past
   individual failures, report back only a compact result table." Keep the
   ~750-token-per-call responses out of your own context entirely.

Call `createJiraIssue` with:
- `cloudId`: your resolved cloudId (from the workspace template or discovery)
- `projectKey`: the resolved project key
- `issueTypeName`: `"Task"` / `"Story"` / `"Bug"` / `"Epic"`
- `summary`: per the mapping/derivation rules above
- `description`: per the mapping/derivation rules above (`contentFormat: "markdown"`)
- `assignee_account_id`: optional, resolved accountId
- `additional_fields`: optional JSON for everything else, e.g.
  `{"labels": ["ai"], "customfield_10016": 3, "parent": {"key": "PROJ-12"}}`
  — the `parent` field (system field, type `issuelink`) links a Story/Task to
  its Epic on **both** team-managed and classic/company-managed projects. If
  unsure whether a given project exposes it, check with
  `getJiraIssueTypeMetaWithFields`.

The tool echoes back a large object (avatars, status metadata, schema). Ignore
the noise — you only need `issues.nodes[0].key` and `webUrl`.

## Step 4 — Epic-only: link the epic back to its source PRD

If the epic was created from a Confluence PRD, the PRD's own metadata table near
the top has an **Epic** row — usually a placeholder like *"Create Jira Epic and
put it here"*. Update it with a link to the new epic, but **ask before editing
the PRD page** — don't do it silently.

Per [[confluence-edit-token-optimization]], edit large Confluence pages cheaply:
1. Fetch the page once (`getConfluencePage`, `contentFormat: "html"`) — expect
   large output; it'll likely be saved to a tool-result file rather than shown
   inline.
2. Do the actual edit with a script (Node.js `fs.readFileSync` + exact string
   `.replace()` on the placeholder row), not by describing the change in prose
   to a subagent and letting it regenerate HTML. Verify the old string occurs
   exactly once before replacing, so a mismatch fails loud instead of silently
   corrupting content.
3. Delegate only the final `updateConfluencePage` push to a subagent (or do it
   inline if the body fits): its job is "read this exact file, call the tool
   with this exact body," nothing else — keep the ~100k-char body out of your
   own context.
4. Link text convention: `<a href="https://<your-site>.atlassian.net/browse/<KEY>"><KEY>: <epic summary></a>`.

## Step 5 — Report back

Give the user the issue key, summary, issue type, project, and the browse URL:
`https://<your-site>.atlassian.net/browse/<ISSUE-KEY>`. For epics linked back to
a PRD, confirm the PRD page was updated (and its new version).

## Quick reference

```
ToolSearch select:mcp__claude_ai_Atlassian_Rovo__createJiraIssue
createJiraIssue(
  cloudId="<RESOLVED_CLOUD_ID>",
  projectKey="<PROJECT_KEY>",
  issueTypeName="Task",       # Task | Story | Bug | Epic
  summary="...",
  description="...",
  contentFormat="markdown",
  additional_fields={"labels": ["..."]}   # optional
)
```
