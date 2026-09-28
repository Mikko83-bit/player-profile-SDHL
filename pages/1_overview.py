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

        # Tunnistetaan pelaajan joukkue
        player_team = str(p.get(team_col, "U19D")).upper()
        is_sdhl = "SDHL" in player_team

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
            st.write(f"**Team:** {p.get(team_col, 'Luleå Hockey')}")

            st.divider()
            st.subheader("🎯 Season Goal")

            goal_val = (
                p.iloc[46]
                if len(p) > 49 and pd.notna(p.iloc[46])
                else "No goal defined."
            )
            st.success(goal_val)

        # --- 3. TUTKAKAAVIO VERTAILULLA (SDHL & U19D) ---
        with col_radar:
            st.subheader("📊 Self-Assessment Radar")

            # Valitaan oletuksena vertailuun pelaajan oma joukkue
            default_benchmarks = (
                ["SDHL Average"] if is_sdhl else ["U19D Average"]
            )

            show_benchmarks = st.multiselect(
                "Compare with:",
                options=["U19D Average", "SDHL Average"],
                default=default_benchmarks,
            )

            # SDHL-joukkueen kiinteät keskiarvot kuvan mukaisesti
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

            # Lasketaan U19D-joukkueen keskiarvo datasta (rajaten U19D-pelaajiin jos joukkuesarake löytyy)
            u19d_df = (
                df[df[team_col].astype(str).str.contains("U19", case=False)]
                if team_col in df.columns
                else df
            )
            if u19d_df.empty:
                u19d_df = df

            for cat_name, info in categories_data.items():
                keywords = info["keywords"]
                sdhl_averages.append(info["sdhl"])

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

                    # U19D keskiarvo
                    col_numeric_u19 = pd.to_numeric(
                        u19d_df[matched_col], errors="coerce"
                    ).dropna()
                    u19_avg = (
                        col_numeric_u19.mean()
                        if not col_numeric_u19.empty
                        else 5.0
                    )
                else:
                    p_score = 5.0
                    u19_avg = 5.0

                player_scores.append(round(p_score, 1))
                u19d_averages.append(round(u19_avg, 2))

            # Suljetaan ympyrä
            labels_closed = labels + [labels[0]]
            player_scores_closed = player_scores + [player_scores[0]]
            u19d_averages_closed = u19d_averages + [u19d_averages[0]]
            sdhl_averages_closed = sdhl_averages + [sdhl_averages[0]]

            fig = go.Figure()

            # 1. SDHL Average - Valkoinen/Harmaa katkoviiva
            if "SDHL Average" in show_benchmarks:
                fig.add_trace(
                    go.Scatterpolar(
                        r=sdhl_averages_closed,
                        theta=labels_closed,
                        name="SDHL Average",
                        line=dict(color="#E0E0E0", width=2, dash="dot"),
                        fill="none",
                    )
                )

            # 2. U19D Average - Sininen katkoviiva
            if "U19D Average" in show_benchmarks:
                fig.add_trace(
                    go.Scatterpolar(
                        r=u19d_averages_closed,
                        theta=labels_closed,
                        name="U19D Average",
                        line=dict(color="#38B6FF", width=2, dash="dash"),
                        fill="none",
                    )
                )

            # 3. Pelaaja (Vain tällä on täyttöväri)
            fig.add_trace(
                go.Scatterpolar(
                    r=player_scores_closed,
                    theta=labels_closed,
                    fill="toself",
                    name=f"{selected_player} ({'SDHL' if is_sdhl else 'U19D'})",
                    line=dict(color="#E30613", width=3),
                    fillcolor="rgba(227, 6, 19, 0.35)",
                )
            )

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10],
                        dtick=2,
                        gridcolor="#333333",
                        tickfont=dict(color="white"),
                    ),
                    angularaxis=dict(
                        gridcolor="#333333",
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
                margin=dict(l=40, r=40, t=10, b=40),
            )

            st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning(f"Data for player '{selected_player}' was not found.")
else:
    st.info("Please select a player from the sidebar.")
