---
name: jira-create-epic
description: Create a new Epic in a Jira project on the hypefast-it Atlassian site via the Atlassian Rovo MCP server, typically sourced from a Confluence PRD. Use whenever the user asks to create a Jira epic, or to turn a PRD into an epic. Handles resolving the project/board, deriving the epic name and description from a PRD page, and the image-only OBJECTIVE section gap.
---

# Create a Jira Epic

Create a new **Epic**-type issue in a Jira project on the **hypefast-it** Atlassian
site using the Atlassian Rovo MCP tools. Epics here are most often created from a
Confluence PRD page, but the skill also covers a plain manually-described epic.

## Fixed environment values

- **Site:** `hypefast-it.atlassian.net`
- **cloudId:** `a6661705-a333-4449-8206-6a19abf3d70f`
- **Create tool:** `mcp__claude_ai_Atlassian_Rovo__createJiraIssue`
- **Read tool (for PRD sourcing):** `mcp__claude_ai_Atlassian_Rovo__getConfluencePage`

These tools are deferred — load them first with `ToolSearch`
(`select:mcp__claude_ai_Atlassian_Rovo__createJiraIssue,mcp__claude_ai_Atlassian_Rovo__getConfluencePage`).
If the cloudId ever fails, re-discover it with `getAccessibleAtlassianResources`.

## Known projects

| Project key | Name | Board URL |
| --- | --- | --- |
| `ERP` | ERP (Odoo, Hypefast/Bohopanna) | https://hypefast-it.atlassian.net/jira/software/c/projects/ERP/boards/98 |
| `ASP` | AI Stuff Playground | https://hypefast-it.atlassian.net/jira/software/projects/ASP/boards/97 |

If the user names a different project or board, resolve / confirm it with
`mcp__claude_ai_Atlassian_Rovo__getVisibleJiraProjects` (use `searchString`), and
confirm the `Epic` issue type is present in that project's `issueTypes`.

## Workflow

### 1. Determine the source

- **From a PRD (Confluence page)** — the common case. Fetch the page with
  `getConfluencePage` (`contentFormat: "markdown"`).
  - **Epic name** = the PRD page **title**, verbatim (e.g.
    `[2026][PRD] Bohopanna ERP - Purchase and Production`).
  - **Epic description** = the PRD's **OBJECTIVE** content — the problem/goal the
    PRD exists to solve.
- **From the user directly** — the user gives a name and/or description inline. Use
  those as-is; still ask for whatever's missing (see below).

Per [[prd-only-sourcing]]: never fetch external files (linked Google Docs, SOPs) or
images to fill this in — PRD page text only.

### 2. Handle the image-only OBJECTIVE gap

Hypefast's PRD template renders the OBJECTIVE section's actual goal statement as
**images**, which the API cannot read (see [[hypefast-skill-repos]]). Below the
images there is usually a readable **Problem Statement** subsection — this is the
best textual proxy for the objective.

Do **not** silently guess or skip the description. Confirm with the user via
`AskUserQuestion` (recommended option = the Problem Statement text; other option =
let the user type/paste the real objective) before creating the issue — the same
rule as any other PRD-image gap.

### 3. Resolve the project/board

If not already known from context, confirm the project key with the user or via
`getVisibleJiraProjects`. Verify `Epic` appears in that project's issue types.

### 4. Create the issue — call `createJiraIssue` inline

Call the tool directly yourself (same rationale as jira-create-backlog-ticket: a
subagent re-pays a fixed MCP-schema-loading tax that isn't worth it for one issue).

Call `createJiraIssue` with:
- `cloudId`: `a6661705-a333-4449-8206-6a19abf3d70f`
- `projectKey`: e.g. `"ERP"`
- `issueTypeName`: `"Epic"`
- `summary`: the epic name (PRD title, or user-given name)
- `description`: the objective / problem statement text
- `contentFormat`: `"markdown"`
- `additional_fields`: optional, e.g. `{"labels": ["prd"]}`

The tool echoes back a large object (avatars, status metadata, schema). Ignore the
noise — you only need `issues.nodes[0].key` and `webUrl`.

### 5. Report back

Give the user the epic key, name, project, and the browse URL:
`https://hypefast-it.atlassian.net/browse/<ISSUE-KEY>`.

If the epic was sourced from a PRD, also note that the PRD's own "Epic" metadata
row (near the top of the page, often a placeholder saying "Create Jira Epic and
put it here") may need updating with this link — ask before editing the PRD page,
don't do it silently.

## Quick reference

```
ToolSearch select:mcp__claude_ai_Atlassian_Rovo__createJiraIssue,mcp__claude_ai_Atlassian_Rovo__getConfluencePage
createJiraIssue(
  cloudId="a6661705-a333-4449-8206-6a19abf3d70f",
  projectKey="ERP",
  issueTypeName="Epic",
  summary="<PRD title>",
  description="<objective / problem statement text>",
  contentFormat="markdown"
)
```
