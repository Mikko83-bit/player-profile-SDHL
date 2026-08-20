import pandas as pd
import streamlit as st

df = st.session_state.get("df")
selected_player = st.session_state.get("selected_player")

if df is not None and selected_player:
    name_col = "Name?" if "Name?" in df.columns else df.columns[0]
    match = df[df[name_col].astype(str).str.strip() == str(selected_player)]

    if not match.empty:
        p = match.iloc[0]

        st.title(f"🎯 {selected_player} — Kehityskohteet & Tavoitteet")

        col_puck, col_no_puck = st.columns(2)

        puck_col = [
            c
            for c in df.columns
            if "Write down 3 specific skills/situations in the game with the puck"
            in c
        ]
        no_puck_col = [
            c
            for c in df.columns
            if "Write down 3 specific skills/situations in the game without the puck"
            in c
            or (
                "Write down 3 specific skills/situations" in c
                and c not in puck_col
            )
        ]

        with col_puck:
            st.subheader("🏒 Peli kiekolla (With Puck)")
            val_puck = (
                p.get(puck_col[0], "Ei kirjauksia")
                if puck_col
                else "Ei kirjauksia"
            )
            st.info(val_puck)

        with col_no_puck:
            st.subheader("🛡️ Peli ilman kiekkoa (Without Puck)")
            val_no_puck = (
                p.get(no_puck_col[0], "Ei kirjauksia")
                if no_puck_col
                else "Ei kirjauksia"
            )
            st.info(val_no_puck)

        st.divider()

        st.subheader("💬 Palaute ja haasteiden käsittely")

        st.write(
            f"**Haasteet:** {p.get('How do you handle challenges during practices', p.get('How do you handle challenges?', '-'))}"
        )
        st.write(
            f"**Vastaanottavaisuus:** {p.get('How receptive are you to feedback?', '-')}"
        )
        st.write(
            f"**Palautteen käsittely:** {p.get('How do you handle feedback (both positive and negative)?', '-')}"
        )
    else:
        st.warning(f"Pelaajan '{selected_player}' tietoja ei löytynyt.")
else:
    st.info("Valitse pelaaja sivupalkista.")
