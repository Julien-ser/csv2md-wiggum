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

    def test_align_left(self):
        """Align left produces :--- in the separator."""
        rows = [["A", "B"], ["1", "2"]]
        result = convert(rows, align="left")
        expected = "| A | B |\n| :--- | :--- |\n| 1 | 2 |"
        assert result == expected

    def test_align_right(self):
        """Align right produces ---: in the separator."""
        rows = [["A", "B"], ["1", "2"]]
        result = convert(rows, align="right")
        expected = "| A | B |\n| ---: | ---: |\n| 1 | 2 |"
        assert result == expected

    def test_align_center(self):
        """Align center produces :--: in the separator."""
        rows = [["A", "B"], ["1", "2"]]
        result = convert(rows, align="center")
        expected = "| A | B |\n| :--: | :--: |\n| 1 | 2 |"
        assert result == expected

    def test_align_default_none(self):
        """No alignment produces --- in the separator."""
        rows = [["A", "B"], ["1", "2"]]
        result = convert(rows, align=None)
        expected = "| A | B |\n| --- | --- |\n| 1 | 2 |"
        assert result == expected

    def test_escape_pipe(self):
        """Pipe characters in cells are escaped with backslash."""
        rows = [["A|B", "B"], ["1", "2"]]
        result = convert(rows)
        assert "| A\\|B | B |" in result

    def test_escape_pipe_in_header(self):
        """Pipe characters in header cells are escaped."""
        rows = [["A|B", "C"], ["1", "2"]]
        result = convert(rows)
        assert "| A\\|B | C |" in result

    def test_newline_replaced_with_br(self):
        """Newlines in cell values are replaced with <br> tags."""
        rows = [["Desc"], ["line1\nline2"]]
        result = convert(rows)
        assert "<br>" in result
        assert "line1<br>line2" in result

    def test_newline_and_carriage_return_replaced(self):
        """Carriage returns and CRLF newlines are replaced with <br>."""
        rows = [["Text"], ["line1\r\nline2\rline3"]]
        result = convert(rows)
        assert "line1<br>line2<br>line3" in result

    def test_escape_pipe_and_newline_combined(self):
        """Both pipe escaping and newline replacement happen in one cell."""
        rows = [["A|B"], ["x\ny|z"]]
        result = convert(rows)
        assert "| A\\|B |" in result
        assert "x<br>y\\|z" in result

    def test_short_row_padded(self):
        """A row shorter than the header is padded with empty cells."""
        rows = [["A", "B", "C"], ["1"]]
        result = convert(rows)
        expected = "| A | B | C |\n| --- | --- | --- |\n| 1 |  |  |"
        assert result == expected

    def test_short_row_padded_with_br(self):
        """Short rows are still escaped and padded correctly."""
        rows = [["A|B", "C"], ["1"]]
        result = convert(rows)
        assert "| A\\|B | C |" in result
        assert "| 1 |  |" in result

    def test_no_header_emits_empty_header_row(self):
        """--no-header emits an empty header row and treats first row as data."""
        rows = [["Alice", "30"], ["Bob", "25"]]
        result = convert(rows, no_header=True)
        expected = "|  |  |\n| --- | --- |\n| Alice | 30 |\n| Bob | 25 |"
        assert result == expected

    def test_no_header_single_row(self):
        """--no-header with a single row emits empty header + separator + data."""
        rows = [["Alice", "30"]]
        result = convert(rows, no_header=True)
        expected = "|  |  |\n| --- | --- |\n| Alice | 30 |"
        assert result == expected

    def test_no_header_with_align(self):
        """--no-header combined with alignment."""
        rows = [["A", "B"], ["1", "2"]]
        result = convert(rows, align="right", no_header=True)
        expected = "|  |  |\n| ---: | ---: |\n| A | B |\n| 1 | 2 |"
        assert result == expected

    def test_no_header_short_row_padded(self):
        """--no-header pads short rows to the first row width."""
        rows = [["A", "B", "C"], ["1"]]
        result = convert(rows, no_header=True)
        expected = "|  |  |  |\n| --- | --- | --- |\n| A | B | C |\n| 1 |  |  |"
        assert result == expected
