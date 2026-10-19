from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

from aussaatrechner.database import add_observation, connect, empirical_success, list_observations
from aussaatrechner.engine import recommend
from aussaatrechner.models import GardenObservation
from aussaatrechner.repository import load_plants
from aussaatrechner.solar import day_length_hours


ROOT = Path(__file__).resolve().parent
PLANT_DATA = ROOT / "data" / "plants.json"
DB_PATH = ROOT / "data" / "garden.db"

METHOD_LABELS = {
    "outdoor": "Freiland",
    "protected": "Geschützt / Gewächshaus / Frühbeet",
}

st.set_page_config(page_title="Aussaatrechner MVP", page_icon="🌱", layout="wide")

plants = load_plants(PLANT_DATA)
conn = connect(DB_PATH)

st.title("SOFTWAREENTWICKLER")
st.subheader("Aussaatrechner MVP 0.1")
st.caption(
    "Baseline für ein späteres standort-, licht-, wetter- und datenbasiertes "
    "Garden Decision Support System."
)

with st.expander("Was dieser MVP wissenschaftlich noch NICHT behauptet", expanded=True):
    st.write(
        "Der Eignungsscore ist **keine Erfolgswahrscheinlichkeit**. "
        "Er ist eine transparente Heuristik auf Basis quellenbasierter "
        "Aussaatfenster. Tageslänge wird bereits berechnet, aber noch nicht "
        "als kulturspezifischer Wachstumsfaktor in den Score eingerechnet."
    )

tab_now, tab_data, tab_sources = st.tabs(
    ["Was kann ich säen?", "Eigene Gartendaten", "Quellen & Modell"]
)

