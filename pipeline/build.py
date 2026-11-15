import json
import sys
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

from pipeline.load import load
from pipeline.validate import validate

EXPORTS = [
    "player_records",
    "head_to_head",
]  # views to publish, one JSON file each


def json_default(o):
    if isinstance(o, Decimal):
        return float(o)  # DuckDB returns DECIMAL for `* 1.0` ratios
    if isinstance(o, (date, datetime)):
        return o.isoformat()
    raise TypeError(f"Cannot serialize {type(o)}")


def rows_as_dicts(con, query: str) -> list[dict]:
    cur = con.execute(query)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=json_default))


def build(data_dir: Path, out_dir: Path) -> int:
    if validate(data_dir):  # stop before publishing bad data
        print("Validation failed, nothing built.")
        return 1

    con = load(data_dir)
    for view in EXPORTS:
        write_json(
            out_dir / f"{view}.json",
            rows_as_dicts(con, f"SELECT * FROM {view}"),
        )
        print(f"wrote {view}.json")
    write_json(
        out_dir / "players.json", rows_as_dicts(con, "SELECT * FROM players")
    )
    print("wrote players.json")
    return 0


if __name__ == "__main__":
    data_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data")
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("docs/data")
    sys.exit(build(data_dir, out_dir))
