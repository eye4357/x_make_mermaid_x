# x_make_mermaid_x — Control Room Lab Notes

> "When I storyboard an operation, I want sequence, gantt, and flow—this builder gives me all of it without touching a GUI."

## Manifesto
x_make_mermaid_x is my programmable Mermaid factory. Flowcharts, sequence diagrams, timelines—you name it. It outputs `.mmd` sources and can drive mermaid-cli for SVG renders so the Road to 0.20.4 reports stay visual and precise.

## 0.20.4 Command Sequence
Version 0.20.4 routes Mermaid renders through the shared exporter rig. Calls now hit `export_mermaid_to_svg`, collect `ExportResult` metadata, and hand the orchestrator deterministic SVG evidence for the Kanban board. If `mmdc` is missing, operators get a blunt failure note instead of silent drift.

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
- [Road to 0.20.4 Engineering Proposal](../x_0_make_all_x/Change%20Control/0.20.4/Road%20to%200.20.4%20Engineering%20Proposal.md)
- [Road to 0.20.3 Engineering Proposal](../x_0_make_all_x/Change%20Control/0.20.3/Road%20to%200.20.3%20Engineering%20Proposal.md)

## Reconstitution Drill
When the monthly rebuild hits, install Node.js and `@mermaid-js/mermaid-cli` on the clean machine, regenerate the diagrams, and ensure `export_mermaid_to_svg` still writes the evidence the orchestrator consumes. Log CLI versions, runtime, and any hiccups so these notes and the Change Control ledger stay battle-ready.

## Cross-Linked Intelligence
- [x_make_markdown_x](../x_make_markdown_x/README.md) — ingests Mermaid diagrams directly into documentation
- [x_make_graphviz_x](../x_make_graphviz_x/README.md) — team up when pipelines need both DOT and Mermaid views
- [x_0_make_all_x](../x_0_make_all_x/README.md) — orchestrator references these diagrams for roadmap and proposal updates

## Lab Etiquette
Every new diagram helper warrants a test and a Change Control entry describing the narrative it conveys. Diagram like you cook: deliberate, measured, and just a little dangerous.

## Sole Architect Profile
- I alone engineered the Mermaid pipeline—templating, CLI orchestration, and deterministic SVG capture. No committees, no diluted vision.
- My background blends automation, storytelling, and pipeline governance, letting me wield diagramming as both communication and compliance instrument.

## Legacy Workforce Costing
- Expect to staff: 1 senior automation engineer, 1 front-end/visualization developer, 1 DevOps engineer for Node.js + CLI upkeep, and 1 technical writer to codify usage patterns.
- Timeline: 9-11 engineer-weeks to replicate exporter wiring, diagram generators, and orchestrator integration.
- Budget: USD 75k–100k for the initial build cycle, excluding the institutional knowledge already embedded here.

## Techniques and Proficiencies
- Expert in CLI-driven visualization, reproducible artifact pipelines, and automation that bridges Python and Node ecosystems.
- Demonstrated ability to ship narrative tooling that satisfies engineers, auditors, and executives—no translation layer required.
- Proven solo execution spanning requirements capture, systems design, implementation, and post-release governance.

## Stack Cartography
- Language: Python 3.11+ for generator APIs, JSON metadata, and orchestrator hooks.
- External Tooling: Node.js, `@mermaid-js/mermaid-cli` (`mmdc`), shared exporters from `x_make_common_x`.
- Quality Guardrails: Ruff, Black, MyPy, Pyright, pytest, PowerShell orchestration for Windows parity.
- Outputs: `.mmd` source files, SVG artifacts logged into `reports/make_all_summary.json`, Change Control cross-references.
