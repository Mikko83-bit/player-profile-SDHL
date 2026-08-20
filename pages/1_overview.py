import os
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

        st.title(f"👤 {selected_player} — Overview")

        # Asettelu: 1 osa kuvalle, 2 osaa tiedoille, 2 osaa tutkakaaviolle
        col_img, col_info, col_radar = st.columns([1, 2, 2])

        # --- 1. PELAAJAKUVA ---
        with col_img:
            # Muutetaan nimi tiedostomuotoon (esim. "Maja Nylen" -> "Maja_Nylen")
            formatted_name = selected_player.replace(" ", "_")
            
            # Etsitään sopivaa kuvaformaattia
            img_found = False
            for ext in [".png", ".jpg", ".jpeg", ".PNG", ".JPG"]:
                img_path = os.path.join("images", f"{formatted_name}{ext}")
                if os.path.exists(img_path):
                    st.image(img_path, use_container_width=True)
                    img_found = True
                    break
            
            # Jos kuvaa ei löydy, näytetään paikkamerkki
            if not img_found:
                st.image(
                    "https://via.placeholder.com/200x250.png?text=No+Image",
                    use_container_width=True,
                )

        # --- 2. PERUSTIEDOT ---
        with col_info:
            st.subheader("PLAYER INFORMATION")
            st.write(f"**Name:** {selected_player}")
            st.write(f"**Number:** {p.get('Nummer?', '-')}")
            st.write(f"**Team:** {p.get(team_col, '-')}")

            st.divider()
            st.subheader("🎯 Season Goal")
            st.success(
                p.get(
                    "Vad är ditt mål med den här säsongen?",
                    "No goal defined.",
                )
            )

        # --- 3. TUTKAKAAVIO ---
        with col_radar:
            st.subheader("📊 Self-Assessment Radar")
            overview_cats = {
                "Skating": "Hur är din skridskoåkning?",
                "Shooting": "Hur är ditt skott?",
                "Puck Control": "Hur är din puckföring/puckkontroll?",
                "Hockey Sense": "Hur är din spelförståelse?",
                "Passing": "Hur är din kvalitet i passning/mottagning?",
                "Defense": "Hur är din kvalitet i försvarsspelet?",
                "Offense": "Hur är din kvalitet i anfallsspelet?",
                "Physical Play": "Hur är din kvalitet i det fysiska spelet?",
                "Team System": "Hur är din förståelse för spelsystemet?",
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
        st.warning(f"Data for player '{selected_player}' was not found.")
else:
    st.info("Please select a player from the sidebar.")
