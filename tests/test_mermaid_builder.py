"""Tests for the Mermaid diagram builder utilities."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import pytest

import x_cls_make_mermaid_x as mermaid_module
from x_cls_make_mermaid_x import CommandError, MermaidBuilder


def test_flowchart_source_includes_nodes_and_edges() -> None:
    builder = (
        MermaidBuilder()
        .flowchart("TD")
        .node("A", "Start")
        .node("B", "End", shape="round")
        .edge("A", "B", "go", arrow="-->", style="stroke-width:2px")
    )

    mermaid = builder.source()

    assert mermaid.startswith("flowchart TD")
    assert 'A["Start"]' in mermaid
    assert "B(End)" in mermaid
    assert "A -->|go| B stroke-width:2px" in mermaid


def test_to_svg_returns_none_when_cli_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    builder = MermaidBuilder().flowchart("LR").node("A", "Start")
    mmd_path = tmp_path / "diagram.mmd"

    def missing_cli(cmd: str, mode: int | None = None, path: str | None = None) -> None:  # noqa: ARG001
        return None

    monkeypatch.setattr(mermaid_module.shutil, "which", missing_cli)

    result = builder.to_svg(mmd_path=str(mmd_path))

    assert result is None
    assert mmd_path.exists()
    assert "flowchart" in mmd_path.read_text(encoding="utf-8")
    assert not (tmp_path / "diagram.svg").exists()


def test_to_svg_invokes_cli_when_available(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    builder = MermaidBuilder().flowchart("LR").node("A", "Start")
    mmd_path = tmp_path / "diagram.mmd"
    svg_path = tmp_path / "diagram.svg"
    fake_cli = tmp_path / "mmdc.exe"
    fake_cli.touch()

    def locate_cli(cmd: str, mode: int | None = None, path: str | None = None) -> str:  # noqa: ARG001
        return str(fake_cli)

    monkeypatch.setattr(mermaid_module.shutil, "which", locate_cli)

    captured: dict[str, Any] = {}

    def fake_run(args: list[str], capture_output: bool, text: bool, check: bool) -> subprocess.CompletedProcess[str]:
        captured["args"] = tuple(args)
        captured["kwargs"] = {
            "capture_output": capture_output,
            "text": text,
            "check": check,
        }
        return subprocess.CompletedProcess(args=args, returncode=0, stdout="done", stderr="")

    monkeypatch.setattr(mermaid_module.subprocess, "run", fake_run)

    result = builder.to_svg(mmd_path=str(mmd_path), svg_path=str(svg_path))

    assert result == str(svg_path)
    assert captured["args"][0] == str(fake_cli)
    assert captured["kwargs"]["capture_output"] is True
    assert not svg_path.exists()


def test_run_command_returns_completed_process(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run(args: list[str], capture_output: bool, text: bool, check: bool) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(args=args, returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(mermaid_module.subprocess, "run", fake_run)

    result = mermaid_module.run_command(["mmdc", "--version"])

    assert isinstance(result, subprocess.CompletedProcess)
    assert result.stdout == "ok"


def test_run_command_raises_command_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run(args: list[str], capture_output: bool, text: bool, check: bool) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(args=args, returncode=2, stdout="", stderr="boom")

    monkeypatch.setattr(mermaid_module.subprocess, "run", fake_run)

    with pytest.raises(CommandError) as excinfo:
        mermaid_module.run_command(["mmdc", "render"], check=True)

    err = excinfo.value  # type: ignore[attr-defined]
    assert isinstance(err, CommandError)
    assert err.returncode == 2
    assert err.stderr == "boom"
    assert tuple(err.argv) == ("mmdc", "render")
