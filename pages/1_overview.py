import pandas as pd
import plotly.express as px
import streamlit as st

df = st.session_state.get("df")
selected_player = st.session_state.get("selected_player")
name_col = st.session_state.get("name_col", "Name")
team_col = st.session_state.get("team_col", "TEAM")

if df is not None and selected_player:
    match = df[df[name_col].astype(str).str.strip() == str(selected_player)]

    if not match.empty:
        p = match.iloc[0]

        st.title(f"👤 {selected_player} — Perustiedot & Yleiskatsaus")

        col_info, col_radar = st.columns([1, 1])

        with col_info:
            st.subheader("PLAYER INFORMATION")
            st.write(f"**Nimi:** {selected_player}")
            st.write(f"**Numero:** {p.get('Nummer?', '-')}")
            st.write(f"**Joukkue:** {p.get(team_col, '-')}")

            st.divider()
            st.subheader("🎯 Kauden tavoite")
            st.success(
                p.get(
                    "Vad är ditt mål med den här säsongen?",
                    "Ei määritelty kauden tavoitetta.",
                )
            )

        with col_radar:
            st.subheader("📊 Self-Assessment Overview")
            overview_cats = {
                "Luistelu": "Hur är din skridskoåkning?",
                "Laukaus": "Hur är ditt skott?",
                "Kiekonhallinta": "Hur är din puckföring/puckkontroll?",
                "Peliäly": "Hur är din spelförståelse?",
                "Syöttäminen": "Hur är din kvalitet i passning/mottagning?",
                "Puolustus": "Hur är din kvalitet i försvarsspelet?",
                "Hyökkäys": "Hur är din kvalitet i anfallsspelet?",
                "Kamppailu": "Hur är din kvalitet i det fysiska spelet?",
                "Pelitapa": "Hur är din förståelse för spelsystemet?",
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
