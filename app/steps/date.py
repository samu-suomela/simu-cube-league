from datetime import date

import streamlit as st
from streamlit.runtime.state import SessionStateProxy

from app.config import COLS, DATA, DELIM


def date_step(ss: SessionStateProxy):

    selected_date = st.date_input("Event date", value=date.today())
    if st.button("Start / resume event"):
        event_date = DATA / "events" / selected_date.isoformat()
        if not (event_date / "matches.csv").exists():
            event_date.mkdir(parents=True, exist_ok=True)
            (event_date / "matches.csv").write_text(DELIM.join(COLS) + "\n")
        ss.event_date = selected_date
        ss.step = "players"
        st.rerun()
    st.stop()
