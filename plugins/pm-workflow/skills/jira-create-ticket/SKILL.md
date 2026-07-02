---
name: jira-create-ticket
description: Create a new Jira issue (Task, Story, Bug, or Epic) on the hypefast-it Atlassian site via the Atlassian Rovo MCP server. Use whenever the user asks to create a Jira ticket/issue/story/task/bug/epic, add something to a backlog, file a new work item, or turn a PRD into an epic. Handles issue-type selection, field gathering, PRD-sourced epics (including the image-only OBJECTIVE gap), and linking a created epic back to its source PRD.
---

# Create a Jira Issue (Task / Story / Bug / Epic)

Create a new issue on the **hypefast-it** Atlassian site using the Atlassian Rovo
MCP tools. A new issue lands in the project backlog by default (no sprint
assigned). This skill covers both ordinary backlog items (Task/Story/Bug) and
Epics — including epics sourced from a Confluence PRD.

## Fixed environment values

- **Site:** `hypefast-it.atlassian.net`
- **cloudId:** `a6661705-a333-4449-8206-6a19abf3d70f`
- **Create tool:** `mcp__claude_ai_Atlassian_Rovo__createJiraIssue`
- **Confluence read/write tools (epics sourced from a PRD only):**
  `getConfluencePage`, `updateConfluencePage`

These tools are deferred — load what you need first with `ToolSearch`
(`select:mcp__claude_ai_Atlassian_Rovo__createJiraIssue` or add the Confluence
tools when doing PRD work). If the cloudId ever fails, re-discover it with
`getAccessibleAtlassianResources`.

## Known projects

| Project key | Name | Board URL |
| --- | --- | --- |
| `ERP` | ERP (Odoo, Hypefast/Bohopanna) | https://hypefast-it.atlassian.net/jira/software/c/projects/ERP/boards/98 |
| `ASP` | AI Stuff Playground | https://hypefast-it.atlassian.net/jira/software/projects/ASP/boards/97 |

If the user names a different project, resolve / confirm it with
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

### Fields reference (ASP project example — team-managed)

| Field | Required? | How to resolve |
| --- | --- | --- |
| Project | ✅ | Project key, e.g. `ASP`. |
| Issue type | ✅ | `Task` / `Story` / `Bug`. |
| Summary | ✅ | The ticket title. |
| Description | optional | Free text / Markdown. |
| Assignee | optional | Resolve name → accountId with `lookupJiraAccountId`. |
| Labels | optional | Array of strings, e.g. `["backend","ai"]`. |
| Story point estimate | optional | `customfield_10016` (number). |
| Start date | optional | `customfield_10015` (YYYY-MM-DD). |
| Due date | optional | `duedate` (YYYY-MM-DD). |
| Parent (Epic) | optional | `parent` = epic issue key, e.g. `ASP-12`. |

Other projects may expose different/extra fields (e.g. Priority) — check with
`getJiraIssueTypeMetaWithFields` if unsure.

## Step 2b — Gather inputs for Epic

- **From a Confluence PRD (common case):**
  - Fetch the page with `getConfluencePage` (`contentFormat: "markdown"`).
  - **Epic name** = the PRD page **title**, with any leading tag prefix like
    `[2026][PRD]` **stripped** — e.g. page title
    `[2026][PRD] Bohopanna ERP - Purchase and Production` → epic summary
    `Bohopanna ERP - Purchase and Production`. Keep the rest of the title as-is.
  - **Epic description** = the PRD's **OBJECTIVE** content.
    Hypefast's PRD template renders the OBJECTIVE goal statement as **images**,
    unreadable via API (see [[hypefast-skill-repos]]). Below the images there is
    usually a readable **Problem Statement** subsection — the best textual proxy.
    Confirm with the user via `AskUserQuestion` before creating the issue
    (recommended option = Problem Statement text; other = user pastes the real
    objective). Never fetch external files/images to fill this gap — PRD page
    text only ([[prd-only-sourcing]]).
- **From the user directly:** use the given name/description as-is; still ask
  for whatever's missing.
- Confirm the target project/board and that `Epic` appears in its issue types.

## Step 3 — Create the issue inline

Call the tool directly yourself — **do not delegate to a subagent** for the
create call. A subagent re-pays a fixed startup tax (its own system prompt +
reloading the ~50 Atlassian MCP tool schemas, ~14k tokens) to avoid the tool's
~750-token verbose response — a net loss for one-off issue creation. Inline is
the cheapest available method.

Call `createJiraIssue` with:
- `cloudId`: `a6661705-a333-4449-8206-6a19abf3d70f`
- `projectKey`: e.g. `"ASP"` / `"ERP"`
- `issueTypeName`: `"Task"` / `"Story"` / `"Bug"` / `"Epic"`
- `summary`: per the mapping/derivation rules above
- `description`: per the mapping/derivation rules above (`contentFormat: "markdown"`)
- `assignee_account_id`: optional, resolved accountId
- `additional_fields`: optional JSON for everything else, e.g.
  `{"labels": ["ai"], "customfield_10016": 3, "parent": {"key": "ASP-12"}}`

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
4. Link text convention: `<a href="https://hypefast-it.atlassian.net/browse/<KEY>"><KEY>: <epic summary></a>`.

## Step 5 — Report back

Give the user the issue key, summary, issue type, project, and the browse URL:
`https://hypefast-it.atlassian.net/browse/<ISSUE-KEY>`. For epics linked back to
a PRD, confirm the PRD page was updated (and its new version).

## Quick reference

```
ToolSearch select:mcp__claude_ai_Atlassian_Rovo__createJiraIssue
createJiraIssue(
  cloudId="a6661705-a333-4449-8206-6a19abf3d70f",
  projectKey="ASP",           # or "ERP"
  issueTypeName="Task",       # Task | Story | Bug | Epic
  summary="...",
  description="...",
  contentFormat="markdown",
  additional_fields={"labels": ["..."]}   # optional
)
```
