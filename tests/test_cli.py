"""Tests for the csv2md CLI."""

import csv
import subprocess
import sys
from pathlib import Path
from textwrap import dedent


def test_module_runs_no_args():
    """python -m csv2md with no args reads from stdin and exits 0."""
    result = subprocess.run(
        [sys.executable, "-m", "csv2md"],
        input="",
        capture_output=True,
        text=True,
        cwd=".",
    )
    assert result.returncode == 0


def test_module_no_args_reads_stdin_csv():
    """python -m csv2md with no file arg converts CSV from stdin."""
    csv_input = "Name,Age\nAlice,30\n"
    result = subprocess.run(
        [sys.executable, "-m", "csv2md"],
        input=csv_input,
        capture_output=True,
        text=True,
        cwd=".",
    )
    assert result.returncode == 0
    assert "| Name | Age |" in result.stdout
    assert "| --- | --- |" in result.stdout
    assert "| Alice | 30 |" in result.stdout


def test_cli_converts_csv_file():
    """python -m csv2md converts a CSV file to Markdown."""
    csv_content = "Name,Age\nAlice,30\nBob,25\n"
    csv_path = Path("tests/sample.csv")
    csv_path.write_text(csv_content)

    try:
        result = subprocess.run(
            [sys.executable, "-m", "csv2md", str(csv_path)],
            capture_output=True,
            text=True,
            cwd=".",
        )
        assert result.returncode == 0
        assert "| Name | Age |" in result.stdout
        assert "| --- | --- |" in result.stdout
        assert "| Alice | 30 |" in result.stdout
        assert "| Bob | 25 |" in result.stdout
    finally:
        csv_path.unlink(missing_ok=True)


def test_cli_stdin_dash():
    """python -m csv2md - reads from stdin via dash."""
    csv_input = "Name,Age\nAlice,30\n"
    result = subprocess.run(
        [sys.executable, "-m", "csv2md", "-"],
        input=csv_input,
        capture_output=True,
        text=True,
        cwd=".",
    )
    assert result.returncode == 0
    assert "| Name | Age |" in result.stdout


def test_cli_align_center():
    """--align center produces :-: separators."""
    csv_input = "Name,Age\nAlice,30\n"
    result = subprocess.run(
        [sys.executable, "-m", "csv2md", "--align", "center"],
        input=csv_input,
        capture_output=True,
        text=True,
        cwd=".",
    )
    assert result.returncode == 0
    assert "| Name | Age |" in result.stdout
    assert "| :--: | :--: |" in result.stdout


def test_cli_align_short_flag():
    """-a right produces ---: separators."""
    csv_input = "Name,Age\nAlice,30\n"
    result = subprocess.run(
        [sys.executable, "-m", "csv2md", "-a", "right"],
        input=csv_input,
        capture_output=True,
        text=True,
        cwd=".",
    )
    assert result.returncode == 0
    assert "| ---: | ---: |" in result.stdout


def test_cli_no_header():
    """--no-header treats first row as data and emits empty header."""
    csv_input = "Alice,30\nBob,25\n"
    result = subprocess.run(
        [sys.executable, "-m", "csv2md", "--no-header"],
        input=csv_input,
        capture_output=True,
        text=True,
        cwd=".",
    )
    assert result.returncode == 0
    # Empty header row: two empty cells
    assert "|  |  |" in result.stdout
    assert "| --- | --- |" in result.stdout
    # First row (Alice, 30) appears as data
    assert "| Alice | 30 |" in result.stdout


def test_cli_missing_file():
    """A non-existent file prints an error to stderr and exits 1."""
    result = subprocess.run(
        [sys.executable, "-m", "csv2md", "does_not_exist.csv"],
        capture_output=True,
        text=True,
        cwd=".",
    )
    assert result.returncode == 1
    assert "cannot open file" in result.stderr
    assert result.stdout == ""


def test_cli_empty_input():
    """Empty stdin prints an error to stderr and exits 1."""
    result = subprocess.run(
        [sys.executable, "-m", "csv2md"],
        input="",
        capture_output=True,
        text=True,
        cwd=".",
    )
    assert result.returncode == 1
    assert "empty input" in result.stderr


def test_cli_empty_file():
    """An empty CSV file prints an error to stderr and exits 1."""
    empty_path = Path("tests/empty_test.csv")
    empty_path.write_text("")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "csv2md", str(empty_path)],
            capture_output=True,
            text=True,
            cwd=".",
        )
         assert result.returncode == 1
        assert "empty input" in result.stderr
    finally:
        empty_path.unlink(missing_ok=True)


def test_cli_malformed_csv():
    """A malformed CSV prints an error to stderr, exits 1, and shows no traceback."""
    from unittest import mock
    from io import StringIO
    from csv2md import cli as cli_module

    with mock.patch.object(cli_module, "_read_csv_stream", side_effect=csv.Error("unexpected end of data")):
        with mock.patch("sys.stderr", new=StringIO()):
            exit_code = cli_module.main([])
            assert exit_code == 1
            assert "malformed CSV" in sys.stderr.getvalue()
