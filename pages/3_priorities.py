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

        val_puck = p.iloc[29] if len(p) > 29 else "No entries"
        val_no_puck = p.iloc[30] if len(p) > 30 else "No entries"

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

        # --- 2. Handling Challenges (Haasteiden käsittely) ---
        st.subheader("⚡ Handling Challenges")

        val_challenge_rating = p.iloc[43] if len(p) > 43 else "-"
        val_challenge_good = p.iloc[44] if len(p) > 44 else "-"
        val_challenge_dev = p.iloc[45] if len(p) > 45 else "-"

        st.write(f"**Challenge Handling Rating (1-10):** {val_challenge_rating}")

        col_c_good, col_c_dev = st.columns(2)

        with col_c_good:
            st.write("**What You Do Well:**")
            st.write(
                f"> {val_challenge_good if pd.notna(val_challenge_good) and str(val_challenge_good).strip() not in ['nan', ''] else '-'}"
            )

        with col_c_dev:
            st.write("**What You Need to Develop:**")
            st.write(
                f"> {val_challenge_dev if pd.notna(val_challenge_dev) and str(val_challenge_dev).strip() not in ['nan', ''] else '-'}"
            )

        st.divider()

        # --- 3. Feedback & Season Goal (Palautteen käsittely ja kauden tavoite) ---
        st.subheader("💬 Feedback & Season Goal")

        col_left, col_right = st.columns(2)

        val_mottaglig = p.iloc[46] if len(p) > 46 else "-"
        val_feedback = p.iloc[47] if len(p) > 47 else "-"
        val_feedback_extra = p.iloc[49] if len(p) > 49 else "-"  # Kolumn 49 lisätieto
        goal_val = p.iloc[48] if len(p) > 48 else "No goal set."

        with col_left:
            st.write("**Receptiveness to Feedback (1-10):**")
            st.write(
                f"> {val_mottaglig if pd.notna(val_mottaglig) and str(val_mottaglig).strip() not in ['nan', ''] else '-'}"
            )

            st.write("**Handling Feedback (Positive & Negative):**")
            st.write(
                f"> {val_feedback if pd.notna(val_feedback) and str(val_feedback).strip() not in ['nan', ''] else '-'}"
            )

            if pd.notna(val_feedback_extra) and str(val_feedback_extra).strip() not in ["nan", ""]:
                st.write("**Additional Feedback Notes:**")
                st.write(f"> {val_feedback_extra}")

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
