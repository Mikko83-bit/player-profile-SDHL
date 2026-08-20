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
        ["🏒 Yksilölliset Taidot", "💪 Arjen Standardit & Mielentila"]
    )

    with tab1:
        st.subheader("INDIVIDUAL SKILLS & GAME PERFORMANCE (1–10)")
        skills = {
            "Luistelu": "How would you rate your skating?",
            "Laukaus": "How would you rate your shot?",
            "Kiekonhallinta": "How would you rate your puck handling/control?",
            "Syöttäminen": "How would you rate your passing and receiving ability?",
            "Peliäly": "How would you rate your hockey sense?",
            "Puolustus": "How would you rate your defensive play?",
            "Hyökkäys": "How is your offensive play?",
            "Kamppailu": "How is your physical play?",
            "Pelitapa": "How is your understanding of the team system?",
        }

        col1, col2 = st.columns(2)
        for idx, (label, col_name) in enumerate(skills.items()):
            target_col = col1 if idx % 2 == 0 else col2
            with target_col:
                val = get_clean_val(p.get(col_name, 5))
                k = f"skills_{selected_player}_{label}"
                st.slider(f"**{label}**", 1, 10, val, key=k)
                st.write("---")

    with tab2:
        st.subheader("HOCKEY CHARACTER & DAILY STANDARDS")
        char_areas = [
            ("Työmoraali harjoituksissa", "Work ethic practices"),
            ("Työmoraali peleissä", "Work ethic games"),
            ("Valmistautuminen harjoituksiin", "Preparations practices"),
            ("Valmistautuminen peleihin", "Preparations games"),
            ("Haasteiden käsittely", "How do you handle challenges?"),
            (
                "Palautteen vastaanotto",
                "How do you handle feedback (both positive and negative)?",
            ),
        ]

        col1, col2 = st.columns(2)
        for idx, (label, col_name) in enumerate(char_areas):
            target_col = col1 if idx % 2 == 0 else col2
            with target_col:
                val = get_clean_val(p.get(col_name, 8))
                k = f"char_{selected_player}_{label}"
                st.slider(f"**{label}**", 1, 10, val, key=k)
                st.info(f"**Kirjaus:** {p.get(col_name, '-')}")
else:
    st.warning("Valitse pelaaja vasemmasta sivupalkista.")
