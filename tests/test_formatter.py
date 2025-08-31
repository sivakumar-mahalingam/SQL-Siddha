import pytest

from sql_siddha.formatter import format_sql


@pytest.mark.parametrize(
    "sql, expected",
    [
        ("select * from users", "SELECT *\nFROM users;"),
        (
            "select * from users; select id from orders",
            "SELECT *\nFROM users;\nSELECT id\nFROM orders;",
        ),
    ],
)
def test_format_sql(sql, expected):
    assert format_sql(sql) == expected


def test_format_invalid_dialect():
    with pytest.raises(NotImplementedError):
        format_sql("SELECT 1", dialect="invalid")
