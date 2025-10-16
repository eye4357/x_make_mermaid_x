# Changelog — Control Room Production Log

All notable changes to x_make_mermaid_x are cataloged here. We hold to [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) standards and Semantic Versioning so every diagram evolution is traceable.

## [0.20.4] - 2025-10-15
### Changed
- Routed Mermaid renders through the shared `export_mermaid_to_svg` helper, emitting `ExportResult` telemetry and clear failure reasons when `mmdc` is offline.
- README tightened for the Road to 0.20.4 release to document the exporter hookup and Kanban evidence capture.

## [0.20.3] - 2025-10-14
### Changed
- Adjusted documentation and roadmap links for the Road to 0.20.3 release, highlighting the JSON-first storyboard updates.

## [0.20.2] - 2025-10-14
### Changed
- Rewrote the documentation to chart the Road to 0.20.2 storyboard expectations and hardened the guidance for the refreshed diagram pipeline.

## [0.20.1] - 2025-10-13
### Changed
- Updated README guidance to point at the Road to 0.20.1 control-room ledger so diagram tooling always mirrors the live cook.

## [0.20.0-prep] - 2025-10-12
### Added
- Documented the Mermaid factory in the control-room tone to align with the Road to 0.20.0 storytelling cadence.
- Linked the builder to Markdown, Graphviz, and orchestration hubs for unified reporting.

### Changed
- Clarified expectations for diagram contributions: automate the render, log the change, and never skip the Change Control entry.
