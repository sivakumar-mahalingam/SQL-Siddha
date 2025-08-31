"""SQL formatting utilities."""

from __future__ import annotations

from typing import Literal

import re
import sqlparse


SUPPORTED_DIALECTS = {"ansi"}


def _format_merge(
    stmt: str,
    *,
    keyword_case: Literal["upper", "lower", None] = "upper",
    identifier_case: Literal["upper", "lower", None] = None,
) -> str:
    """Custom formatter for MERGE statements.

    ``sqlparse`` does not properly reindent MERGE statements. This helper uses a
    simple regex-based approach to structure the statement into the expected
    multi-line format and then applies the requested casing rules.
    """

    pattern = re.compile(
        r"merge\s+into\s+(?P<target>.+?)\s+using\s+(?P<source>.+?)\s+on\s+(?P<on>.+?)\s+"
        r"when\s+matched\s+then\s+update\s+set\s+(?P<set>.+?)\s+when\s+not\s+matched\s+"
        r"then\s+insert\s*\((?P<cols>.+?)\)\s+values\s*\((?P<vals>.+?)\);?",
        re.IGNORECASE | re.DOTALL,
    )
    m = pattern.match(stmt.strip())
    if not m:
        # Fallback to generic formatting if the pattern doesn't match
        formatted = sqlparse.format(
            stmt,
            keyword_case=keyword_case,
            identifier_case=identifier_case,
            reindent=True,
            strip_whitespace=True,
        ).strip()
        if not formatted.endswith(";"):
            formatted = formatted.rstrip(";") + ";"
        return formatted

    target = m.group("target").strip()
    source = m.group("source").strip()
    on_cond = m.group("on").strip()
    set_clause = m.group("set").strip()
    cols = m.group("cols").replace("\n", " ").strip()
    vals = m.group("vals").replace("\n", " ").strip()

    formatted = (
        "MERGE INTO "
        + target
        + "\nUSING "
        + source
        + "\n    ON "
        + on_cond
        + "\nWHEN MATCHED THEN\n    UPDATE\n    SET "
        + set_clause
        + "\nWHEN NOT MATCHED THEN\n    INSERT ("
        + cols
        + ")\n    VALUES ("
        + vals
        + ");"
    )

    # Apply casing without altering whitespace/indentation
    formatted = sqlparse.format(
        formatted,
        keyword_case=keyword_case,
        identifier_case=identifier_case,
        reindent=False,
        strip_whitespace=False,
    ).strip()
    if not formatted.endswith(";"):
        formatted = formatted.rstrip(";") + ";"
    return formatted


def format_sql(
    sql: str,
    dialect: Literal["ansi"] = "ansi",
    *,
    keyword_case: Literal["upper", "lower", None] = "upper",
    identifier_case: Literal["upper", "lower", None] = None,
) -> str:
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

    formatted_parts: list[str] = []

    # Format each individual statement and preserve order
    for raw_stmt in sqlparse.split(sql):
        stmt = raw_stmt.strip()
        if not stmt:
            continue

        if stmt.lstrip().upper().startswith("MERGE"):
            formatted = _format_merge(
                stmt,
                keyword_case=keyword_case,
                identifier_case=identifier_case,
            )
        else:
            formatted = sqlparse.format(
                stmt,
                keyword_case=keyword_case,
                identifier_case=identifier_case,
                reindent=True,
                strip_whitespace=True,
            ).strip()
            if not formatted.endswith(";"):
                formatted = formatted.rstrip(";") + ";"
        formatted_parts.append(formatted)

    return "\n".join(formatted_parts)
