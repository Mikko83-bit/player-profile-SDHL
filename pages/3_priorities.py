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

        # --- 1. Game With Puck / Without Puck ---
        col_puck, col_no_puck = st.columns(2)

        puck_col = [
            c for c in df.columns
            if "skriv ner 3 konkreta moment i spelet med puck" in str(c).lower()
        ]
        no_puck_col = [
            c for c in df.columns
            if "skriv ner 3 konkreta moment i spelet utan puck" in str(c).lower()
        ]

        with col_puck:
            st.subheader("🏒 Game With Puck")
            val_puck = p.get(puck_col[0], "No entries") if puck_col else "No entries"
            st.info(
                val_puck
                if pd.notna(val_puck) and str(val_puck).strip() not in ["nan", ""]
                else "No entries"
            )

        with col_no_puck:
            st.subheader("🛡️ Game Without Puck")
            val_no_puck = p.get(no_puck_col[0], "No entries") if no_puck_col else "No entries"
            st.info(
                val_no_puck
                if pd.notna(val_no_puck) and str(val_no_puck).strip() not in ["nan", ""]
                else "No entries"
            )

        st.divider()

        # --- 2. Strengths & Areas to Develop (Tapa 1: Haetaan sarakkeista AT ja AU) ---
        st.subheader("⭐ Strengths & Areas to Develop")
        col_good, col_dev = st.columns(2)

        # Excelin sarake AT on indeksi 45 (A=0, Z=25, AA=26, AT=45)
        # Oletetaan "Vad gör du bra?" = AT (44) ja "Vad behöver du utveckla?" = AU (45)
        COL_AT_INDEX = 44

        val_good = p.iloc[COL_AT_INDEX] if len(p) > COL_AT_INDEX else "-"
        val_dev = p.iloc[COL_AT_INDEX + 1] if len(p) > (COL_AT_INDEX + 1) else "-"

        with col_good:
            st.write("**What You Do Well:**")
            st.write(
                f"> {val_good if pd.notna(val_good) and str(val_good).strip() not in ['nan', ''] else '-'}"
            )

        with col_dev:
            st.write("**What You Need to Develop:**")
            st.write(
                f"> {val_dev if pd.notna(val_dev) and str(val_dev).strip() not in ['nan', ''] else '-'}"
            )

        st.divider()

        # --- 3. Feedback, Challenges & Season Goal ---
        st.subheader("💬 Feedback, Challenges & Season Goal")

        col_left, col_right = st.columns(2)

        # Etsitään muut sarakkeet turvallisesti hakusanoilla
        utmaning_col = [c for c in df.columns if "utmaningar" in str(c).lower()]
        mottaglig_col = [c for c in df.columns if "mottaglig" in str(c).lower()]
        feedback_col = [c for c in df.columns if "negativ och positiv" in str(c).lower()]
        goal_col = [c for c in df.columns if "mål med den här säsongen" in str(c).lower()]

        with col_left:
            st.write("**Handling Challenges in Practices/Games:**")
            val_utmaning = p.get(utmaning_col[0], "-") if utmaning_col else "-"
            st.write(
                f"> {val_utmaning if pd.notna(val_utmaning) and str(val_utmaning).strip() not in ['nan', ''] else '-'}"
            )

            st.write("**Receptiveness to Feedback:**")
            val_mottaglig = p.get(mottaglig_col[0], "-") if mottaglig_col else "-"
            st.write(
                f"> {val_mottaglig if pd.notna(val_mottaglig) and str(val_mottaglig).strip() not in ['nan', ''] else '-'}"
            )

            st.write("**Handling Feedback (Positive & Negative):**")
            val_feedback = p.get(feedback_col[0], "-") if feedback_col else "-"
            st.write(
                f"> {val_feedback if pd.notna(val_feedback) and str(val_feedback).strip() not in ['nan', ''] else '-'}"
            )

        with col_right:
            st.write("**Season Goal:**")
            goal_val = p.get(goal_col[0], "No goal set.") if goal_col else "No goal set."
            st.success(
                goal_val
                if pd.notna(goal_val) and str(goal_val).strip() not in ["nan", ""]
                else "No goal set."
            )

    else:
        st.warning(f"Data for player '{selected_player}' was not found.")
else:
    st.info("Please select a player from the sidebar.")
