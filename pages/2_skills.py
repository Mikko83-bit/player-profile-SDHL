import pandas as pd
import streamlit as st

df = st.session_state.get("df")
selected_player = st.session_state.get("selected_player")


def get_clean_val(val, default=5):
    try:
        clean = int(round(float(val))) if pd.notna(val) else default
        return max(1, min(10, clean))
    except (ValueError, TypeError):
        return default


def render_skill_block(label, score_col, str_num, dev_num, p, player_name):
    val = get_clean_val(p.get(score_col, 5))
    st.slider(
        f"**{label}**", 1, 10, val, key=f"sk_{player_name}_{label}_{str_num}"
    )

    str_col = f"What are your strengths?{str_num}".strip()
    dev_col = f"What do you need to develop?{dev_num}".strip()

    st.caption(f"💪 **Vahvuudet:** {p.get(str_col, 'Ei kirjauksia')}")
    st.caption(f"🎯 **Kehitettävää:** {p.get(dev_col, 'Ei kirjauksia')}")
    st.write("---")


if df is not None and selected_player:
    name_col = "Name?" if "Name?" in df.columns else df.columns[0]
    match = df[df[name_col].astype(str).str.strip() == str(selected_player)]

    if not match.empty:
        p = match.iloc[0]

        st.title(f"📊 {selected_player} — Taidot & Peliesitys")

        # Kolme eri välilehteä
        tab1, tab2, tab3 = st.tabs(
            [
                "🛠️ Tekniset Taidot",
                "🧠 Taktiset Taidot & Peliäly",
                "💪 Arjen Standardit",
            ]
        )

        # 1. TEKNISET TAIDOT
        with tab1:
            st.subheader("TECHNICAL SKILLS")
            tech_skills = [
                ("Luistelu", "How would you rate your skating?", "", ""),
                ("Laukaus", "How would you rate your shot?", " 2", " 2"),
                (
                    "Kiekonhallinta",
                    "How would you rate your puck handling/control",
                    " 3",
                    " 3",
                ),
                (
                    "Syöttäminen",
                    "How would you rate your passing and receiving",
                    " 5",
                    " 5",
                ),
            ]

            col1, col2 = st.columns(2)
            for idx, (label, score_col, str_num, dev_num) in enumerate(
                tech_skills
            ):
                target_col = col1 if idx % 2 == 0 else col2
                with target_col:
                    render_skill_block(
                        label, score_col, str_num, dev_num, p, selected_player
                    )

        # 2. TAKTISET TAIDOT
        with tab2:
            st.subheader("TACTICAL SKILLS & GAME UNDERSTANDING")
            tactical_skills = [
                (
                    "Peliäly",
                    "How would you rate your hockey sense?",
                    " 4",
                    " 4",
                ),
                (
                    "Puolustus",
                    "How would you rate your defensive play?",
                    " 6",
                    " 6",
                ),
                ("Hyökkäys", "How is your offensive play?", " 7", " 7"),
                ("Kamppailu", "How is your physical play?", " 8", " 8"),
                (
                    "Pelitapa",
                    "How is your understanding of the team system",
                    "",
                    "",
                ),
            ]

            col1, col2 = st.columns(2)
            for idx, (label, score_col, str_num, dev_num) in enumerate(
                tactical_skills
            ):
                target_col = col1 if idx % 2 == 0 else col2
                with target_col:
                    render_skill_block(
                        label, score_col, str_num, dev_num, p, selected_player
                    )

        # 3. ARJEN STANDARDIT
        with tab3:
            st.subheader("DAILY STANDARDS & PREPARATIONS")
            char_map = [
                (
                    "Työmoraali harjoituksissa",
                    "How is your work ethic during practice?",
                    " 9",
                    " 9",
                ),
                (
                    "Työmoraali peleissä",
                    "How is your work ethic during games?",
                    " 10",
                    " 10",
                ),
                (
                    "Valmistautuminen harjoituksiin",
                    "How are your preparations around practice?",
                    " 11",
                    " 11",
                ),
                (
                    "Valmistautuminen peleihin",
                    "How are your preparations around games?",
                    " 12",
                    " 12",
                ),
            ]

            col1, col2 = st.columns(2)
            for idx, (label, score_col, str_num, dev_num) in enumerate(
                char_map
            ):
                target_col = col1 if idx % 2 == 0 else col2
                with target_col:
                    render_skill_block(
                        label, score_col, str_num, dev_num, p, selected_player
                    )
    else:
        st.warning(f"Pelaajan '{selected_player}' tietoja ei löytynyt.")
else:
    st.info("Valitse pelaaja sivupalkista.")
