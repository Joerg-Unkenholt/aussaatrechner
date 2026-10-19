# 4. Datenmodell

## Pflanzendaten

Aktuell werden Pflanzendaten in `data/plants.json` gespeichert.

Wichtige Felder:

- `crop_id`
- deutscher Name
- wissenschaftlicher Name
- Aussaatfenster
- Anbaumethode
- Quellenpräzision
- Quellenaussage
- Quell-URL

## Gartenbeobachtungen

SQLite-Tabelle `observations`:

- ID
- Kultur-ID
- Aussaatdatum
- Beetname
- Anbaumethode
- Erfolg/Misserfolg
- optionale Erntemenge
- Notizen
- Erstellungszeitpunkt

## Aktuelle Erfolgsdefinition

Im MVP gilt eine Kultur als erfolgreich, wenn sie eine **nutzbare Erntereife** erreicht hat.

Diese Definition ist eine Vereinfachung. Spätere Versionen sollen mindestens unterscheiden:

- Keimung
- Etablierung
- Erntereife
- Ertrag
- Qualität
- Kulturzeit
- Ausfallgründe

## Datenschutz

Lokale Gartendaten und persönliche Daten werden nicht in das öffentliche Git-Repository aufgenommen. Die `.gitignore` schließt lokale Datenbanken und private Exportordner aus.
