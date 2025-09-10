from __future__ import annotations

import json
from typing import Any, Dict


def make_manifest(cfg) -> Dict[str, Any]:
    # Flatten only essential, stable fields for downstream consumers.
    return {
        "schema_version": cfg.schema_version,
        "scenario_name": cfg.scenario_name,
        "pd_mode": getattr(getattr(cfg, "pd", None), "mode", "mixed"),
        "workload": {
            "streaming": bool(cfg.workload.streaming),
            "input_len": list(cfg.workload.input_len),
            "output_cap": list(cfg.workload.output_cap),
            "concurrency": list(cfg.workload.concurrency),
        },
        "service": getattr(cfg, "service", None) or {},
    }


def to_json(manifest: Dict[str, Any]) -> str:
    return json.dumps(manifest, indent=2, sort_keys=True) + "\n"
