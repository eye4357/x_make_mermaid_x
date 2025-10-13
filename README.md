# x_make_mermaid_x — Lab Notes from Walter White

> "When I storyboard an operation, I want sequence, gantt, and flow—this builder gives me all of it without touching a GUI."

## Manifesto
x_make_mermaid_x is my programmable Mermaid factory. Flowcharts, sequence diagrams, timelines—you name it. It outputs `.mmd` sources and can drive mermaid-cli for SVG renders so the Road to 0.20.0 reports stay visual and precise.

## Ingredients
- Python 3.11+
- Node.js with `@mermaid-js/mermaid-cli` (`mmdc` on PATH) for SVG generation
- Ruff, Black, MyPy, and Pyright to safeguard the builder APIs

## Cook Instructions
1. `python -m venv .venv`
2. `.\.venv\Scripts\Activate.ps1`
3. `python -m pip install --upgrade pip`
4. `pip install -r requirements.txt`
5. `python -m x_make_mermaid_x.tests.example` or your own scripts to render diagrams and confirm the CLI toolchain is live

## Quality Assurance
| Check | Command |
| --- | --- |
| Formatting sweep | `python -m black .`
| Lint interrogation | `python -m ruff check .`
| Type audit | `python -m mypy .`
| Static contract scan | `python -m pyright`
| Functional verification | `pytest`

## Distribution Chain
- [Changelog](./CHANGELOG.md)
- [Road to 0.20.0 Control Room](../x_0_make_all_x/Change%20Control/0.20.0/index.md)
- [Road to 0.20.0 Engineering Proposal](../x_0_make_all_x/Change%20Control/0.20.0/Road%20to%200.20.0%20Engineering%20Proposal%20-%20Walter%20White.md)

## Cross-Linked Intelligence
- [x_make_markdown_x](../x_make_markdown_x/README.md) — ingests Mermaid diagrams directly into documentation
- [x_make_graphviz_x](../x_make_graphviz_x/README.md) — team up when pipelines need both DOT and Mermaid views
- [x_0_make_all_x](../x_0_make_all_x/README.md) — orchestrator references these diagrams for roadmap and proposal updates

## Lab Etiquette
Every new diagram helper warrants a test and a Change Control entry describing the narrative it conveys. Diagram like you cook: deliberate, measured, and just a little dangerous.
