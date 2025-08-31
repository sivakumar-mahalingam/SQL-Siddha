import subprocess
import sys


def run_cli(*args, input_path=None):
    cmd = [sys.executable, "-m", "sql_siddha.cli", *args]
    return subprocess.run(cmd, capture_output=True, text=True)


def test_cli_format(tmp_path):
    path = tmp_path / "query.sql"
    path.write_text("select * from users")
    result = run_cli("format", str(path))
    assert result.returncode == 0
    assert path.read_text().strip() == "SELECT *\nFROM users;"


def test_cli_lint(tmp_path):
    path = tmp_path / "query.sql"
    path.write_text("select * from users")
    result = run_cli("lint", str(path))
    assert result.returncode == 1
    assert "Keyword 'select' should be uppercase" in result.stdout


def test_cli_format_multiple_statements(tmp_path):
    path = tmp_path / "queries.sql"
    path.write_text("select * from users; select id from orders")
    result = run_cli("format", str(path))
    assert result.returncode == 0
    expected = "SELECT *\nFROM users;\nSELECT id\nFROM orders;"
    assert path.read_text().strip() == expected


def test_cli_lint_multiple_statements(tmp_path):
    path = tmp_path / "queries.sql"
    path.write_text("SELECT * FROM users; select * from orders")
    result = run_cli("lint", str(path))
    assert result.returncode == 1
    stdout = result.stdout
    assert "Statement should end with a semicolon" in stdout
    assert "Keyword 'select' should be uppercase" in stdout


def test_cli_missing_file():
    result = run_cli("lint", "missing.sql")
    assert result.returncode == 1
    assert "File not found" in result.stderr
