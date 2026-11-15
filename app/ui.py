from pathlib import Path

import streamlit as st
from streamlit.runtime.state import SessionStateProxy

from app.data import delete_match


def show_matches(
    ss: SessionStateProxy,
    match_rows: list,
    round_number: int,
    players: dict,
    matches_csv: Path,
) -> None:
    for i, r in match_rows:
        a = players[int(r["player1"])]
        b = players[int(r["player2"])]

        col1, col2, col3 = st.columns([5, 1, 1])

        col1.markdown(f"{a} **{r['wins_p1']} - {r['wins_p2']}** {b}")

        if col2.button("Edit", key=f"edit_{round_number}_{i}"):
            ss.edit_index = i
            ss.edit_round = round_number
            ss.step = "edit"
            st.rerun()

        if col3.button("Delete", key=f"delete_{round_number}_{i}"):
            delete_match(i, matches_csv)
            st.rerun()
