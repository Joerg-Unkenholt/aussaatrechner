from pathlib import Path


def test_gitignore_exists():
    assert Path(".gitignore").exists()


def test_local_database_is_ignored_by_policy():
    text = Path(".gitignore").read_text(encoding="utf-8")
    assert "data/garden.db" in text
    assert ".venv/" in text
    assert ".env" in text
