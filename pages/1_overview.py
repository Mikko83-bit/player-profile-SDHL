import pandas as pd
import plotly.express as px
import streamlit as st

df = st.session_state.get("df")
selected_player = st.session_state.get("selected_player")

if df is not None and selected_player:
    name_col = "Name?" if "Name?" in df.columns else df.columns[0]
    match = df[df[name_col].astype(str).str.strip() == str(selected_player)]

    if not match.empty:
        p = match.iloc[0]

        st.title(f"👤 {selected_player} — Perustiedot & Yleiskatsaus")

        col_info, col_radar = st.columns([1, 1])

        with col_info:
            st.subheader("PLAYER INFORMATION")
            st.write(f"**Nimi:** {selected_player}")
            st.write(f"**Pelipaikka:** {p.get('Position', '-')}")
            st.write(f"**Joukkue:** {p.get('Team', 'Luleå Hockey / MSK')}")
            st.write(f"**Syntymävuosi:** {p.get('Birth Year', '-')}")
            st.write(f"**Kätisyys:** {p.get('Shoots', '-')}")

            st.divider()
            st.subheader("🎯 Kauden tavoite")
            st.success(
                p.get(
                    "What is your goal for this season?",
                    "Ei määritelty kauden tavoitetta.",
                )
            )

        with col_radar:
            st.subheader("📊 Self-Assessment Overview")
            overview_cats = {
                "Luistelu": "How would you rate your skating?",
                "Laukaus": "How would you rate your shot?",
                "Kiekonhallinta": "How would you rate your puck handling/control",
                "Peliäly": "How would you rate your hockey sense?",
                "Syöttäminen": "How would you rate your passing and receiving",
                "Puolustus": "How would you rate your defensive play?",
                "Hyökkäys": "How is your offensive play?",
                "Kamppailu": "How is your physical play?",
                "Pelitapa": "How is your understanding of the team system",
            }

            scores = []
            labels = []
            for lbl, col in overview_cats.items():
                val = p.get(col, 5)
                try:
                    clean_val = (
                        int(round(float(val))) if pd.notna(val) else 5
                    )
                except (ValueError, TypeError):
                    clean_val = 5
                scores.append(clean_val)
                labels.append(lbl)

            df_radar = pd.DataFrame(dict(r=scores, theta=labels))
            fig = px.line_polar(
                df_radar,
                r="r",
                theta="theta",
                line_close=True,
                range_r=[0, 10],
            )
            fig.update_traces(fill="toself", line_color="#E30613")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"Pelaajan '{selected_player}' tietoja ei löytynyt.")
else:
    st.info("Valitse pelaaja sivupalkista.")
