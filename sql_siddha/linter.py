"""SQL linting utilities."""

from __future__ import annotations

from typing import List, Literal

import sqlparse
from sqlparse import tokens as T

SUPPORTED_DIALECTS = {"ansi"}


def lint_sql(sql: str, dialect: Literal["ansi"] = "ansi") -> List[str]:
    """Lint a SQL string and return a list of messages.

    Parameters
    ----------
    sql:
        The SQL statement to lint. May contain multiple statements.
    dialect:
        Currently only ``"ansi"`` is supported. Future dialects may be added.
    """

    if dialect not in SUPPORTED_DIALECTS:
        raise NotImplementedError(f"Dialect '{dialect}' is not supported yet")

    messages: List[str] = []

    statements = [s for s in sqlparse.split(sql) if s.strip()]
    if not statements:
        return ["No SQL statement found"]

    for stmt in statements:
        parsed = sqlparse.parse(stmt)
        if not parsed:
            messages.append("No SQL statement found")
            continue
        statement = parsed[0]

        # Check that the final non-whitespace token is a semicolon
        meaningful_tokens = [t for t in statement.tokens if not t.is_whitespace]
        if meaningful_tokens and meaningful_tokens[-1].value != ";":
            messages.append("Statement should end with a semicolon")

        # Check that keywords are uppercase
        for token in statement.flatten():
            if token.ttype in T.Keyword and token.value != token.value.upper():
                messages.append(f"Keyword '{token.value}' should be uppercase")

    return messages
