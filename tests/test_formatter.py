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
            "MERGE INTO target t USING SOURCE s ON t.id = s.id WHEN matched THEN\nUPDATE\nSET col = s.col WHEN NOT matched THEN\nINSERT (id,\n        col)\nVALUES (s.id, s.col);",
        ),
    ],
)
def test_format_sql(sql, expected):
    assert format_sql(sql) == expected


def test_format_invalid_dialect():
    with pytest.raises(NotImplementedError):
        format_sql("SELECT 1", dialect="invalid")
