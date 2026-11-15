import csv
import io
from pathlib import Path

import duckdb
from streamlit.runtime.state import SessionStateProxy

from app.config import COLS, DATA, DELIM
from pipeline.load import load


def load_players(data_dir: Path = DATA) -> dict:
    with (data_dir / "players.csv").open(newline="") as f:
        rdr = csv.reader(f, delimiter=DELIM)
        next(rdr)
        return {int(r[0]): r[1] for r in rdr}


def get_matches_path(ss: SessionStateProxy, data_dir: Path = DATA) -> Path:
    return data_dir / "events" / ss.event_date.isoformat() / "matches.csv"


def read_rows(matches_csv: Path) -> list:

    with matches_csv.open(newline="") as f:
        return list(csv.DictReader(f, delimiter=DELIM))


def try_add(matches_csv: Path, row: dict) -> None:
    old = matches_csv.read_text()
    if not old.endswith("\n"):
        old += "\n"
    buf = io.StringIO()
    csv.writer(buf, delimiter=DELIM, lineterminator="\n").writerow(
        [row[c] for c in COLS]
    )
    matches_csv.write_text(old + buf.getvalue())
    return validate_matches(matches_csv, old)


def replace_match(matches_csv: Path, index: int, row: dict) -> None:
    old = matches_csv.read_text()
    rows = read_rows(matches_csv)

    rows[index] = row

    buf = io.StringIO()
    writer = csv.DictWriter(
        buf,
        fieldnames=COLS,
        delimiter=DELIM,
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)

    matches_csv.write_text(buf.getvalue())

    return validate_matches(matches_csv, old)


def validate_matches(matches_csv: Path, old: str) -> None:
    try:
        con = load(matches_csv.parents[2])
        con.close()

    except duckdb.Error:
        matches_csv.write_text(old)
        raise


def delete_match(index: int, matches_csv: Path) -> None:
    """Delete a match by its CSV row index."""
    rows = read_rows(matches_csv)
    rows.pop(index)

    buf = io.StringIO()
    writer = csv.DictWriter(
        buf,
        fieldnames=COLS,
        delimiter=DELIM,
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)

    matches_csv.write_text(buf.getvalue())
