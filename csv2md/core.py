"""Core conversion logic for csv2md.

Public functions:
    convert: Convert a list of CSV rows into a Markdown table string.
"""

from __future__ import annotations

type Align = "left" | "right" | "center" | None


def convert(rows: list[list[str]], align: Align = None) -> str:
    """Convert a list of CSV rows into a GitHub-flavoured Markdown table.

    The first row is treated as the header row. A separator row
    (``| --- | --- | ...``) is inserted between the header and data rows.

    Args:
        rows: A list of rows, where each row is a list of string cell values.
            The first row is treated as the header.
        align: Column alignment. One of ``"left"``, ``"right"``,
            ``"center"``, or ``None`` (default, no alignment).

    Returns:
        A Markdown table as a string, or an empty string if *rows* is empty.

    Example:
        >>> convert([["Name", "Age"], ["Alice", "30"]])
        '| Name | Age |\\n| --- | --- |\\n| Alice | 30 |'
    """
    if not rows:
        return ""

    header = rows[0]
    width = len(header)
    lines: list[str] = []

    lines.append(_format_row(_escape_cells(header)))
    lines.append(_format_separator(width, align))

    for row in rows[1:]:
        padded = _pad_row(row, width)
        lines.append(_format_row(_escape_cells(padded)))

    return "\n".join(lines)


def _format_separator(ncols: int, align: Align = None) -> str:
    """Build the separator row for *ncols* columns with optional alignment.

    Args:
        ncols: Number of columns in the table.
        align: One of ``"left"``, ``"right"``, ``"center"``, or ``None``.

    Returns:
        A separator row string like ``| --- | --- |`` or ``| :--- | ---: |``.
    """
    if align == "left":
        cell = ":---"
    elif align == "right":
        cell = "---:"
    elif align == "center":
        cell = ":--:"
    else:
        cell = "---"

    return _format_row([cell] * ncols)


def _format_row(cells: list[str]) -> str:
    """Format a list of cells as a Markdown table row.

    Args:
        cells: The cell values for this row.

    Returns:
        A string like ``| cell1 | cell2 |``.
    """
    return "| " + " | ".join(cells) + " |"
