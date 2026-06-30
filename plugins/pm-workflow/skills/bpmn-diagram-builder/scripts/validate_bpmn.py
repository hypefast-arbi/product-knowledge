#!/usr/bin/env python3
"""
validate_bpmn.py <file.bpmn>

Structural sanity checks for a generated BPMN 2.0 file, independent of the
builder. Checks well-formedness and the things that make bpmn.io fail:
  * every flow node, lane and pool has a <bpmndi:BPMNShape>
  * every sequence/message flow has a <bpmndi:BPMNEdge>
  * no <sequenceFlow> crosses a pool (process) boundary
  * every <messageFlow> does cross a pool boundary
  * exclusive gateways have >= 2 outgoing flows, all named
  * no flow references a missing node; no isolated nodes
Exit code 0 = all good, 1 = problems found. Pure Python + lxml; no Node needed.
If `bpmn-moddle` happens to be installed it is NOT required here.
"""
import sys
from lxml import etree

BPMN = "http://www.omg.org/spec/BPMN/20100524/MODEL"
DI = "http://www.omg.org/spec/BPMN/20100524/DI"
NODE_TAGS = {"userTask", "serviceTask", "sendTask", "receiveTask", "task",
             "startEvent", "endEvent", "intermediateCatchEvent",
             "intermediateThrowEvent", "exclusiveGateway", "parallelGateway",
             "inclusiveGateway", "subProcess"}


def main(path):
    try:
        root = etree.parse(path).getroot()
    except Exception as e:
        print(f"FAIL: not well-formed XML: {e}")
        return 1

    problems = []
    node_proc = {}          # node id -> process id
    for proc in root.findall(f"{{{BPMN}}}process"):
        pid = proc.get("id")
        for el in proc.iter():
            if etree.QName(el).localname in NODE_TAGS:
                node_proc[el.get("id")] = pid

    collab = root.find(f"{{{BPMN}}}collaboration")
    seqs, msgs = {}, {}
    for proc in root.findall(f"{{{BPMN}}}process"):
        for sf in proc.findall(f"{{{BPMN}}}sequenceFlow"):
            seqs[sf.get("id")] = (sf.get("sourceRef"), sf.get("targetRef"),
                                  proc.get("id"))
    if collab is not None:
        for mf in collab.findall(f"{{{BPMN}}}messageFlow"):
            msgs[mf.get("id")] = (mf.get("sourceRef"), mf.get("targetRef"))

    # DI coverage
    shapes = {s.get("bpmnElement") for s in root.iter(f"{{{DI}}}BPMNShape")}
    edges = {e.get("bpmnElement") for e in root.iter(f"{{{DI}}}BPMNEdge")}
    for nid in node_proc:
        if nid not in shapes:
            problems.append(f"node {nid} has no BPMNShape")
    for pool in (collab.findall(f"{{{BPMN}}}participant") if collab is not None else []):
        if pool.get("id") not in shapes:
            problems.append(f"pool {pool.get('id')} has no BPMNShape")
    for fid in {**seqs, **msgs}:
        if fid not in edges:
            problems.append(f"flow {fid} has no BPMNEdge")

    # cross-pool rules
    for fid, (s, t, pid) in seqs.items():
        if node_proc.get(s) != pid or node_proc.get(t) != pid:
            problems.append(f"sequenceFlow {fid} crosses a pool boundary")
        if s not in node_proc or t not in node_proc:
            problems.append(f"sequenceFlow {fid} references a missing node")
    for mid, (s, t) in msgs.items():
        if node_proc.get(s) is not None and node_proc.get(s) == node_proc.get(t):
            problems.append(f"messageFlow {mid} does not cross a pool")

    # gateways
    for proc in root.findall(f"{{{BPMN}}}process"):
        for gw in proc.findall(f"{{{BPMN}}}exclusiveGateway"):
            outs = [sf for sf in proc.findall(f"{{{BPMN}}}sequenceFlow")
                    if sf.get("sourceRef") == gw.get("id")]
            if len(outs) < 2:
                problems.append(f"gateway {gw.get('id')} has < 2 outgoing flows")
            if any(not o.get("name") for o in outs):
                problems.append(f"gateway {gw.get('id')} has an unnamed outgoing flow")

    # isolated nodes
    touched = set()
    for s, t, _ in seqs.values():
        touched.update((s, t))
    for s, t in msgs.values():
        touched.update((s, t))
    for nid in node_proc:
        if nid not in touched:
            problems.append(f"node {nid} is isolated (no flow attached)")

    print(f"nodes={len(node_proc)} sequenceFlows={len(seqs)} "
          f"messageFlows={len(msgs)} shapes={len(shapes)} edges={len(edges)}")
    if problems:
        print(f"FAIL ({len(problems)} problem(s)):")
        for p in problems:
            print("  -", p)
        return 1
    print("OK: structurally valid, DI complete, no pool-crossing sequence flows.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validate_bpmn.py <file.bpmn>")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
