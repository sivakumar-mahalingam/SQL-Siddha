import subprocess
import sys


def run_cli(*args):
    cmd = [sys.executable, "-m", "sql_siddha.cli", *args]
    return subprocess.run(cmd, capture_output=True, text=True)


def test_format_success(tmp_path):
    path = tmp_path / "query.sql"
    path.write_text("select * from users")
    result = run_cli("format", str(path))
    assert result.returncode == 0
    assert result.stdout == ""
    assert path.read_text() == "SELECT *\nFROM users;\n"


def test_format_missing_file():
    result = run_cli("format", "missing.sql")
    assert result.returncode == 1
    assert "File not found" in result.stderr


def test_lint_success(tmp_path):
    path = tmp_path / "query.sql"
    path.write_text("SELECT * FROM users;")
    result = run_cli("lint", str(path))
    assert result.returncode == 0
    assert result.stdout == ""


def test_lint_failure(tmp_path):
    path = tmp_path / "query.sql"
    path.write_text("select * from users;")
    result = run_cli("lint", str(path))
    assert result.returncode == 1
    assert "Keyword 'select' should be uppercase" in result.stdout
