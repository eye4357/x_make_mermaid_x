"""Tests for the Mermaid diagram builder utilities."""

# ruff: noqa: S101 - tests rely on assert statements for clarity

from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING, cast

from x_make_mermaid_x import x_cls_make_mermaid_x as mermaid_module
from x_make_mermaid_x.x_cls_make_mermaid_x import CommandError, MermaidBuilder

if TYPE_CHECKING:
    from pathlib import Path

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


def test_to_svg_returns_none_when_cli_missing(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    builder = MermaidBuilder().flowchart("LR").node("A", "Start")
    mmd_path = tmp_path / "diagram.mmd"

    def missing_cli(
        _cmd: str, _mode: int | None = None, _path: str | None = None
    ) -> None:
        return None

    monkeypatch.setattr(
        "x_make_mermaid_x.x_cls_make_mermaid_x.shutil.which",
        missing_cli,
    )

    result = builder.to_svg(mmd_path=str(mmd_path))

    assert result is None, "When CLI is missing, to_svg should return None"
    assert mmd_path.exists(), "DOT fallback should be written"
    assert "flowchart" in mmd_path.read_text(
        encoding="utf-8"
    ), "Fallback file should contain Mermaid source"
    assert not (
        tmp_path / "diagram.svg"
    ).exists(), "SVG file should not be created without CLI"


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
        _cmd: str, _mode: int | None = None, _path: str | None = None
    ) -> str:
        return str(fake_cli)

    monkeypatch.setattr(
        "x_make_mermaid_x.x_cls_make_mermaid_x.shutil.which",
        locate_cli,
    )

    captured: dict[str, object] = {}

    def fake_run(
        args: list[str],
        *,
        capture_output: bool = False,
        text: bool = False,
        check: bool = False,
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

    assert result == str(
        svg_path
    ), "CLI path should be returned when invocation succeeds"
    args_obj = captured.get("args")
    assert isinstance(args_obj, tuple), "Captured args should be a tuple"
    args = cast("tuple[str, ...]", args_obj)
    assert args, "Captured args should not be empty"
    assert args[0] == str(fake_cli), "Mermaid CLI path should be first argument"
    kwargs_obj = captured.get("kwargs")
    assert isinstance(kwargs_obj, dict), "Captured kwargs should be a dict"
    kwargs = cast("dict[str, object]", kwargs_obj)
    assert kwargs.get("capture_output") is True, "CLI should capture stdout/stderr"
    assert not svg_path.exists(), "SVG should not be created during dry run"


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
