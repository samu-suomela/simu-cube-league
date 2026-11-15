from pathlib import Path

import streamlit as st
from streamlit.runtime.state import SessionStateProxy

from app.data import read_rows, replace_match


def edit_step(ss: SessionStateProxy, matches_csv: Path, players: dict) -> None:
    index = ss.edit_index
    rows = read_rows(matches_csv)
    r = rows[index]

    p1 = int(r["player1"])
    p2 = int(r["player2"])

    st.subheader(f"Editing Round {r['round']}: {players[p1]} vs {players[p2]}")

    with st.form("edit_match"):
        w1 = st.radio(
            f"{players[p1]} game wins",
            [2, 1, 0],
            index=[2, 1, 0].index(int(r["wins_p1"])),
            horizontal=True,
        )

        w2 = st.radio(
            f"{players[p2]} game wins",
            [2, 1, 0],
            index=[2, 1, 0].index(int(r["wins_p2"])),
            horizontal=True,
        )

        old_on_play = int(r["g1_on_play"]) if r["g1_on_play"] != "" else p1

        on_play = st.radio(
            "On the play in game 1",
            [p1, p2],
            index=[p1, p2].index(old_on_play),
            format_func=players.get,
            horizontal=True,
        )

        save = st.form_submit_button("Save changes")
        cancel = st.form_submit_button("Cancel")

    if cancel:
        ss.step = "players"
        st.rerun()

    if save:
        if w1 == 2 and w2 == 2:
            st.error("Best of three: only one player can have 2 wins.")
        else:
            updated = {
                "round": r["round"],
                "player1": p1,
                "player2": p2,
                "wins_p1": w1,
                "wins_p2": w2,
                "g1_on_play": on_play,
            }

            replace_match(matches_csv, index, updated)

            ss.step = "players"
            st.rerun()
