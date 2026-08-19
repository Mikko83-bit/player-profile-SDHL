import plotly.express as px
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Pelaajaprofiilit - SDHL", page_icon="🏒")
st.title("🏒 Pelaajien kehitysprofiilit")

# Sanakirja pelaajien tiedoista
players_data = {
    "Elsi": {
        "skating": 6,
        "shooting": 5,
        "puck_control": 4,
        "hockey_sense": 6,
        "passing": 6,
        "defense": 4,
        "offense": 5,
        "physical": 5,
        "goals": "**1.** Liike kiekon kanssa & kiekon suojaus\n**2.** Laukaukset haastavista asennoista\n**3.** Aktiivinen puolustaminen"
    },
    "Pelaaja 2": {
        "skating": 8,
        "shooting": 7,
        "puck_control": 6,
        "hockey_sense": 7,
        "passing": 7,
        "defense": 6,
        "offense": 8,
        "physical": 6,
        "goals": "**1.** Suoraviivaisuus hyökkäysalueella\n**2.** Aloitusten voittaminen\n**3.** Taklauspeli"
    }
}

# Pelaajan valinta vetovalikosta
selected_player = st.selectbox("Valitse pelaaja", list(players_data.keys()))

# Haetaan valitun pelaajan tiedot
player_info = players_data[selected_player]

st.header(f"1. Taitojen itsearviointi: {selected_player}")
col1, col2 = st.columns(2)

with col1:
    skating = st.slider("Luistelu", 1, 10, player_info["skating"])
    shooting = st.slider("Laukaus", 1, 10, player_info["shooting"])
    puck_control = st.slider("Kiekonhallinta", 1, 10, player_info["puck_control"])
    hockey_sense = st.slider("Peliäly", 1, 10, player_info["hockey_sense"])

with col2:
    passing = st.slider("Syöttäminen", 1, 10, player_info["passing"])
    defense = st.slider("Puolustuspeli", 1, 10, player_info["defense"])
    offense = st.slider("Hyökkäyspeli", 1, 10, player_info["offense"])
    physical = st.slider("Kamppailupeli", 1, 10, player_info["physical"])

st.header("2. Yhteenveto (Radar Chart)")
categories = [
    "Luistelu", "Laukaus", "Kiekonhallinta", "Peliäly",
    "Syöttäminen", "Puolustus", "Hyökkäys", "Kamppailu"
]
values = [
    skating, shooting, puck_control, hockey_sense,
    passing, defense, offense, physical
]

df = pd.DataFrame(dict(r=values, theta=categories))
fig = px.line_polar(df, r="r", theta="theta", line_close=True, range_r=[0, 10])
st.plotly_chart(fig)

st.header("3. Kauden tavoitteet")
st.write(player_info["goals"])
