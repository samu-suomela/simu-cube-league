from datetime import date
from pathlib import Path

import duckdb

SCHEMA = Path(__file__).with_name("schema.sql")
VIEWS = Path(__file__).with_name("views.sql")


def load(data_dir: Path) -> duckdb.DuckDBPyConnection:

    players_csv = data_dir / "players.csv"
    events_dir = data_dir / "events"

    con = duckdb.connect()
    con.execute(SCHEMA.read_text())
    con.execute(VIEWS.read_text())

    con.execute(f"""
        INSERT INTO players (id, name)
        SELECT id, name FROM read_csv('{players_csv}')
    """)

    for folder in sorted(events_dir.iterdir()):
        event_date = date.fromisoformat(folder.name)
        con.execute(
            f"""INSERT INTO matches (event_date, round, player1, player2, wins_p1, wins_p2, g1_on_play)
                SELECT ?, round, player1, player2, wins_p1, wins_p2, g1_on_play
                FROM read_csv('{folder / "matches.csv"}')""",
            [event_date],
        )
    return con


def get_columns() -> list:
    con = duckdb.connect()
    con.execute(SCHEMA.read_text())
    return [
        r[0]
        for r in con.execute("DESCRIBE matches").fetchall()
        if r[0] != "event_date"
    ]
