from __future__ import annotations

from dataclasses import dataclass
from typing import List, TypedDict


@dataclass(frozen=True)
class BaseRouter:
    name: str


@dataclass(frozen=True)
class MixedRouter(BaseRouter):
    strategy: str = "single"


@dataclass(frozen=True)
class SeparatedRouter(BaseRouter):
    strategy: str = "split"


def choose_router(cfg) -> BaseRouter:
    mode = getattr(getattr(cfg, "pd", None), "mode", "mixed")
    if mode == "separated":
        return SeparatedRouter(name="separated")
    return MixedRouter(name="mixed")


class PlanDict(TypedDict):
    mode: str
    streaming: bool
    components: List[str]


def build_plan(cfg) -> PlanDict:
    r = choose_router(cfg)
    plan: PlanDict = {
        "mode": r.name,
        "streaming": bool(cfg.workload.streaming),
        "components": ["router", "loadgen", "metrics"],
    }
    return plan
