import os
from pathlib import Path

import pytest
from pydantic import ValidationError

from bench_core import loader


def _fixture_path(name: str) -> str:
    here = Path(__file__).resolve()
    root = here.parents[2]  # project root
    return str(root / "tests" / "data" / name)


def test_load_raises_on_empty_paths():
    with pytest.raises(ValueError):
        loader.load_and_validate([])


def test_load_single_file_minimal_ok():
    path = _fixture_path("scenario_base.yaml")
    cfg = loader.load_and_validate([path])
    assert cfg.schema_version == "v1"
    assert cfg.scenario_name == "basic_stream_toppp"
    assert cfg.workload.streaming is True
    assert cfg.pd.mode in {"mixed", "separated"}


def test_deep_merge_overlay_wins():
    base = _fixture_path("scenario_base.yaml")
    overlay = _fixture_path("scenario_overlay.yaml")
    cfg = loader.load_and_validate([base, overlay])
    # overlay flips streaming and updates concurrency
    assert cfg.workload.streaming is False
    assert cfg.workload.concurrency == [8, 32]


def test_validation_rejects_wrong_schema_version():
    bad = _fixture_path("scenario_bad_version.yaml")
    with pytest.raises(ValidationError):
        loader.load_and_validate([bad])
