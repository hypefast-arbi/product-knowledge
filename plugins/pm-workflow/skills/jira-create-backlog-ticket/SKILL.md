---
name: jira-create-backlog-ticket
description: Create a new backlog ticket (issue) in a Jira project on the hypefast-it Atlassian site via the Atlassian Rovo MCP server. Use whenever the user asks to create a Jira ticket/issue/story/task/bug, add something to a backlog, or file a new work item. Handles asking for the missing summary, choosing the issue type, and optional fields like description, assignee, labels, story points, and parent epic.
---

# Create a Jira Backlog Ticket

Create a new issue in a Jira project on the **hypefast-it** Atlassian site using the
Atlassian Rovo MCP tools. A new issue lands in the project backlog by default
(no sprint assigned), which is exactly what "backlog ticket" means.

## Fixed environment values

- **Site:** `hypefast-it.atlassian.net`
- **cloudId:** `a6661705-a333-4449-8206-6a19abf3d70f`
- **Create tool:** `mcp__claude_ai_Atlassian_Rovo__createJiraIssue`

These tools are deferred — load them first with `ToolSearch`
(`select:mcp__claude_ai_Atlassian_Rovo__createJiraIssue`). If the cloudId ever
fails, re-discover it with `mcp__claude_ai_Atlassian_Rovo__getAccessibleAtlassianResources`.

## Known projects

| Project key | Name | Board URL |
| --- | --- | --- |
| `ASP` | AI Stuff Playground | https://hypefast-it.atlassian.net/jira/software/projects/ASP/boards/97 |

If the user names a different project, resolve / confirm it with
`mcp__claude_ai_Atlassian_Rovo__getVisibleJiraProjects` (use `searchString`).

## Fields

In the ASP project (a team-managed software project), the issue create screen has
only **three required fields**, and two of them are fixed/derived:

| Field | Required? | How to resolve |
| --- | --- | --- |
| **Project** | ✅ required | The project key (e.g. `ASP`). Fixed per request. |
| **Issue type** | ✅ required | One of `Task`, `Story`, `Bug`, `Epic`. Ask if unclear; default to **Task** for generic work, **Story** for a user-facing feature, **Bug** for a defect. |
| **Summary** | ✅ required | The ticket title — **the only thing you genuinely need from the user.** |
| Description | optional | Free text / Markdown. Strongly recommended. |
| Assignee | optional | Resolve a name → accountId with `lookupJiraAccountId`. |
| Labels | optional | Array of strings, e.g. `["backend","ai"]`. |
| Story point estimate | optional | `customfield_10016` (number). |
| Start date | optional | `customfield_10015` (YYYY-MM-DD). |
| Due date | optional | `duedate` (YYYY-MM-DD). |
| Parent (Epic) | optional | `parent` = epic issue key, e.g. `ASP-12`. |
| Priority | optional | Not on the ASP create screen — skip unless another project exposes it. |

So: **the minimum to create a ticket is the Summary.** Everything else is optional.
Always confirm the issue type, and ask for a description if the user gave none —
a one-line title alone makes a poor backlog item.

### Mapping "title" / "summary" / "description" → Jira fields

Jira has only **two** text fields on this screen: *Summary* (a single-line title)
and *Description* (the body). Users here often supply three labelled values —
**title**, **summary**, and **description**. Map them deterministically:

| User says | Goes to Jira field |
| --- | --- |
| **title** | `summary` (the Jira Summary field — the single-line title) |
| **summary** | first line of `description`, rendered **bold** as a lead-in |
| **description** | the rest of `description`, after a blank line |

So a request `title: TEST DESC / summary: xxxxxx / description: abc…` becomes:
- Jira **summary** = `TEST DESC`
- Jira **description** (markdown) =
  ```
  **xxxxxx**

  abc…
  ```

Rules:
- If the user gives only a **title** (no summary/description), use it as the Jira
  Summary and leave Description empty (or offer to draft one).
- If the user gives a **summary** but no **title**, treat the summary as the title
  (Jira Summary) — don't create an empty title.
- Never silently drop any of the three values; everything the user typed must land
  in either Summary or Description.

## Workflow

### 1. Gather inputs

Ask **only** for what's missing — don't re-ask for anything in the user's prompt.

- **Title / Summary** — required. Apply the title/summary/description mapping
  above. If missing, ask for it.
- **Issue type** — if the user didn't say, ask (or apply the default rule above).
  Use `AskUserQuestion` with options Task / Story / Bug when it's ambiguous.
- **Description** — if missing, offer to draft one or ask for detail.
- Any optional fields the user mentioned (assignee, labels, points, parent, dates).

### 2. Create the issue — call `createJiraIssue` inline

Call the tool directly yourself. **Do not delegate to a subagent** — a subagent
re-pays a fixed startup tax (its own system prompt + reloading the ~50 Atlassian
MCP tool schemas, ~14k tokens) to avoid the tool's ~750-token verbose response.
That's a net loss for one-off ticket creation. Inline is the cheapest available
method; the only leaner option is a direct REST `curl` call, which needs a Jira
API token this MCP server doesn't expose.

Call `createJiraIssue` with:
- `cloudId`: `a6661705-a333-4449-8206-6a19abf3d70f`
- `projectKey`: e.g. `"ASP"`
- `issueTypeName`: `"Task"` / `"Story"` / `"Bug"` / `"Epic"`
- `summary`: the **title** (per the mapping table above)
- `description`: the body — the user's "summary" as a **bold** lead-in line, blank
  line, then their "description" (use `contentFormat: "markdown"`)
- `assignee_account_id`: optional, resolved accountId
- `additional_fields`: optional JSON for everything else, e.g.
  `{"labels": ["ai"], "customfield_10016": 3, "parent": {"key": "ASP-12"}}`

The tool echoes back a large object (avatars, status metadata, schema). Ignore the
noise — you only need `issues.nodes[0].key` and the `webUrl`.

### 3. Report back

Give the user the issue key, summary, issue type, project, and the browse URL:
`https://hypefast-it.atlassian.net/browse/<ISSUE-KEY>`.

## Quick reference

```
ToolSearch select:mcp__claude_ai_Atlassian_Rovo__createJiraIssue
createJiraIssue(
  cloudId="a6661705-a333-4449-8206-6a19abf3d70f",
  projectKey="ASP",
  issueTypeName="Task",
  summary="...",
  description="...",
  contentFormat="markdown",
  additional_fields={"labels": ["..."]}   # optional
)
```
