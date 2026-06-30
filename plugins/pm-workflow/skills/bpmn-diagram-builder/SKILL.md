---
name: bpmn-diagram-builder
description: Build BPMN process diagrams as files that render in bpmn.io (.bpmn) and draw.io/diagrams.net (.drawio) — swimlane pools/lanes, cross-pool message flows, colour, and full DI layout. Use whenever the user wants a BPMN diagram, process map, swimlane diagram, or workflow model as a file (incl. ERP/system-integration flows, or any mention of .bpmn, BPMN 2.0, bpmn.io, draw.io, diagrams.net, pools/lanes, swimlanes, or "turn this process into a diagram").
---

# BPMN Diagram Builder

Produce BPMN process diagrams that open cleanly in **bpmn.io** (the `.bpmn`
BPMN 2.0 XML format) and/or **diagrams.net / draw.io** (the `.drawio` mxGraph
format). These are two *different* file formats — a `.bpmn` file does **not**
import reliably into draw.io and vice-versa. This skill emits both from one model.

## The five rules that make or break the file

1. **DI is mandatory, or the canvas is blank.** bpmn.io renders nothing unless
   every node/lane/pool has a `<bpmndi:BPMNShape>` with `<dc:Bounds>` and every
   sequence/message flow has a `<bpmndi:BPMNEdge>` with `<di:waypoint>`s. The
   generator produces these for every element automatically.
2. **A `sequenceFlow` may NEVER cross a pool boundary.** Links inside one pool
   (including between its lanes) are `sequenceFlow`; links between pools
   (human↔system, system↔system) are `messageFlow`, declared in the
   `collaboration`. Bidirectional syncs = two separate, separately-labelled
   message flows. The generator raises an error if you break this.
3. **Colour lives in two places.** Set `color:background-color` /
   `color:border-color` on the semantic element AND `bioc:fill` / `bioc:stroke`
   on the matching DI shape, or colours won't survive import. The generator does
   both from a single colour key.
4. **draw.io is a separate emit.** Same model, different schema (mxGraph
   `<mxCell>` with swimlane styles, dashed message-flow edges). Emit it
   separately; never tell the user to import the `.bpmn` into draw.io.
5. **Never place two nodes at the same (lane, col).** They render on top of each
   other. The classic case is a system pool's start event sharing a column with
   its first task. The generator auto-bumps collisions and warns, but design the
   model to avoid them.

## Workflow

### Step 1 — Model the process before drawing anything
Identify:
- **Pools** (participants): one per organisation/system. Human-org pools get
  **lanes** (departments/roles); system pools usually have none.
- **Nodes** per pool, each with a `col` = its step index along the flow, mapped
  to element types (see table). Human actions go in the human pool's lanes;
  automated system actions go in the relevant system pool.
- **Flows**: same-pool → `seq`; cross-pool (the integration syncs) → `msg`,
  each labelled with the data/action transferred ("sync GR qty",
  "create Incoming Transfer", "kirim qty receipt").
- Leave a **gap in `col`** between independent sub-flows so they read as
  separate bands, and add a `textAnnotation` header per band.

### Step 2 — Build with the generator (do not hand-write XML)
Use `scripts/bpmn_builder.py`. Read its module docstring for the full API; the
shape is:

```python
import sys; sys.path.insert(0, "<skill>/scripts")
from bpmn_builder import Builder

b = Builder(orientation="vertical")     # "vertical" = tall & narrow; "horizontal" = wide
b.pool("A", "Hypefast (Brand & Ops)", lanes=["Sales", "Procurement", "Finance"])
b.pool("B", "System: Odoo", tint="#EAF3FB")
b.node("Start", "A", 0, "event", "Mulai", "human", lane="Sales", subtype="start")
b.node("PR",    "A", 1, "task",  "Submit PR", "human", lane="Sales", subtype="user")
b.node("OPR",   "B", 1, "task",  "Create PR record", "odoo", subtype="receive")
b.seq("Start", "PR")
b.msg("PR", "OPR", "input PR")           # cross-pool ⇒ message flow
b.annotation("AnnF1", "FLOW 1: Pembelian RM", "A", 0)
b.validate()                             # raises on structural problems; returns warnings
b.emit_bpmn("/mnt/user-data/outputs/diagram.bpmn")
b.emit_drawio("/mnt/user-data/outputs/diagram.drawio")
```

