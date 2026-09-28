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

        # --- 3. TUTKAKAAVIO VERTAILULLA (U19D) ---
        with col_radar:
            st.subheader("📊 Self-Assessment Radar")

            # Määritetään kategoriat ja etsitään oikea sarake otsikon perusteella
            # Kokeillaan sekä englannin- että ruotsinkielisiä hakusanoja sarakkeista
            categories_search = {
                "Skating": ["skating", "skridskoåkning"],
                "Shooting": ["shot", "skott"],
                "Puck Control": [
                    "puck handling",
                    "puckkontroll",
                    "puckföring",
                ],
                "Hockey Sense": ["game sense", "spelförståelse"],
                "Passing": ["passing", "passning"],
                "Defense": ["defensive play", "försvarsspelet"],
                "Offense": ["offensive play", "anfallsspelet"],
                "Physical Play": ["physical play", "fysiska spelet"],
                "Team System": ["playbook", "spelsystemet"],
            }

            labels = list(categories_search.keys())
            player_scores = []
            team_averages = []

            for cat_name, keywords in categories_search.items():
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

                    # Koko joukkueen puhtaat numeeriset arvot ja keskiarvo
                    col_numeric = pd.to_numeric(
                        df[matched_col], errors="coerce"
                    ).dropna()
                    t_avg = col_numeric.mean() if not col_numeric.empty else 5.0
                else:
                    p_score = 5.0
                    t_avg = 5.0

                player_scores.append(round(p_score, 1))
                team_averages.append(round(t_avg, 2))

            # Suljetaan ympyrä Plotly-tutkakaaviota varten
            labels_closed = labels + [labels[0]]
            player_scores_closed = player_scores + [player_scores[0]]
            team_averages_closed = team_averages + [team_averages[0]]

            # Luodaan Plotly-graafi
            fig = go.Figure()

            # 1. Koko U19D-joukkueen keskiarvo (Harmaa täyttö + katkoviiva)
            fig.add_trace(
                go.Scatterpolar(
                    r=team_averages_closed,
                    theta=labels_closed,
                    fill="toself",
                    name="U19D Average",
                    line=dict(color="#4A90E2", width=2, dash="dash"),
                    fillcolor="rgba(74, 144, 226, 0.25)",
                )
            )

            # 2. Valitun pelaajan omat pisteet (Punainen täyttö + paksu viiva)
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
                    ),
                    angularaxis=dict(gridcolor="#444444"),
                ),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.25,
                    xanchor="center",
                    x=0.5,
                ),
                margin=dict(l=40, r=40, t=20, b=40),
            )

            st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning(f"Data for player '{selected_player}' was not found.")
else:
    st.info("Please select a player from the sidebar.")
