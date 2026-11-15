import shutil
from pathlib import Path

import pytest

MATCHES_CSV = Path(__file__).parent / "fixtures/events/2026-11-14/matches.csv"
PLAYERS_CSV = Path(__file__).parent / "fixtures/players.csv"


@pytest.fixture
def matches_csv(tmp_path: Path) -> Path:
    event_dir = tmp_path / "events" / "2026-11-14"
    event_dir.mkdir(parents=True)

    csv_path = event_dir / "matches.csv"
    shutil.copy(MATCHES_CSV, csv_path)
    shutil.copy(PLAYERS_CSV, tmp_path / "players.csv")

    return csv_path


@pytest.fixture
def original_matches(matches_csv):
    return matches_csv.read_text()