with tab_now:
    st.markdown("### Standort und Zeitpunkt")

    with st.form("recommendation_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            target_date = st.date_input("Datum", value=date.today())
        with col2:
            latitude = st.number_input(
                "Breitengrad",
                min_value=-90.0,
                max_value=90.0,
                value=51.0,
                step=0.01,
                help="Beispielwert. Später wird hier die Adress-/Kartenabfrage angeschlossen.",
            )
        with col3:
            longitude = st.number_input(
                "Längengrad",
                min_value=-180.0,
                max_value=180.0,
                value=10.0,
                step=0.01,
                help="Im MVP nur Kontext; für die Tageslängendauer ist er nicht nötig.",
            )

        method_label = st.selectbox("Anbauart", options=list(METHOD_LABELS.values()))
        submitted = st.form_submit_button("Empfehlungen berechnen")

    if submitted:
        method = next(key for key, value in METHOD_LABELS.items() if value == method_label)
        daylight = day_length_hours(latitude, target_date)

        st.markdown("### Standortkontext")
        m1, m2, m3 = st.columns(3)
        m1.metric("Tageslänge", f"{daylight:.2f} h")
        m2.metric("Breitengrad", f"{latitude:.2f}°")
        m3.metric("Längengrad", f"{longitude:.2f}°")

        st.info(
            "Tageslänge ist hier astronomischer Kontext. Bewölkung, Verschattung, "
            "Globalstrahlung, Temperatur und Bodenbedingungen fehlen noch."
        )

        empirical_rates = {
            plant.crop_id: empirical_success(conn, plant.crop_id)
            for plant in plants
        }
        recs = recommend(
            plants=plants,
            target_date=target_date,
            method=method,
            empirical_rates=empirical_rates,
        )

        if not recs:
            st.warning("Für diese Anbauart sind im kleinen MVP-Datensatz noch keine Kulturen hinterlegt.")
        else:
            st.markdown("### Ergebnis")
            for rec in recs:
                with st.container(border=True):
                    left, right = st.columns([3, 1])
                    with left:
                        st.markdown(f"#### {rec.name_de}")
                        st.caption(rec.scientific_name)
                        st.write(f"**Einstufung:** {rec.category}")
                        st.write(rec.reason)
                        st.write(f"**Quellenhinweis:** {rec.source_text}")
                        st.markdown(f"[Quelle öffnen]({rec.source_url})")
                    with right:
                        st.metric("Eignungsscore", f"{rec.suitability_score}/100")
                        if rec.empirical_success_rate is None:
                            st.caption(
                                f"Eigene Daten: n={rec.empirical_n}. "
                                "Ab n=5 zeigt der MVP die beobachtete Erfolgsrate."
                            )
                        else:
                            st.metric(
                                "Eigene Erfolgsrate",
                                f"{rec.empirical_success_rate * 100:.0f}%",
                            )
                            st.caption(
                                f"n={rec.empirical_n}; beobachtete Quote, "
                                "noch keine kalibrierte Prognose."
                            )

with tab_data:
    st.markdown("### Beobachtung aus dem eigenen Garten erfassen")
    st.write(
        "Im MVP gilt eine Kultur als **erfolgreich**, wenn sie eine nutzbare "
        "Erntereife erreicht hat."
    )

    plant_options = {p.name_de: p.crop_id for p in plants}

    with st.form("observation_form"):
        col1, col2 = st.columns(2)
        with col1:
            crop_name = st.selectbox("Kultur", options=list(plant_options.keys()))
            sowing_date = st.date_input("Aussaatdatum", value=date.today(), key="obs_date")
            bed_name = st.text_input("Beet", value="Beet 1")
        with col2:
            method_label_obs = st.selectbox(
                "Anbauart", options=list(METHOD_LABELS.values()), key="obs_method"
            )
            success_label = st.selectbox(
                "Ergebnis",
                ["Erfolgreich – nutzbare Erntereife erreicht", "Nicht erfolgreich"],
            )
            harvest_kg = st.number_input(
                "Erntemenge in kg (optional)",
                min_value=0.0,
                value=0.0,
                step=0.1,
            )

        notes = st.text_area(
            "Notizen", placeholder="z. B. Schneckenfraß, Trockenheit, Schatten …"
        )
        save = st.form_submit_button("Beobachtung speichern")

    if save:
        crop_id = plant_options[crop_name]
        method = next(
            key for key, value in METHOD_LABELS.items() if value == method_label_obs
        )
        success = success_label.startswith("Erfolgreich")
        harvest_value = None if harvest_kg == 0 else float(harvest_kg)

        if not bed_name.strip():
            st.error("Bitte einen Beetnamen angeben.")
        else:
            obs = GardenObservation(
                crop_id=crop_id,
                sowing_date=sowing_date,
                bed_name=bed_name,
                method=method,
                success=success,
                harvest_kg=harvest_value,
                notes=notes,
            )
            add_observation(conn, obs)
            st.success("Beobachtung gespeichert.")

    rows = list_observations(conn)
    st.markdown("### Gespeicherte Beobachtungen")
    if rows:
        df = pd.DataFrame(rows)
        df["Kultur"] = df["crop_id"].map({p.crop_id: p.name_de for p in plants})
        df["Erfolg"] = df["success"].map({1: "ja", 0: "nein"})
        df["Anbauart"] = df["method"].map(METHOD_LABELS)
        shown = df[
            [
                "id",
                "Kultur",
                "sowing_date",
                "bed_name",
                "Anbauart",
                "Erfolg",
                "harvest_kg",
                "notes",
            ]
        ].rename(
            columns={
                "id": "ID",
                "sowing_date": "Aussaat",
                "bed_name": "Beet",
                "harvest_kg": "Ernte kg",
                "notes": "Notizen",
            }
        )
        st.dataframe(shown, use_container_width=True, hide_index=True)
        st.download_button(
            "Beobachtungen als CSV exportieren",
            data=shown.to_csv(index=False).encode("utf-8"),
            file_name="garten_beobachtungen.csv",
            mime="text/csv",
        )
    else:
        st.caption("Noch keine Beobachtungen gespeichert.")

with tab_sources:
    st.markdown("### Modellgrenzen")
    st.write(
        """
        **Version 0.1 ist absichtlich ein Baseline-Modell.**

        - Aussaatfenster: quellenbasiert, aber teilweise nur monatsweise angenähert.
        - Eignungsscore: Projekt-Heuristik, keine Wahrscheinlichkeit.
        - Tageslänge: astronomisch berechnet; noch ohne Globalstrahlung oder Verschattung.
        - Wetter: noch nicht integriert.
        - Google-/Karten-Daten: noch nicht integriert.
        - Eigene Daten: werden bereits strukturiert gesammelt.
        """
    )

    st.markdown("### Pflanzendaten und Quellen")
    source_rows = []
    for plant in plants:
        for window in plant.windows:
            source_rows.append(
                {
                    "Kultur": plant.name_de,
                    "Methode": METHOD_LABELS[window.method],
                    "Monate": f"{window.start_month}–{window.end_month}",
                    "Quellengenauigkeit": window.source_precision,
                    "Quellenaussage": window.source_text,
                    "URL": window.source_url,
                }
            )
    st.dataframe(pd.DataFrame(source_rows), use_container_width=True, hide_index=True)

    st.markdown("### Nächster Umbaupunkt")
    st.write(
        "Die Recommendation Engine liegt getrennt von UI, Datenbank und Pflanzendaten. "
        "Wir können im nächsten Schritt Wetter-/Strahlungsdaten hinzufügen, ohne "
        "die komplette Anwendung neu zu schreiben."
    )
