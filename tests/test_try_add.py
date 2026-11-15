import duckdb
import pytest

from app.data import try_add


def test_wrong_g1_on_play(matches_csv, original_matches):
    new_row = {
        "round": 4,
        "player1": 9,
        "player2": 8,
        "wins_p1": 2,
        "wins_p2": 1,
        "g1_on_play": 7,
    }

    with pytest.raises(duckdb.ConstraintException):
        try_add(matches_csv, new_row)

    assert matches_csv.read_text() == original_matches


def test_missing_data(matches_csv, original_matches):
    new_row = {
        "round": 4,
        "player1": 9,
        "player2": 9,
        "wins_p1": 2,
        "wins_p2": 1,
    }

    with pytest.raises(KeyError):
        try_add(matches_csv, new_row)

    assert matches_csv.read_text() == original_matches


def test_same_p1_p2(matches_csv, original_matches):
    new_row = {
        "round": "4",
        "player1": "7",
        "player2": "7",
        "wins_p1": "2",
        "wins_p2": "1",
        "g1_on_play": "1",
    }

    with pytest.raises(duckdb.ConstraintException):
        try_add(matches_csv, new_row)

    assert matches_csv.read_text() == original_matches
