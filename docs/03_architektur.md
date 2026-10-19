# 3. Softwarearchitektur

## Ziel

Die Software ist modular aufgebaut, damit einzelne Komponenten später ausgetauscht oder erweitert werden können.

```text
Streamlit UI
    ↓
Recommendation Engine
    ↓
Plant Repository
    ↓
Garden Observation Database

zusätzlich:
Solar / Day-Length Module
```

## Aktuelle Module

### `app.py`
Benutzeroberfläche. Enthält keine zentrale Fachlogik, sondern ruft Fachmodule auf.

### `aussaatrechner/engine.py`
Regelbasierte Recommendation Engine.

### `aussaatrechner/models.py`
Datenstrukturen für Pflanzen, Aussaatfenster, Empfehlungen und Gartenbeobachtungen.

### `aussaatrechner/repository.py`
Lädt Pflanzendaten aus JSON.

### `aussaatrechner/database.py`
SQLite-Zugriff für persönliche Gartenbeobachtungen.

### `aussaatrechner/solar.py`
Astronomische Tageslängenberechnung.

## Geplante Erweiterungen

```text
Adresse
  ↓
Geocoding Provider
  ↓
Standortprofil
  ↓
Wetter-/Klimadaten
  ↓
Strahlungsdaten
  ↓
Recommendation Engine
  ↓
Garten-/Beetprofil
  ↓
empirisches Modell
```

Externe Anbieter sollen über austauschbare Schnittstellen angebunden werden, damit das Projekt nicht von einem einzelnen Dienst abhängig ist.
