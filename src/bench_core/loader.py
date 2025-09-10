from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, MutableMapping, Sequence

import yaml
from pydantic import BaseModel, Field, ValidationError, field_validator


class Workload(BaseModel):
    streaming: bool
    input_len: List[int] = Field(..., min_length=2, max_length=2)
    output_cap: List[int] = Field(..., min_length=2, max_length=2)
    concurrency: List[int] = Field(..., min_length=2, max_length=2)


class PD(BaseModel):
    mode: str

    @field_validator("mode")
    @classmethod
    def _mode_allowed(cls, v: str) -> str:
        if v not in {"mixed", "separated"}:
            raise ValueError("pd.mode must be 'mixed' or 'separated'")
        return v


class Reports(BaseModel):
    html: bool | None = None
    grafana: bool | None = None
    pr_comment: bool | None = None


class CI(BaseModel):
    repeats: int | None = None
    timeout_minutes: int | None = None
    failure_policy: str = Field(default="stop")

    @field_validator("failure_policy")
    @classmethod
    def _policy_allowed(cls, v: str) -> str:
        if v not in {"stop", "continue"}:
            raise ValueError("ci.failure_policy must be 'stop' or 'continue'")
        return v


class Scenario(BaseModel):
    schema_version: str
    scenario_name: str
    workload: Workload
    pd: PD | None = None
    service: Dict[str, Any] | None = None
    ci: CI | None = None
    reports: Reports | None = None

    model_config = {
        "extra": "allow",  # allow forward-compatible keys
    }

    @field_validator("schema_version")
    @classmethod
    def _schema_is_v1(cls, v: str) -> str:
        if v != "v1":
            raise ValueError("Only schema_version 'v1' is supported")
        return v


def _deep_merge(
    a: MutableMapping[str, Any], b: MutableMapping[str, Any]
) -> Dict[str, Any]:
    """Deep merge two mapping trees without mutating inputs.

    Values from b override values from a. Nested dicts are merged recursively.
    """
    out: Dict[str, Any] = dict(a)
    for k, v in b.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge(out[k], v)  # type: ignore[arg-type]
        else:
            out[k] = v
    return out


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def load_and_validate(paths: Sequence[str | Path]) -> Scenario:
    """Load one or more YAML files and validate into a Scenario.

    Later files override earlier ones via deep-merge.
    """
    if not paths:
        raise ValueError("At least one path is required")

    merged: Dict[str, Any] = {}
    for p in paths:
        path = Path(p)
        if not path.exists():
            raise FileNotFoundError(path)
        piece = _load_yaml(path)
        merged = _deep_merge(merged, piece)

    try:
        return Scenario.model_validate(merged)
    except ValidationError:
        # re-raise to keep pydantic's rich message for callers/tests
        raise
