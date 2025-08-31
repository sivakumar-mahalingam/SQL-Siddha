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
        (
            "merge into target t using source s on t.id = s.id when matched then update set col = s.col when not matched then insert (id, col) values (s.id, s.col);",
            "MERGE INTO target t\nUSING SOURCE s\n    ON t.id = s.id\nWHEN MATCHED THEN\n    UPDATE\n    SET col = s.col\nWHEN NOT MATCHED THEN\n    INSERT (id, col)\n    VALUES (s.id, s.col);",
        ),
    ],
)
def test_format_sql(sql, expected):
    assert format_sql(sql) == expected


def test_format_invalid_dialect():
    with pytest.raises(NotImplementedError):
        format_sql("SELECT 1", dialect="invalid")


def test_format_case_options():
    sql = "select id from users"
    assert (
        format_sql(sql, keyword_case="lower")
        == "select id\nfrom users;"
    )
    assert (
        format_sql(sql, keyword_case="upper", identifier_case="upper")
        == "SELECT ID\nFROM USERS;"
    )
