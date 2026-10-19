# Aussaatrechner

Ein modularer, quellenorientierter MVP für ein späteres **Garden Decision Support System**.

## Projektidee

Das Projekt entstand aus einer praktischen Frage im eigenen Garten:

> Was kann ich an meinem Standort heute noch sinnvoll aussäen – und wie kann ich meine Gartenfläche über das Jahr besser für die Eigenversorgung nutzen?

Der aktuelle Stand ist bewusst ein Baseline-System. Er kombiniert quellenbasierte Aussaatfenster, astronomische Tageslänge und eigene Gartendaten. Eine echte statistische Erfolgswahrscheinlichkeit ist noch nicht Bestandteil des MVP.

## Status

**Version:** 0.1.1 – Portfolio-ready baseline

### Bereits implementiert

- Streamlit-Weboberfläche
- modulare Recommendation Engine
- astronomische Tageslänge
- quellenverknüpfte Pflanzendaten
- lokale SQLite-Datenbank für Gartenbeobachtungen
- empirische Erfolgsrate ab fünf Beobachtungen
- automatisierte Tests
- Git-/Portfolio-Struktur

### Noch nicht implementiert

- automatische Adress-/Standortsuche
- Wetter- und Klimadaten
- Globalstrahlung
- Verschattung
- echtes probabilistisches Modell
- Fläche-×-Zeit-Optimierung
- Selbstversorgungsmodell

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Tests

```bash
pytest -q
```

## Projektstruktur

```text
aussaatrechner/
├── app.py
├── aussaatrechner/
├── data/
├── docs/
├── tests/
├── .env.example
├── .gitignore
├── CHANGELOG.md
├── README.md
├── pyproject.toml
└── requirements.txt
```

## Wissenschaftliche Arbeitsweise

Das Projekt trennt zwischen belegten Fakten, Annahmen, Heuristiken, Beobachtungen, Prognosen und Hypothesen. Der aktuelle Eignungsscore ist **keine Erfolgswahrscheinlichkeit**.

## Startdaten und Quellen

Die erste Pflanzendatenbank enthält bewusst nur wenige Kulturen. Quellen sind in `data/plants.json` direkt an den jeweiligen Einträgen hinterlegt. Die astronomische Tageslängenberechnung basiert auf NOAA-Solarformeln.

## Dokumentation

- [Entstehungsgeschichte](docs/01_entstehungsgeschichte.md)
- [Forschungsfrage](docs/02_forschungsfrage.md)
- [Architektur](docs/03_architektur.md)
- [Datenmodell](docs/04_datenmodell.md)
- [Modellgrenzen](docs/05_modellgrenzen.md)
- [Roadmap](docs/06_roadmap.md)

## Repository-Hygiene

Folgende Daten gehören ausdrücklich **nicht** ins öffentliche Repository: `.venv`, echte `.env`-Dateien und API-Schlüssel, lokale SQLite-Datenbanken, persönliche Gartendaten, Exporte sowie Cache- und Build-Dateien. Diese Dateien werden über `.gitignore` ausgeschlossen.
