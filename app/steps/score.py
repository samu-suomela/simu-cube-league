from pathlib import Path

import streamlit as st
from streamlit.runtime.state import SessionStateProxy

from app.data import try_add


def score_step(
    ss: SessionStateProxy, matches_csv: Path, players: dict, current_round: int
) -> None:

    p1, p2 = ss.pair
    st.subheader(f"{players[p1]} vs {players[p2]}")
    with st.form("scores"):
        w1 = st.radio(
            f"{players[p1]} game wins",
            [2, 1, 0],
            index=2,
            horizontal=True,
        )

        w2 = st.radio(
            f"{players[p2]} game wins",
            [2, 1, 0],
            index=2,
            horizontal=True,
        )
        st.write("On the play in game 1")
        on_play = st.radio(
            "On the play in game 1",
            [p1, p2],
            format_func=players.get,
            horizontal=True,
            label_visibility="collapsed",
        )
        save = st.form_submit_button("Save match")
        back = st.form_submit_button("Back")
    if back:
        ss.step = "players"
        st.rerun()
    if save:
        if w1 == 2 and w2 == 2:
            st.error("Best of three: only one player can have 2 wins.")
        else:
            try_add(
                matches_csv,
                {
                    "round": current_round,
                    "player1": p1,
                    "player2": p2,
                    "wins_p1": w1,
                    "wins_p2": w2,
                    "g1_on_play": on_play,
                },
            )
            ss.step = "players"
            st.rerun()
