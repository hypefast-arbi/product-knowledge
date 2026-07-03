#!/usr/bin/env node
/**
 * Parse a Hypefast-style "Description of the User Flows" requirement table
 * (User Story | Module | Acceptance Criteria | Description, optionally prefixed
 * with a Dev/Standard Solution column) out of a Confluence page's markdown export,
 * and emit a product-spec-style Gherkin .feature file.
 *
 * See ../references/gherkin-parsing-notes.md for the splitting approach and a
 * Gherkin-parser gotcha re: trailing "# TICKET-ID" comments.
 * See ../references/feature-taxonomy.md for how to build the feature map.
 *
 * Usage:
 *   node parse-requirement-table.js <prd-body.md> <EPIC-KEY> <feature-map.json> [outfile] [--no-draft] [--heading "Description of the User Flows"]
 *
 * feature-map.json shape:
 *   { "2": "bom-cogs", "12": ["bom-cogs", "procurement"], ... }
 *   (keys are the numeric part of the story key, e.g. "12" for ERP-12)
 *
 * Prints a summary to stdout; writes the .feature file to <outfile> (default:
 * ./<EPIC-KEY>-acceptance-criteria.feature next to this script's cwd).
 */
const fs = require('fs');
const path = require('path');

function fail(msg) {
  console.error('ERROR:', msg);
  process.exit(1);
}

const args = process.argv.slice(2);
const positional = args.filter(a => !a.startsWith('--'));
const flags = args.filter(a => a.startsWith('--'));
const noDraft = flags.includes('--no-draft');
const headingFlagIdx = flags.findIndex(f => f === '--heading');
const tableHeading = headingFlagIdx >= 0 ? flags[headingFlagIdx + 1] : 'Description of the User Flows';

const [prdPath, epicKey, featureMapPath, outfileArg] = positional;
if (!prdPath || !epicKey || !featureMapPath) {
  fail('usage: parse-requirement-table.js <prd-body.md> <EPIC-KEY> <feature-map.json> [outfile] [--no-draft]');
}

const body = fs.readFileSync(prdPath, 'utf8');
const featureMap = JSON.parse(fs.readFileSync(featureMapPath, 'utf8'));
const outfile = outfileArg || path.join(process.cwd(), `${epicKey}-acceptance-criteria.feature`);

const lines = body.split('\n');

// Locate the table: find the heading line by prefix match (not .includes —
// a Description cell can mention a later section's name in prose and false-match).
const headingNeedle = tableHeading.trim();
const startIdx = lines.findIndex(l => {
  const stripped = l.replace(/[#*]/g, '').trim();
  return stripped === headingNeedle;
});
if (startIdx === -1) fail(`could not find a heading line matching "${headingNeedle}"`);

// Table rows are contiguous lines starting with "|" after the heading.
let i = startIdx + 1;
while (i < lines.length && !lines[i].trim().startsWith('|')) i++;
const tableStart = i;
while (i < lines.length && lines[i].trim().startsWith('|')) i++;
const tableLines = lines.slice(tableStart, i).filter(l => l.trim().startsWith('|'));

if (tableLines.length < 3) fail('found the heading but fewer than 3 table lines after it (header + separator + >=1 data row expected)');

// tableLines[0] = header, tableLines[1] = separator, rest = data rows
const dataRows = tableLines.slice(2);

function splitTableRow(row) {
  let r = row.trim().replace(/^\|/, '').replace(/\|$/, '');
  return r.split('|').map(c => c.trim());
}

function splitScenarios(acText) {
  const parts = acText.split(/Scenario:\s*/).map(s => s.trim()).filter(Boolean);
  return parts.map(part => {
    const m = part.match(/^(.*?)\s+(Given that.*)$/s);
    if (!m) fail('could not split title/body for scenario text: ' + part.slice(0, 120));
    const title = m[1].trim();
    const rest = m[2].trim();
    const clauses = rest.split(/\s+(?=(?:Given that|When|Then|And)\b)/).map(c => c.trim());
    return { title, clauses };
  });
}

// Detect the User Story column by finding the cell containing a "[KEY-N: title](url)" link.
// Supports both the 4-column (User Story|Module|AC|Description) and 5-column
// (Dev/Standard Solution|User Story|Module|AC|Description) table shapes.
const headerCells = splitTableRow(tableLines[0]);
const linkColIdx = headerCells.findIndex((_, idx) =>
  dataRows.length && /\[[A-Z]+-\d+:/.test(splitTableRow(dataRows[0])[idx] || '')
);
if (linkColIdx === -1) fail('could not find the User Story column (expected a "[KEY-N: title](url)" markdown link in some cell)');
const acColIdx = linkColIdx + 2; // Module then Acceptance Criteria, per the standard 4/5-col layout

let acCounter = 0;
const storyBlocks = [];
const keyPrefix = epicKey.split('-')[0];

for (const row of dataRows) {
  const cells = splitTableRow(row);
  const userStoryCell = cells[linkColIdx];
  const acCell = cells[acColIdx];
  if (!userStoryCell || !acCell) { console.error('SKIPPING malformed row:', cells.slice(0, 2)); continue; }

  const idMatch = userStoryCell.match(new RegExp(`\\[(${keyPrefix}-\\d+):\\s*([^\\]]+)\\]`));
  if (!idMatch) { console.error('NO STORY ID MATCH, skipping row:', userStoryCell.slice(0, 80)); continue; }
  const storyKey = idMatch[1];
  const storyNum = storyKey.split('-')[1];

  let features = featureMap[storyNum];
  if (!features) { console.error(`NO FEATURE MAPPING for ${storyKey} — tagging with no @feature, fix features.yml/feature-map manually`); features = []; }
  if (!Array.isArray(features)) features = [features];

  const scenarios = splitScenarios(acCell);
  const scenarioTexts = scenarios.map(sc => {
    acCounter++;
    const tagParts = [`@id:${epicKey}/AC-${acCounter}`, ...features.map(f => '@' + f)];
    if (!noDraft) tagParts.push('@draft');
    const tags = `${tagParts.join(' ')} # ${storyKey}`;
    return [
      `  ${tags}`,
      `  Scenario: ${sc.title}`,
      ...sc.clauses.map(c => `    ${c}`),
    ].join('\n');
  });

  storyBlocks.push({ storyKey, scenarioTexts });
}

const out = storyBlocks.map(b => b.scenarioTexts.join('\n\n')).join('\n\n') + '\n';
// Caller is expected to prepend their own `Feature: <title>` header + description —
// this script emits only the AC blocks so the header can be reviewed/edited separately.
fs.writeFileSync(outfile, out);

console.log('Table heading matched:', headingNeedle);
console.log('Data rows found:', dataRows.length);
console.log('Total AC scenarios:', acCounter);
console.log('Stories:', storyBlocks.map(b => `${b.storyKey} (${b.scenarioTexts.length} AC)`).join(', '));
console.log('Written to:', outfile);
console.log('\nReminder: prepend a `Feature: <title>` header line + one-line description before this content.');
