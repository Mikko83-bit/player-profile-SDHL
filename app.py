import pandas as pd
import plotly.express as px
import streamlit as st

# Sivun asetukset
st.set_page_config(page_title="Pelaajaprofiilit - SDHL", page_icon="🏒", layout="wide")
st.title("🏒 Pelaajien kehitysprofiilit")


# Ladataan data Excel-tiedostosta
@st.cache_data
def load_data():
    return pd.read_excel("Player profile.xlsx")


try:
    df = load_data()

    # Esitään nimen sisältävä sarake
    name_col = next((col for col in ["Name", "Nimi", "Pelaaja"] if col in df.columns), None)

    if name_col:
        # Pelaajan valinta vetovalikosta
        players = df[name_col].dropna().unique().tolist()
        selected_player = st.selectbox("Valitse pelaaja:", players)

        # Suodatetaan valitun pelaajan rivi
        player_data = df[df[name_col] == selected_player].iloc[0]

        # Etsitään numeeriset arviointisarakkeet (kysymykset, joiden vastaus on numero 1-10)
        rating_cols = []
        for col in df.columns:
            val = player_data[col]
            if isinstance(val, (int, float)) and 1 <= val <= 10:
                rating_cols.append(col)

        # Luodaan kaksi saraketta käyttöliittymään
        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.subheader(f"📊 Numerovastausten yhteenveto: {selected_player}")

            if rating_cols:
                # Lyhennetään pitkiä kysymysotsikoita kaaviota varten
                short_labels = [c.split("?")[0][:25] + "..." if len(c) > 25 else c for c in rating_cols]
                values = [player_data[c] for c in rating_cols]

                # Tutkakaavio (Radar Chart)
                df_radar = pd.DataFrame(dict(r=values, theta=short_labels))
                fig = px.line_polar(df_radar, r="r", theta="theta", line_close=True, range_r=[0, 10])
                fig.update_traces(fill="toself")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Pelaajalle ei löytynyt numeerisia arvioita (1–10).")

        with col_right:
            st.subheader("📋 Kaikki vastaukset ja kehityskohteet")
            
            # Näytetään sanalliset vastaukset ja kehityskohteet siististi
            for col in df.columns:
                if col != name_col:
                    val = player_data[col]
                    if pd.notna(val):
                        st.markdown(f"**{col}**")
                        st.write(val)
                        st.divider()

    else:
        st.error("Excel-tiedostosta ei löytynyt 'Name'- tai 'Nimi'-saraketta.")

except Exception as e:
    st.error(f"Virhe ladattaessa Excel-tiedostoa: {e}")
