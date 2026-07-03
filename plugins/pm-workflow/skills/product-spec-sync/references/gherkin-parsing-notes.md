# Parsing a requirement table's AC cell into Gherkin, and a parser gotcha

## The AC cell shape you're parsing

A Hypefast-style requirement table (produced by the `requirement-table` skill) has
an Acceptance Criteria cell containing 1–N scenarios concatenated as plain text,
each following [[gherkin-template-preference]] exactly:

```
Scenario: <title> - <label> Given that <clause> When <clause> And <clause> Then <clause> And <clause>  Scenario: <title2> - <label2> Given that ...
```

No newlines survive the table cell — everything is one run-on string per row, with
just a double space between scenarios sometimes and not always.

## Splitting algorithm (used by scripts/parse-requirement-table.js)

1. **Split into scenarios** on `/Scenario:\s*/`, filtering empty pieces. This is
   safe because "Scenario:" doesn't appear inside a title or clause in this house
   style.
2. **Split each scenario into title vs. clauses** on the first occurrence of
   `Given that`: everything before it is the title (`<title> - <label>`),
   everything from `Given that` onward is the clause body.
3. **Split the clause body into individual Given/When/Then/And lines** with a
   lookahead split: `/\s+(?=(?:Given that|When|Then|And)\b)/`. This works because
   in this house style, `When`, `Then`, and `And` only ever appear as clause
   starters — never as a normal English word mid-sentence in a title or clause. If
   you're parsing a PRD that doesn't strictly follow this template, spot-check a
   sample before trusting the split — a stray "And" or "When" as an ordinary word
   would produce a bogus line break.

Validate the parse by regenerating and re-reading a handful of scenarios before
writing anything — a bad split reads as garbled Gherkin immediately.

## Gotcha: where a trailing "# TICKET-ID" comment is safe

CONTRIBUTING-style guidance that allows "a trailing `# TICKET-NNNN` comment ... for
traceability" is ambiguous about exactly which line it goes on, and getting it
wrong silently corrupts the rendered site rather than failing the build. Verified
empirically against the `gherkin-official` Python parser (the parser this kind of
repo tends to use):

| Placement | Result |
| --- | --- |
| End of the `@id:... @tag` **tag line** | Parsed fine. The tokenizer silently drops the trailing `# ...` — it doesn't even show up in the parser's own `comments` list, and doesn't pollute the tags array. Effectively an inert, human-readable-only annotation in the source file; zero effect on the generated site. |
| End of the `Scenario: ...` **line** | **Breaks silently.** The `# TICKET-NNNN` text gets absorbed into the *scenario's name string itself* — e.g. `Scenario: something` becomes named `"something # TICKET-NNNN"` — which then renders as part of the visible title on the generated site. |
| On its **own line** (before the tags or before `Scenario:`) | Parsed fine and shows up in the parser's `comments` list as a real Gherkin comment, cleanly separate from both the tags and the scenario name. |

**Rule: put a trailing per-ticket comment on the tag line, or on its own line —
never appended after `Scenario: <title>`.** If you're working against a different
Gherkin implementation than `gherkin-official`, re-verify this with a 5-line throwaway
test file before trusting it (the standard Gherkin spec only guarantees comments
starting a line; anything past that is implementation behavior, not spec).

A throwaway verification script:

```python
from gherkin.parser import Parser
from gherkin.token_scanner import TokenScanner

text = '''Feature: Test
  @id:TEST/AC-1 @foo # TICKET-123
  Scenario: something
    Given a thing
    Then it works
'''
doc = Parser().parse(TokenScanner(text))
scenario = doc['feature']['children'][0]['scenario']
print(scenario['name'])                      # should be "something", not "something # TICKET-123"
print([t['name'] for t in scenario['tags']])  # should be exactly the real tags
```

## Windows build-environment gotchas (not content bugs)

Hit these while building/testing a Python-based generator repo from a Windows Git
Bash shell — both look like something's broken but aren't:

- **`python` / `python3` not on PATH.** Windows ships PATH shims for these that
  just open the Microsoft Store instead of running anything. Use the **`py`
  launcher** instead (`py build.py`, `py -m pytest`, `py -m pip install -r
  requirements.txt`).
- **A UnicodeEncodeError on a `→`-style arrow (or any non-ASCII) in a script's own
  success-message print**, e.g. `'charmap' codec can't encode character '→'`.
  This is Windows' default `cp1252` console codec, not a bug in the content you
  just wrote. Prefix the command with `PYTHONIOENCODING=utf-8` (Git Bash) or set
  `$env:PYTHONIOENCODING="utf-8"` (PowerShell) and re-run.
- **No `jq` on Windows by default**, for picking apart a large persisted JSON
  tool-result file. Use PowerShell `Get-Content -Raw | ConvertFrom-Json` (then
  index/loop in PowerShell), or a small Node one-off — whichever runtime is
  already warm in the session.
