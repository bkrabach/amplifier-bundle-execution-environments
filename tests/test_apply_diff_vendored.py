"""Test that apply_diff.py is correctly vendored into the tools-env-all module.

This is a vendor integrity test — it verifies the file exists with the correct
Apache-2.0 license header and that it contains the expected apply_diff function.
"""

import os
import hashlib

# Paths
DEST_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "modules",
    "tools-env-all",
    "amplifier_module_tools_env_all",
    "apply_diff.py",
)
SOURCE_PATH = (
    "/home/bkrabach/dev/attractor-dev-machine"
    "/amplifier-bundle-filesystem"
    "/modules/tool-apply-patch"
    "/amplifier_module_tool_apply_patch/apply_diff.py"
)


def test_apply_diff_file_exists():
    """apply_diff.py must exist at the vendored destination path."""
    assert os.path.isfile(os.path.realpath(DEST_PATH)), (
        f"apply_diff.py not found at {DEST_PATH}"
    )


def test_apply_diff_has_apache_license_header():
    """The vendored file must contain the Apache-2.0 copyright header."""
    with open(DEST_PATH) as f:
        content = f.read()
    assert "Apache License, Version 2.0" in content or "Apache-2.0" in content, (
        "Apache-2.0 license marker not found in apply_diff.py"
    )
    assert "Copyright" in content, "Copyright notice not found in apply_diff.py"


def test_apply_diff_contains_apply_diff_function():
    """The vendored file must define the apply_diff function."""
    with open(DEST_PATH) as f:
        content = f.read()
    assert "def apply_diff(" in content, (
        "apply_diff() function not found in vendored file"
    )


def test_apply_diff_content_matches_source():
    """Vendored file content must be byte-for-byte identical to the source."""

    def sha256(path):
        h = hashlib.sha256()
        with open(path, "rb") as f:
            h.update(f.read())
        return h.hexdigest()

    src_hash = sha256(SOURCE_PATH)
    dst_hash = sha256(os.path.realpath(DEST_PATH))
    assert src_hash == dst_hash, (
        f"Vendored apply_diff.py does not match source.\n"
        f"  source sha256: {src_hash}\n"
        f"  dest   sha256: {dst_hash}"
    )


def test_apply_diff_is_importable():
    """The vendored module must be importable (no syntax errors)."""
    import sys
    import importlib.util

    module_name = "_test_apply_diff_vendored"
    spec = importlib.util.spec_from_file_location(
        module_name, os.path.realpath(DEST_PATH)
    )
    assert spec is not None, "Could not create ModuleSpec for apply_diff.py"
    assert spec.loader is not None, "ModuleSpec has no loader"
    mod = importlib.util.module_from_spec(spec)
    # Register in sys.modules BEFORE exec_module so @dataclass decorators
    # can resolve cls.__module__ back through sys.modules (Python 3.12 requirement).
    sys.modules[module_name] = mod
    try:
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
        assert hasattr(mod, "apply_diff"), "apply_diff symbol not found after import"
    finally:
        sys.modules.pop(module_name, None)
