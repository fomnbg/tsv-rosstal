import mysql.connector
import os
import json
from dotenv import load_dotenv

# Lade die Werte aus der .env Datei
load_dotenv()

def load_used_member_numbers(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if isinstance(data, dict):
                return set(data.get("used_numbers", []))
            else:
                return set()
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def save_used_member_numbers(file_path, used_numbers):
    with open(file_path, 'w') as file:
        json.dump(list(used_numbers), file)

def generate_member_numbers(starting_number, count, used_numbers):
    generated_numbers = []
    for i in range(count):
        number = f"{starting_number}-{i}" if i > 0 else starting_number
        while number in used_numbers:
            i += 1
            number = f"{starting_number}-{i}" if i > 0 else starting_number
        used_numbers.add(number)
        generated_numbers.append(number)
    return generated_numbers

def write_to_database(form_data):
    form_dict = dict(form_data)
    
    # Holen Sie sich die Mitgliedsnummer oder verwenden Sie 10000 als Standardwert
    base_number = form_dict.get('membership_number', 10000)
    
    for i in range(1, 6):
        if f'vn{i}' in form_dict and form_dict[f'vn{i}']:
            vorname = form_dict.get(f'vn{i}', '')
            nachname = form_dict.get(f'nn{i}', '')
            geburtsdatum = form_dict.get(f'date{i}', '')
            email = form_dict.get(f'email{i}', '')
            mobile = form_dict.get(f'mobile{i}', '')
            sportart_member = form_dict.get(f'sportart_member{i}', '')
            geschlecht = form_dict.get(f'gender{i}', '')

            # Load used member numbers
            used_numbers = load_used_member_numbers('used_member_numbers.json')

            # Generate member numbers starting from a new base number
            member_numbers = generate_member_numbers(base_number, 1, used_numbers)

            try:
                connection = mysql.connector.connect(
                    host=os.environ.get('DB_HOST'),
                    user=os.environ.get('DB_USER'),
                    password=os.environ.get('DB_PASSWORD'),
                    database=os.environ.get('DB_NAME'),
                    port='3306'
                )
                cursor = connection.cursor()

                insert_query = "INSERT INTO fom_test2 (vorname, nachname, geburtsdatum, email, telefon, sportart, geschlecht, mitgliedsnummer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

                for number in member_numbers:
                    cursor.execute(insert_query, (vorname, nachname, geburtsdatum, email, mobile, sportart_member, geschlecht, number))

                save_used_member_numbers('used_member_numbers.json', used_numbers)

                connection.commit()
                cursor.close()
                connection.close()

            except Exception as e:
                print(f"Fehler beim Schreiben in die Datenbank: {e}")

