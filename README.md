# csv2md

A small command-line tool that converts a CSV file into a GitHub-flavoured Markdown table.

**Status:** Task 2 — Core conversion complete (CSV → Markdown table with header + separator rows)

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

- If no file is given (or `-` is used), input is read from stdin.
- A file path points to a CSV file to convert.

## Development

```bash
pip install -r requirements.txt
pip install -e .
pytest tests/ -v
```

## License

MIT
