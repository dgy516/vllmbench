from __future__ import annotations

import argparse
import sys
from typing import Iterable, List

from . import errors as err
from . import loader


def _format_summary(cfg) -> str:
    lines: List[str] = []
    lines.append(f"schema_version: {cfg.schema_version}")
    lines.append(f"scenario_name: {cfg.scenario_name}")
    lines.append(f"workload.streaming: {cfg.workload.streaming}")
    lines.append(f"workload.concurrency: {cfg.workload.concurrency}")
    return "\n".join(lines) + "\n"


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="vllmbench", add_help=True)
    parser.add_argument(
        "-f",
        "--file",
        dest="files",
        action="append",
        required=True,
        help="Scenario YAML file(s); later files override earlier ones",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        cfg = loader.load_and_validate(args.files)
    except FileNotFoundError as e:
        print(f"error {err.E_IO}: file not found: {e}", file=sys.stderr)
        return 2
    except Exception as e:  # noqa: BLE001
        # Best-effort classification for config/validation errors
        msg = str(e)
        code = (
            err.E_CONFIG
            if "schema_version" in msg or "validation" in msg.lower()
            else err.E_USAGE
        )
        print(f"error {code}: {msg}", file=sys.stderr)
        return 2

    sys.stdout.write(_format_summary(cfg))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
