import pandas as pd
import streamlit as st

df = st.session_state.get("df")
selected_player = st.session_state.get("selected_player")
name_col = st.session_state.get("name_col", "Name")


def get_clean_val(val, default=5):
    try:
        clean = int(round(float(val))) if pd.notna(val) else default
        return max(1, min(10, clean))
    except (ValueError, TypeError):
        return default


def render_skill_block(label, score_col, str_col, dev_col, p, player_name):
    val = get_clean_val(p.get(score_col, 5))
    st.slider(
        f"**{label}**",
        1,
        10,
        val,
        key=f"sk_{player_name}_{label}_{score_col[:10]}",
    )

    st.caption(f"💪 **Strengths:** {p.get(str_col, 'No entries')}")
    st.caption(f"🎯 **To Develop:** {p.get(dev_col, 'No entries')}")
    st.write("---")


if df is not None and selected_player:
    match = df[df[name_col].astype(str).str.strip() == str(selected_player)]

    if not match.empty:
        p = match.iloc[0]

        st.title(f"📊 {selected_player} — Skills & Performance")

        tab1, tab2, tab3 = st.tabs(
            [
                "🛠️ Technical Skills",
                "🧠 Tactical & Hockey Sense",
                "💪 Daily Standards",
            ]
        )

        with tab1:
            st.subheader("TECHNICAL SKILLS")
            tech_skills = [
                (
                    "Skating",
                    "Hur är din skridskoåkning?",
                    "Vad är du bra på?",
                    "Vad behöver du utveckla?",
                ),
                (
                    "Shooting",
                    "Hur är ditt skott?",
                    "Vad är du bra på? 2",
                    "Vad behöver du utveckla? 2",
                ),
                (
                    "Puck Handling",
                    "Hur är din puckföring/puckkontroll?",
                    "Vad är du bra på? 3",
                    "Vad behöver du utveckla? 3",
                ),
                (
                    "Passing & Receiving",
                    "Hur är din kvalitet i passning/mottagning?",
                    "Vad är du bra på? 5",
                    "Vad behöver du utveckla? 5",
                ),
            ]

            col1, col2 = st.columns(2)
            for idx, (label, score_col, str_col, dev_col) in enumerate(
                tech_skills
            ):
                target_col = col1 if idx % 2 == 0 else col2
                with target_col:
                    render_skill_block(
                        label, score_col, str_col, dev_col, p, selected_player
                    )

        with tab2:
            st.subheader("TACTICAL SKILLS & GAME UNDERSTANDING")
            tactical_skills = [
                (
                    "Hockey Sense",
                    "Hur är din spelförståelse?",
                    "Vad är du bra på? 4",
                    "Vad behöver du utveckla? 4",
                ),
                (
                    "Defensive Play",
                    "Hur är din kvalitet i försvarsspelet?",
                    "Vad är du bra på? 6",
                    "Vad behöver du utveckla? 6",
                ),
                (
                    "Offensive Play",
                    "Hur är din kvalitet i anfallsspelet?",
                    "Vad är jag bra på?",
                    "Vad behöver du utveckla? 7",
                ),
                (
                    "Physical Play",
                    "Hur är din kvalitet i det fysiska spelet?",
                    "Vad är jag bra på? 2",
                    "Vad behöver du utveckla? 8",
                ),
                (
                    "Understanding System",
                    "Hur är din förståelse för spelsystemet?",
                    "Vilka moment hanterar jag bra?",
                    "Vilka moment behöver jag utveckla?",
                ),
            ]

            col1, col2 = st.columns(2)
            for idx, (label, score_col, str_col, dev_col) in enumerate(
                tactical_skills
            ):
                target_col = col1 if idx % 2 == 0 else col2
                with target_col:
                    render_skill_block(
                        label, score_col, str_col, dev_col, p, selected_player
                    )

        with tab3:
            st.subheader("DAILY STANDARDS & PREPARATIONS")
            char_map = [
                (
                    "Work Ethic (Practice)",
                    "Hur är din arbetsmoral vid träning?",
                    "Vad gör du bra?",
                    "Vad behöver du utveckla? 9",
                ),
                (
                    "Work Ethic (Games)",
                    "Hur är din arbetsmoral vid match?",
                    "Vad gör du bra? 2",
                    "Vad behöver du utveckla? 10",
                ),
                (
                    "Preparation (Practice)",
                    "Hur är dina förberedelser runt träning?",
                    "Vad gör du bra? 3",
                    "Vad behöver du utveckla? 11",
                ),
                (
                    "Preparation (Games)",
                    "Hur är dina förberedelser runt match?",
                    "Vad gör du bra? 4",
                    "Vad behöver du utveckla? 12",
                ),
            ]

            col1, col2 = st.columns(2)
            for idx, (label, score_col, str_col, dev_col) in enumerate(
                char_map
            ):
                target_col = col1 if idx % 2 == 0 else col2
                with target_col:
                    render_skill_block(
                        label, score_col, str_col, dev_col, p, selected_player
                    )
    else:
        st.warning(f"Data for player '{selected_player}' was not found.")
else:
    st.info("Please select a player from the sidebar.")
