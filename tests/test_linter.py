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
    ],
)
def test_lint_errors(sql, expected):
    assert lint_sql(sql) == expected


def test_lint_invalid_dialect():
    with pytest.raises(NotImplementedError):
        lint_sql("SELECT 1", dialect="invalid")

