# -*- coding: utf-8 -*-
"""
bpmn_builder.py — model-driven generator for BPMN diagrams that render correctly
in BOTH bpmn.io (BPMN 2.0 XML) and diagrams.net / draw.io (mxGraph XML).

Why a generator instead of hand-writing XML:
  * bpmn.io shows a BLANK canvas unless EVERY node has a <bpmndi:BPMNShape> and
    EVERY flow has a <bpmndi:BPMNEdge>. Generating guarantees that.
  * A <bpmn:sequenceFlow> may NEVER cross a pool boundary; cross-pool links must
    be <bpmn:messageFlow>. The builder enforces this and raises on violation.
  * Colors must be set in two places (semantic element + DI shape). Done here.
  * draw.io uses a DIFFERENT schema (mxGraph). Same model -> emit_drawio().

Typical usage
-------------
    from bpmn_builder import Builder
    b = Builder(orientation="vertical")          # or "horizontal"
    b.pool("A", "Hypefast", lanes=["Sales", "Finance"])
    b.pool("B", "System: Odoo")
    b.node("Start", pool="A", lane="Sales", col=0, kind="event",
           subtype="start", label="Mulai", color="human")
    b.node("PR", pool="A", lane="Sales", col=1, kind="task",
           subtype="user", label="Submit PR", color="human")
    b.node("OdooPR", pool="B", col=1, kind="task", subtype="receive",
           label="Create PR record", color="odoo")
    b.seq("Start", "PR")
    b.msg("PR", "OdooPR", "input PR")            # cross-pool -> message flow
    b.validate()                                 # raises on structural problems
    b.emit_bpmn("out.bpmn")
    b.emit_drawio("out.drawio")

Model vocabulary
----------------
kind:    "event" | "task" | "gateway"
subtype: event   -> "start" | "end" | "catch"
         task    -> "user" | "service" | "send" | "receive"
         gateway -> "exclusive" (default) | "parallel" | "inclusive"
color keys (default palette): "odoo"(blue) "jubelio"(green) "jurnal"(orange)
         "human"(gray). Add your own via b.colors[...] = (fill, stroke).
col:     integer step index along the flow direction (0,1,2,...). Leave gaps
         between separate sub-flows so they read as bands.
"""
from xml.sax.saxutils import escape

# ------------------------------------------------------------------ geometry
TRACK = 170          # perpendicular thickness of one lane / single-lane pool
STEP_V = 95          # spacing per col when orientation == vertical
STEP_H = 175         # spacing per col when orientation == horizontal
POOL_TITLE = 30
LANE_TITLE = 26
PERP_ORIGIN = 130    # left (vertical) / top (horizontal) of first pool
PAR_ORIGIN = 200     # y (vertical) / x (horizontal) of col 0 centre
POOL_GAP = 40        # gap between separate pools
PAR_PAD = 90         # padding added before/after content along flow axis

SIZE = {"event": (36, 36), "gateway": (50, 50), "task": (110, 80)}

DEFAULT_COLORS = {
    "odoo":    ("#C5E1F5", "#1E70B8"),
    "jubelio": ("#C8E6C9", "#2E7D32"),
    "jurnal":  ("#FFE0B2", "#E65100"),
    "human":   ("#F5F5F5", "#6B6B6B"),
}
POOL_TINT = {  # light background tint for draw.io pools, by leading color
    "odoo": "#EAF3FB", "jubelio": "#EAF6EA", "jurnal": "#FFF4E6", "human": "#FAFAFA",
}


