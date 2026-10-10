"""Core conversion logic for csv2md.

Public functions:
    convert: Convert a list of CSV rows into a Markdown table string.
"""

from __future__ import annotations


def convert(rows: list[list[str]]) -> str:
    """Convert a list of CSV rows into a GitHub-flavoured Markdown table.

    The first row is treated as the header row. A separator row
    (``| --- | --- | ...``) is inserted between the header and data rows.

    Args:
        rows: A list of rows, where each row is a list of string cell values.
              The first row is treated as the header.

    Returns:
        A Markdown table as a string, or an empty string if *rows* is empty.

    Example:
        >>> convert([["Name", "Age"], ["Alice", "30"]])
        '| Name | Age |\\n| --- | --- |\\n| Alice | 30 |'
    """
    if not rows:
        return ""

    header = rows[0]
    lines: list[str] = []

    lines.append(_format_row(header))
    lines.append(_format_row(["---"] * len(header)))

    for row in rows[1:]:
        lines.append(_format_row(row))

    return "\n".join(lines)


def _format_row(cells: list[str]) -> str:
    """Format a list of cells as a Markdown table row.

    Args:
        cells: The cell values for this row.

    Returns:
        A string like ``| cell1 | cell2 |``.
    """
    return "| " + " | ".join(cells) + " |"
