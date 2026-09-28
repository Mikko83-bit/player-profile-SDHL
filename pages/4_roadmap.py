import pandas as pd
import streamlit as st

df = st.session_state.get("df")
selected_player = st.session_state.get("selected_player")
name_col = st.session_state.get("name_col", "Name")
create_player_ppt = st.session_state.get("create_player_ppt")

st.title("🗺️ Player Roadmap & PPT Export")

if df is not None and selected_player:
    match = df[df[name_col].astype(str).str.strip() == str(selected_player)]

    if not match.empty:
        p = match.iloc[0]

        # Apufunktio sarakkeen turvalliseen hakemiseen
        def get_val(idx, default_val="-"):
            if len(p) > idx and pd.notna(p.iloc[idx]):
                val = str(p.iloc[idx]).strip()
                return val if val != "" else default_val
            return default_val

        # Haetaan valitun pelaajan omat vastaukset sarakkeista
        season_goal = get_val(47, "Not set")
        off_zone = get_val(20, "Offensive development")
        def_zone = get_val(17, "Defensive development")
        mental = get_val(43, "Mental focus")
        technical = get_val(2, "Skating & skills")
        tactical = get_val(26, "Game understanding")
        off_ice = get_val(23, "Physical preparation")
        daily_train = get_val(31, "Practice ethic")

        st.subheader(f"Player: {selected_player}")
        st.write(
            "Generate and download a personalized PowerPoint roadmap based on survey responses."
        )

        st.divider()

        if create_player_ppt:
            # Luodaan esitys pelaajan omilla tiedoilla
            ppt_file = create_player_ppt(
                selected_player,
                season_goal,
                off_zone,
                def_zone,
                mental,
                technical,
                tactical,
                off_ice,
                daily_train,
            )

            st.download_button(
                label=f"📥 Download {selected_player} Roadmap (.pptx)",
                data=ppt_file,
                file_name=f"Roadmap_{selected_player}.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )
        else:
            st.error("PowerPoint generator function is not available.")
    else:
        st.warning(f"Player '{selected_player}' not found.")
else:
    st.info("Please select a player from the sidebar.")
