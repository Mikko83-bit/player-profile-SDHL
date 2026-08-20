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


if df is not None and selected_player:
    p = df[df[df.columns[0]] == selected_player].iloc[0]

    st.title(f"📊 {selected_player} — Taidot & Peliesitys")

    tab1, tab2 = st.tabs(
        ["🏒 Yksilölliset Taidot & Peliesitys", "💪 Arjen Standardit"]
    )

    with tab1:
        st.subheader("INDIVIDUAL SKILLS & GAME PERFORMANCE")

        # Määritellään taitoluokat ja niitä vastaavat sanalliset kentät Excelistä
        skills_map = [
            ("Luistelu", "How would you rate your skating?", "", ""),
            ("Laukaus", "How would you rate your shot?", " 2", " 2"),
            (
                "Kiekonhallinta",
                "How would you rate your puck handling/control",
                " 3",
                " 3",
            ),
            (
                "Peliäly",
                "How would you rate your hockey sense?",
                " 4",
                " 4",
            ),
            (
                "Syöttäminen",
                "How would you rate your passing and receiving",
                " 5",
                " 5",
            ),
            (
                "Puolustus",
                "How would you rate your defensive play?",
                " 6",
                " 6",
            ),
            ("Hyökkäys", "How is your offensive play?", " 7", " 7"),
            ("Kamppailu", "How is your physical play?", " 8", " 8"),
        ]

        col1, col2 = st.columns(2)
        for idx, (label, score_col, str_num, dev_num) in enumerate(skills_map):
            target_col = col1 if idx % 2 == 0 else col2
            with target_col:
                val = get_clean_val(p.get(score_col, 5))
                st.slider(
                    f"**{label}**",
                    1,
                    10,
                    val,
                    key=f"sk_{selected_player}_{label}",
                )

                str_col = f"What are your strengths?{str_num}".strip()
                dev_col = f"What do you need to develop?{dev_num}".strip()

                st.caption(
                    f"💪 **Vahvuudet:** {p.get(str_col, 'Ei kirjauksia')}"
                )
                st.caption(
                    f"🎯 **Kehitettävää:** {p.get(dev_col, 'Ei kirjauksia')}"
                )
                st.write("---")

    with tab2:
        st.subheader("WORK ETHIC & PREPARATIONS")

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
        for idx, (label, score_col, str_num, dev_num) in enumerate(char_map):
            target_col = col1 if idx % 2 == 0 else col2
            with target_col:
                val = get_clean_val(p.get(score_col, 8))
                st.slider(
                    f"**{label}**",
                    1,
                    10,
                    val,
                    key=f"ch_{selected_player}_{label}",
                )

                str_col = f"What are your strengths?{str_num}".strip()
                dev_col = f"What do you need to develop?{dev_num}".strip()

                st.caption(
                    f"💪 **Vahvuudet:** {p.get(str_col, 'Ei kirjauksia')}"
                )
                st.caption(
                    f"🎯 **Kehitettävää:** {p.get(dev_col, 'Ei kirjauksia')}"
                )
                st.write("---")
else:
    st.warning("Valitse pelaaja vasemmasta sivupalkista.")
