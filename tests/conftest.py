import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    # Works whether this repo is checked out as a subdir (vllmbench/) or standalone.
    here = Path(__file__).resolve()
    project_root = here.parent  # tests/
    if project_root.name == "tests":
        project_root = project_root.parent
    src = project_root / "src"
    if src.exists():
        sys.path.insert(0, str(src))


_ensure_src_on_path()

