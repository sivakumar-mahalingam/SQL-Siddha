"""SQL formatting utilities."""

from __future__ import annotations

from typing import Literal

import sqlparse


SUPPORTED_DIALECTS = {"ansi"}


def format_sql(sql: str, dialect: Literal["ansi"] = "ansi") -> str:
    """Return a formatted SQL string.

    Parameters
    ----------
    sql:
        The SQL statement to format. May contain multiple statements.
    dialect:
        Currently only ``"ansi"`` is supported. Future dialects may be added.
    """

    if dialect not in SUPPORTED_DIALECTS:
        raise NotImplementedError(f"Dialect '{dialect}' is not supported yet")

    formatted_parts = []

    # Format each individual statement and preserve order
    for raw_stmt in sqlparse.split(sql):
        stmt = raw_stmt.strip()
        if not stmt:
            continue

        formatted = sqlparse.format(
            stmt,
            keyword_case="upper",
            reindent=True,
            strip_whitespace=True,
        ).strip()
        if not formatted.endswith(";"):
            formatted = formatted.rstrip(";") + ";"
        formatted_parts.append(formatted)

    return "\n".join(formatted_parts)
