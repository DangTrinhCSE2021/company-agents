"""
csv2json.py — Convert a CSV file to JSON on stdout.

Usage:
    python csv2json.py <path/to/file.csv>

Output:
    Pretty-printed JSON array of objects to stdout.
    Each object corresponds to one data row; keys come from the header row.

Exit codes:
    0  success
    1  file / path error (not found, permission denied, wrong extension, binary)
    2  content error (empty file, malformed CSV, encoding failure)
    3  unexpected I/O error
"""

import csv
import json
import os
import sys


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

EXIT_OK = 0
EXIT_FILE_ERROR = 1
EXIT_CONTENT_ERROR = 2
EXIT_IO_ERROR = 3

VALID_EXTENSIONS = {".csv"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _err(message: str) -> None:
    """Write an error message to stderr."""
    print(f"Error: {message}", file=sys.stderr)


def _open_with_encoding(path: str):
    """
    Return an open text file handle, trying UTF-8 first then latin-1.
    Raises UnicodeDecodeError only if both encodings fail (should not happen
    with latin-1, which covers all 256 byte values).
    Raises PermissionError / OSError as normal.
    """
    try:
        fh = open(path, newline="", encoding="utf-8")
        # Force a read to trigger any decode error early.
        fh.read(1)
        fh.seek(0)
        return fh, "utf-8"
    except UnicodeDecodeError:
        pass

    # Fall back to latin-1
    fh = open(path, newline="", encoding="latin-1")
    return fh, "latin-1"


def _is_likely_binary(path: str) -> bool:
    """
    Heuristic: read the first 8 KB and check for null bytes, which almost
    always indicates binary content.
    """
    try:
        with open(path, "rb") as fh:
            chunk = fh.read(8192)
        return b"\x00" in chunk
    except OSError:
        return False


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def convert(path: str) -> int:
    """
    Read the CSV at *path*, convert to JSON, write to stdout.
    Returns an exit code integer.
    """
    # --- Extension check ---------------------------------------------------
    _, ext = os.path.splitext(path)
    if ext.lower() not in VALID_EXTENSIONS:
        _err(
            f"'{path}' does not have a .csv extension "
            f"(got '{ext or '(none)'}').  "
            "Only .csv files are supported."
        )
        return EXIT_FILE_ERROR

    # --- Existence / permission checks ------------------------------------
    if not os.path.exists(path):
        _err(f"File not found: '{path}'")
        return EXIT_FILE_ERROR

    if not os.path.isfile(path):
        _err(f"'{path}' is not a regular file.")
        return EXIT_FILE_ERROR

    # --- Binary content check ---------------------------------------------
    if _is_likely_binary(path):
        _err(
            f"'{path}' appears to be a binary file, not a text CSV.  "
            "Refusing to process."
        )
        return EXIT_FILE_ERROR

    # --- Open with encoding negotiation -----------------------------------
    try:
        fh, encoding = _open_with_encoding(path)
    except PermissionError:
        _err(f"Permission denied: cannot read '{path}'.")
        return EXIT_FILE_ERROR
    except UnicodeDecodeError as exc:
        _err(
            f"Could not decode '{path}' as UTF-8 or latin-1: {exc}.  "
            "The file may be corrupt or use an unsupported encoding."
        )
        return EXIT_CONTENT_ERROR
    except OSError as exc:
        _err(f"I/O error opening '{path}': {exc}")
        return EXIT_IO_ERROR

    # --- Read & parse CSV -------------------------------------------------
    try:
        with fh:
            raw = fh.read()
    except PermissionError:
        _err(f"Permission denied while reading '{path}'.")
        return EXIT_FILE_ERROR
    except OSError as exc:
        _err(f"I/O error reading '{path}': {exc}")
        return EXIT_IO_ERROR

    if not raw.strip():
        _err(f"'{path}' is empty.  Nothing to convert.")
        return EXIT_CONTENT_ERROR

    # Parse using csv.DictReader
    import io

    try:
        reader = csv.DictReader(io.StringIO(raw))

        # DictReader.fieldnames triggers the header row read.
        headers = reader.fieldnames
        if headers is None:
            # Should be unreachable given the empty-file check above, but guard anyway.
            _err(f"'{path}' has no header row.")
            return EXIT_CONTENT_ERROR

        rows = []
        for line_num, row in enumerate(reader, start=2):  # data starts at line 2
            # csv.DictReader uses None as the key for extra fields and stores
            # overflow values in row[None].
            if None in row:
                extra_values = row[None]
                _err(
                    f"Malformed CSV: row {line_num} has more columns than the "
                    f"header ({len(headers)} header column(s)).  "
                    f"Extra value(s): {extra_values}"
                )
                return EXIT_CONTENT_ERROR

            # Check for fewer columns than headers (missing fields become None).
            missing = [k for k, v in row.items() if v is None]
            if missing:
                _err(
                    f"Malformed CSV: row {line_num} has fewer columns than the "
                    f"header.  Missing field(s): {missing}"
                )
                return EXIT_CONTENT_ERROR

            rows.append(dict(row))

    except csv.Error as exc:
        _err(f"CSV parse error in '{path}': {exc}")
        return EXIT_CONTENT_ERROR

    # --- Output -----------------------------------------------------------
    try:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    except BrokenPipeError:
        # Consumer (e.g. `head`) closed the pipe — not an error on our side.
        pass
    except OSError as exc:
        _err(f"I/O error writing output: {exc}")
        return EXIT_IO_ERROR

    return EXIT_OK


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) != 2:
        script = os.path.basename(sys.argv[0])
        print(
            f"Usage: python {script} <path/to/file.csv>\n"
            "\n"
            "Converts a CSV file to a JSON array of objects and writes it to stdout.\n"
            "The first row of the CSV is used as field names (header row).",
            file=sys.stderr,
        )
        sys.exit(EXIT_FILE_ERROR)

    path = sys.argv[1]
    sys.exit(convert(path))


if __name__ == "__main__":
    main()
