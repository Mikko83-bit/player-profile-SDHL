import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Pelaajaprofiilit - SDHL", page_icon="🏒", layout="wide")
st.title("🏒 Pelaajien kehitysprofiilit")

@st.cache_data
def load_data():
    return pd.read_excel("Player profile.xlsx")

try:
    df = load_data()
    
    # Valitaan pelaaja
    players = df["Name?"].dropna().unique().tolist()
    selected_player = st.selectbox("Valitse pelaaja", players)
    
    # Pelaajan rivi Excelissä
    p = df[df["Name?"] == selected_player].iloc[0]

    st.header(f"📊 Taitoprofiili: {selected_player}")
    
    categories = {
        "Luistelu": "How would you rate your skating?",
        "Laukaus": "How would you rate your shot?",
        "Kiekonhallinta": "How would you rate your puck handling/control?",
        "Peliäly": "How would you rate your hockey sense?",
        "Syöttäminen": "How would you rate your passing and receiving ability?",
        "Puolustus": "How would you rate your defensive play?",
        "Hyökkäys": "How is your offensive play?",
        "Kamppailu": "How is your physical play?",
        "Pelitapa": "How is your understanding of the team system?"
    }

    col_sliders, col_chart = st.columns([1, 1])

    updated_scores = {}

    with col_sliders:
        st.subheader("⚙️ Arvot Excelistä (1–10)")
        
        for label, col_name in categories.items():
            # Haetaan arvo Excelistä
            raw_val = p.get(col_name, 5)
            
            # Muunnetaan arvo varmasti puhtaaksi kokonaisluvuksi (1-10)
            try:
                clean_val = int(round(float(raw_val))) if pd.notna(raw_val) else 5
                # Varmistetaan että arvo pysyy välillä 1–10
                clean_val = max(1, min(10, clean_val))
            except (ValueError, TypeError):
                clean_val = 5

            key_name = f"slider_{selected_player}_{label}"

            # Jos pelaaja vaihtui, päivitetään uuden pelaajan arvo muistiin
            if key_name not in st.session_state:
                st.session_state[key_name] = clean_val

            # Liukukytkin pakotetuilla kokonaisluvuilla (step=1)
            updated_scores[label] = st.slider(
                label, 
                min_value=1, 
                max_value=10, 
                step=1,
                key=key_name
            )

    with col_chart:
        labels = list(updated_scores.keys())
        scores = list(updated_scores.values())

        df_radar = pd.DataFrame(dict(r=scores, theta=labels))
        fig = px.line_polar(df_radar, r='r', theta='theta', line_close=True, range_r=[0, 10])
        fig.update_traces(fill='toself')
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # TAVOITTEET JA KEHITYSKOHTEET
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏒 Peli kiekolla (3 tavoitetta)")
        st.info(p.get("Write down 3 specific skills/situations in the game with the puck", "Ei kirjauksia"))

        st.subheader("🛡️ Peli ilman kiekkoa (3 tavoitetta)")
        st.info(p.get("Write down 3 specific skills/situations in the game without the puck", "Ei kirjauksia"))

    with col2:
        st.subheader("🎯 Kauden tavoite")
        st.success(p.get("What is your goal for this season?", "Ei määritelty"))

        st.subheader("💬 Palaute")
        st.write(f"**Suhtautuminen palautteeseen:** {p.get('How do you handle feedback (both positive and negative)?', '-')}")

except Exception as e:
    st.error(f"Virhe ladattaessa tietoja: {e}")
