import pandas as pd
import streamlit as st

df = st.session_state.get("df")
selected_player = st.session_state.get("selected_player")
name_col = st.session_state.get("name_col", "Name")

if df is not None and selected_player:
    match = df[df[name_col].astype(str).str.strip() == str(selected_player)]

    if not match.empty:
        p = match.iloc[0]

        st.title(f"🎯 {selected_player} — Kehityskohteet & Tavoitteet")

        # 1. PELI KIEKOLLA JA ILMAN KIEKKOA
        col_puck, col_no_puck = st.columns(2)

        # Etsitään ruotsinkieliset pitkät otsikot sarakkeista
        puck_col = [
            c
            for c in df.columns
            if "Skriv ner 3 konkreta moment i spelet med puck" in str(c)
        ]
        no_puck_col = [
            c
            for c in df.columns
            if "Skriv ner 3 konkreta moment i spelet utan puck" in str(c)
        ]

        with col_puck:
            st.subheader("🏒 Peli kiekolla (Med puck)")
            val_puck = (
                p.get(puck_col[0], "Ei kirjauksia")
                if puck_col
                else "Ei kirjauksia"
            )
            st.info(
                val_puck
                if pd.notna(val_puck) and str(val_puck) != "nan"
                else "Ei kirjauksia"
            )

        with col_no_puck:
            st.subheader("🛡️ Peli ilman kiekkoa (Utan puck)")
            val_no_puck = (
                p.get(no_puck_col[0], "Ei kirjauksia")
                if no_puck_col
                else "Ei kirjauksia"
            )
            st.info(
                val_no_puck
                if pd.notna(val_no_puck) and str(val_no_puck) != "nan"
                else "Ei kirjauksia"
            )

        st.divider()

        # 2. HAASTEET, PALAUTE JA TAVOITTEET
        st.subheader("💬 Haasteet, palaute ja kauden tavoite")

        col_left, col_right = st.columns(2)

        with col_left:
            st.write("**Haasteiden käsittely harjoituksissa/peleissä:**")
            st.write(
                f"> {p.get('Hur hanterar du utmaningar vid träningar/match', '-')}"
            )

            st.write("**Vastaanottavaisuus palautteelle:**")
            st.write(
                f"> {p.get('Hur mottaglig är du för feedback?', '-')}"
            )

            st.write("**Palautteen käsittely (positiivinen & negatiivinen):**")
            st.write(
                f"> {p.get('Hur hanterar du feedback (negativ och positiv)?', '-')}"
            )

        with col_right:
            st.write("**Kauden tavoite (Mål för säsongen):**")
            goal_val = p.get("Vad är ditt mål med den här säsongen?", "-")
            st.success(
                goal_val
                if pd.notna(goal_val) and str(goal_val) != "nan"
                else "Ei asetettua tavoitetta"
            )

    else:
        st.warning(f"Pelaajan '{selected_player}' tietoja ei löytynyt.")
else:
    st.info("Valitse pelaaja sivupalkista.")
