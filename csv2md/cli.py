"""Command-line interface for csv2md.

Usage:
    python -m csv2md [options] [file]

If *file* is omitted or '-', input is read from stdin.
"""

import argparse
import csv
import sys
from pathlib import Path

from csv2md.core import convert


def main(argv: list[str] | None = None) -> int:
    """Entry point for the csv2md command-line tool.

    Reads a CSV file (or stdin), converts it to a Markdown table,
    and prints the result to stdout.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:]).

    Returns:
        Exit code (0 on success, 1 on error).
    """
    parser = argparse.ArgumentParser(
        prog="csv2md",
        description="Convert a CSV file into a GitHub-flavoured Markdown table.",
    )
    parser.add_argument(
        "-a", "--align",
        choices=["left", "right", "center"],
        default=None,
        help="Align columns left, right, or center (default: no alignment).",
    )
    parser.add_argument(
        "--no-header",
        action="store_true",
        default=False,
        help="Treat the first row as data instead of a header; emit an empty header row.",
    )
    parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help="Path to the CSV file. If omitted or '-', reads from stdin.",
    )
    args = parser.parse_args(argv)

    csv_path = Path(args.file) if args.file and args.file != "-" else None
    rows = _read_csv_file(csv_path) if csv_path else _read_csv_stream(sys.stdin)

    output = convert(rows, align=args.align, no_header=args.no_header)
    sys.stdout.write(output + "\n")
    return 0


def _read_csv_file(path: Path) -> list[list[str]]:
    """Read and parse a CSV file into a list of rows.

    Args:
        path: Path to the CSV file.

    Returns:
        A list of rows, each row a list of string cells.
    """
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.reader(fh))


def _read_csv_stream(stream) -> list[list[str]]:
    """Read and parse CSV from a stream (e.g. stdin).

    Args:
        stream: A text stream to read CSV from.

    Returns:
        A list of rows, each row a list of string cells.
    """
    return list(csv.reader(stream))


if __name__ == "__main__":
    raise SystemExit(main())
