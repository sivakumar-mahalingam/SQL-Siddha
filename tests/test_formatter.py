from sql_siddha.formatter import format_sql


def test_format_sql_adds_semicolon_and_uppercases():
    sql = "select * from users"
    expected = "SELECT *\nFROM users;"
    assert format_sql(sql) == expected


def test_format_sql_multiple_statements():
    sql = "select * from users; select id from orders"
    expected = "SELECT *\nFROM users;\nSELECT id\nFROM orders;"
    assert format_sql(sql) == expected
