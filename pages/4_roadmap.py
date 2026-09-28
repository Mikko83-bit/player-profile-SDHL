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

        # Poimitaan kauden tavoite kyselystä (tai käytetään oletusta)
        s_goal = (
            p.iloc[47]
            if len(p) > 47 and pd.notna(p.iloc[47])
            else "Womens team practice/games"
        )

        st.subheader(f"Player: {selected_player}")
        st.write(
            "Generate and download the visual Player Roadmap presentation in PowerPoint format."
        )

        st.divider()

        if create_player_ppt:
            # Luodaan PowerPoint-tiedosto uudella kahden parametrin funktiolla
            ppt_file = create_player_ppt(selected_player, s_goal)

            # Latauspainike
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