class Builder:
    def __init__(self, orientation="vertical", target_ns="http://example.com/bpmn"):
        assert orientation in ("vertical", "horizontal")
        self.orientation = orientation
        self.target_ns = target_ns
        self.colors = dict(DEFAULT_COLORS)
        self.pools = []          # list of dict(id, name, lanes[list], tint)
        self.nodes = {}          # id -> dict
        self.seqs = []           # dict(id, src, tgt, label, pool)
        self.msgs = []           # dict(id, src, tgt, label)
        self.annotations = []    # dict(id, text, pool, col)
        self.warnings = []
        self._sc = 0
        self._mc = 0
        self._occupied = set()   # (pool_or_lane_track_key, col)

    # ---------------------------------------------------------------- model
    def pool(self, pid, name, lanes=None, tint=None):
        self.pools.append(dict(id=pid, name=name, lanes=list(lanes or []), tint=tint))
        return pid

    def _track_key(self, pool, lane):
        return f"{pool}/{lane}" if lane else f"{pool}/_"

    def node(self, nid, pool, col, kind, label, color, lane=None,
             subtype=None, evdef=None):
        assert nid not in self.nodes, f"duplicate node id {nid}"
        if subtype is None:
            subtype = {"event": "start", "task": "service", "gateway": "exclusive"}[kind]
        key = self._track_key(pool, lane)
        # auto-resolve overlaps: two nodes must not share the same (track, col)
        while (key, col) in self._occupied:
            self.warnings.append(
                f"node {nid}: ({pool}/{lane or '-'}, col {col}) occupied -> bumped to {col + 1}")
            col += 1
        self._occupied.add((key, col))
        self.nodes[nid] = dict(id=nid, pool=pool, lane=lane, col=col, kind=kind,
                               subtype=subtype, label=label, color=color,
                               evdef=evdef, track=key)
        return nid

    def seq(self, src, tgt, label=""):
        ps, pt = self.nodes[src]["pool"], self.nodes[tgt]["pool"]
        if ps != pt:
            raise ValueError(
                f"sequenceFlow {src}->{tgt} crosses pool boundary "
                f"({ps}!={pt}). Use msg() for cross-pool links.")
        self._sc += 1
        fid = f"Flow_{self._sc:03d}"
        self.seqs.append(dict(id=fid, src=src, tgt=tgt, label=label, pool=ps))
        return fid

    def msg(self, src, tgt, label=""):
        ps, pt = self.nodes[src]["pool"], self.nodes[tgt]["pool"]
        if ps == pt:
            raise ValueError(
                f"messageFlow {src}->{tgt} stays inside pool {ps}. "
                f"Use seq() for same-pool links.")
        self._mc += 1
        mid = f"Msg_{self._mc:03d}"
        self.msgs.append(dict(id=mid, src=src, tgt=tgt, label=label))
        return mid

    def annotation(self, aid, text, pool, col):
        self.annotations.append(dict(id=aid, text=text, pool=pool, col=col))
        return aid

    # ------------------------------------------------------------- layout
    def _layout(self):
        # assign a perpendicular position to each track in pool/lane order
        order, perp_left, pool_span = [], {}, {}
        cur = PERP_ORIGIN
        for p in self.pools:
            start = cur
            tracks = [self._track_key(p["id"], ln) for ln in p["lanes"]] or \
                     [self._track_key(p["id"], None)]
            for tk in tracks:
                order.append(tk)
                perp_left[tk] = cur
                cur += TRACK
            pool_span[p["id"]] = (start, cur)   # [left, right) along perp axis
            cur += POOL_GAP
        self._perp_left = perp_left
        self._pool_span = pool_span
        self._perp_extent = cur - POOL_GAP
        step = STEP_V if self.orientation == "vertical" else STEP_H
        self._step = step
        max_col = max(n["col"] for n in self.nodes.values())
        self._par_extent = PAR_ORIGIN + max_col * step + PAR_PAD

    def _center(self, n):
        perp = self._perp_left[n["track"]] + TRACK / 2
        par = PAR_ORIGIN + n["col"] * self._step
        return (perp, par) if self.orientation == "vertical" else (par, perp)

    def _bounds(self, n):
        w, h = SIZE[n["kind"]]
        cx, cy = self._center(n)
        return cx - w / 2, cy - h / 2, w, h

    def _pool_bounds(self, pid):
        lo, hi = self._pool_span[pid]
        if self.orientation == "vertical":
            return lo, 80, hi - lo, self._par_extent - 80 + 60
        return 80, lo, self._par_extent - 80 + 60, hi - lo

    def _lane_bounds(self, pid, lane):
        tk = self._track_key(pid, lane)
        left = self._perp_left[tk]
        if self.orientation == "vertical":
            return left, 80 + POOL_TITLE, TRACK, self._par_extent - 80 + 60 - POOL_TITLE
        return 80 + POOL_TITLE, left, self._par_extent - 80 + 60 - POOL_TITLE, TRACK

    def _is_horizontal_flag(self):
        # BPMN isHorizontal: pools drawn as horizontal bands when flow is horizontal
        return self.orientation == "horizontal"

    # -------------------------------------------------------- validation
    def validate(self):
        errs = []
        ids = set(self.nodes)
        for f in self.seqs:
            if f["src"] not in ids or f["tgt"] not in ids:
                errs.append(f"seq {f['id']} references missing node")
            if self.nodes[f["src"]]["pool"] != self.nodes[f["tgt"]]["pool"]:
                errs.append(f"seq {f['id']} crosses pool boundary")
        for m in self.msgs:
            if self.nodes[m["src"]]["pool"] == self.nodes[m["tgt"]]["pool"]:
                errs.append(f"msg {m['id']} does not cross a pool")
        # gateways need >=2 named outgoing
        for nid, n in self.nodes.items():
            if n["kind"] == "gateway":
                outs = [f for f in self.seqs if f["src"] == nid]
                if len(outs) < 2 or any(not o["label"] for o in outs):
                    errs.append(f"gateway {nid}: needs >=2 labelled outgoing flows")
        # isolated nodes
        for nid in ids:
            if not any(f["src"] == nid or f["tgt"] == nid for f in self.seqs) \
               and not any(m["src"] == nid or m["tgt"] == nid for m in self.msgs):
                errs.append(f"node {nid} is isolated (no flow attached)")
        if errs:
            raise ValueError("Validation failed:\n  - " + "\n  - ".join(errs))
        return self.warnings

    # ------------------------------------------------------------- BPMN
    def emit_bpmn(self, path):
        self._layout()
        o = []
        a = o.append
        a('<?xml version="1.0" encoding="UTF-8"?>')
        a('<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"')
        a('    xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"')
        a('    xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"')
        a('    xmlns:di="http://www.omg.org/spec/DD/20100524/DI"')
        a('    xmlns:bioc="http://bpmn.io/schema/bpmn/biocolor/1.0"')
        a('    xmlns:color="http://www.omg.org/spec/BPMN/non-normative/color/1.0"')
        a(f'    id="Definitions_1" targetNamespace="{self.target_ns}">')
        a('  <bpmn:collaboration id="Collab_1">')
        for p in self.pools:
            a(f'    <bpmn:participant id="Pool_{p["id"]}" name="{escape(p["name"])}" '
              f'processRef="Proc_{p["id"]}" />')
        for m in self.msgs:
            a(f'    <bpmn:messageFlow id="{m["id"]}" name="{escape(m["label"])}" '
              f'sourceRef="{m["src"]}" targetRef="{m["tgt"]}" />')
        a('  </bpmn:collaboration>')

        for p in self.pools:
            a(f'  <bpmn:process id="Proc_{p["id"]}" isExecutable="false">')
            if p["lanes"]:
                a(f'    <bpmn:laneSet id="LaneSet_{p["id"]}">')
                for ln in p["lanes"]:
                    a(f'      <bpmn:lane id="Lane_{p["id"]}_{ln}" name="{escape(ln)}">')
                    for nid, n in self.nodes.items():
                        if n["pool"] == p["id"] and n["lane"] == ln:
                            a(f'        <bpmn:flowNodeRef>{nid}</bpmn:flowNodeRef>')
                    a('      </bpmn:lane>')
                a('    </bpmn:laneSet>')
            for nid, n in self.nodes.items():
                if n["pool"] == p["id"]:
                    self._render_bpmn_node(o, n)
            for f in self.seqs:
                if f["pool"] == p["id"]:
                    a(f'    <bpmn:sequenceFlow id="{f["id"]}" name="{escape(f["label"])}" '
                      f'sourceRef="{f["src"]}" targetRef="{f["tgt"]}" />')
            for ann in self.annotations:
                if ann["pool"] == p["id"]:
                    a(f'    <bpmn:textAnnotation id="{ann["id"]}">'
                      f'<bpmn:text>{escape(ann["text"])}</bpmn:text></bpmn:textAnnotation>')
            a('  </bpmn:process>')

        # DI
        a('  <bpmndi:BPMNDiagram id="Diagram_1">')
        a('    <bpmndi:BPMNPlane id="Plane_1" bpmnElement="Collab_1">')
        ish = "true" if self._is_horizontal_flag() else "false"

        def shape(el, x, y, w, h, isd=None, ck=None):
            extra = "" if isd is None else f' isHorizontal="{isd}"'
            bioc = ""
            if ck:
                fill, stroke = self.colors[ck]
                bioc = (f' bioc:stroke="{stroke}" bioc:fill="{fill}"'
                        f' color:background-color="{fill}" color:border-color="{stroke}"')
            a(f'      <bpmndi:BPMNShape id="{el}_di" bpmnElement="{el}"{extra}{bioc}>')
            a(f'        <dc:Bounds x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" />')
            a('      </bpmndi:BPMNShape>')

        for p in self.pools:
            x, y, w, h = self._pool_bounds(p["id"])
            shape(f'Pool_{p["id"]}', x, y, w, h, isd=ish)
            for ln in p["lanes"]:
                lx, ly, lw, lh = self._lane_bounds(p["id"], ln)
                shape(f'Lane_{p["id"]}_{ln}', lx, ly, lw, lh, isd=ish)
        for nid, n in self.nodes.items():
            x, y, w, h = self._bounds(n)
            shape(nid, x, y, w, h, ck=n["color"])
        for ann in self.annotations:
            ax, ay = self._annotation_xy(ann)
            shape(ann["id"], ax, ay, 360, 24)

        for f in self.seqs:
            self._edge(o, f["id"], self._seq_wp(f))
        for m in self.msgs:
            self._edge(o, m["id"], self._msg_wp(m))
        a('    </bpmndi:BPMNPlane>')
        a('  </bpmndi:BPMNDiagram>')
        a('</bpmn:definitions>')
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(o))
        return path

    def _render_bpmn_node(self, o, n):
        a = o.append
        nid, lbl, st = n["id"], escape(n["label"]), n["subtype"]
        fill, stroke = self.colors[n["color"]]
        col_attr = f' color:background-color="{fill}" color:border-color="{stroke}"'
        inc = [f["id"] for f in self.seqs if f["tgt"] == nid]
        out = [f["id"] for f in self.seqs if f["src"] == nid]
        inner = "".join(f'      <bpmn:incoming>{i}</bpmn:incoming>\n' for i in inc)
        inner += "".join(f'      <bpmn:outgoing>{x}</bpmn:outgoing>\n' for x in out)
        if n["kind"] == "event":
            tag = {"start": "startEvent", "end": "endEvent",
                   "catch": "intermediateCatchEvent"}[st]
            evd = f'      <bpmn:messageEventDefinition id="{nid}_d" />\n' \
                if n["evdef"] == "message" else ""
            a(f'    <bpmn:{tag} id="{nid}" name="{lbl}"{col_attr}>')
            o.append(inner + evd)
            a(f'    </bpmn:{tag}>')
        elif n["kind"] == "gateway":
            tag = {"exclusive": "exclusiveGateway", "parallel": "parallelGateway",
                   "inclusive": "inclusiveGateway"}[st]
            a(f'    <bpmn:{tag} id="{nid}" name="{lbl}"{col_attr}>')
            o.append(inner)
            a(f'    </bpmn:{tag}>')
        else:
            tag = {"user": "userTask", "service": "serviceTask",
                   "send": "sendTask", "receive": "receiveTask"}[st]
            a(f'    <bpmn:{tag} id="{nid}" name="{lbl}"{col_attr}>')
            o.append(inner)
            a(f'    </bpmn:{tag}>')

    def _edge(self, o, eid, pts):
        o.append(f'      <bpmndi:BPMNEdge id="{eid}_di" bpmnElement="{eid}">')
        for px, py in pts:
            o.append(f'        <di:waypoint x="{px:.0f}" y="{py:.0f}" />')
        o.append('      </bpmndi:BPMNEdge>')

    # waypoint routing in flow-axis-aware terms (par = flow dir, perp = lane dir)
    def _seq_wp(self, f):
        s, t = self.nodes[f["src"]], self.nodes[f["tgt"]]
        sx, sy = self._center(s); tx, ty = self._center(t)
        sw, sh = SIZE[s["kind"]]; tw, th = SIZE[t["kind"]]
        v = self.orientation == "vertical"
        s_par, t_par = (sy, ty) if v else (sx, tx)
        if t_par < s_par - 2:                      # back-edge / loop -> route aside
            if v:
                rx = max(sx, tx) + TRACK / 2 + 30
                return [(sx + sw/2, sy), (rx, sy), (rx, ty), (tx + tw/2, ty)]
            ry = max(sy, ty) + TRACK / 2 + 25
            return [(sx, sy + sh/2), (sx, ry), (tx, ry), (tx, ty + th/2)]
        if v:
            if abs(sx - tx) < 4:
                return [(sx, sy + sh/2), (tx, ty - th/2)]
            mid = (sy + sh/2 + ty - th/2) / 2
            return [(sx, sy + sh/2), (sx, mid), (tx, mid), (tx, ty - th/2)]
        if abs(sy - ty) < 4:
            return [(sx + sw/2, sy), (tx - tw/2, ty)]
        mid = (sx + sw/2 + tx - tw/2) / 2
        return [(sx + sw/2, sy), (mid, sy), (mid, ty), (tx - tw/2, ty)]

    def _msg_wp(self, m):
        s, t = self.nodes[m["src"]], self.nodes[m["tgt"]]
        sx, sy = self._center(s); tx, ty = self._center(t)
        sw, sh = SIZE[s["kind"]]; tw, th = SIZE[t["kind"]]
        v = self.orientation == "vertical"
        if v:  # message flows run perpendicular -> horizontal connectors
            sp = (sx + sw/2, sy) if sx < tx else (sx - sw/2, sy)
            tp = (tx - tw/2, ty) if sx < tx else (tx + tw/2, ty)
            if abs(sy - ty) < 4:
                return [sp, tp]
            mid = (sp[0] + tp[0]) / 2
            return [sp, (mid, sy), (mid, ty), tp]
        sp = (sx, sy + sh/2) if sy < ty else (sx, sy - sh/2)
        tp = (tx, ty - th/2) if sy < ty else (tx, ty + th/2)
        if abs(sx - tx) < 4:
            return [sp, tp]
        mid = (sp[1] + tp[1]) / 2
        return [sp, (sx, mid), (tx, mid), tp]

    def _annotation_xy(self, ann):
        lo, hi = self._pool_span[ann["pool"]]
        par = PAR_ORIGIN + ann["col"] * self._step - 55
        if self.orientation == "vertical":
            return lo, par
        return par, lo - 30

    # ----------------------------------------------------------- draw.io
    def emit_drawio(self, path):
        self._layout()
        o = []
        a = o.append
        a('<?xml version="1.0" encoding="UTF-8"?>')
        a('<mxfile host="app.diagrams.net" type="device">')
        a('  <diagram id="d1" name="BPMN">')
        a('    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" '
          'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
          'pageWidth="850" pageHeight="1169" math="0" shadow="0">')
        a('      <root>')
        a('        <mxCell id="0" />')
        a('        <mxCell id="1" parent="0" />')
        # draw.io horizontal flag is INVERTED vs intuition: a *vertical* pool
        # (lanes as columns, flow downward) uses horizontal=1 (title on top).
        dh = 1 if self.orientation == "vertical" else 0

        def vtx(cid, val, style, x, y, w, h):
            a(f'        <mxCell id="{cid}" value="{escape(val)}" style="{style}" '
              f'vertex="1" parent="1">')
            a(f'          <mxGeometry x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" '
              f'height="{h:.0f}" as="geometry" />')
            a('        </mxCell>')

        # pools then lanes (behind nodes), all absolute on layer "1"
        for p in self.pools:
            x, y, w, h = self._pool_bounds(p["id"])
            tint = p["tint"] or "#FAFAFA"
            vtx(f'dpool_{p["id"]}', p["name"],
                f'swimlane;html=1;horizontal={dh};startSize={POOL_TITLE};'
                f'fillColor={tint};strokeColor=#444444;fontStyle=1;fontSize=13;'
                f'swimlaneFillColor=none;', x, y, w, h)
            for ln in p["lanes"]:
                lx, ly, lw, lh = self._lane_bounds(p["id"], ln)
                vtx(f'dlane_{p["id"]}_{ln}', ln,
                    f'swimlane;html=1;horizontal={dh};startSize={LANE_TITLE};'
                    f'fillColor=none;strokeColor=#999999;fontSize=10;', lx, ly, lw, lh)
        for nid, n in self.nodes.items():
            x, y, w, h = self._bounds(n)
            vtx(f'd_{nid}', n["label"], self._drawio_style(n), x, y, w, h)
        for ann in self.annotations:
            ax, ay = self._annotation_xy(ann)
            vtx(f'd_{ann["id"]}', ann["text"],
                'text;html=1;strokeColor=none;fillColor=none;align=left;'
                'verticalAlign=middle;fontStyle=1;fontSize=14;', ax, ay, 360, 24)

        def edge(cid, val, style, src, tgt):
            a(f'        <mxCell id="{cid}" value="{escape(val)}" style="{style}" '
              f'edge="1" parent="1" source="{src}" target="{tgt}">')
            a('          <mxGeometry relative="1" as="geometry" />')
            a('        </mxCell>')

        for f in self.seqs:
            edge(f'de_{f["id"]}', f["label"],
                 'edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;'
                 'endFill=1;strokeColor=#444444;fontSize=9;labelBackgroundColor=#FFFFFF;',
                 f'd_{f["src"]}', f'd_{f["tgt"]}')
        for m in self.msgs:
            edge(f'de_{m["id"]}', m["label"],
                 'edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;dashed=1;dashPattern=6 4;'
                 'startArrow=oval;startFill=0;endArrow=open;endFill=0;strokeColor=#1565C0;'
                 'fontSize=9;fontColor=#1565C0;labelBackgroundColor=#FFFFFF;',
                 f'd_{m["src"]}', f'd_{m["tgt"]}')
        a('      </root>')
        a('    </mxGraphModel>')
        a('  </diagram>')
        a('</mxfile>')
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(o))
        return path

    def _drawio_style(self, n):
        fill, stroke = self.colors[n["color"]]
        if n["kind"] == "task":
            return f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize=10;"
        if n["kind"] == "gateway":
            return f"rhombus;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize=9;"
        sw = {"start": 1, "end": 3, "catch": 2}[n["subtype"]]
        extra = "dashed=1;" if n["subtype"] == "catch" else ""
        return (f"ellipse;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
                f"strokeWidth={sw};fontSize=8;{extra}")
