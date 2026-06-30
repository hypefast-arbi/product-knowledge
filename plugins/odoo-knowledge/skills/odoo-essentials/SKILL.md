---
name: odoo-essentials
description: Functional knowledge of Odoo core essentials — stages, activities, reporting, search/filters, contacts, data import/export, and platform-wide features. Use whenever the user asks about Odoo basics, navigation, core workflows, or cross-module fundamentals.
---

# Odoo Essentials — Functional Knowledge

You are acting as a functional Odoo consultant. Use this knowledge to guide, configure, troubleshoot, and explain core Odoo platform features.

## Stages & Pipelines

Stages define progress steps in kanban-based modules (CRM, Project, Helpdesk, etc.).

- Stages can be **shared** (all teams see them) or **team-specific**
- Each stage can have: folded state, progress bar, rotting lead detection, linked email/SMS templates
- To configure: open any kanban view → click the gear icon on a column → Edit Stage
- **Rotting**: marks leads/tasks that have been in a stage too long without activity — set threshold in days

## Activities

Activities are scheduled follow-up actions attached to any Odoo record.

- **Types**: Email, Phone Call, Meeting, To-Do, Upload Document (customizable)
- **Schedule from**: Chatter bottom toolbar, Kanban activity dot, List view activity column, or Activity view (dedicated view showing all scheduled activities across records)
- **Custom activity types**: Settings → Technical → Activity Types — configure default delay, chaining to a next activity, decoration color
- **Meeting activities** open Calendar automatically
- Activities show as colored dots in kanban (green = today, orange = overdue, grey = future)

## Reporting

- **Graph view**: bar, line, pie charts — toggle measures from the Measures dropdown
- **Pivot view**: cross-tab analysis with row/column grouping, custom measures, expand/collapse groups
- **Comparison**: compare two time periods side by side (previous period, previous year)
- **Download**: export pivot as XLSX, graph as image
- Access via the top-right view switcher (list / kanban / graph / pivot icons)

## Search, Filter & Group

- **Search bar** (top): type to search across default fields; use the dropdown to target specific fields
- **Filters**: pre-built (My Records, Active, Starred) + custom date/field filters
- **Group By**: group records by any field — stack multiple groups
- **Favorites**: save a search+filter+group combination; optionally share with all users or set as default
- **Period filters**: This Week / Month / Quarter / Year quick selectors on date fields

## Rich-Text Editor (Chatter / Description fields)

- **Powerbox**: type `/` inside any rich-text field to open command menu — insert headings, lists, images, tables, separators, code blocks
- **Inline formatting**: bold (`Ctrl+B`), italic (`Ctrl+I`), underline (`Ctrl+U`), strikethrough
- **Media**: insert images by URL or upload; insert icons from icon library
- **Mentions**: `@name` mentions a user and sends notification; `#channel` links a discuss channel

## Contact Management

Contacts (`res.partner`) are shared across all modules.

| Field | Notes |
|---|---|
| Type | Individual or Company; set a Company parent for individuals |
| Tags | Free-form labels for segmentation |
| Sales | Salesperson, Sales Team, Pricelist, Payment Terms |
| Purchase | Currency, Payment Terms, delivery lead times |
| Accounting | Fiscal position, bank accounts, customer/vendor flags |
| Private info | Citizenship, private email, certificate level (for HR) |

- **Merge contacts**: Contacts list → select duplicates → Action → Merge
- **Deduplication**: Contacts → Action → Deduplicate Contacts — finds duplicates by name/email/phone
- **Archived contacts** remain linked to historical records but don't appear in dropdowns

## Data Import / Export

### Export
1. Open any list view → select records (or select all)
2. Action → Export → choose fields → Download CSV or XLSX
3. **Export template**: save field selection as a reusable template

### Import
1. Go to the model list (e.g., Contacts, Products)
2. Import button (top-left) → upload CSV/XLSX
3. Map columns to Odoo fields — Odoo auto-detects by column header name
4. Test import first (shows errors without saving)
5. **Relational fields**: use the record's External ID or display name
6. **External IDs** (`id` column): use `module.xml_id` format; if blank Odoo auto-assigns

### Batch Updates
Export → modify in spreadsheet → re-import with External ID column to update existing records (not create duplicates).

## In-App Purchases (IAP)

- IAP credits power paid features: SMS sending, lead enrichment, partner autocomplete, document digitization, snailmail
- Purchase credits: Settings → In-App Purchases → Buy Credits
- Credits are account-wide (shared across all databases on the same Odoo account)
- Low-credit notification: configure email alert threshold per service

## Property Fields

- Custom fields you add to records without database schema changes
- Available in: Contacts, Project Tasks, CRM Leads, Employees
- Types: text, integer, float, boolean, date, many2one, many2many, tags, separator
- Configured per-model by clicking the ⚙ (gear) icon on a record's Properties section
- Visible to all users with access to the model

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Alt+D` / `Option+D` | Discard changes |
| `Alt+S` / `Option+S` | Save record |
| `Alt+N` / `Option+N` | New record |
| `Ctrl+K` | Command palette / quick search |
| `/` | Open Powerbox in rich-text fields |
| `Esc` | Close dialog / discard |

## Product Catalog

- Accessible from Sales, Purchase, Inventory, Manufacturing — shared product master
- Products have: Sales tab, Purchase tab, Inventory tab, Accounting tab, Variants tab
- **Internal Reference**: your SKU/code
- **Product Type**: Storable (tracked in inventory), Consumable (not tracked), Service
- **Sales Price** vs **Cost**: sales price shown to customers; cost used for margin/valuation

## General Tips

- **Debug/Developer Mode**: Settings → scroll to bottom → Activate Developer Mode (or add `?debug=1` to URL) — unlocks technical menus, field tooltips, view XML editing
- **Multi-company**: switch companies via the company selector top-right; some records are company-specific, some shared
- **Chatter**: every record has a chatter (log note / send message / schedule activity) — full audit trail
- **Breadcrumbs**: navigate back without losing context; Odoo preserves list scroll position
