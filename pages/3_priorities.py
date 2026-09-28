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

        # --- 1. Game With Puck / Without Puck (Sarakkeet 30 ja 31) ---
        col_puck, col_no_puck = st.columns(2)

        val_puck = p.iloc[30] if len(p) > 30 else "No entries"
        val_no_puck = p.iloc[31] if len(p) > 31 else "No entries"

        with col_puck:
            st.subheader("🏒 Game With Puck")
            st.info(
                val_puck
                if pd.notna(val_puck) and str(val_puck).strip() not in ["nan", ""]
                else "No entries"
            )

        with col_no_puck:
            st.subheader("🛡️ Game Without Puck")
            st.info(
                val_no_puck
                if pd.notna(val_no_puck) and str(val_no_puck).strip() not in ["nan", ""]
                else "No entries"
            )

        st.divider()

        # --- 2. Strengths & Areas to Develop ---
        # Käytetään sarakkeita 42 ("Vad gör du bra? 4") ja 43 ("Vad behöver du utveckla? 12")
        # (Jos haluat ottaa mieluummin sarakkeet 33 ja 34, vaihda indeksit: 33 ja 34)
        st.subheader("⭐ Strengths & Areas to Develop")
        col_good, col_dev = st.columns(2)

        val_good = p.iloc[42] if len(p) > 42 else "-"
        val_dev = p.iloc[43] if len(p) > 43 else "-"

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

        # --- 3. Feedback, Challenges & Season Goal (Sarakkeet 44, 45, 46, 47) ---
        st.subheader("💬 Feedback, Challenges & Season Goal")

        col_left, col_right = st.columns(2)

        val_utmaning = p.iloc[44] if len(p) > 44 else "-"
        val_mottaglig = p.iloc[45] if len(p) > 45 else "-"
        val_feedback = p.iloc[46] if len(p) > 46 else "-"
        goal_val = p.iloc[47] if len(p) > 47 else "No goal set."

        with col_left:
            st.write("**Handling Challenges in Practices/Games:**")
            st.write(
                f"> {val_utmaning if pd.notna(val_utmaning) and str(val_utmaning).strip() not in ['nan', ''] else '-'}"
            )

            st.write("**Receptiveness to Feedback:**")
            st.write(
                f"> {val_mottaglig if pd.notna(val_mottaglig) and str(val_mottaglig).strip() not in ['nan', ''] else '-'}"
            )

            st.write("**Handling Feedback (Positive & Negative):**")
            st.write(
                f"> {val_feedback if pd.notna(val_feedback) and str(val_feedback).strip() not in ['nan', ''] else '-'}"
            )

        with col_right:
            st.write("**Season Goal:**")
            st.success(
                goal_val
                if pd.notna(goal_val) and str(goal_val).strip() not in ["nan", ""]
                else "No goal set."
            )

    else:
        st.warning(f"Data for player '{selected_player}' was not found.")
else:
    st.info("Please select a player from the sidebar.")
