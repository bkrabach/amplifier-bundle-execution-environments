"""Root conftest for execution-environments test suite.

Handles graceful collection skips for tests that require optional
dependencies (amplifier_module_tools_env_ssh, amplifier_module_tools_env_local,
asyncssh) that are not present in the standard install.
"""

from __future__ import annotations

import importlib
from pathlib import Path


def _dep_available(module_name: str) -> bool:
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False


# Tests with optional dependencies: {path_relative_to_tests_dir: [required_modules]}
_OPTIONAL_DEP_TESTS: dict[str, list[str]] = {
    "test_e2e_multi_env.py": [
        "amplifier_module_tools_env_local",
        "amplifier_module_tools_env_docker",
        "amplifier_module_tools_env_ssh",
    ],
    "integration/test_phase4_ssh.py": [
        "amplifier_module_tools_env_ssh",
    ],
}

# Compute which files to skip based on available dependencies
_TESTS_DIR = Path(__file__).parent
_SKIP_FILES: set[Path] = set()

for _rel_path, _deps in _OPTIONAL_DEP_TESTS.items():
    for _dep in _deps:
        if not _dep_available(_dep):
            _SKIP_FILES.add((_TESTS_DIR / _rel_path).resolve())
            break


def pytest_ignore_collect(collection_path, config):
    """Skip test files whose optional dependencies are not installed."""
    if collection_path.resolve() in _SKIP_FILES:
        return True
    return None
