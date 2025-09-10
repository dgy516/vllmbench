from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BenchError(Exception):
    code: str
    message: str

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"[{self.code}] {self.message}"


E_CONFIG = "E_CONFIG"
E_IO = "E_IO"
E_USAGE = "E_USAGE"
