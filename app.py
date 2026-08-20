import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Luleå/MSSK - Spelarprofiler", page_icon="🏒", layout="wide"
)

# Tiedoston nimi täsmälleen Excelisi mukaan
EXCEL_FILE = "Spelarprofil - Luleå_MSSK SDHL_U19D.xlsx"


@st.cache_data
def load_data():
    return pd.read_excel(EXCEL_FILE)


try:
    df = load_data()
    st.session_state["df"] = df

    # Tunnistetaan nimesarake (Name? tai ensimmäinen sarake)
    name_col = "Name?" if "Name?" in df.columns else df.columns[0]
    df[name_col] = df[name_col].astype(str).str.strip()

    st.sidebar.title("🏒 Luleå/MSSK Profiler")

    # Joukkueen suodatus (SDHL vs U19D)
    if "Team" in df.columns:
        teams = ["Kaikki joukkueet"] + [
            str(t).strip() for t in df["Team"].dropna().unique()
        ]
        selected_team = st.sidebar.selectbox("🏆 Valitse joukkue / Lag", teams)

        if selected_team != "Kaikki joukkueet":
            df_filtered = df[df["Team"].astype(str).str.strip() == selected_team]
        else:
            df_filtered = df
    else:
        df_filtered = df

    # Pelaajavalikko suodatetun listan mukaan
    players = [
        p
        for p in df_filtered[name_col].unique()
        if p and p != "nan" and p != "None"
    ]
    selected_player = st.sidebar.selectbox("👤 Valitse pelaaja", players)

    st.session_state["selected_player"] = selected_player

    # Navigaatiorakenne
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

except FileNotFoundError:
    st.error(
        f"❌ Tiedostoa '{EXCEL_FILE}' ei löytynyt projektin juurikansiosta. Varmista että tiedoston nimi ja pääte ovat täsmälleen oikein GitHubissa."
    )
except Exception as e:
    st.error(f"Virhe ladattaessa tietoja: {e}")
