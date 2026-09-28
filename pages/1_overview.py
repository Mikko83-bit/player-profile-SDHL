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

            num_val = (
                p.iloc[1]
                if len(p) > 1 and pd.notna(p.iloc[1])
                else p.get("Nummer?", "-")
            )
            st.write(f"**Number:** {num_val}")
            st.write(f"**Team:** {p.get(team_col, 'Luleå U19D')}")

            st.divider()
            st.subheader("🎯 Season Goal")

            goal_val = (
                p.iloc[46]
                if len(p) > 46 and pd.notna(p.iloc[46])
                else "No goal defined."
            )
            st.success(goal_val)

        # --- 3. TUTKAKAAVIO VERTAILULLA (U19D & SDHL) ---
        with col_radar:
            st.subheader("📊 Self-Assessment Radar")

            # Määritetään kategoriat, hakusanat Excel-sarakkeille sekä SDHL-joukkueen kiinteät keskiarvot kuvan mukaisesti
            categories_data = {
                "Skating": {
                    "keywords": ["skating", "skridskoåkning"],
                    "sdhl": 6.37,
                },
                "Shooting": {"keywords": ["shot", "skott"], "sdhl": 5.74},
                "Puck Control": {
                    "keywords": [
                        "puck handling",
                        "puckkontroll",
                        "puckföring",
                    ],
                    "sdhl": 5.68,
                },
                "Hockey Sense": {
                    "keywords": ["game sense", "spelförståelse"],
                    "sdhl": 7.26,
                },
                "Passing": {
                    "keywords": ["passing", "passning"],
                    "sdhl": 6.58,
                },
                "Defense": {
                    "keywords": ["defensive play", "försvarsspelet"],
                    "sdhl": 6.26,
                },
                "Offense": {
                    "keywords": ["offensive play", "anfallsspelet"],
                    "sdhl": 6.16,
                },
                "Physical Play": {
                    "keywords": ["physical play", "fysiska spelet"],
                    "sdhl": 6.05,
                },
                "Team System": {
                    "keywords": ["playbook", "spelsystemet"],
                    "sdhl": 7.37,
                },
            }

            labels = list(categories_data.keys())
            player_scores = []
            u19d_averages = []
            sdhl_averages = []

            for cat_name, info in categories_data.items():
                keywords = info["keywords"]
                sdhl_averages.append(info["sdhl"])

                # Etsitään oikea sarake df:stä hakusanojen avulla
                matched_col = None
                for col in df.columns:
                    col_str = str(col).lower()
                    if any(kw in col_str for kw in keywords):
                        matched_col = col
                        break

                if matched_col is not None:
                    # Pelaajan oma arvo
                    val = p.get(matched_col)
                    try:
                        p_score = float(val) if pd.notna(val) else 5.0
                    except (ValueError, TypeError):
                        p_score = 5.0

                    # U19D Joukkueen keskiarvo ladatusta datasta
                    col_numeric = pd.to_numeric(
                        df[matched_col], errors="coerce"
                    ).dropna()
                    u19_avg = (
                        col_numeric.mean() if not col_numeric.empty else 5.0
                    )
                else:
                    p_score = 5.0
                    u19_avg = 5.0

                player_scores.append(round(p_score, 1))
                u19d_averages.append(round(u19_avg, 2))

            # Suljetaan ympyrä Plotly-tutkakaaviota varten
            labels_closed = labels + [labels[0]]
            player_scores_closed = player_scores + [player_scores[0]]
            u19d_averages_closed = u19d_averages + [u19d_averages[0]]
            sdhl_averages_closed = sdhl_averages + [sdhl_averages[0]]

            # Luodaan Plotly-graafi
            fig = go.Figure()

            # 1. SDHL Average (Harmaa katkoviiva)
            fig.add_trace(
                go.Scatterpolar(
                    r=sdhl_averages_closed,
                    theta=labels_closed,
                    name="SDHL Average",
                    line=dict(color="#A0A0A0", width=2, dash="dashdot"),
                    fill="none",
                )
            )

            # 2. U19D Average (Sininen katkoviiva)
            fig.add_trace(
                go.Scatterpolar(
                    r=u19d_averages_closed,
                    theta=labels_closed,
                    fill="toself",
                    name="U19D Average",
                    line=dict(color="#4A90E2", width=2, dash="dash"),
                    fillcolor="rgba(74, 144, 226, 0.2)",
                )
            )

            # 3. Valitun pelaajan omat pisteet (Punainen täyttö + paksu viiva)
            fig.add_trace(
                go.Scatterpolar(
                    r=player_scores_closed,
                    theta=labels_closed,
                    fill="toself",
                    name=selected_player,
                    line=dict(color="#E30613", width=3),
                    fillcolor="rgba(227, 6, 19, 0.45)",
                )
            )

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10],
                        dtick=2,
                        gridcolor="#444444",
                        tickfont=dict(color="white"),
                    ),
                    angularaxis=dict(
                        gridcolor="#444444",
                        tickfont=dict(color="white", size=11),
                    ),
                    bgcolor="rgba(0,0,0,0)",
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.25,
                    xanchor="center",
                    x=0.5,
                    font=dict(color="white", size=11),
                ),
                margin=dict(l=40, r=40, t=20, b=40),
            )

            st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning(f"Data for player '{selected_player}' was not found.")
else:
    st.info("Please select a player from the sidebar.")
