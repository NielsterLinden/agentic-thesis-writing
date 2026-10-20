from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="session")
def root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def linter():
    return load_module("check_writing_rules",
                       ROOT / "plugin" / "skills" / "tudelft-writing-rules" / "check_writing_rules.py")


@pytest.fixture(scope="session")
def figure_import():
    return load_module("figure_import", ROOT / "plugin" / "skills" / "figure-import" / "figure_import.py")


@pytest.fixture(scope="session")
def atw():
    return load_module("atw", ROOT / "scripts" / "atw.py")
