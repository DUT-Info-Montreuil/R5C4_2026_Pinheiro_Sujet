import json
import streamlit as st


@st.cache_data
def load_fixture(filename):
    try:
        with open(f"fixtures/{filename}", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def render_page1():
    st.title("📊 Vue Générale & Indicateurs Décisionnels")

    indicateurs_data = load_fixture("indicateurs.json")

    if indicateurs_data:
        st.caption(
            f"Période analysée : **{indicateurs_data.get('periode', 'N/A')}** "
            f"(Référence : **{indicateurs_data.get('periode_reference', 'N/A')}**)"
        )

        cols = st.columns(3)
        indicators = indicateurs_data.get("indicateurs", [])

        for idx, kpi in enumerate(indicators):
            with cols[idx % 3]:
                valeur = kpi.get("valeur")
                ecart = kpi.get("ecart")
                sens = kpi.get("sens")

                delta_str = None
                delta_color = "normal"

                if ecart is not None:
                    pct = ecart * 100
                    delta_str = f"{pct:+.1f}% vs ref"

                    # Si une hausse est défavorable (ex: hausse du temps d'attente), la couleur s'inverse
                    if sens == "hausse_defavorable":
                        delta_color = "inverse"

                st.metric(
                    label=kpi.get("nom", f"Indicateur {idx+1}"),
                    value=f"{valeur} {kpi.get('unite', '')}".strip(),
                    delta=delta_str,
                    delta_color=delta_color,
                )
    else:
        st.warning("Fixture 'indicateurs.json' non trouvée dans le dossier fixtures/.")

    st.markdown("---")
    st.info(
        "💡 *Note Séance 3 : Les 3 visualisations Plotly seront développées lors de la Séance 4.*"
    )