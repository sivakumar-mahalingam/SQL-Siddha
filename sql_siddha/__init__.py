"""SQL Siddha: A simple SQL linter and formatter."""

__all__ = ["format_sql", "lint_sql"]

from .formatter import format_sql
from .linter import lint_sql
