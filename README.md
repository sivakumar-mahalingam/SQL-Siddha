# SQL Siddha

SQL Siddha is a minimal SQL linter and formatter. It currently supports only the ANSI SQL dialect; other dialects can be added later.
Both the linter and formatter can process files containing multiple SQL statements.

## Installation

```bash
pip install .
```

## Usage

Format a SQL file in place:

```bash
sql-siddha format path/to/query.sql
```

Lint a SQL file:

```bash
sql-siddha lint path/to/query.sql
```

Both commands support a ``--dialect`` option which defaults to ``ansi``.
