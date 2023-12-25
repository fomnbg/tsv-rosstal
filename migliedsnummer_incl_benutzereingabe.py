import random

class MitgliedsnummerGenerator:
    def __init__(self):
        self.generated_numbers = set()

    def generiere_mitgliedsnummer(self):
        while True:
            mitgliedsnummer = random.randint(1000, 9999)
            if mitgliedsnummer not in self.generated_numbers:
                self.generated_numbers.add(mitgliedsnummer)
                return mitgliedsnummer

class Mitglied:
    def __init__(self, geschlecht, vorname, nachname, geburtsdatum, plz, ort, handynummer):
        self.geschlecht = geschlecht
        self.vorname = vorname
        self.nachname = nachname
        self.geburtsdatum = geburtsdatum
        self.plz = plz
        self.ort = ort
        self.handynummer = handynummer
        self.mitgliedsnummer = None

    def setze_mitgliedsnummer(self, mitgliedsnummer):
        self.mitgliedsnummer = mitgliedsnummer

# Beispiel zur Verwendung des Codes
if __name__ == "__main__":
    generator = MitgliedsnummerGenerator()

    mitglieder = []

    while True:
        geschlecht = input("Geschlecht des Mitglieds (oder 'exit' zum Beenden): ")
        if geschlecht.lower() == 'exit':
            break

        vorname = input("Vorname des Mitglieds: ")
        nachname = input("Nachname des Mitglieds: ")
        geburtsdatum = input("Geburtsdatum des Mitglieds: ")
        plz = input("Postleitzahl des Mitglieds: ")
        ort = input("Ort des Mitglieds: ")
        handynummer = input("Handynummer des Mitglieds: ")

        mitglied = Mitglied(geschlecht, vorname, nachname, geburtsdatum, plz, ort, handynummer)
        mitglied.setze_mitgliedsnummer(generator.generiere_mitgliedsnummer())

        mitglieder.append(mitglied)

    for index, mitglied in enumerate(mitglieder, start=1):
        print(f"\nMitglied {index}:")
        print(f"Geschlecht: {mitglied.geschlecht}")
        print(f"Vorname: {mitglied.vorname}")
        print(f"Nachname: {mitglied.nachname}")
        print(f"Geburtsdatum: {mitglied.geburtsdatum}")
        print(f"PLZ: {mitglied.plz}")
        print(f"Ort: {mitglied.ort}")
        print(f"Handynummer: {mitglied.handynummer}")
        print(f"Mitgliedsnummer: {mitglied.mitgliedsnummer}")
