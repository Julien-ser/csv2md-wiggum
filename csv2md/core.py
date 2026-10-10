"""Core conversion logic for csv2md.

Public functions:
    convert: Convert a list of CSV rows into a Markdown table string.
"""

from __future__ import annotations

type Align = "left" | "right" | "center" | None


def convert(rows: list[list[str]], align: Align = None, no_header: bool = False) -> str:
    """Convert a list of CSV rows into a GitHub-flavoured Markdown table.

    By default the first row is treated as the header row and a separator row
    (``| --- | --- | ...``) is inserted between the header and data rows.

    Args:
        rows: A list of rows, where each row is a list of string cell values.
            The first row is treated as the header unless *no_header* is set.
        align: Column alignment. One of ``"left"``, ``"right"``,
            ``"center"``, or ``None`` (default, no alignment).
        no_header: When ``True``, the first row is treated as data and an
            empty header row is emitted instead.

    Returns:
        A Markdown table as a string, or an empty string if *rows* is empty.

    Example:
        >>> convert([["Name", "Age"], ["Alice", "30"]])
        '| Name | Age |\\n| --- | --- |\\n| Alice | 30 |'
    """
    if not rows:
        return ""

    width = len(rows[0])
    lines: list[str] = []

    if no_header:
        lines.append(_format_row([""] * width))
    else:
        lines.append(_format_row(_escape_cells(rows[0])))
    lines.append(_format_separator(width, align))

    data = rows if no_header else rows[1:]
    for row in data:
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


def _escape_cells(cells: list[str]) -> list[str]:
    """Escape pipe characters and replace newlines in cell values.

    Pipe characters (``|``) are escaped as ``\\|`` so they do not
    break the Markdown table structure. Newline characters (both ``\\n``
    and ``\\r``) are replaced with ``<br>`` tags to keep each row on
    a single line.

    Args:
        cells: A list of raw cell string values.

    Returns:
        A new list of escaped cell strings.
    """
    escaped: list[str] = []
    for cell in cells:
        cell = cell.replace("|", "\\|")
        cell = cell.replace("\r\n", "<br>").replace("\n", "<br>").replace("\r", "<br>")
        escaped.append(cell)
    return escaped


def _pad_row(row: list[str], width: int) -> list[str]:
    """Pad a row with empty strings up to *width* columns.

    If *row* has more cells than *width*, it is returned unchanged.

    Args:
        row: The row to potentially pad.
        width: The target number of columns (the header width).

    Returns:
        A row list padded to *width* columns.
    """
    if len(row) < width:
        row = row + [""] * (width - len(row))
    return row


def _format_row(cells: list[str]) -> str:
    """Format a list of cells as a Markdown table row.

    Args:
        cells: The cell values for this row.

    Returns:
        A string like ``| cell1 | cell2 |``.
    """
    return "| " + " | ".join(cells) + " |"
