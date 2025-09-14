# x_make_mermaid_x

Flexible Mermaid builder that emits `.mmd` and can convert to SVG via mermaid-cli.

Features:
- Diagram types: Flowchart, Sequence, Class, State (v2), ER, Gantt, Journey, Pie, Timeline, Mindmap, GitGraph, Requirement, Quadrant.
- Flowchart helpers: nodes, edges, subgraphs, styles, classes, hyperlinks, and link styling
  - node(id, label, shape)
  - edge(src, dst, label=None, arrow="-->", style="stroke:#1e90ff,stroke-width:2px")
  - style_node(id, "fill:#eef,stroke:#336,stroke-width:2px")
  - class_def("warn", {"fill":"#fee","stroke":"#c33"}), add_class(["A","B"], "warn")
  - click(id, url, tooltip)
  - link_style(index, css) and link_style_last(css) if you add a helper
- Global directives/themes:
  - set_directive('%%{init: {"theme":"forest"}}%%')
  - or build your own payload for themeVariables

Usage:
```python
from x_4357_make_mermaid_x.x_cls_make_mermaid_x import x_cls_make_mermaid_x as M

m = M().flowchart("LR")
m.node("A","Start","round").node("B","End","stadium").edge("A","B","go")
m.style_node("B", "fill:#efe,stroke:#393,stroke-width:2px")
m.click("B", "https://example.com", "Open example")
path = m.save("example.mmd")
# Convert to SVG (requires mermaid-cli)
m.to_svg("example.mmd","example.svg")
```

SVG conversion:
- Install Node.js and mermaid-cli: `npm install -g @mermaid-js/mermaid-cli`
- Ensure `mmdc` is on PATH. Then `m.to_svg(...)` or `mmdc -i example.mmd -o example.svg`.
m.to_svg("example.mmd","example.svg")
```

SVG conversion:
- Install Node.js and mermaid-cli: `npm install -g @mermaid-js/mermaid-cli`
- Ensure `mmdc` is on PATH. Then `m.to_svg(...)` or `mmdc -i example.mmd -o example.svg`.
