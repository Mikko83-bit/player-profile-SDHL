import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Luleå/MSSK - Player Profiles", page_icon="🏒", layout="wide"
)

EXCEL_FILE = "Spelarprofil - Luleå_MSSK SDHL_U19D.xlsx"


@st.cache_data
def load_data():
    return pd.read_excel(EXCEL_FILE)


try:
    df = load_data()
    st.session_state["df"] = df

    team_col = "TEAM" if "TEAM" in df.columns else df.columns[0]
    name_col = "Name" if "Name" in df.columns else df.columns[2]

    df[team_col] = df[team_col].astype(str).str.strip()
    df[name_col] = df[name_col].astype(str).str.strip()

    st.sidebar.title("🏒 Luleå/MSSK Profiles")

    # Team Filter
    teams = ["All Teams"] + [
        t
        for t in df[team_col].dropna().unique()
        if t and t != "nan" and t != "None"
    ]
    selected_team = st.sidebar.selectbox("🏆 Select Team", teams)

    if selected_team != "All Teams":
        df_filtered = df[df[team_col] == selected_team]
    else:
        df_filtered = df

    # Player Filter
    players = [
        p
        for p in df_filtered[name_col].unique()
        if p and p != "nan" and p != "None"
    ]
    selected_player = st.sidebar.selectbox("👤 Select Player", players)

    st.session_state["selected_player"] = selected_player
    st.session_state["name_col"] = name_col
    st.session_state["team_col"] = team_col

    # Navigation structure with English page titles
    overview_page = st.Page(
        "pages/1_overview.py", title="Overview & Player Info", icon="👤"
    )
    skills_page = st.Page(
        "pages/2_skills.py", title="Skills & Performance", icon="📊"
    )
    priorities_page = st.Page(
        "pages/3_priorities.py", title="Development & Goals", icon="🎯"
    )

    pg = st.navigation(
        {"Player Profile": [overview_page, skills_page, priorities_page]}
    )
    pg.run()

except FileNotFoundError:
    st.error(f"❌ File '{EXCEL_FILE}' not found in the root directory.")
except Exception as e:
    st.error(f"Error loading data: {e}")
