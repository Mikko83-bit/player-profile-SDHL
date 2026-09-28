from io import BytesIO
import pandas as pd
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


# --- PPTX GENERATOR FUNKTIO (Pelaajakohtaiset vastaukset) ---
def create_player_ppt(
    player_name,
    season_goal,
    off_zone,
    def_zone,
    mental,
    technical,
    tactical,
    off_ice,
    daily_train,
):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)

    # Nimi (Vasen yläkulma)
    txBox = slide.shapes.add_textbox(
        Inches(0.6), Inches(0.4), Inches(5.0), Inches(1.2)
    )
    tf = txBox.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "Name:"
    p1.font.size = Pt(22)

    p2 = tf.add_paragraph()
    p2.text = str(player_name)
    p2.font.size = Pt(26)
    p2.font.bold = True

    # Athletes reflections (Oikea yläkulma)
    txBox_refl = slide.shapes.add_textbox(
        Inches(8.5), Inches(0.8), Inches(4.5), Inches(1.5)
    )
    tf_refl = txBox_refl.text_frame
    tf_refl.word_wrap = True

    p_r1 = tf_refl.paragraphs[0]
    p_r1.text = "Athletes reflections"
    p_r1.font.size = Pt(14)
    p_r1.font.underline = True

    p_r2 = tf_refl.add_paragraph()
    p_r2.text = "Dream goals:"
    p_r2.font.size = Pt(14)

    p_r3 = tf_refl.add_paragraph()
    p_r3.text = f"Season: {season_goal}"
    p_r3.font.size = Pt(14)

    # Punaisen laatikon luontiapuri
    def add_red_box(left, top, width, height, title, content_text):
        shape = slide.shapes.add_shape(1, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(179, 0, 0)
        shape.line.color.rgb = RGBColor(179, 0, 0)

        tf = shape.text_frame
        tf.word_wrap = True

        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(15)
        p_title.font.bold = True
        p_title.font.color.rgb = RGBColor(255, 204, 0)
        p_title.alignment = PP_ALIGN.CENTER

        p_item = tf.add_paragraph()
        p_item.text = str(content_text)
        p_item.font.size = Pt(12)
        p_item.font.color.rgb = RGBColor(255, 255, 255)
        p_item.alignment = PP_ALIGN.CENTER

    # Piirretään laatikot pelaajan omilla vastauksilla
    add_red_box(
        Inches(4.1),
        Inches(0.8),
        Inches(3.8),
        Inches(1.5),
        "Dream goals",
        f"Season: {season_goal}",
    )

    add_red_box(
        Inches(1.8), Inches(2.7), Inches(3.6), Inches(1.3), "Offensive zone", off_zone
    )

    add_red_box(
        Inches(5.8), Inches(2.7), Inches(3.8), Inches(1.3), "Defensive zone", def_zone
    )

    add_red_box(
        Inches(1.2), Inches(4.7), Inches(3.4), Inches(1.3), "Mental", mental
    )

    add_red_box(
        Inches(6.5),
        Inches(4.7),
        Inches(3.6),
        Inches(1.3),
        "Weekly Process",
        "6x ice+off-ice training\n1-2 games per week",
    )

    add_red_box(
        Inches(0.8), Inches(6.3), Inches(2.6), Inches(1.0), "Technical", technical
    )

    add_red_box(
        Inches(3.7), Inches(6.3), Inches(2.6), Inches(1.0), "Tactical", tactical
    )

    add_red_box(
        Inches(6.6), Inches(6.3), Inches(2.6), Inches(1.0), "Off-ice", off_ice
    )

    add_red_box(
        Inches(9.5),
        Inches(6.3),
        Inches(2.8),
        Inches(1.0),
        "Training (daily)",
        daily_train,
    )

    binary_output = BytesIO()
    prs.save(binary_output)
    binary_output.seek(0)
    return binary_output


# Tallennettaan funktio muistiin
st.session_state["create_player_ppt"] = create_player_ppt

try:
    df = load_data()
    st.session_state["df"] = df

    team_col = "TEAM" if "TEAM" in df.columns else df.columns[0]
    name_col = "Name" if "Name" in df.columns else df.columns[2]

    df[team_col] = df[team_col].astype(str).str.strip()
    df[name_col] = df[name_col].astype(str).str.strip()

    st.sidebar.title("🏒 Luleå/MSSK Profiles")

    # Joukkueen valinta
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

    # Pelaajan valinta
    players = [
        p
        for p in df_filtered[name_col].unique()
        if p and p != "nan" and p != "None"
    ]
    selected_player = st.sidebar.selectbox("👤 Select Player", players)

    st.session_state["selected_player"] = selected_player
    st.session_state["name_col"] = name_col
    st.session_state["team_col"] = team_col

    # Navigaatiosivut
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
