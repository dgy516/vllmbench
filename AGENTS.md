# Repository Guidelines

## Project Structure & Module Organization
- `src/bench_core/`: Python package (e.g., `loader.py`). Add new modules under `bench_core`.
- `tests/unit/` and `tests/integration/`: Pytest suites; prefer small, focused unit tests.
- `docs/SRS-HLD.md`: System requirements and high‑level design overview.
- `.github/`: CI for lint, typecheck, and tests (Python 3.11).
- `hooks/`: Local Git hooks (e.g., `pre-push`).
- `requirements-dev.txt`: Dev and test dependencies.

## Build, Test, and Development Commands
- Create env: `python3.11 -m venv .venv && source .venv/bin/activate`
- Install deps: `pip install -r requirements-dev.txt`
- Make imports work: `export PYTHONPATH="$PWD/src:$PYTHONPATH"`
- Run tests: `pytest -q`
- Lint/format: `ruff check src tests`; `black --check src tests`; `isort --check-only src tests`
- Type check: `mypy --ignore-missing-imports src`
- Optional Make targets (if included by your repo): `make bootstrap`; `make check` (see `MAKEFILE_APPEND.txt`).

## Coding Style & Naming Conventions
- Python, 4-space indent, type hints for public functions.
- Formatting via Black (default settings) and import order via isort.
- Lint with Ruff; fix issues or suppress with clear justification.
- Naming: packages/modules `snake_case`; classes `PascalCase`; functions/vars `snake_case`; constants `UPPER_SNAKE_CASE`.
- Prefer absolute imports from `bench_core` (example: `from bench_core import loader`).

## Testing Guidelines
- TDD preferred: write/commit tests first, then implementation. Keep tests deterministic.
- File names: `tests/**/test_*.py`; test functions `test_*`.
- Run locally with `pytest -q`; ensure failures reproduce before fixing.
- Add unit tests for new logic and adjust integration tests if behavior changes.

## Commit & Pull Request Guidelines
- Commits: small, descriptive, imperative mood. Prefer Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).
- PRs: clear scope and description, link issues, show TDD evidence, and ensure CI is green. Follow `.github/pull_request_template.md`.
- Rollback: if needed, `git revert <merge-commit>`.

## CI & Hooks
- CI runs Ruff, Black, isort, MyPy, and Pytest on Python 3.11.
- Enable local checks before push: `git config core.hooksPath hooks` (runs `hooks/pre-push`).
- Note: Some CI/hooks reference `vllmbench/src` and `vllmbench/tests` for mono‑repo setups. When working from this directory, use `src` and `tests` paths instead.
