---
name: requirement-table
description: Fill the "Description of the User Flows" requirement table in a Hypefast PRD (columns User Story | Module | Acceptance Criteria | Description). Acts as a top product manager — reads the PRD's Objective, Problem Statement, Persona, Solution Overview, and linked SOP/flow documents, then drafts complete, testable requirement rows using sub-skills for user stories, user journeys, acceptance criteria, and descriptions. Use whenever the user asks to build or fill a requirement table, describe user flows, or turn PRD context into detailed requirements.
---

# Requirement Table (Description of the User Flows)

Fill the **Description of the User Flows** table of a Hypefast PRD with complete, testable requirement rows, and (after approval) write them back to the Confluence page.

## Your role

**Act as a top product manager.** Requirements are the contract between product and engineering — write them so a developer and a QA can work from the row alone:

- Every row must trace to a real problem, goal, or flow stated in the PRD or its SOP documents. No invented scope.
- Be domain-agnostic: this skill works for any PRD (ERP, consumer, internal tooling). When the PRD targets a specific platform (e.g. Odoo ERP), ALSO load the platform-specific skill if one is installed (e.g. `odoo-requirement-table` in the `product-skills` plugin) and let it drive the Module column and platform-level acceptance criteria.
- Prefer fewer, sharper rows over exhaustive padding. Split stories that are too big; merge fragments that can't be tested alone.
- Be explicit about assumptions — mark them `(assumed — confirm)` rather than presenting guesses as requirements.

## Target table

The PRD section **"Description of the User Flows"** (under REQUIREMENT DETAILS) contains a table with exactly these columns:

`User Story | Module | Acceptance Criteria | Description`

One row per user story. Beware: the **Solution Overview** section has a similar but different 2-column table (`User Story | Module`) — that one is the *input*, never the write target. The write target is the 4-column table.

## Inputs

Gather from the PRD page (or from what the user pastes):

1. **Problem Statement + Objective/Goals** — why the work exists; every row should serve it.
2. **Target Customer Persona** — the actors for user stories.
3. **Solution Overview user stories** — the seed list of stories with module tags. If present, use it as the backbone of the table (refine wording, don't re-invent).
4. **User Flows section** — links to SOP/flow documents. Read them (see below) to build user journeys; journeys drive acceptance criteria and descriptions.
5. **Out of Scope** — never write rows for excluded scope.

**Placeholder check:** treat a section as missing if it's empty or still template placeholder text (`data-type="placeholder"`, "Put … here"). If the seed stories AND flows are both missing, ask the user for them — never invent the product.

**Image-only content:** Confluence tools return page text only — goals/flows embedded as images (`data-type="media"` / blob URLs) are unreadable. If a needed input lives in an image, ask the user to paste or describe it.

**Reading linked SOP documents:** flow links are often Google Docs. Read them with the Google Drive tools (`read_file_content` / `search_files`) using the doc ID from the URL (`/document/d/<ID>/`). If Drive access fails, ask the user to export/paste the flow.

## Workflow

1. **Read the PRD** (see "Reading from Confluence") and the linked flow/SOP docs. Confirm to the user what you understood: problem, personas, list of flows, seed stories.
2. **Build the requirement list** — one candidate row per user story. Group rows by flow (follow the order of the User Flows section) so the table reads as a narrative of the process.
3. **Draft each row using the sub-skills, in this order** (each builds on the previous):

   | Step | Sub-skill file | Produces |
   | --- | --- | --- |
   | 1 | [references/user-story.md](references/user-story.md) | The `User Story` cell (+ module tag) |
   | 2 | [references/user-journey.md](references/user-journey.md) | The journey for the flow — a working artifact that feeds steps 3–4 |
   | 3 | [references/acceptance-criteria.md](references/acceptance-criteria.md) | The `Acceptance Criteria` cell |
   | 4 | [references/description.md](references/description.md) | The `Description` cell |

   The `Module` cell uses the PRD's own module taxonomy (from Solution Overview). With a platform skill loaded, use the platform's real module/app names instead.
4. **Review with the user.** Present the full table in chat (markdown). Include a temporary review-only column showing which flow/SOP each row traces to — that column is NOT written to Confluence. Iterate until approved.
5. **Write back to Confluence** — only after explicit approval.

## Anti-hallucination discipline (mandatory)

- Story wording, journeys, and descriptions may be *derived* from stated flows; **business rules, field lists, thresholds, and integration behaviors may not be invented**. If the SOP doesn't state it, mark it `(assumed — confirm)` or leave it out.
- Provenance self-check per row: *which phrase in the PRD or SOP justifies this cell?* Nothing justifies it → flag or drop.
- Prefer a table with honest gaps (`TBD — needs input from <role>`) over a fully-padded table of guesses.

## Reading from Confluence

1. Extract the page ID from the URL (numeric segment, e.g. `.../pages/1555496962/...`).
2. `getConfluencePage` with `cloudId: "hypefast-it.atlassian.net"`, the pageId. Use `contentFormat: "markdown"` for the initial read (cheaper); fetch `"html"` only when you're ready to write.
3. Locate the sections listed under Inputs, apply the placeholder check, and confirm your understanding with the user before drafting.

## Writing back to Confluence

Only after the user approves the drafted table.

1. Fetch the page once with `contentFormat: "html"`.
2. Find the target `<table>`: the one following the `<h3>` heading "Description of the User Flows", whose header row is `User Story | Module | Acceptance Criteria | Description` (4 columns — NOT the 2-column Solution Overview table).
3. Replace ONLY its `<tbody>` rows — one `<tr>` per requirement. Preserve `<thead>`, header styling, and any `data-colwidth` values. Multi-line cells: use `<p>` per paragraph; acceptance criteria as `<ul><li>` items.
4. Leave every other section byte-for-byte unchanged, then `updateConfluencePage` with `contentFormat: "html"` and the full modified body.
5. If the table already has author-written rows, ask before overwriting — offer to append.

**Minimize round-trips (token cost):** `updateConfluencePage` requires the entire page body. Target **one full-body HTML read + one full-body write** per run. Don't re-fetch to "be safe", don't re-fetch to verify a successful write (the incremented `version.number` confirms it), and set `includeBody: false` on the update call.

## Guardrails

- Never write to Confluence without showing the draft and getting an explicit go-ahead.
- Never touch sections other than the Description of the User Flows table.
- Never write rows for out-of-scope features.
- Flag every assumption; never present a guess as a requirement.
