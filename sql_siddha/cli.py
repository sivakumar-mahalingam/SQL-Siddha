"""Command line interface for SQL Siddha."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional
import sys

from .formatter import format_sql
from .linter import lint_sql


def _read_input(path: Optional[str]) -> str:
    if path:
        try:
            return Path(path).read_text()
        except FileNotFoundError:
            print(f"File not found: {path}", file=sys.stderr)
            raise SystemExit(1)
    return ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SQL Siddha linter and formatter")
    sub = parser.add_subparsers(dest="command", required=True)

    p_format = sub.add_parser("format", help="Format SQL")
    p_format.add_argument("path", help="Path to SQL file")
    p_format.add_argument("--dialect", default="ansi", help="SQL dialect")
    p_format.add_argument("-o", "--output", help="Output file; default overwrites input")

    p_lint = sub.add_parser("lint", help="Lint SQL")
    p_lint.add_argument("path", help="Path to SQL file")
    p_lint.add_argument("--dialect", default="ansi", help="SQL dialect")

    args = parser.parse_args(argv)

    if args.command == "format":
        sql = _read_input(args.path)
        formatted = format_sql(sql, dialect=args.dialect)
        output_path = args.output or args.path
        Path(output_path).write_text(
            formatted + ("\n" if not formatted.endswith("\n") else "")
        )
        return 0
    else:  # lint
        sql = _read_input(args.path)
        messages = lint_sql(sql, dialect=args.dialect)
        for msg in messages:
            print(msg)
        return 0 if not messages else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
