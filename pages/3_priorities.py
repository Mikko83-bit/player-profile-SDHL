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

        # --- 1. Game With Puck / Without Puck (Kolumner 30 & 31) ---
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

        # --- 2. Handling Challenges & Strengths/Areas to Develop ---
        st.subheader("⚡ Handling Challenges & Development")

        # Index 44 = Hur hanterar du utmaningar vid träningar/matcher? (Siffra)
        # Index 45 = Vad gör du bra? (Svar 1)
        # Index 46 = Vad behöver du utveckla? (Svar 2)
        val_challenge_rating = p.iloc[44] if len(p) > 44 else "-"
        val_good = p.iloc[45] if len(p) > 45 else "-"
        val_dev = p.iloc[46] if len(p) > 46 else "-"

        st.write(f"**Challenge Rating:** {val_challenge_rating}")

        col_good, col_dev = st.columns(2)

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

        # --- 3. Feedback & Season Goal ---
        st.subheader("💬 Feedback & Season Goal")

        col_left, col_right = st.columns(2)

        # Hämta övriga kolumner dynamiskt eller via index
        mottaglig_col = [c for c in df.columns if "mottaglig" in str(c).lower()]
        feedback_col = [c for c in df.columns if "negativ och positiv" in str(c).lower()]
        goal_col = [c for c in df.columns if "mål med den här säsongen" in str(c).lower()]

        with col_left:
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
