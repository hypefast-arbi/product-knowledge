# bpmn.io / BPMN 2.0 reference

Read this when debugging a blank canvas, missing colours, or a schema error in a
hand-edited `.bpmn`. For normal work, prefer `scripts/bpmn_builder.py`.

## Required root namespaces
A valid file is a full `<bpmn:definitions>` document with exactly these:

```xml
<bpmn:definitions
  xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
  xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
  xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
  xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
  xmlns:bioc="http://bpmn.io/schema/bpmn/biocolor/1.0"
  xmlns:color="http://www.omg.org/spec/BPMN/non-normative/color/1.0"
  id="Definitions_1" targetNamespace="http://example.com/bpmn">
```

## Two halves: semantic model + DI
The file MUST contain both, or bpmn.io renders an empty canvas.

1. **Semantic model**
   - `<bpmn:collaboration>` holding one `<bpmn:participant>` per pool
     (`processRef` → a process) and all `<bpmn:messageFlow>` elements.
   - One `<bpmn:process>` per pool. A pool with lanes has a `<bpmn:laneSet>`
     whose `<bpmn:lane>`s list their nodes via `<bpmn:flowNodeRef>`.
   - Flow nodes (`userTask`, `serviceTask`, `sendTask`, `receiveTask`,
     `startEvent`, `endEvent`, `intermediateCatchEvent`, `exclusiveGateway`…),
     each with `<bpmn:incoming>` / `<bpmn:outgoing>` children.
   - `<bpmn:sequenceFlow>` (inside a process; same-pool only) with
     `sourceRef` / `targetRef`.

2. **Diagram interchange** — `<bpmndi:BPMNDiagram>` → `<bpmndi:BPMNPlane bpmnElement="Collab_1">` containing:
   - a `<bpmndi:BPMNShape bpmnElement="…">` with `<dc:Bounds x y width height>`
     for **every** pool, lane, node, and text annotation;
   - a `<bpmndi:BPMNEdge bpmnElement="…">` with ≥2 `<di:waypoint x y>` for
     **every** sequence flow and message flow.
   - Pools and lanes carry `isHorizontal="true"` (lanes stacked vertically,
     flow left→right) or `isHorizontal="false"` (lanes as columns, flow
     top→bottom).

## The cross-pool rule
`sequenceFlow` is illegal across a pool boundary — bpmn.io will reject it or
refuse to connect. Anything human↔system or system↔system is a `messageFlow`
declared in the `<bpmn:collaboration>`. A two-way sync (e.g. Odoo creates GR →
Jubelio creates Incoming Transfer, then Jubelio returns validated qty → Odoo
updates GR) is **two** message flows, one each direction, each labelled.

## Colour
Set on BOTH the semantic element and its DI shape:

```xml
<bpmn:serviceTask id="T1" name="Auto-create GR"
    color:background-color="#C5E1F5" color:border-color="#1E70B8">
  ...
</bpmn:serviceTask>
...
<bpmndi:BPMNShape id="T1_di" bpmnElement="T1"
    bioc:stroke="#1E70B8" bioc:fill="#C5E1F5"
    color:background-color="#C5E1F5" color:border-color="#1E70B8">
  <dc:Bounds x="100" y="100" width="110" height="80" />
</bpmndi:BPMNShape>
```
Suggested palette: Odoo blue `#C5E1F5`/`#1E70B8`, Jubelio green
`#C8E6C9`/`#2E7D32`, Jurnal orange `#FFE0B2`/`#E65100`, human gray
`#F5F5F5`/`#6B6B6B`.

## Wait / message catch events
`<bpmn:intermediateCatchEvent>` needs an event definition to be valid; a "goods
arrived?" wait is naturally a `<bpmn:messageEventDefinition>` child. A bare
intermediate catch with no definition is invalid.

## Validating
`bpmn-moddle` is the parser bpmn.io itself uses:

```js
import BpmnModdle from 'bpmn-moddle';
const { warnings, rootElement } =
  await new BpmnModdle().fromXML(readFileSync('f.bpmn','utf8'));
```
Warnings of the form `unknown attribute <color:background-color>` are **benign**
— a bare moddle lacks the colour extension, but the bpmn.io app reads the
`bioc:` attributes and renders colours correctly. Treat any *other* warning as a
real problem.
