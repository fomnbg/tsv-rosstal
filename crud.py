import mysql.connector
import os
import json
from dotenv import load_dotenv

load_dotenv()


def load_used_member_numbers(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'next_membership_number': 10000, 'used_numbers': []}


def save_used_member_numbers(file_path, used_numbers):
    with open(file_path, 'w') as file:
        json.dump(used_numbers, file)


def generate_member_numbers(starting_number, count, used_numbers):
    generated_numbers = []
    for i in range(count):
        number = f"{starting_number}-{i}" if i > 0 else starting_number
        while number in used_numbers['used_numbers']:
            i += 1
            number = f"{starting_number}-{i}" if i > 0 else starting_number
        used_numbers['used_numbers'].append(number)
        generated_numbers.append(number)
    return generated_numbers


def write_to_database(form_data):
    for i in range(1, 6):
        if f'vn{i}' in form_data and form_data[f'vn{i}']:
            vorname = form_data.get(f'vn{i}', '')
            nachname = form_data.get(f'nn{i}', '')
            geburtsdatum = form_data.get(f'date{i}', '')
            email = form_data.get(f'email{i}', '')
            mobile = form_data.get(f'mobile{i}', '')
            sportart_member = form_data.get(f'sportarten_member{i}', '')
            geschlecht = form_data.get(f'gender{i}', '')

            if i == 1:
                adresse = form_data.get('adresse', '')
                ort = form_data.get('ort', '')
                iban = form_data.get('iban', '')
            else:
                adresse = ort = iban = None

            used_numbers = load_used_member_numbers('used_member_numbers.json')

            base_number = used_numbers['next_membership_number']

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

                insert_query = "INSERT INTO mitgliedstest (vorname, nachname, geburtsdatum, email, telefon, sportart, geschlecht, mitgliedsnummer, adresse, ort, iban) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                for number in member_numbers:
                    cursor.execute(insert_query, (
                    vorname, nachname, geburtsdatum, email, mobile, sportart_member, geschlecht, number, adresse, ort, iban ))

                used_numbers['next_membership_number'] += 1

                save_used_member_numbers('used_member_numbers.json', used_numbers)

                connection.commit()
                cursor.close()
                connection.close()

            except Exception as e:
                print(f"Fehler beim Schreiben in die Datenbank: {e}")
