"""Tests for the Mermaid diagram builder utilities."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, cast

import pytest

from x_make_mermaid_x import x_cls_make_mermaid_x as mermaid_module
from x_make_mermaid_x.x_cls_make_mermaid_x import CommandError, MermaidBuilder

if TYPE_CHECKING:
    from _pytest._code.code import ExceptionInfo
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

    if not mermaid.startswith("flowchart TD"):
        raise AssertionError("Mermaid source should start with flowchart header")
    if 'A["Start"]' not in mermaid:
        raise AssertionError("Start node should be present")
    if "B(End)" not in mermaid:
        raise AssertionError("End node should use round shape")
    if "A -->|go| B stroke-width:2px" not in mermaid:
        raise AssertionError("Edge with label and style should be emitted")


def test_to_svg_returns_none_when_cli_missing(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    builder = MermaidBuilder().flowchart("LR").node("A", "Start")
    mmd_path = tmp_path / "diagram.mmd"

    def missing_cli(
        cmd: str, mode: int | None = None, path: str | None = None
    ) -> None:
        return None

    monkeypatch.setattr(
        "x_make_mermaid_x.x_cls_make_mermaid_x.shutil.which",
        missing_cli,
    )

    result = builder.to_svg(mmd_path=str(mmd_path))

    if result is not None:
        raise AssertionError("When CLI is missing, to_svg should return None")
    if not mmd_path.exists():
        raise AssertionError("DOT fallback should be written")
    if "flowchart" not in mmd_path.read_text(encoding="utf-8"):
        raise AssertionError("Fallback file should contain Mermaid source")
    if (tmp_path / "diagram.svg").exists():
        raise AssertionError("SVG file should not be created without CLI")


def test_to_svg_invokes_cli_when_available(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    builder = MermaidBuilder().flowchart("LR").node("A", "Start")
    mmd_path = tmp_path / "diagram.mmd"
    svg_path = tmp_path / "diagram.svg"
    fake_cli = tmp_path / "mmdc.exe"
    fake_cli.touch()

    def locate_cli(
        cmd: str, mode: int | None = None, path: str | None = None
    ) -> str:
        return str(fake_cli)

    monkeypatch.setattr(
        "x_make_mermaid_x.x_cls_make_mermaid_x.shutil.which",
        locate_cli,
    )

    captured: dict[str, object] = {}

    def fake_run(
        args: list[str], capture_output: bool, text: bool, check: bool
    ) -> subprocess.CompletedProcess[str]:
        captured["args"] = tuple(args)
        captured["kwargs"] = {
            "capture_output": capture_output,
            "text": text,
            "check": check,
        }
        return subprocess.CompletedProcess(
            args=args, returncode=0, stdout="done", stderr=""
        )

    monkeypatch.setattr(
        "x_make_mermaid_x.x_cls_make_mermaid_x.subprocess.run",
        fake_run,
    )

    result = builder.to_svg(mmd_path=str(mmd_path), svg_path=str(svg_path))

    if result != str(svg_path):
        raise AssertionError("CLI path should be returned when invocation succeeds")
    args = captured.get("args")
    if not isinstance(args, tuple) or not args or args[0] != str(fake_cli):
        raise AssertionError("Mermaid CLI path should be first argument")
    kwargs_obj = captured.get("kwargs")
    if not isinstance(kwargs_obj, dict):
        raise AssertionError("Captured kwargs should be a dict")
    kwargs = cast("dict[str, object]", kwargs_obj)
    if kwargs.get("capture_output") is not True:
        raise AssertionError("CLI should capture stdout/stderr")
    if svg_path.exists():
        raise AssertionError("SVG should not be created during dry run")


def test_run_command_returns_completed_process(monkeypatch: MonkeyPatch) -> None:
    def fake_run(
        args: list[str], capture_output: bool, text: bool, check: bool
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args=args, returncode=0, stdout="ok", stderr=""
        )

    monkeypatch.setattr(
        "x_make_mermaid_x.x_cls_make_mermaid_x.subprocess.run",
        fake_run,
    )

    result = mermaid_module.run_command(["mmdc", "--version"])

    if result.stdout != "ok":
        raise AssertionError("stdout should be passed through")


def test_run_command_raises_command_error(monkeypatch: MonkeyPatch) -> None:
    def fake_run(
        args: list[str], capture_output: bool, text: bool, check: bool
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args=args, returncode=2, stdout="", stderr="boom"
        )

    monkeypatch.setattr(
        "x_make_mermaid_x.x_cls_make_mermaid_x.subprocess.run",
        fake_run,
    )

    with pytest.raises(CommandError) as excinfo:
        mermaid_module.run_command(["mmdc", "render"], check=True)

    info = cast("ExceptionInfo[CommandError]", excinfo)
    err = info.value
    if err.returncode != 2:
        raise AssertionError("CommandError should expose return code")
    if err.stderr != "boom":
        raise AssertionError("CommandError should expose stderr output")
    if tuple(err.argv) != ("mmdc", "render"):
        raise AssertionError("CommandError should expose argv")
