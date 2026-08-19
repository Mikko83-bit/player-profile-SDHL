import plotly.express as px
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Pelaajaprofiili - SDHL", page_icon="🏒")
st.title("🏒 Pelaajan kehitysprofiili: Elsi")

st.header("1. Taitojen itsearviointi")
col1, col2 = st.columns(2)

with col1:
    skating = st.slider("Luistelu", 1, 10, 6)
    shooting = st.slider("Laukaus", 1, 10, 5)
    puck_control = st.slider("Kiekonhallinta", 1, 10, 4)
    hockey_sense = st.slider("Peliäly", 1, 10, 6)

with col2:
    passing = st.slider("Syöttäminen", 1, 10, 6)
    defense = st.slider("Puolustuspeli", 1, 10, 4)
    offense = st.slider("Hyökkäyspeli", 1, 10, 5)
    physical = st.slider("Kamppailupeli", 1, 10, 5)

st.header("2. Yhteenveto (Radar Chart)")
categories = [
    "Luistelu",
    "Laukaus",
    "Kiekonhallinta",
    "Peliäly",
    "Syöttäminen",
    "Puolustus",
    "Hyökkäys",
    "Kamppailu",
]
values = [
    skating,
    shooting,
    puck_control,
    hockey_sense,
    passing,
    defense,
    offense,
    physical,
]

df = pd.DataFrame(dict(r=values, theta=categories))
fig = px.line_polar(df, r="r", theta="theta", line_close=True, range_r=[0, 10])
st.plotly_chart(fig)

st.header("3. Kauden tavoitteet")
st.write(
    "**1.** Liike kiekon kanssa & kiekon suojaus\n**2.** Laukaukset haastavista asennoista\n**3.** Aktiivinen puolustaminen"
)
