from pathlib import Path

from bench_core import loader, manifest


def _fixture_path(name: str) -> str:
    here = Path(__file__).resolve()
    root = here.parents[2]
    return str(root / "tests" / "data" / name)


def test_manifest_from_base_config():
    cfg = loader.load_and_validate([_fixture_path("scenario_base.yaml")])
    m = manifest.make_manifest(cfg)
    assert m["schema_version"] == "v1"
    assert m["scenario_name"] == "basic_stream_toppp"
    assert m["pd_mode"] == "mixed"
    assert m["workload"]["streaming"] is True
    assert m["workload"]["concurrency"] == [4, 16]


def test_manifest_respects_overlay_updates():
    base = _fixture_path("scenario_base.yaml")
    overlay = _fixture_path("scenario_overlay.yaml")
    cfg = loader.load_and_validate([base, overlay])
    m = manifest.make_manifest(cfg)
    assert m["workload"]["streaming"] is False
    assert m["workload"]["concurrency"] == [8, 32]


def test_manifest_to_json_roundtrip():
    cfg = loader.load_and_validate([_fixture_path("scenario_base.yaml")])
    m = manifest.make_manifest(cfg)
    s = manifest.to_json(m)
    # ensure it is valid JSON and roundtrips to same dict
    import json

    assert json.loads(s) == m
