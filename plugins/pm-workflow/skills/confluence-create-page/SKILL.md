---
name: confluence-create-page
description: Create a new page in a Confluence space (hypefast-it) via the Atlassian Rovo MCP server. Use whenever the user asks to create a Confluence page, add a page under a parent page, make a PRD page, or create a doc in a Confluence space. Handles asking for a missing page name and choosing between a blank page or a PRD-templated page.
---

# Create a Confluence Page

Create a new page in the **hypefast-it** Confluence site using the Atlassian Rovo MCP tools.

## Fixed environment values

- **Site:** `hypefast-it.atlassian.net`
- **cloudId:** `a6661705-a333-4449-8206-6a19abf3d70f`
- **Create tool:** `mcp__claude_ai_Atlassian_Rovo__createConfluencePage`

If the cloudId ever fails, re-discover it with `mcp__claude_ai_Atlassian_Rovo__getAccessibleAtlassianResources`. These tools are deferred — load them first with `ToolSearch` (`select:mcp__claude_ai_Atlassian_Rovo__createConfluencePage`, etc.).

## Workflow

### 1. Gather the required inputs

Before creating, you need three things. Ask **only** for what's missing — don't re-ask for anything the user already gave in their prompt.

| Input | How to resolve | If missing |
| --- | --- | --- |
| **Page title** | From the user's prompt | **Ask the user for the name** (and nothing else) |
| **Page type** | blank or PRD — from the user's prompt | **Ask: "Blank page or PRD page?"** |
| **Location** | Parent page and/or space | See step 2 |

Use the `AskUserQuestion` tool for the page-type choice (options: "Blank page", "PRD page"). Only ask if the user didn't already make it clear. If the user just says "create a page" with a name and no type, default behavior is to **ask** blank vs PRD; if they say "create a blank page" use blank without asking; if they say "PRD" use PRD without asking.

### 2. Resolve the location

- **If the user gives a parent page URL** (e.g. `.../spaces/TECHPRODUC/pages/1546977300/ERP`):
  - `parentId` = the numeric ID in the URL (`1546977300`).
  - `spaceId` = resolve from the space key in the URL (`TECHPRODUC`) — see space resolution below.
- **If the user gives only a space** (no parent): create at the space root — set `spaceId`, omit `parentId`.
- **If neither is given:** ask which space (and optionally parent page) the page should go under.

**Resolve a space key → spaceId** with `mcp__claude_ai_Atlassian_Rovo__getConfluenceSpaces` using the `keys` filter (do NOT list all spaces — the full list is too large):
```
getConfluenceSpaces(cloudId, keys: "TECHPRODUC")  →  results[0].id  (e.g. "33166")
```
Known: `TECHPRODUC` (Tech-Product) → spaceId `33166`.

### 3. Create the page

The parameters for `createConfluencePage` are:
- `cloudId`: `a6661705-a333-4449-8206-6a19abf3d70f`
- `spaceId`: resolved space ID
- `parentId`: parent page ID (omit for space root)
- `title`: the page title
- `contentFormat`: `"html"`
- `body`: blank or PRD body (below)
- `status`: `"current"` to publish (default), or `"draft"` if the user wants a draft

**How you call it depends on the page type — for token efficiency:**

- **Blank page** → call `createConfluencePage` **inline yourself**. The body is a
  single empty paragraph, so there's nothing bulky to isolate.

- **PRD page** → **DELEGATE to a subagent** via the `Agent` tool (`subagent_type:
  "general-purpose"`). The PRD template is ~20k tokens of HTML, and it would
  otherwise pass through your context three times (reading the file + sending the
  body + the tool echoing the whole stored page back). Spawning a subagent
  quarantines all of that — your context only sees the returned URL.

  Pass the subagent a **self-contained** prompt (it starts fresh, without this
  skill loaded). Give it the resolved values and tell it to return only a small
  result. Template prompt:

  ```
  Create a Confluence PRD page, then report back ONLY the result fields below — do
  NOT echo the page body.

  Steps:
  1. Read the template file VERBATIM: /Users/hypefast/.claude/skills/confluence-create-page/prd-template.html
  2. Load the create tool: ToolSearch select:mcp__claude_ai_Atlassian_Rovo__createConfluencePage
  3. Call mcp__claude_ai_Atlassian_Rovo__createConfluencePage with:
       cloudId="a6661705-a333-4449-8206-6a19abf3d70f"
       spaceId="<RESOLVED_SPACE_ID>"
       parentId="<PARENT_ID or omit>"
       title="<TITLE>"
       contentFormat="html"
       status="<current|draft>"
       body=<the exact, unmodified contents of prd-template.html>
  4. Return ONLY: page title, page ID, and the value of _links.webui.
     Do not include the page body or storage HTML in your response.
  ```

  Substitute the resolved title, spaceId, parentId, and status before sending.

### 4. Report back

Give the user the page title, parent, space, page ID, and the page URL (the
`_links.webui` value prefixed with `https://hypefast-it.atlassian.net/wiki`). For a
PRD page, these come back from the subagent's result — relay them.

## Bodies

### Blank page

A minimal empty page — just a single empty paragraph:
```html
<p></p>
```

### PRD page

**ALWAYS** use the official Hypefast PRD template stored in this skill at
`prd-template.html`, passed as the `body` **exactly** as-is (with `contentFormat:
"html"`). This is the **only** PRD template — never use any built-in/improvised
scaffold. Per step 3, the **subagent** reads this file and makes the call — you
should NOT read the template into your own context.

Title convention for PRDs: `[YYYY][PRD]<Project Name>`.

The template is the canonical "Project Documentation and Requirements Overview"
structure: a Page Properties panel (Document status / author / Epic / Designer /
Developer / QA / Figma URL), a Section Shortcut TOC, then **OBJECTIVE** (Problem
Statement, Target Customer Persona, Success Criteria, Solution Overview),
**REQUIREMENT DETAILS** (Display Requirement, User Flows, Access Restrictions,
Activity Log, Analytics Requirements, Proposed Release Plan, Third-Party
Integrations), **GO-TO-MARKET CHECKLIST**, **APPENDIX** (incl. Design
Reusability), and **SUPPORTERS**.

Use it verbatim — do not strip the macros (Page Properties, TOC, Jira), the
placeholder spans, or the table styling. The user fills the placeholders in
Confluence after the page is created.

> Source of truth: this template was captured from the Confluence page
> "Project Documentation and Requirements Overview" (TECHPRODUC, page
> `1554907138`). If that page is updated, re-fetch it with
> `getConfluencePage(cloudId, pageId, contentFormat:"html")` and overwrite
> `prd-template.html`.

## Quick reference

**Blank page — call inline:**
```
ToolSearch select:mcp__claude_ai_Atlassian_Rovo__createConfluencePage
createConfluencePage(
  cloudId="a6661705-a333-4449-8206-6a19abf3d70f",
  spaceId="33166",            # TECHPRODUC
  parentId="1546977300",      # optional
  title="...",
  contentFormat="html",
  body="<p></p>",
  status="current"
)
```

**PRD page — delegate (keeps the ~20k-token template out of your context):**
```
Agent(subagent_type="general-purpose", prompt=<self-contained prompt from step 3>)
  → reads prd-template.html, calls createConfluencePage, returns only title + ID + webui URL
```