`color` keys built in: `odoo` (blue), `jubelio` (green), `jurnal` (orange),
`human` (gray). Add more via `b.colors["wms"] = ("#FILL", "#STROKE")`.

### Step 3 — Choose orientation by flow count
- **One or two flows** → `horizontal` reads most naturally (standard left-to-right
  swimlanes).
- **Several stacked flows** → `vertical`: pools/lanes become columns, each flow
  runs top-to-bottom, flows stack down the page. This keeps width fixed instead
  of sprawling to many thousands of px. (draw.io's `horizontal` swimlane flag is
  inverted vs intuition — a *vertical* pool uses `horizontal=1`; the generator
  handles this.)

### Step 4 — Validate before delivering
Always call `b.validate()` (it checks: no `sequenceFlow` crosses a pool, every
`messageFlow` does cross one, gateways have ≥2 labelled outgoing flows, no
isolated nodes). Then confirm the `.bpmn` actually parses with bpmn.io's own
parser using `scripts/validate_bpmn.py <file.bpmn>` if Node + `bpmn-moddle` are
available. Colour-namespace warnings ("unknown attribute <color:…>") are
**benign and expected** — they come from a bare moddle without the colour
extension; colours still render in the bpmn.io app via the `bioc:` attributes.

### Step 5 — Deliver
Present both files. Tell the user: open the `.bpmn` in bpmn.io (or any bpmn-js
editor) and the `.drawio` in app.diagrams.net via File → Open or by dragging it
onto the canvas. If vertical, mention it's tall — use fit-to-page.

## Element type mapping

| Process concept | kind / subtype |
|---|---|
| Manual human action | `kind="task", subtype="user"` (userTask) |
| Automated system action | `kind="task", subtype="service"` (serviceTask) |
| System transmits data across pools | `subtype="send"` (sendTask) |
| System awaits data across pools | `subtype="receive"` (receiveTask) |
| Decision point | `kind="gateway", subtype="exclusive"` — give each outgoing `seq` a name ("Ya / DP required", "Tidak") |
| Start / end | `kind="event", subtype="start"` / `"end"` |
| Wait / "goods arrived?" | `kind="event", subtype="catch"`, optionally `evdef="message"` |
| Section header | `b.annotation(id, text, pool, col)` |

## Reference files
- `references/bpmnio_di_reference.md` — BPMN 2.0 namespaces, the DI shape/edge
  structure, colour attributes, and the exact failure modes (read when debugging
  a blank canvas, mis-coloured nodes, or a schema error).
- `references/drawio_mxgraph_reference.md` — mxGraph cell anatomy, swimlane
  styles, the inverted `horizontal` flag, message-flow edge styling, and why we
  use absolute coordinates instead of nested containers (read when adjusting the
  draw.io output).

## Common failure modes (and the fix)
- **Blank canvas in bpmn.io** → missing DI for some element. Use the generator;
  never hand-edit shapes out.
- **"sequenceFlow crosses participant" / arrows refuse to connect** → you used a
  `seq` across pools; switch to `msg`.
- **Nodes overlapping** → two nodes share a `(lane, col)`; check `validate()`
  warnings and renumber.
- **Colours vanish on import** → only set on the semantic element OR only on the
  shape; both are required (generator does both).
- **draw.io shows a wide mess when you wanted tall** → set
  `orientation="vertical"`.
- **User imported `.bpmn` into draw.io and it looked wrong** → give them the
  `.drawio` file instead; the formats are not interchangeable.
