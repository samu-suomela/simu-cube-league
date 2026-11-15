import pytest

from app.data import delete_match, read_rows


def test_delete_match(matches_csv):
    original_rows = read_rows(matches_csv)

    delete_match(0, matches_csv)

    remaining_rows = read_rows(matches_csv)

    assert len(remaining_rows) == len(original_rows) - 1
    assert original_rows[0] not in remaining_rows


def test_delete_nonexisting_match(matches_csv):
    original_rows = read_rows(matches_csv)
    with pytest.raises(IndexError):
        delete_match(9999, matches_csv)

    remaining_rows = read_rows(matches_csv)
    assert original_rows == remaining_rows
