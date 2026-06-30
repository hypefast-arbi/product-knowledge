# product-knowledge

A Claude Code **plugin marketplace** holding Arbi's product-management skills and Odoo functional knowledge. Version-controlled here so the skills are backed up, shareable with the team, and updated with a single `git pull`.

## What's inside

Two independently-installable plugins:

| Plugin | Skills | Use it when |
|---|---|---|
| **pm-workflow** | `confluence-create-page`, `jira-create-backlog-ticket`, `success-criteria`, `bpmn-diagram-builder` | Doing PM execution work — PRDs, backlog, success metrics, process diagrams |
| **odoo-knowledge** | `odoo-essentials`, `odoo-finance`, `odoo-hr`, `odoo-productivity`, `odoo-sales`, `odoo-services`, `odoo-supply-chain` | Answering Odoo functional questions |

## Install

```bash
# add this repo as a marketplace (once per machine)
claude plugin marketplace add hypefast-arbi/product-knowledge

# install only what you need on this machine
claude plugin install pm-workflow@product-knowledge
claude plugin install odoo-knowledge@product-knowledge
```

Or from inside a session: `/plugin marketplace add hypefast-arbi/product-knowledge` then `/plugin install pm-workflow@product-knowledge`.

To update later: `claude plugin marketplace update product-knowledge`.

## Why it's split into two plugins (token efficiency)

At session start Claude loads **only each skill's `name` + `description`** (the frontmatter) into context — never the body. The body of a `SKILL.md` loads only when the skill is actually triggered, and `references/` + `scripts/` files load only when the skill explicitly reads them (progressive disclosure).

So the always-on token cost of a machine = the sum of the frontmatter descriptions of every **installed** skill. The design here keeps that minimal:

1. **Selective install.** A laptop that only does PM work installs `pm-workflow` and pays nothing for the 7 Odoo descriptions. This is the single biggest lever.
2. **Tight descriptions.** Each description carries just enough trigger keywords to auto-activate, no prose. (`bpmn-diagram-builder` was trimmed from ~1,500 to ~440 chars.)
3. **Progressive disclosure.** Heavy detail lives in `references/` (e.g. the BPMN DI / mxGraph references) and loads only on demand, not at startup.

If a machine has many skills and you still want to shrink startup cost, `skillOverrides` (`name-only` mode) and `skillListingBudgetFraction` in `settings.json` are further levers.

## Layout

```
.claude-plugin/marketplace.json     # lists the two plugins
plugins/
  pm-workflow/
    .claude-plugin/plugin.json
    skills/<skill>/SKILL.md
  odoo-knowledge/
    .claude-plugin/plugin.json
    skills/<skill>/SKILL.md
```

## Editing a skill

Edit the `SKILL.md` in this repo, commit, push, then `claude plugin marketplace update product-knowledge` on each machine. Keep frontmatter `description`s short (trigger keywords only) and push long material into `references/`.
