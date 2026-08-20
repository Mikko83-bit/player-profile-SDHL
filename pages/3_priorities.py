import pandas as pd
import streamlit as st

df = st.session_state.get("df")
selected_player = st.session_state.get("selected_player")

if df is not None and selected_player:
    p = df[df[df.columns[0]] == selected_player].iloc[0]

    st.title(f"🎯 {selected_player} — Kehityskohteet & Tavoitteet")

    col_puck, col_no_puck = st.columns(2)

    with col_puck:
        st.subheader("🏒 Peli kiekolla (With Puck)")
        st.info(
            p.get(
                "Write down 3 specific skills/situations in the game with the puck",
                "Ei kirjauksia",
            )
        )

    with col_no_puck:
        st.subheader("🛡️ Peli ilman kiekkoa (Without Puck)")
        st.info(
            p.get(
                "Write down 3 specific skills/situations in the game without the puck",
                "Ei kirjauksia",
            )
        )

    st.divider()

    st.subheader("💬 Palaute ja kehittyminen")
    st.write(
        f"**Suhtautuminen palautteeseen:** {p.get('How do you handle feedback (both positive and negative)?', '-')}"
    )
    st.write(
        f"**Mielentila ja haasteet:** {p.get('How do you handle challenges?', '-')}"
    )
else:
    st.warning("Valitse pelaaja vasemmasta sivupalkista.")
