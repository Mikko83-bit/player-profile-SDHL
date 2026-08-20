import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Luleå Hockey - SDHL Player Profile", 
    page_icon="🏒", 
    layout="wide"
)

# Datan lataus ja jako kaikille sivuille st.session_state-muistiin
@st.cache_data
def load_data():
    return pd.read_excel("Player profile.xlsx")

try:
    df = load_data()
    st.session_state["df"] = df

    # Valitaan pelaaja sivupalkissa (sidebar), jotta se säilyy sivulta toiselle
    players = df["Name?"].dropna().unique().tolist() if "Name?" in df.columns else df.iloc[:, 0].dropna().unique().tolist()
    
    st.sidebar.title("🏒 Luleå Hockey SDHL")
    selected_player = st.sidebar.selectbox("👤 Valitse pelaaja", players)
    st.session_state["selected_player"] = selected_player

    # --- MÄÄRITELLÄÄN SIVUT JA NAVIGAATIO (st.navigation) ---
    overview_page = st.Page("pages/1_overview.py", title="Perustiedot & Yleiskatsaus", icon="👤")
    skills_page = st.Page("pages/2_skills.py", title="Taidot & Peliesitys", icon="📊")
    priorities_page = st.Page("pages/3_priorities.py", title="Kehityskohteet & Tavoitteet", icon="🎯")

    # Ryhmitelty navigaatio
    pg = st.navigation({
        "Pelaajaprofiili": [overview_page, skills_page, priorities_page]
    })

    # Suoritetaan valittu sivu
    pg.run()

except Exception as e:
    st.error(f"Virhe ladattaessa tietoja: {e}")
