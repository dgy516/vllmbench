from pathlib import Path

import pytest

from bench_core import cli


def _fixture_path(name: str) -> str:
    here = Path(__file__).resolve()
    root = here.parents[2]
    return str(root / "tests" / "data" / name)


def test_cli_reports_config_error_with_code(capsys: pytest.CaptureFixture[str]):
    bad = _fixture_path("scenario_bad_version.yaml")
    rc = cli.main(["-f", bad])
    assert rc == 2
    err = capsys.readouterr().err
    assert "E_CONFIG" in err
    assert "schema_version" in err


def test_cli_reports_io_error_with_code(capsys: pytest.CaptureFixture[str]):
    rc = cli.main(["-f", "/path/does/not/exist.yaml"])  # type: ignore[path-type]
    assert rc == 2
    err = capsys.readouterr().err
    assert "E_IO" in err
    assert "No such file" in err or "not found" in err.lower()
