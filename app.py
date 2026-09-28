from io import BytesIO
import pandas as pd

# --- PPTX LIB IMPORT ---
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import streamlit as st

st.set_page_config(
    page_title="Luleå/MSSK - Player Profiles", page_icon="🏒", layout="wide"
)

EXCEL_FILE = "Spelarprofil - Luleå_MSSK SDHL_U19D.xlsx"


@st.cache_data
def load_data():
    return pd.read_excel(EXCEL_FILE)


# --- PPTX GENERATOR FUNKTIO ---
def create_player_ppt(player_name, season_goal, technical, mental):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)

    # Nimi-otsikko
    txBox = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.4), Inches(12), Inches(0.8)
    )
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = f"Name: {player_name}"
    p.font.size = Pt(28)
    p.font.bold = True

    # Punaisen laatikon luontiapuri
    def add_red_box(left, top, width, height, title, content_list):
        shape = slide.shapes.add_shape(1, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(179, 0, 0)
        shape.line.color.rgb = RGBColor(179, 0, 0)

        tf = shape.text_frame
        tf.word_wrap = True

        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(16)
        p_title.font.bold = True
        p_title.font.color.rgb = RGBColor(255, 204, 0)
        p_title.alignment = PP_ALIGN.CENTER

        for item in content_list:
            p_item = tf.add_paragraph()
            p_item.text = str(item)
            p_item.font.size = Pt(12)
            p_item.font.color.rgb = RGBColor(255, 255, 255)
            p_item.alignment = PP_ALIGN.CENTER

    # Elementtien sijoittelu
    add_red_box(
        Inches(4.5),
        Inches(0.8),
        Inches(4.3),
        Inches(1.4),
        "Dream goals",
        ["Career: Professional", f"Season: {season_goal}"],
    )
    add_red_box(
        Inches(1.5),
        Inches(2.4),
        Inches(4.8),
        Inches(1.2),
        "Offensive zone",
        ["Tehokkuus"],
    )
    add_red_box(
        Inches(7.0),
        Inches(2.4),
        Inches(4.8),
        Inches(1.2),
        "Defensive zone",
        ["Omanpään puolustuspelaaminen (kokonaisvaltainen)"],
    )

    add_red_box(
        Inches(0.8),
        Inches(4.0),
        Inches(4.5),
        Inches(1.3),
        "Mental",
        ["Tunteiden hallinta", "Epäonnistumisten käsittely", f"Mental: {mental}"],
    )
    add_red_box(
        Inches(8.0),
        Inches(4.0),
        Inches(4.5),
        Inches(1.3),
        "Weekly Process",
        ["6x jää + oheisharjoittelu", "1-2 peliä viikossa"],
    )

    add_red_box(
        Inches(0.5),
        Inches(5.6),
        Inches(2.8),
        Inches(1.3),
        "Technical",
        ["Luistelun monipuolisuus", f"Focus: {technical}"],
    )
    add_red_box(
        Inches(3.6),
        Inches(5.6),
        Inches(2.8),
        Inches(1.3),
        "Tactical",
        ["Erikoistilannepelaaminen"],
    )
    add_red_box(
        Inches(6.7),
        Inches(5.6),
        Inches(2.8),
        Inches(1.3),
        "Off-ice",
        ["Liikkuvuus", "Nopeus"],
    )
    add_red_box(
        Inches(9.8),
        Inches(5.6),
        Inches(2.8),
        Inches(1.3),
        "Training (daily)",
        ["Teema jokaiselle päivälle"],
    )

    binary_output = BytesIO()
    prs.save(binary_output)
    binary_output.seek(0)
    return binary_output


# Tallennetaan funktio session_stateen, jotta muut sivut voivat kutsua sitä
st.session_state["create_player_ppt"] = create_player_ppt


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
    roadmap_page = st.Page(
        "pages/4_roadmap.py", title="Roadmap & PPT Export", icon="🗺️"
    )

    pg = st.navigation(
        {
            "Player Profile": [
                overview_page,
                skills_page,
                priorities_page,
                roadmap_page,
            ]
        }
    )
    pg.run()

except FileNotFoundError:
    st.error(f"❌ File '{EXCEL_FILE}' not found in the root directory.")
except Exception as e:
    st.error(f"Error loading data: {e}")
