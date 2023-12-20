import json
import os

def mitgliedsnummer_vergeben(vorname, nachname):
    mitglieder_dateipfad = "mitglieder.json"

    # Überprüfen, ob die JSON-Datei existiert
    if not os.path.exists(mitglieder_dateipfad):
        with open(mitglieder_dateipfad, "w") as f:
            json.dump({}, f)

    # Laden der bestehenden Zuordnung von Mitgliedsnummern
    with open(mitglieder_dateipfad, "r") as f:
        mitglieder_dict = json.load(f)

    # Überprüfen, ob die Mitgliedsnummer bereits vergeben ist
    for mitgliedsnummer, daten in mitglieder_dict.items():
        if daten["Vorname"] == vorname and daten["Nachname"] == nachname:
            return f"Mitgliedsnummer {mitgliedsnummer} bereits vergeben."

    # Neue Mitgliedsnummer generieren
    neue_mitgliedsnummer = len(mitglieder_dict) + 1

    # Hinzufügen der neuen Zuordnung von Mitgliedsnummer zu Vornamen und Nachnamen
    mitglieder_dict[str(neue_mitgliedsnummer)] = {"Vorname": vorname, "Nachname": nachname}

    # Speichern der aktualisierten Zuordnung in der JSON-Datei
    with open(mitglieder_dateipfad, "w") as f:
        json.dump(mitglieder_dict, f, indent=2)

    return f"Mitgliedsnummer {neue_mitgliedsnummer} für {vorname} {nachname} vergeben."

# Beispielaufruf
print(mitgliedsnummer_vergeben("Max", "Mustermann"))
print(mitgliedsnummer_vergeben("Anna", "Schmidt"))

