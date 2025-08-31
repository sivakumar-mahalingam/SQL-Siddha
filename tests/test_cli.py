import pytest

from sql_siddha.cli import main


def test_cli_format(tmp_path, capsys):
    path = tmp_path / "query.sql"
    path.write_text("select * from users")
    assert main(["format", str(path)]) == 0
    assert path.read_text().strip() == "SELECT *\nFROM users;"
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_cli_lint_success(tmp_path, capsys):
    path = tmp_path / "query.sql"
    path.write_text("SELECT * FROM users;")
    assert main(["lint", str(path)]) == 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_cli_lint_failure(tmp_path, capsys):
    path = tmp_path / "query.sql"
    path.write_text("select * from users")
    assert main(["lint", str(path)]) == 1
    captured = capsys.readouterr()
    assert "Keyword 'select' should be uppercase" in captured.out


def test_cli_format_multiple_statements(tmp_path):
    path = tmp_path / "queries.sql"
    path.write_text("select * from users; select id from orders")
    assert main(["format", str(path)]) == 0
    expected = "SELECT *\nFROM users;\nSELECT id\nFROM orders;"
    assert path.read_text().strip() == expected


def test_cli_lint_multiple_statements(tmp_path, capsys):
    path = tmp_path / "queries.sql"
    path.write_text("SELECT * FROM users; select * from orders")
    assert main(["lint", str(path)]) == 1
    captured = capsys.readouterr()
    assert "Statement should end with a semicolon" in captured.out
    assert "Keyword 'select' should be uppercase" in captured.out


def test_cli_lint_missing_file(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["lint", "missing.sql"])
    assert exc.value.code == 1
    captured = capsys.readouterr()
    assert "File not found" in captured.err


def test_cli_format_missing_file(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["format", "missing.sql"])
    assert exc.value.code == 1
    captured = capsys.readouterr()
    assert "File not found" in captured.err


def test_cli_format_output_file(tmp_path, capsys):
    path = tmp_path / "query.sql"
    path.write_text("select * from users")
    out_path = tmp_path / "formatted.sql"
    assert main(["format", str(path), "--output", str(out_path)]) == 0
    assert path.read_text() == "select * from users"
    assert out_path.read_text().strip() == "SELECT *\nFROM users;"
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_cli_invalid_dialect_format(tmp_path):
    path = tmp_path / "query.sql"
    path.write_text("select * from users")
    with pytest.raises(NotImplementedError):
        main(["format", str(path), "--dialect", "invalid"])


def test_cli_invalid_dialect_lint(tmp_path):
    path = tmp_path / "query.sql"
    path.write_text("select * from users")
    with pytest.raises(NotImplementedError):
        main(["lint", str(path), "--dialect", "invalid"])

