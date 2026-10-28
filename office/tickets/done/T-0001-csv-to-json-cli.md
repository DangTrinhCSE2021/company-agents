---
id: T-0001
title: Build CLI tool to convert CSV to JSON
status: done
owner: engineer
suggested_owner: engineer
priority: medium
project: csv-to-json-cli
created: 2026-10-28
updated: 2026-10-28
clarified: 2026-10-28
closed: 2026-10-28
---

## Request
> Build a small CLI that converts CSV to JSON

## Summary
Create a simple Python command-line tool that reads CSV files and outputs their contents as JSON, with robust error handling for edge cases and unexpected failures.

## Acceptance criteria
- [ ] Built in Python (no external libraries beyond standard library unless essential)
- [ ] CLI accepts a CSV file as input via file path argument
- [ ] Outputs valid JSON to stdout
- [ ] First row of CSV is treated as column headers
- [ ] Handles quoted fields and embedded commas correctly
- [ ] Returns exit code 0 for success, non-zero for all errors
- [ ] Robust error handling with clear, informative messages for:
  - [ ] File not found
  - [ ] Permission denied
  - [ ] Empty file
  - [ ] Malformed/invalid CSV (e.g., inconsistent column counts, invalid syntax)
  - [ ] Encoding errors
  - [ ] Any unexpected I/O failures (exits gracefully with descriptive message)
- [ ] No extra command-line flags needed beyond the essential file path argument
- [ ] README documents usage with at least one example

## Open questions
None

## Work log
- 2026-10-28 — Created csv2json.py (single-file Python CLI, stdlib only) and README.md. Verified all acceptance criteria by running the script against test inputs: normal CSV, header-only, empty file, file-not-found, wrong extension, too-many-columns, too-few-columns, latin-1 encoding fallback, binary file detection, quoted fields with embedded commas. All exit codes and error messages matched expectations.; files: projects/csv-to-json-cli/csv2json.py, projects/csv-to-json-cli/README.md; verified: manual test runs covering every edge case listed in acceptance criteria — all passed.
