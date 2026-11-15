import sys
from pathlib import Path

import duckdb

from pipeline.load import load


def find_check_views(con) -> list[str]:
    rows = con.execute(
        "SELECT view_name FROM duckdb_views() WHERE NOT internal"
    ).fetchall()
    return sorted(name for (name,) in rows if name.startswith("check_"))


def validate(data_dir: Path) -> int:
    """Return the number of problems found."""
    try:
        con = load(data_dir)
    except (duckdb.Error, ValueError, OSError) as e:
        print(f"LOAD FAILED: {type(e).__name__}: {e}")
        return 1

    views = find_check_views(con)
    if not views:
        print("FAILED: no checks found")
        return 1

    problems = 0
    for view in views:
        rows = con.execute(f"SELECT * FROM {view}").fetchall()
        if rows:
            problems += 1
            print(f"FAILED: {view}: {len(rows)} row(s)")
            for row in rows[:10]:
                print("   ", row)
        else:
            print(f"ok\t{view}")
    return problems


if __name__ == "__main__":
    data_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data")
    sys.exit(1 if validate(data_dir) else 0)
