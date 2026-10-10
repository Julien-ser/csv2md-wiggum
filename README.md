# csv2md

A small command-line tool that converts a CSV file into a GitHub-flavoured Markdown table.

**Status:** Task 5 — Cell escaping (pipes, newlines) and short-row padding complete

## Requirements

- Python 3.10+
- pytest (for running tests)

## Installation

```bash
pip install -e .
```

Or run directly without installing:

```bash
python -m csv2md
```

## Usage

```bash
python -m csv2md [options] [file]
```

## Options

| Option | Description |
|--------|-------------|
| `file` | Path to a CSV file. If omitted or `-`, reads from stdin. |
| `--align left` | Align columns left (`:---`). |
| `--align right` | Align columns right (`:--:`). |
| `--align center` | Align columns center (`:--:`). |

Cells containing pipe characters (`|`) are automatically escaped so the table structure is preserved. Newlines within cells are converted to `<br>` tags. Rows shorter than the header row are padded with empty cells.

## Sample Input and Output

## Development

```bash
pip install -r requirements.txt
pip install -e .
pytest tests/ -v
```

## License

MIT
