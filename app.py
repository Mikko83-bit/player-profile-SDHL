import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Luleå Hockey - SDHL Player Profile",
    page_icon="🏒",
    layout="wide",
)


@st.cache_data
def load_data():
    return pd.read_excel("Player profile.xlsx")


try:
    df = load_data()
    st.session_state["df"] = df

    # Etsitään nimesarake (ensimmäinen sarake tai Name?)
    name_col = "Name?" if "Name?" in df.columns else df.columns[0]

    # Puhdistetaan nimitiedot tyhjistä välimerkeistä
    df[name_col] = df[name_col].astype(str).str.strip()
    players = [
        p for p in df[name_col].unique() if p and p != "nan" and p != "None"
    ]

    st.sidebar.title("🏒 Luleå Hockey SDHL")
    selected_player = st.sidebar.selectbox("👤 Valitse pelaaja", players)
    st.session_state["selected_player"] = selected_player

    # Sivujen määrittely
    overview_page = st.Page(
        "pages/1_overview.py", title="Perustiedot & Yleiskatsaus", icon="👤"
    )
    skills_page = st.Page(
        "pages/2_skills.py", title="Taidot & Peliesitys", icon="📊"
    )
    priorities_page = st.Page(
        "pages/3_priorities.py", title="Kehityskohteet & Tavoitteet", icon="🎯"
    )

    pg = st.navigation(
        {"Pelaajaprofiili": [overview_page, skills_page, priorities_page]}
    )
    pg.run()

except Exception as e:
    st.error(f"Virhe ladattaessa tietoja: {e}")
