# diagrams.net / draw.io (mxGraph) reference

Read when adjusting the `.drawio` output. draw.io does **not** use BPMN 2.0 XML;
it uses mxGraph. Never tell the user to import a `.bpmn` into draw.io — emit a
native `.drawio` from the same model instead.

## File skeleton
```xml
<mxfile host="app.diagrams.net" type="device">
  <diagram id="d1" name="BPMN">
    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" page="1"
                  pageWidth="850" pageHeight="1169">
      <root>
        <mxCell id="0" />              <!-- root -->
        <mxCell id="1" parent="0" />   <!-- default layer; everything parents here -->
        <!-- vertices and edges -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```
`id="0"` and `id="1"` are reserved; give every other cell a unique id (we prefix
nodes `d_…` and edges `de_…`).

## Vertices and edges
```xml
<mxCell id="d_T1" value="Label" style="…" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="110" height="80" as="geometry" />
</mxCell>
<mxCell id="de_F1" value="sync qty" style="…" edge="1" parent="1"
        source="d_A" target="d_B">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```
Edges reference `source`/`target` by cell id and draw.io auto-routes them, so
no explicit waypoints are needed.

## Absolute coordinates, not nested containers
Nesting a cell inside a swimlane makes its geometry **relative** to that
swimlane (and lanes-in-pools is two levels deep), which is fiddly and a common
source of misplacement. The robust approach used here: draw pools and lanes as
swimlane-styled bands on the default layer (`parent="1"`) **first** (so they sit
behind), then place all nodes with **absolute** coordinates also on `parent="1"`
on top. Painting order = document order, so list pools, then lanes, then nodes.
Trade-off: dragging a pool won't drag its contents — acceptable for a generated
reference diagram, and it always renders correctly.

## The inverted `horizontal` flag
This is the biggest gotcha. For a swimlane:
- `horizontal=0` → title rotated on the **left**, lanes stacked vertically,
  flow reads **left→right**. This is the *horizontal pool*.
- `horizontal=1` → title on **top**, lanes side-by-side as columns, flow reads
  **top→bottom**. This is the *vertical pool*.

So a vertical layout uses `horizontal=1`. Match `startSize` to the title band
(≈30 for a pool, ≈26 for a lane).

## Styles used
- Pool: `swimlane;html=1;horizontal={0|1};startSize=30;fillColor=<tint>;strokeColor=#444444;fontStyle=1;swimlaneFillColor=none;`
- Lane: `swimlane;html=1;horizontal={0|1};startSize=26;fillColor=none;strokeColor=#999999;`
- Task: `rounded=1;whiteSpace=wrap;html=1;fillColor=<fill>;strokeColor=<stroke>;`
- Gateway: `rhombus;whiteSpace=wrap;html=1;fillColor=<fill>;strokeColor=<stroke>;`
- Event: `ellipse;whiteSpace=wrap;html=1;fillColor=<fill>;strokeColor=<stroke>;strokeWidth=N;`
  — start `strokeWidth=1`, end `strokeWidth=3`, intermediate catch `strokeWidth=2;dashed=1`.
- Sequence flow: `edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=1;strokeColor=#444444;`
- Message flow (BPMN convention = dashed, open arrow, circle at source):
  `edgeStyle=orthogonalEdgeStyle;dashed=1;dashPattern=6 4;startArrow=oval;startFill=0;endArrow=open;endFill=0;strokeColor=#1565C0;`
- Section header: `text;html=1;strokeColor=none;fillColor=none;align=left;fontStyle=1;`

## Opening
File → Open (or drag the `.drawio` onto the canvas) at app.diagrams.net or in
the desktop app. Use Ctrl/Cmd+Shift+H to fit the (often tall) diagram to the
window.
