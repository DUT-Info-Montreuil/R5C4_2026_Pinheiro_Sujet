import json
import streamlit as st
from views.page1 import render_page1
from views.page2 import render_page2

st.set_page_config(
    page_title="Pilotage des Files de Jeu",
    page_icon="🎮",
    layout="wide",
)


@st.cache_data
def load_referentiel():
    try:
        with open("fixtures/referentiel.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


referentiel_data = load_referentiel()

# --- BARRE LATÉRALE (SIDEBAR) ---
st.sidebar.title("🎮 Pilotage des Files")

# Navigation entre les pages (conserve les filtres en changeant de page)
page_choice = st.sidebar.radio(
    "Navigation", ["Vue Générale & Indicateurs", "Consultation des Parties"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Filtres")

# Extraction des options du référentiel
if referentiel_data:
    annees_opts = ["Toutes"] + [str(a) for a in referentiel_data.get("annees", [])]
    serveurs_opts = ["Tous"] + [s["code"] for s in referentiel_data.get("serveurs", [])]
    jeux_opts = ["Tous"] + [j["nom"] for j in referentiel_data.get("jeux", [])]
    files_opts = ["Toutes"] + [f["nom"] for f in referentiel_data.get("files", [])]
else:
    annees_opts, serveurs_opts, jeux_opts, files_opts = ["Toutes"], ["Tous"], ["Tous"], ["Toutes"]

selected_annee = st.sidebar.selectbox("Année", annees_opts)
selected_serveur = st.sidebar.selectbox("Serveur", serveurs_opts)
selected_jeu = st.sidebar.selectbox("Jeu", jeux_opts)
selected_file = st.sidebar.selectbox("File", files_opts)

# --- RENDU DE LA PAGE ---
if page_choice == "Vue Générale & Indicateurs":
    render_page1()
elif page_choice == "Consultation des Parties":
    render_page2()