import streamlit as st
from streamlit.runtime.state import SessionStateProxy

from app.config import DATA
from pipeline.validate import validate


def players_step(
    ss: SessionStateProxy,
    players: dict,
    current_round: int,
    current_round_matches: list,
    round_key: str,
) -> None:
    ids = sorted(players, key=lambda pid: players[pid].casefold())
    p1 = st.selectbox(
        "Player 1",
        ids,
        index=None,
        format_func=lambda pid: players[pid],
        placeholder="Choose Player 1",
    )
    p2 = st.selectbox(
        "Player 2",
        ids,
        index=None,
        format_func=lambda pid: players[pid],
        placeholder="Choose Player 2",
    )
    if st.button("Enter Results"):
        busy = {
            int(r[k])
            for _, r in current_round_matches
            for k in ("player1", "player2")
        }
        if p1 is None or p2 is None:
            st.error("Pick both players.")
        elif p1 == p2:
            st.error("Pick two different players.")
        elif {p1, p2} & busy:
            names = " and ".join(players[p] for p in (p1, p2) if p in busy)
            st.error(f"{names} already played in round {current_round}.")
        else:
            ss.pair = (p1, p2)
            ss.step = "scores"
            st.rerun()

    _, mid, right = st.columns(3)
    if mid.button("Next round", disabled=not current_round_matches):
        ss[round_key] = current_round + 1
        st.rerun()
    if right.button("Finish event"):
        n = validate(DATA)  # prints details to the terminal
        if n == 0:
            st.success("Looks good, ready to commit.")
        else:
            st.error(f"{n} check(s) failed, see the terminal.")
