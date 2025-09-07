import sqlite3

from src.security.db_utils import execute_db, fetch_one, fetch_all


def test_execute_and_fetch(tmp_path):
    db_file = tmp_path / "helpers.db"
    execute_db(db_file, "CREATE TABLE items(id INTEGER PRIMARY KEY, name TEXT)")
    execute_db(db_file, "INSERT INTO items(name) VALUES (?)", ("alpha",))
    execute_db(db_file, "INSERT INTO items(name) VALUES (?)", ("beta",))

    row = fetch_one(db_file, "SELECT name FROM items WHERE id = ?", (1,))
    assert row == ("alpha",)

    rows = fetch_all(db_file, "SELECT name FROM items ORDER BY id")
    assert rows == [("alpha",), ("beta",)]

    # Ensure data persisted by reading through sqlite3 directly
    with sqlite3.connect(db_file) as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM items")
        assert cur.fetchone()[0] == 2
