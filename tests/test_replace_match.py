import duckdb
import pytest

from app.data import read_rows, replace_match


def test_replace_match(matches_csv):
    original_rows = read_rows(matches_csv)

    new_row = {
        "round": "4",
        "player1": "7",
        "player2": "8",
        "wins_p1": "2",
        "wins_p2": "1",
        "g1_on_play": "7",
    }

    replace_match(matches_csv, 0, new_row)

    updated_rows = read_rows(matches_csv)

    assert updated_rows[0] == new_row
    assert len(updated_rows) == len(original_rows)


def test_replace_match_invalid_index(matches_csv):
    rows = read_rows(matches_csv)

    with pytest.raises(IndexError):
        replace_match(matches_csv, len(rows), {})


def test_replace_match_invalid(matches_csv, original_matches):
    same_player_row = {
        "round": 4,
        "player1": 7,
        "player2": 7,
        "wins_p1": 2,
        "wins_p2": 1,
        "g1_on_play": 7,
    }

    with pytest.raises(duckdb.ConstraintException):
        replace_match(matches_csv, 0, same_player_row)

    wrong_g1_on_play = {
        "round": 4,
        "player1": 7,
        "player2": 8,
        "wins_p1": 2,
        "wins_p2": 1,
        "g1_on_play": 1,
    }

    with pytest.raises(duckdb.ConstraintException):
        replace_match(matches_csv, 0, wrong_g1_on_play)

    assert matches_csv.read_text() == original_matches
