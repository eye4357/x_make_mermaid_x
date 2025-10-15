"""Tests for the Mermaid diagram builder utilities."""

# ruff: noqa: S101 - tests rely on assert statements for clarity

from __future__ import annotations

import subprocess
from collections.abc import Sequence
from pathlib import Path
from subprocess import CompletedProcess
from typing import TYPE_CHECKING

from x_make_mermaid_x import x_cls_make_mermaid_x as mermaid_module
from x_make_mermaid_x.x_cls_make_mermaid_x import CommandError, MermaidBuilder

if TYPE_CHECKING:
    from _pytest.monkeypatch import MonkeyPatch


def test_flowchart_source_includes_nodes_and_edges() -> None:
    builder = (
        MermaidBuilder()
        .flowchart("TD")
        .node("A", "Start")
        .node("B", "End", shape="round")
        .edge("A", "B", "go", arrow="-->", style="stroke-width:2px")
    )

    mermaid = builder.source()

    assert mermaid.startswith(
        "flowchart TD"
    ), "Mermaid source should start with flowchart header"
    assert 'A["Start"]' in mermaid, "Start node should be present"
    assert "B(End)" in mermaid, "End node should use round shape"
    assert (
        "A -->|go| B stroke-width:2px" in mermaid
    ), "Edge with label and style should be emitted"


def test_to_svg_returns_none_when_cli_missing(tmp_path: Path) -> None:
    builder = MermaidBuilder().flowchart("LR").node("A", "Start")
    mmd_path = tmp_path / "diagram.mmd"

    result = builder.to_svg(mmd_path=str(mmd_path))

    assert result is None, "When CLI is missing, to_svg should return None"
    assert mmd_path.exists(), "DOT fallback should be written"
    assert "flowchart" in mmd_path.read_text(
        encoding="utf-8"
    ), "Fallback file should contain Mermaid source"
    assert not (
        tmp_path / "diagram.svg"
    ).exists(), "SVG file should not be created without CLI"


def test_to_svg_invokes_cli_when_available(tmp_path: Path) -> None:
    captured: dict[str, Sequence[str]] = {}

    def runner(command: Sequence[str]) -> CompletedProcess[str]:
        captured["command"] = command
        try:
            out_index = command.index("-o") + 1
        except ValueError:  # pragma: no cover - defensive guard
            raise AssertionError("-o flag missing from command")
        svg_target = Path(command[out_index])
        svg_target.write_text("<svg />", encoding="utf-8")
        return CompletedProcess(list(command), 0, stdout="done", stderr="")

    fake_cli = tmp_path / "mmdc.exe"
    fake_cli.write_text("binary", encoding="utf-8")

    builder = MermaidBuilder(
        runner=runner,
        mermaid_cli=str(fake_cli),
    ).flowchart("LR").node("A", "Start")
    mmd_path = tmp_path / "diagram.mmd"
    svg_path = tmp_path / "diagram.svg"

    result = builder.to_svg(mmd_path=str(mmd_path), svg_path=str(svg_path))

    assert result == str(svg_path), "SVG path should be returned on success"
    assert svg_path.exists(), "SVG file should be written by exporter"
    command = captured.get("command")
    assert command is not None
    assert command[0] == str(fake_cli)
    last_result = builder.get_last_export_result()
    assert last_result and last_result.succeeded is True


def test_run_command_returns_completed_process(
    monkeypatch: MonkeyPatch,
) -> None:
    def fake_run(
        args: list[str],
        *,
        capture_output: bool = False,
        text: bool = False,
        check: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        _ = (capture_output, text, check)
        return subprocess.CompletedProcess(
            args=args, returncode=0, stdout="ok", stderr=""
        )

    monkeypatch.setattr(
        "x_make_mermaid_x.x_cls_make_mermaid_x.subprocess.run",
        fake_run,
    )

    result = mermaid_module.run_command(["mmdc", "--version"])

    assert result.stdout == "ok", "stdout should be passed through"


def test_run_command_raises_command_error(monkeypatch: MonkeyPatch) -> None:
    def fake_run(
        args: list[str],
        *,
        capture_output: bool = False,
        text: bool = False,
        check: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        _ = (capture_output, text, check)
        return subprocess.CompletedProcess(
            args=args, returncode=2, stdout="", stderr="boom"
        )

    monkeypatch.setattr(
        "x_make_mermaid_x.x_cls_make_mermaid_x.subprocess.run",
        fake_run,
    )

    err: CommandError | None = None
    try:
        mermaid_module.run_command(["mmdc", "render"], check=True)
    except CommandError as caught:
        err = caught
    else:  # pragma: no cover - defensive safeguard
        message = "CommandError should have been raised"
        raise AssertionError(message)

    assert err is not None
    expected_return_code = 2
    assert (
        err.returncode == expected_return_code
    ), "CommandError should expose return code"
    assert err.stderr == "boom", "CommandError should expose stderr output"
    assert tuple(err.argv) == (
        "mmdc",
        "render",
    ), "CommandError should expose argv"
