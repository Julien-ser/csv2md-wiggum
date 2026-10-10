"""Command-line interface for csv2md.

Usage:
    python -m csv2md [options] [file]
"""

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    """Entry point for the csv2md command-line tool.

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
        "file",
        nargs="?",
        default=None,
        help="Path to the CSV file. If omitted or '-', reads from stdin.",
    )
    args = parser.parse_args(argv)

    sys.stdout.write("csv2md is ready\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
