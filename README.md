# x_make_mermaid_x

Flexible Mermaid builder that emits `.mmd` and can convert to SVG via mermaid-cli.

Features:
- Diagram types: Flowchart, Sequence, Class, State (v2), ER, Gantt, Journey, Pie, Timeline, Mindmap, GitGraph, Requirement, Quadrant.
- Flowchart helpers: nodes, edges, subgraphs, styles, classes, hyperlinks, and link styling
  - node(id, label, shape)
  - edge(src, dst, label=None, arrow="-->", style="stroke:#f66,stroke-width:2px")
  - style_node(id, "fill:#eef,stroke:#336,stroke-width:2px")
  - class_def("warn", {"fill":"#fee","stroke":"#c33"}), add_class(["A","B"], "warn")
  - click(id, url, tooltip)
  - link_style_last("stroke:#1e90ff,stroke-width:3px") / link_style_at(i, css)
- Global themes/directives:
  - set_theme("dark", {"primaryColor":"#222","fontFamily":"Consolas"})
  - set_directive('%%{init: {"theme":"forest"}}%%')
- Sequence: participant, message, autonumber(), hide_footbox(), block("alt", "Title", [...]), note_over, activate/deactivate
- State: state_node, state_trans, state_direction("LR"), state_start/end, state_subgraph
- ER: er_entity, er_rel
- Gantt: gantt(), gantt_section(), gantt_task(), gantt_options(axis_format="MMM D", today_marker="stroke-width:2px", excludes=["weekends"])
- Pie: pie(), pie_slice(), pie_show_data()

Usage:
```python
from x_4357_make_mermaid_x.x_cls_make_mermaid_x import x_cls_make_mermaid_x as M

m = M().flowchart("LR").set_theme("default")
m.node("A","Start","round").node("B","End","stadium").edge("A","B","go")
m.link_style_last("stroke:#1e90ff,stroke-width:3px")
m.class_def("good", {"fill":"#efe","stroke":"#393"}).add_class("B","good")
m.click("B", "https://example.com", "Open example")
path = m.save("example.mmd")
# Convert to SVG (requires mermaid-cli)
m.to_svg("example.mmd","example.svg")
```

SVG conversion:
- Install Node.js and mermaid-cli: `npm install -g @mermaid-js/mermaid-cli`
- Ensure `mmdc` is on PATH. Then `m.to_svg(...)` or `mmdc -i example.mmd -o example.svg`.
