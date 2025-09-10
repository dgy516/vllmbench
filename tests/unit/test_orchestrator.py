from pathlib import Path

from bench_core import loader, orchestrator


def _fixture_path(name: str) -> str:
    here = Path(__file__).resolve()
    root = here.parents[2]
    return str(root / "tests" / "data" / name)


def test_choose_router_mixed_by_default():
    cfg = loader.load_and_validate([_fixture_path("scenario_base.yaml")])
    r = orchestrator.choose_router(cfg)
    assert isinstance(r, orchestrator.MixedRouter)
    assert r.name == "mixed"


def test_choose_router_separated_when_configured():
    base = _fixture_path("scenario_base.yaml")
    sep = _fixture_path("scenario_separated_overlay.yaml")
    cfg = loader.load_and_validate([base, sep])
    r = orchestrator.choose_router(cfg)
    assert isinstance(r, orchestrator.SeparatedRouter)
    assert r.name == "separated"


def test_build_plan_contains_mode_and_streaming():
    base = _fixture_path("scenario_base.yaml")
    overlay = _fixture_path("scenario_overlay.yaml")  # flips streaming = false
    cfg = loader.load_and_validate([base, overlay])
    plan = orchestrator.build_plan(cfg)
    assert plan["mode"] in {"mixed", "separated"}
    assert plan["streaming"] is False
    assert "router" in plan["components"]
