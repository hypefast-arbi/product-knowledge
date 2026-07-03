# Grouping stories into feature tags

A "product-spec"-style repo's feature registry (e.g. `features.yml`) is a shared,
site-wide taxonomy — every epic's ACs get grouped into it, not just the one you're
adding. Treat proposing new entries as a design decision worth getting right, not
a mechanical step.

## Where to find the grouping

1. **Prefer the PRD's own named flows.** If the PRD has a "User Flows" (or
   equivalent) section listing named SOPs/processes (e.g. "BOM & COGS management",
   "Procurement", "Vendor payment"), those names are usually the right granularity
   for a feature — they're already how the business thinks about the work, and
   each row's Description cell often states outright which flow it belongs to
   ("Step 2 of the BOM approval flow...", "Start of the Vendor Payment flow...").
   Read every row's Description for this signal before falling back to guessing.
2. **Fall back to the Module column** only if the PRD has no named-flow structure.
   Beware: a "Module" value is often the underlying platform's module name (e.g.
   an ERP app name), not a product-facing feature — several stories can share a
   module but belong to conceptually different features, or vice versa. Don't
   equate the two blindly; use Module as a hint, not the taxonomy itself.
3. **Match the existing repo's granularity.** Look at 1–2 existing epic files and
   their feature tags before inventing new ones — if the repo's existing features
   read as "a page/tab a user lands on" (e.g. `checkout`, `orders`), don't propose
   a much finer- or coarser-grained set for the new epic. Consistency across epics
   matters more than any single epic's internal purity.

## Cross-tagging (multiple features on one AC)

The existing repo will cross-tag a story under two features only when it
genuinely bridges them — e.g. a story that surfaces one feature's data inside
another feature's screen. Keep this **sparing**: check how often existing epics
do it (usually a small minority of ACs) and match that rate. Don't cross-tag
defensively "just in case" — over-tagging dilutes what each feature page shows as
"live" and makes the Features index noisier than it needs to be.

## Writing the registry entry

Each new feature entry needs (matching the existing registry's schema — confirm
against a real entry, this is illustrative):

- `name` — a short, human title (Title Case), shown on the Features index.
- `description` — one sentence, written from the *product* perspective ("what can
  a user/role do here"), not a restatement of the Jira epic name or Module value.
- Any automation-mapping field the registry has — leave empty/omit for a
  brand-new feature; that mapping is usually populated later by whoever owns test
  automation, not by this sync.

## What to show the user for review

A compact table is enough — don't dump the full scenario text at this stage:

| Story | Title | Feature tag(s) |
| --- | --- | --- |
| EPIC-2 | Create BOM request | `bom-cogs` |
| EPIC-12 | Show related POs on manufacturing order | `bom-cogs`, `procurement` |
| ... | | |

Plus the new registry entries as a small diff-style list (name + description each).
Get explicit confirmation on both the grouping and the new entries before writing
`Step 6` in the main skill file.
