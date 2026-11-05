import json
import streamlit as st


@st.cache_data
def load_fixture(filename):
    try:
        with open(f"fixtures/{filename}", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def render_page2():
    st.title("📋 Consultation des Parties")

    parties_data = load_fixture("parties.json")

    if parties_data:
        parties_list = parties_data.get("data", [])
        total_parties = parties_data.get("total", len(parties_list))
        limit = parties_data.get("limit", 20)

        st.write(f"**{total_parties}** parties trouvées (Affichage par page de {limit})")

        # Contrôle de pagination fictive basée sur la fixture
        col_page, col_blank = st.columns([1, 3])
        with col_page:
            st.number_input("Page", min_value=1, value=1, step=1)

        # Affichage du tableau de parties
        st.dataframe(parties_list, use_container_width=True)
    else:
        st.warning("Fixture 'parties.json' non trouvée dans le dossier fixtures/.")