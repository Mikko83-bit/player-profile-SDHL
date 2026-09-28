import os
import pandas as pd
import plotly.graph_objects as go
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

        col_img, col_info, col_radar = st.columns([1, 2, 2.5])

        # --- 1. PELAAJAKUVA ---
        with col_img:
            formatted_name = selected_player.replace(" ", "_")
            img_found = False
            for ext in [".png", ".jpg", ".jpeg", ".PNG", ".JPG"]:
                img_path = os.path.join("images", f"{formatted_name}{ext}")
                if os.path.exists(img_path):
                    st.image(img_path, use_container_width=True)
                    img_found = True
                    break

            if not img_found:
                st.image(
                    "https://via.placeholder.com/200x250.png?text=No+Image",
                    use_container_width=True,
                )

        # --- 2. PERUSTIEDOT ---
        with col_info:
            st.subheader("PLAYER INFORMATION")
            st.write(f"**Name:** {selected_player}")

            # Haetaan numero turvallisesti
            num_val = (
                p.iloc[1]
                if len(p) > 1 and pd.notna(p.iloc[1])
                else p.get("Nummer?", "-")
            )
            st.write(f"**Number:** {num_val}")
            st.write(f"**Team:** {p.get(team_col, 'Luleå U19D')}")

            st.divider()
            st.subheader("🎯 Season Goal")

            # Kauden tavoite kyselystä (sarake 46/47)
            goal_val = (
                p.iloc[46]
                if len(p) > 46 and pd.notna(p.iloc[46])
                else "No goal defined."
            )
            st.success(goal_val)

        # --- 3. TUTKAKAAVIO VERTAILULLA (U19D) ---
        with col_radar:
            st.subheader("📊 Self-Assessment Radar")

            # Määritetään osa-alueet ja niitä vastaavat sarakeindeksit
            categories = {
                "Skating": 2,
                "Shooting": 5,
                "Puck Control": 8,
                "Hockey Sense": 11,
                "Passing": 14,
                "Defense": 17,
                "Offense": 20,
                "Physical Play": 23,
                "Team System": 26,
            }

            labels = list(categories.keys())
            player_scores = []
            team_averages = []

            for cat_name, col_idx in categories.items():
                # 1. Pelaajan oma arvo
                val = p.iloc[col_idx] if len(p) > col_idx else None
                try:
                    p_score = float(val) if pd.notna(val) else 5.0
                except (ValueError, TypeError):
                    p_score = 5.0
                player_scores.append(p_score)

                # 2. U19D Joukkueen keskiarvo sarakeindeksistä
                try:
                    col_data = pd.to_numeric(
                        df.iloc[:, col_idx], errors="coerce"
                    )
                    team_avg = col_data.mean()
                    if pd.isna(team_avg):
                        team_avg = 5.0
                except Exception:
                    team_avg = 5.0
                team_averages.append(round(team_avg, 2))

            # Suljetaan ympyrä Plotly-tutkakaaviota varten
            labels_closed = labels + [labels[0]]
            player_scores_closed = player_scores + [player_scores[0]]
            team_averages_closed = team_averages + [team_averages[0]]

            # Luodaan Plotly-graafi kahdella eri tasolla
            fig = go.Figure()

            # Joukkueen keskiarvo (U19D) - Katkoviiva / Harmaa alue
            fig.add_trace(
                go.Scatterpolar(
                    r=team_averages_closed,
                    theta=labels_closed,
                    fill="toself",
                    name="U19D Average",
                    line=dict(color="#888888", dash="dash"),
                    fillcolor="rgba(180, 180, 180, 0.2)",
                )
            )

            # Pelaajan omat pisteet - Punainen
            fig.add_trace(
                go.Scatterpolar(
                    r=player_scores_closed,
                    theta=labels_closed,
                    fill="toself",
                    name=selected_player,
                    line=dict(color="#E30613", width=3),
                    fillcolor="rgba(227, 6, 19, 0.4)",
                )
            )

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 10], dtick=2)
                ),
                showlegend=True,
                legend=dict(
                    orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5
                ),
                margin=dict(l=40, r=40, t=20, b=40),
            )

            st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning(f"Data for player '{selected_player}' was not found.")
else:
    st.info("Please select a player from the sidebar.")
