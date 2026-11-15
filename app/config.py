from pathlib import Path

from pipeline.load import get_columns

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DELIM = ";"
COLS = get_columns()
