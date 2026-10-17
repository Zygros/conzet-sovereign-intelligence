"""Skip this imported tree when pytest is rooted at the parent hub.

Tests still collect when pytest is launched from this directory.
"""
from pathlib import Path


def pytest_ignore_collect(collection_path, config):
    root = Path(str(config.rootpath)).resolve()
    here = Path(__file__).resolve().parent
    if root == here or root not in here.parents:
        return None
    try:
        rel = Path(str(collection_path)).resolve().relative_to(here)
    except ValueError:
        return None
    name = rel.name
    if rel.parts and rel.parts[0] in {"tests", "test"}:
        return True
    if name.startswith("test_") and name.endswith(".py"):
        return True
    if name.endswith("_test.py"):
        return True
    return None
