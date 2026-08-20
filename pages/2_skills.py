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

    st.caption(f"💪 **Vahvuudet:** {p.get(str_col, 'Ei kirjauksia')}")
    st.caption(f"🎯 **Kehitettävää:** {p.get(dev_col, 'Ei kirjauksia')}")
    st.write("---")


if df is not None and selected_player:
    match = df[df[name_col].astype(str).str.strip() == str(selected_player)]

    if not match.empty:
        p = match.iloc[0]

        st.title(f"📊 {selected_player} — Taidot & Peliesitys")

        tab1, tab2, tab3 = st.tabs(
            [
                "🛠️ Tekniset Taidot",
                "🧠 Taktiset Taidot & Peliäly",
                "💪 Arjen Standardit",
            ]
        )

        with tab1:
            st.subheader("TECHNICAL SKILLS")
            tech_skills = [
                (
                    "Luistelu",
                    "Hur är din skridskoåkning?",
                    "Vad är du bra på?",
                    "Vad behöver du utveckla?",
                ),
                (
                    "Laukaus",
                    "Hur är ditt skott?",
                    "Vad är du bra på? 2",
                    "Vad behöver du utveckla? 2",
                ),
                (
                    "Kiekonhallinta",
                    "Hur är din puckföring/puckkontroll?",
                    "Vad är du bra på? 3",
                    "Vad behöver du utveckla? 3",
                ),
                (
                    "Syöttäminen",
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
                    "Peliäly",
                    "Hur är din spelförståelse?",
                    "Vad är du bra på? 4",
                    "Vad behöver du utveckla? 4",
                ),
                (
                    "Puolustus",
                    "Hur är din kvalitet i försvarsspelet?",
                    "Vad är du bra på? 6",
                    "Vad behöver du utveckla? 6",
                ),
                (
                    "Hyökkäys",
                    "Hur är din kvalitet i anfallsspelet?",
                    "Vad är jag bra på?",
                    "Vad behöver du utveckla? 7",
                ),
                (
                    "Kamppailu",
                    "Hur är din kvalitet i det fysiska spelet?",
                    "Vad är jag bra på? 2",
                    "Vad behöver du utveckla? 8",
                ),
                (
                    "Pelitapa",
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
                    "Työmoraali harjoituksissa",
                    "Hur är din arbetsmoral vid träning?",
                    "Vad gör du bra?",
                    "Vad behöver du utveckla? 9",
                ),
                (
                    "Työmoraali peleissä",
                    "Hur är din arbetsmoral vid match?",
                    "Vad gör du bra? 2",
                    "Vad behöver du utveckla? 10",
                ),
                (
                    "Valmistautuminen harjoituksiin",
                    "Hur är dina förberedelser runt träning?",
                    "Vad gör du bra? 3",
                    "Vad behöver du utveckla? 11",
                ),
                (
                    "Valmistautuminen peleihin",
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
        st.warning(f"Pelaajan '{selected_player}' tietoja ei löytynyt.")
else:
    st.info("Valitse pelaaja sivupalkista.")
