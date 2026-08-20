import pandas as pd
import streamlit as st

df = st.session_state.get("df")
selected_player = st.session_state.get("selected_player")
name_col = st.session_state.get("name_col", "Name")

if df is not None and selected_player:
    match = df[df[name_col].astype(str).str.strip() == str(selected_player)]

    if not match.empty:
        p = match.iloc[0]

        st.title(f"🎯 {selected_player} — Development & Goals")

        col_puck, col_no_puck = st.columns(2)

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
            st.subheader("🏒 Game With Puck")
            val_puck = (
                p.get(puck_col[0], "No entries")
                if puck_col
                else "No entries"
            )
            st.info(
                val_puck
                if pd.notna(val_puck) and str(val_puck) != "nan"
                else "No entries"
            )

        with col_no_puck:
            st.subheader("🛡️ Game Without Puck")
            val_no_puck = (
                p.get(no_puck_col[0], "No entries")
                if no_puck_col
                else "No entries"
            )
            st.info(
                val_no_puck
                if pd.notna(val_no_puck) and str(val_no_puck) != "nan"
                else "No entries"
            )

        st.divider()

        st.subheader("💬 Feedback, Challenges & Season Goal")

        col_left, col_right = st.columns(2)

        with col_left:
            st.write("**Handling Challenges in Practices/Games:**")
            st.write(
                f"> {p.get('Hur hanterar du utmaningar vid träningar/match', '-')}"
            )

            st.write("**Receptiveness to Feedback:**")
            st.write(
                f"> {p.get('Hur mottaglig är du för feedback?', '-')}"
            )

            st.write("**Handling Feedback (Positive & Negative):**")
            st.write(
                f"> {p.get('Hur hanterar du feedback (negativ och positiv)?', '-')}"
            )

        with col_right:
            st.write("**Season Goal:**")
            goal_val = p.get("Vad är ditt mål med den här säsongen?", "-")
            st.success(
                goal_val
                if pd.notna(goal_val) and str(goal_val) != "nan"
                else "No goal set."
            )

    else:
        st.warning(f"Data for player '{selected_player}' was not found.")
else:
    st.info("Please select a player from the sidebar.")
