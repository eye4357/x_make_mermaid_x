"""JSON contracts for x_make_mermaid_x."""

from __future__ import annotations

_JSON_VALUE_SCHEMA: dict[str, object] = {
    "type": ["object", "array", "string", "number", "boolean", "null"],
}

_DIRECTIVE_SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {
        "text": {"type": "string", "minLength": 1},
        "payload": {"type": "object"},
    },
    "required": ["text"],
    "additionalProperties": False,
}

_COMMENT_SCHEMA: dict[str, object] = {
    "type": "string",
    "minLength": 1,
}

_NODE_SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {
        "id": {"type": "string", "minLength": 1},
        "label": {"type": ["string", "null"], "minLength": 1},
        "shape": {
            "type": ["string", "null"],
            "enum": [
                "rect",
                "round",
                "stadium",
                "subroutine",
                "cylinder",
                "circle",
                "asym",
                None,
            ],
        },
    },
    "required": ["id"],
    "additionalProperties": False,
}

_EDGE_SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {
        "source": {"type": "string", "minLength": 1},
        "target": {"type": "string", "minLength": 1},
        "label": {"type": ["string", "null"], "minLength": 1},
        "arrow": {
            "type": ["string", "null"],
            "pattern": "^[<-]{0,2}>{0,2}$",
        },
        "style": {"type": ["string", "null"], "minLength": 1},
    },
    "required": ["source", "target"],
    "additionalProperties": False,
}

_BLOCK_INSTRUCTION: dict[str, object] = {
    "type": "object",
    "properties": {
        "type": {
            "type": "string",
            "enum": [
                "line",
                "raw",
                "participant",
                "message",
                "note",
                "activate",
                "deactivate",
                "block",
                "gantt_section",
                "gantt_task",
                "journey_section",
                "journey_step",
                "pie_slice",
                "timeline_entry",
                "git_commit",
                "git_branch",
                "git_checkout",
                "git_merge",
                "mindmap_node",
                "req",
                "req_link",
                "quadrant",
                "quadrant_point",
            ],
        },
        "payload": _JSON_VALUE_SCHEMA,
    },
    "required": ["type", "payload"],
    "additionalProperties": False,
}

_DOCUMENT_SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {
        "diagram": {
            "type": "string",
            "enum": [
                "flowchart",
                "sequenceDiagram",
                "classDiagram",
                "stateDiagram-v2",
                "erDiagram",
                "gantt",
                "journey",
                "pie",
                "timeline",
                "gitGraph",
                "mindmap",
                "requirementDiagram",
                "quadrantChart",
                "sankey-beta",
                "xychart-beta",
                "block-beta",
            ],
        },
        "direction": {
            "type": ["string", "null"],
            "enum": ["LR", "RL", "TB", "BT", None],
        },
        "title": {"type": ["string", "null"], "minLength": 1},
        "date_format": {"type": ["string", "null"], "minLength": 1},
        "directives": {
            "type": "array",
            "items": _DIRECTIVE_SCHEMA,
        },
        "comments": {
            "type": "array",
            "items": _COMMENT_SCHEMA,
        },
        "nodes": {
            "type": "array",
            "items": _NODE_SCHEMA,
        },
        "edges": {
            "type": "array",
            "items": _EDGE_SCHEMA,
        },
        "lines": {
            "type": "array",
            "items": {"type": "string"},
        },
        "instructions": {
            "type": "array",
            "items": _BLOCK_INSTRUCTION,
        },
        "metadata": {
            "type": "object",
            "additionalProperties": _JSON_VALUE_SCHEMA,
        },
    },
    "required": ["diagram"],
    "additionalProperties": False,
}

_EXPORT_SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {
        "exporter": {"type": "string", "minLength": 1},
        "succeeded": {"type": "boolean"},
        "output_path": {"type": ["string", "null"], "minLength": 1},
        "command": {
            "type": "array",
            "items": {"type": "string"},
        },
        "stdout": {"type": "string"},
        "stderr": {"type": "string"},
        "inputs": {
            "type": "object",
            "additionalProperties": {"type": "string"},
        },
        "binary_path": {"type": ["string", "null"], "minLength": 1},
        "detail": {"type": ["string", "null"]},
    },
    "required": [
        "exporter",
        "succeeded",
        "output_path",
        "command",
        "stdout",
        "stderr",
        "inputs",
        "binary_path",
    ],
    "additionalProperties": False,
}

_MERMAID_ARTIFACT_SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {
        "source_path": {"type": "string", "minLength": 1},
        "source_bytes": {"type": "integer", "minimum": 0},
        "svg": _EXPORT_SCHEMA,
    },
    "required": ["source_path", "source_bytes"],
    "additionalProperties": False,
}

INPUT_SCHEMA: dict[str, object] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "x_make_mermaid_x input",
    "type": "object",
    "properties": {
        "command": {"const": "x_make_mermaid_x"},
        "parameters": {
            "type": "object",
            "properties": {
                "output_mermaid": {"type": "string", "minLength": 1},
                "output_svg": {"type": ["string", "null"], "minLength": 1},
                "mermaid_cli_path": {"type": ["string", "null"], "minLength": 1},
                "export_svg": {"type": "boolean"},
                "document": _DOCUMENT_SCHEMA,
                "source": {"type": "string", "minLength": 1},
            },
            "required": ["output_mermaid"],
            "additionalProperties": False,
            "anyOf": [
                {"required": ["document"]},
                {"required": ["source"]},
            ],
        },
    },
    "required": ["command", "parameters"],
    "additionalProperties": False,
}

OUTPUT_SCHEMA: dict[str, object] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "x_make_mermaid_x output",
    "type": "object",
    "properties": {
        "status": {"const": "success"},
        "schema_version": {"const": "x_make_mermaid_x.run/1.0"},
        "generated_at": {"type": "string", "format": "date-time"},
        "mermaid": _MERMAID_ARTIFACT_SCHEMA,
        "messages": {
            "type": "array",
            "items": {"type": "string"},
        },
        "summary": {
            "type": "object",
            "additionalProperties": _JSON_VALUE_SCHEMA,
        },
    },
    "required": ["status", "schema_version", "generated_at", "mermaid"],
    "additionalProperties": False,
}

ERROR_SCHEMA: dict[str, object] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "x_make_mermaid_x error",
    "type": "object",
    "properties": {
        "status": {"const": "failure"},
        "message": {"type": "string", "minLength": 1},
        "details": {
            "type": "object",
            "additionalProperties": _JSON_VALUE_SCHEMA,
        },
    },
    "required": ["status", "message"],
    "additionalProperties": True,
}

__all__ = ["ERROR_SCHEMA", "INPUT_SCHEMA", "OUTPUT_SCHEMA"]
