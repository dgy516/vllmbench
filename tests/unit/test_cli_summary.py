from pathlib import Path

import pytest

from bench_core import cli


def _fixture_path(name: str) -> str:
    here = Path(__file__).resolve()
    root = here.parents[2]
    return str(root / "tests" / "data" / name)


def test_cli_prints_summary_for_single_file(capsys: pytest.CaptureFixture[str]):
    path = _fixture_path("scenario_base.yaml")
    rc = cli.main(["-f", path])
    assert rc == 0
    out = capsys.readouterr().out
    assert "schema_version: v1" in out
    assert "scenario_name: basic_stream_toppp" in out
    assert "workload.streaming: True" in out
    assert "workload.concurrency: [4, 16]" in out


def test_cli_applies_overlay_and_updates_summary(capsys: pytest.CaptureFixture[str]):
    base = _fixture_path("scenario_base.yaml")
    overlay = _fixture_path("scenario_overlay.yaml")
    rc = cli.main(["-f", base, "-f", overlay])
    assert rc == 0
    out = capsys.readouterr().out
    assert "workload.streaming: False" in out
    assert "workload.concurrency: [8, 32]" in out

