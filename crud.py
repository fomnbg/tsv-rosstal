import mysql.connector
import os
from dotenv import load_dotenv

# Lade die Werte aus der .env Datei
load_dotenv()

def write_to_database(form_data):
    # Überprüfung, ob Person 2, 3, 4 und 5 vorhanden sind
    for i in range(1, 6):
        if f'vn{i}' in form_data and form_data[f'vn{i}']:
            # Speichern der Inhalte von allen Personen in einzelnen Variablen
            vorname = form_data.get(f'vn{i}', '')
            nachname = form_data.get(f'nn{i}', '')
            geburtsdatum = form_data.get(f'date{i}', '')
            email = form_data.get(f'email{i}', '')
            mobile = form_data.get(f'mobile{i}', '')
            sportart_member = form_data.get(f'sportart_member{i}', '')

            # Verbindung zur Datenbank herstellen
            try:
                connection = mysql.connector.connect(
                    host= os.environ.get('DB_HOST'),
                    user=os.environ.get('DB_USER'),
                    password=os.environ.get('DB_PASSWORD'),
                    database=os.environ.get('DB_NAME'),
                    port = '3306'
                )
                cursor = connection.cursor()

                # SQL-Befehl für das Einfügen der Daten in die Tabelle
                insert_query = "INSERT INTO nutzertest (vorname, nachname, geburtsdatum, email, telefon, sportart) VALUES (%s, %s, %s, %s, %s, %s)"

                # Daten in die Tabelle einfügen
                cursor.execute(insert_query, (vorname, nachname, geburtsdatum, email, mobile, sportart_member))

                # Änderungen bestätigen und Verbindung schließen
                connection.commit()
                cursor.close()
                connection.close()

            except Exception as e:
                print(f"Fehler beim Schreiben in die Datenbank: {e}")
