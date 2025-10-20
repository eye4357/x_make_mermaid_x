from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import pytest
from x_make_common_x.exporters import ExportResult
from x_make_common_x.json_contracts import validate_payload, validate_schema

from x_make_mermaid_x.json_contracts import (
    ERROR_SCHEMA,
    INPUT_SCHEMA,
    OUTPUT_SCHEMA,
)
from x_make_mermaid_x.x_cls_make_mermaid_x import main_json

if TYPE_CHECKING:
    from _pytest.monkeypatch import MonkeyPatch
else:
    pytest = cast("Any", pytest)

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "json_contracts"
REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"


def _load_fixture(name: str) -> dict[str, object]:
    with (FIXTURE_DIR / f"{name}.json").open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return cast("dict[str, object]", data)


@pytest.fixture(scope="module")
def sample_input() -> dict[str, object]:
    return _load_fixture("input")


@pytest.fixture(scope="module")
def sample_output() -> dict[str, object]:
    return _load_fixture("output")


@pytest.fixture(scope="module")
def sample_error() -> dict[str, object]:
    return _load_fixture("error")


def test_schemas_are_valid() -> None:
    for schema in (INPUT_SCHEMA, OUTPUT_SCHEMA, ERROR_SCHEMA):
        validate_schema(schema)


def test_sample_payloads_match_schema(
    sample_input: dict[str, object],
    sample_output: dict[str, object],
    sample_error: dict[str, object],
) -> None:
    validate_payload(sample_input, INPUT_SCHEMA)
    validate_payload(sample_output, OUTPUT_SCHEMA)
    validate_payload(sample_error, ERROR_SCHEMA)


def test_existing_reports_align_with_schema() -> None:
    if not REPORTS_DIR.exists():
        pytest.skip("no reports directory for mermaid tool")
    report_files = sorted(REPORTS_DIR.glob("x_make_mermaid_x_run_*.json"))
    if not report_files:
        pytest.skip("no mermaid run reports to validate")
    for report_file in report_files:
        with report_file.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        validate_payload(payload, OUTPUT_SCHEMA)


def test_main_json_builds_from_document(
    sample_input: dict[str, object],
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    payload = json.loads(json.dumps(sample_input))
    output_dir = tmp_path / "artifacts"
    payload["parameters"]["output_mermaid"] = str(output_dir / "diagram.mmd")
    payload["parameters"]["output_svg"] = str(output_dir / "diagram.svg")
    fake_cli = tmp_path / "bin" / "mmdc.cmd"
    fake_cli.parent.mkdir(parents=True, exist_ok=True)
    fake_cli.write_text("binary", encoding="utf-8")
    payload["parameters"]["mermaid_cli_path"] = str(fake_cli)

    def fake_export(
        mermaid_source: str,
        *,
        output_dir: Path,
        stem: str,
        mermaid_cli_path: str | None = None,
        runner=None,
        extra_args=None,
    ) -> ExportResult:
        mmd_path = output_dir / f"{stem}.mmd"
        output_dir.mkdir(parents=True, exist_ok=True)
        mmd_path.write_text(mermaid_source, encoding="utf-8")
        svg_path = output_dir / f"{stem}.svg"
        svg_path.write_text("<svg />", encoding="utf-8")
        command = ("mmdc", "-i", str(mmd_path), "-o", str(svg_path))
        return ExportResult(
            exporter="mermaid-cli",
            succeeded=True,
            output_path=svg_path,
            command=command,
            stdout="",
            stderr="",
            inputs={"mermaid": mmd_path},
            binary_path=Path(mermaid_cli_path) if mermaid_cli_path else None,
        )

    monkeypatch.setattr(
        "x_make_mermaid_x.x_cls_make_mermaid_x.export_mermaid_to_svg",
        fake_export,
    )

    result = main_json(payload)

    validate_payload(result, OUTPUT_SCHEMA)
    status_value = result.get("status")
    assert isinstance(status_value, str)
    assert status_value == "success"

    artifact_obj = result.get("mermaid")
    assert isinstance(artifact_obj, dict)
    source_path_value = artifact_obj.get("source_path")
    assert isinstance(source_path_value, str)
    mermaid_path = Path(source_path_value)
    assert mermaid_path.exists()
    source_bytes = artifact_obj.get("source_bytes")
    assert isinstance(source_bytes, int)
    assert source_bytes > 0

    svg_info_obj = artifact_obj.get("svg")
    assert isinstance(svg_info_obj, dict)
    assert svg_info_obj.get("succeeded") is True

    summary_obj = result.get("summary")
    assert isinstance(summary_obj, dict)
    assert summary_obj.get("diagram") == "flowchart"
    assert summary_obj.get("nodes") == 2
    assert summary_obj.get("edges") == 1

    messages_obj = result.get("messages")
    assert isinstance(messages_obj, list)
    assert messages_obj
    first_message = messages_obj[0]
    assert isinstance(first_message, str)
    assert "Mermaid CLI executed successfully" in first_message


def test_main_json_uses_raw_source(tmp_path: Path) -> None:
    payload = {
        "command": "x_make_mermaid_x",
        "parameters": {
            "output_mermaid": str(tmp_path / "raw.mmd"),
            "source": "graph TB; A-->B;",
        },
    }

    result = main_json(payload)

    validate_payload(result, OUTPUT_SCHEMA)
    artifact_obj = result.get("mermaid")
    assert isinstance(artifact_obj, dict)
    source_path_value = artifact_obj.get("source_path")
    assert isinstance(source_path_value, str)
    mermaid_path = Path(source_path_value)
    assert mermaid_path.read_text(encoding="utf-8").endswith("\n")

    summary_obj = result.get("summary")
    assert isinstance(summary_obj, dict)
    assert summary_obj.get("export_svg") is False


def test_main_json_reports_validation_error() -> None:
    payload = {"command": "x_make_mermaid_x", "parameters": {}}

    result = main_json(payload)

    validate_payload(result, ERROR_SCHEMA)
    status_value = result.get("status")
    message_value = result.get("message")
    assert isinstance(status_value, str)
    assert isinstance(message_value, str)
    assert status_value == "failure"
    assert message_value == "input payload failed validation"
