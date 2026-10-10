# csv2md

A small command-line tool that converts a CSV file into a GitHub-flavoured Markdown table. Standard library only (argparse, csv).

**Status:** Complete

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

If *file* is omitted or set to `-`, input is read from stdin.

## Options

| Option | Description |
|--------|-------------|
| `file` | Path to a CSV file. If omitted or `-`, reads from stdin. |
| `-a left` / `--align left` | Align columns left (`:---`). |
| `-a right` / `--align right` | Align columns right (`---:`). |
| `-a center` / `--align center` | Align columns center (`:--:`). |
| `--no-header` | Treat the first row as data instead of a header; emit an empty header row. |

### Error handling

The tool handles errors gracefully:

- **Missing file** — prints `csv2md: cannot open file: <path>` to stderr, exits 1.
- **Empty input** — prints `csv2md: empty input` to stderr, exits 1.
- **Malformed CSV** — prints `csv2md: malformed CSV: <detail>` to stderr, exits 1.

In all error cases, no traceback is shown.

## Sample Input and Output

### Input (`sample.csv`)

```csv
Name,Age,City
Alice,30,"New York"
Bob,25,"San Francisco"
```

### Output

```markdown
| Name | Age | City |
| --- | --- | --- |
| Alice | 30 | New York |
| Bob | 25 | San Francisco |
```

### With alignment

```bash
python -m csv2md --align left sample.csv
```

```markdown
| Name | Age | City |
| :--- | :--- | :--- |
| Alice | 30 | New York |
| Bob | 25 | San Francisco |
```

```bash
python -m csv2md --align right sample.csv
```

```markdown
| Name | Age | City |
| ---: | ---: | ---: |
| Alice | 30 | New York |
| Bob | 25 | San Francisco |
```

```bash
python -m csv2md --align center sample.csv
```

```markdown
| Name | Age | City |
| :--: | :--: | :--: |
| Alice | 30 | New York |
| Bob | 25 | San Francisco |
```

Shorthand: `-a left`, `-a right`, `-a center`.

### Without header

```bash
python -m csv2md --no-header sample.csv
```

```markdown
|  |  |  |
| --- | --- | --- |
| Name | Age | City |
| Alice | 30 | New York |
| Bob | 25 | San Francisco |
```

### From stdin

```bash
echo "a,b,c" | python -m csv2md
```

```markdown
| a | b | c |
| --- | --- | --- |
```

## Development

```bash
pip install -r requirements.txt
pip install -e .
pytest tests/ -v
```

## License

MIT
