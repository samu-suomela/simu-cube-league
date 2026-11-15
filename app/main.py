"""Local match entry. Run with: make entry"""

import streamlit as st

from app.data import (
    get_matches_path,
    load_players,
    read_rows,
)
from app.steps.date import date_step
from app.steps.edit import edit_step
from app.steps.players import players_step
from app.steps.score import score_step
from app.ui import show_matches

ss = st.session_state

if "step" not in ss:
    ss.step = "date"

# ---------- Pick the event date ----------
if ss.step == "date":
    date_step(ss)

if st.sidebar.button("Change event date"):
    ss.step = "date"
    st.rerun()


# ---------- Initialise ----------
matches_csv = get_matches_path(ss)
players = load_players()
rows = read_rows(matches_csv)

round_key = f"round_{ss.event_date}"

if round_key not in ss:
    ss[round_key] = max((int(row["round"]) for row in rows), default=1)

current_round = ss[round_key]
current_round_matches = [
    (i, r) for i, r in enumerate(rows) if int(r["round"]) == current_round
]

# ---------- Main page ----------
st.title("Mökkiliiga")
st.caption(f"Event {ss.event_date.isoformat()}")

previous_rounds = sorted(
    {int(r["round"]) for r in rows if int(r["round"]) < current_round},
    reverse=True,
)
for prev_round in previous_rounds:
    prev_matches = [
        (i, r) for i, r in enumerate(rows) if int(r["round"]) == prev_round
    ]

    with st.expander(f"Round {prev_round} results", expanded=False):
        show_matches(ss, prev_matches, prev_round, players, matches_csv)

st.header(f"Round {current_round}")

current_matches = [
    (i, r) for i, r in enumerate(rows) if int(r["round"]) == current_round
]

if not current_round_matches:
    st.caption("No matches yet.")

show_matches(ss, current_round_matches, current_round, players, matches_csv)

st.divider()

# ---------- Possible steps ----------
if ss.step == "players":
    players_step(ss, players, current_round, current_round_matches, round_key)

elif ss.step == "edit":
    edit_step(ss, matches_csv, players)

elif ss.step == "scores":
    score_step(ss, matches_csv, players, current_round)
