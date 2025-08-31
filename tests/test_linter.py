import pytest

from sql_siddha.linter import lint_sql


@pytest.mark.parametrize(
    "sql, expected",
    [
        ("SELECT * FROM users", ["Statement should end with a semicolon"]),
        (
            "select * from users;",
            ["Keyword 'select' should be uppercase", "Keyword 'from' should be uppercase"],
        ),
        (
            "SELECT * FROM users; select * from orders",
            [
                "Statement should end with a semicolon",
                "Keyword 'select' should be uppercase",
                "Keyword 'from' should be uppercase",
            ],
        ),
        (
            "merge into target t using source s on t.id = s.id when matched then update set col = s.col when not matched then insert (id, col) values (s.id, s.col)",
            [
                "Statement should end with a semicolon",
                "Keyword 'merge' should be uppercase",
                "Keyword 'into' should be uppercase",
                "Keyword 'using' should be uppercase",
                "Keyword 'source' should be uppercase",
                "Keyword 'on' should be uppercase",
                "Keyword 'when' should be uppercase",
                "Keyword 'then' should be uppercase",
                "Keyword 'update' should be uppercase",
                "Keyword 'set' should be uppercase",
                "Keyword 'when' should be uppercase",
                "Keyword 'not' should be uppercase",
                "Keyword 'then' should be uppercase",
                "Keyword 'insert' should be uppercase",
                "Keyword 'values' should be uppercase",
            ],
        ),
    ],
)
def test_lint_errors(sql, expected):
    assert lint_sql(sql) == expected


def test_lint_invalid_dialect():
    with pytest.raises(NotImplementedError):
        lint_sql("SELECT 1", dialect="invalid")

