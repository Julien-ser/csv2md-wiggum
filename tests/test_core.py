"""Tests for the core conversion logic."""

from csv2md.core import convert


class TestConvert:
    """Tests for csv2md.core.convert."""

    def test_simple_table(self):
        """A basic two-row table produces header, separator, and data."""
        rows = [["Name", "Age"], ["Alice", "30"]]
        result = convert(rows)
        expected = "| Name | Age |\n| --- | --- |\n| Alice | 30 |"
        assert result == expected

    def test_multiple_columns(self):
        """A table with many columns."""
        rows = [["A", "B", "C", "D"], ["1", "2", "3", "4"]]
        result = convert(rows)
        assert result == "| A | B | C | D |\n| --- | --- | --- | --- |\n| 1 | 2 | 3 | 4 |"

    def test_multiple_data_rows(self):
        """Multiple data rows after the header."""
        rows = [["Name", "Age"], ["Alice", "30"], ["Bob", "25"]]
        result = convert(rows)
        expected = (
            "| Name | Age |\n"
            "| --- | --- |\n"
            "| Alice | 30 |\n"
            "| Bob | 25 |"
        )
        assert result == expected

    def test_single_header_row(self):
        """Only a header row produces header + separator, no data rows."""
        rows = [["Col1", "Col2"]]
        result = convert(rows)
        assert result == "| Col1 | Col2 |\n| --- | --- |"

    def test_empty_rows(self):
        """An empty list produces an empty string."""
        assert convert([]) == ""

    def test_empty_string_cells(self):
        """Cells with empty strings are handled correctly."""
        rows = [["A", "B"], ["", ""]]
        result = convert(rows)
        assert result == "| A | B |\n| --- | --- |\n|  |  |"
