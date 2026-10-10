"""Tests for the csv2md CLI."""

import subprocess
import sys


def test_module_runs():
    """python -m csv2md should run with exit code 0."""
    result = subprocess.run(
        [sys.executable, "-m", "csv2md"],
        capture_output=True,
        text=True,
        cwd=".",
    )
    assert result.returncode == 0
    assert "csv2md is ready" in result.stdout
