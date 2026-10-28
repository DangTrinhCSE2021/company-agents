# csv-to-json-cli

A single-file Python CLI that converts a CSV file to JSON and prints the result to stdout.

## Requirements

- Python 3.6 or later
- No external dependencies — stdlib only

## Usage

```
python csv2json.py <path/to/file.csv>
```

The first row of the CSV is treated as the header (field names).
Every subsequent row becomes one JSON object in the output array.

## Examples

Given `people.csv`:
```
name,age,city
Alice,30,Berlin
Bob,25,"New York"
```

Run:
```
python csv2json.py people.csv
```

Output:
```json
[
  {
    "name": "Alice",
    "age": "30",
    "city": "Berlin"
  },
  {
    "name": "Bob",
    "age": "25",
    "city": "New York"
  }
]
```

A file that contains only a header row (no data rows) outputs an empty array:
```json
[]
```

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | File/path error (not found, permission denied, wrong extension, binary file) |
| 2 | Content error (empty file, malformed CSV, encoding failure) |
| 3 | Unexpected I/O error |

## Edge cases handled

| Situation | Behaviour |
|-----------|-----------|
| File not found | Exit 1 with descriptive message |
| Permission denied | Exit 1 with descriptive message |
| Empty file | Exit 2 — distinguished from header-only file |
| Header row only (no data) | Exit 0 — outputs `[]` |
| Row with too many columns | Exit 2 with row number and extra values |
| Row with too few columns | Exit 2 with row number and missing field names |
| Non-UTF-8 encoding | Automatically retries with latin-1; exits 2 if both fail |
| Binary / non-text file | Detected via null-byte scan; exit 1 |
| Wrong file extension | Exit 1 — only `.csv` accepted |
| Quoted fields / embedded commas | Handled transparently by Python's `csv` module |
| Broken pipe (e.g. piped to `head`) | Ignored gracefully |
