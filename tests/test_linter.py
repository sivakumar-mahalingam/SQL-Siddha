from sql_siddha.linter import lint_sql


def test_lint_valid_sql():
    sql = "SELECT * FROM users;"
    assert lint_sql(sql) == []


def test_lint_missing_semicolon():
    sql = "SELECT * FROM users"
    assert lint_sql(sql) == ["Statement should end with a semicolon"]


def test_lint_lowercase_keywords():
    sql = "select * from users;"
    messages = lint_sql(sql)
    assert "Keyword 'select' should be uppercase" in messages
    assert "Keyword 'from' should be uppercase" in messages


def test_lint_multiple_statements():
    sql = "SELECT * FROM users; select * from orders"
    messages = lint_sql(sql)
    assert "Statement should end with a semicolon" in messages
    assert "Keyword 'select' should be uppercase" in messages
