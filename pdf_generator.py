import os
from flask import Flask, request, send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image as PlatypusImage
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import HexColor
from PIL import Image as PILImage
from io import BytesIO
import base64
import datetime
from reportlab.lib.units import inch
from reportlab.lib import colors



app = Flask(__name__)

def generate_pdf(file_path, persons1, persons2, persons3, persons4, persons5, sport_person1, sport_person2, sport_person3, sport_person4, sport_person5, membership_type, adresse, ort, kontoinhaber, iban, bic, signature_data):
    signature_image = PILImage.open(BytesIO(base64.b64decode(signature_data.split(',')[1])))

    # PDF Styling ------------------------------------------

    doc = SimpleDocTemplate(file_path, pagesize=letter, leftMargin=30, rightMargin=30)
    story = []

    #Überschriften
    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    style_heading = styles["Heading3"]
    style_heading0 = styles["Heading2"]

    #Fett-Style
    style_bold = styles["Normal"]
    style_bold.fontName = "Helvetica-Bold"  # Setting font to bold

    #Tabellen
    global_table_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')), 
        #('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ])

    col_widths_application = [1.8*inch, 2.2*inch, 1.4*inch, 2*inch]  # Breite Spalten application_table
    col_widths = [1.8*inch, 2*inch]  # Breite Spalten
    col_widths_sports = [1.8*inch, 2*inch, 1.8*inch]  # Breite Spalten application_table

    header_image_path = 'static/fileAblage/pdf_header.png'  # Header PNG öffnen
    header_image = PlatypusImage(header_image_path, width=letter[0], height=0.75*inch)  # PNG auf bolle Breite
    story.insert(0, header_image)  # Bild als erstes Element einfügen

    doc = SimpleDocTemplate(file_path, pagesize=letter, leftMargin=30, rightMargin=30, topMargin=0)  # TopMargin auf 0

    # Überschrift Mitgliedsantrag hinzufügen
    story.append(Spacer(1, 12))

    # Tabelle für Antragsart ------------------------------------------
    if membership_type == "fee-exemption":
        membership_type = "Antrag auf Beitragsbefreiung"
    
    if membership_type == "family-membership":
        membership_type = "Familienitgliedschaft"

    if membership_type == "new-membership":
        membership_type = "Neumitgliedschaft"

    application_type = [
        ["Art des Antrags", membership_type]
    ]
    application_table = Table(application_type, colWidths=col_widths, rowHeights=0.25*inch)
    application_table.setStyle(global_table_style)
    application_table.hAlign = 'LEFT'

    # Add the table to the story
    story.append(application_table)

    # Tabelle für Persönliche Informationen Zahlendes Mitglied ------------------------------------------
    
    zahlendes_mitglied = [
        ["Geschlecht:", persons1['gender'], "Adresse:", adresse],
        ["Vorname:", persons1['vn'], "Postleitzahl, Ort:", ort],
        ["Name:", persons1['nn'], "", ""],
        ["Geburtsdatum:", persons1['date'], "Bankverbindung", ""],
        ["E-Mail:", persons1['email'], "Kontoinhaber:", kontoinhaber],
        ["Telefon/Mobil:", persons1['mobile'], "IBAN:", iban],
        ["Ehrenamtliche Tätigkeit:", "Ja", "BIC:", bic]
    ]

    data_zahlendes_mitglied = [
        [item if isinstance(item, PlatypusImage) else item for item in row] for row in zahlendes_mitglied
    ]

    
    # Identifiziere die Indizes der ersten und vierten Spalte
    first_column_indices = [0, 2]
    fourth_column_indices = [3, 5]

    # Erstelle die aktualisierte Datenstruktur für das zahlende Mitglied
    data_zahlendes_mitglied = [
        [
            Paragraph(row[i], style_bold) if idx in first_column_indices else row[i]
            for idx, i in enumerate(range(len(row)))
        ] for row in zahlendes_mitglied
    ]

    table_zahlendes_mitglied = Table(data_zahlendes_mitglied, colWidths=col_widths_application, rowHeights=0.25*inch)
    table_zahlendes_mitglied.setStyle(global_table_style)
    table_zahlendes_mitglied.hAlign = 'LEFT'

    story.append(Paragraph("Persönliche Informationen Antragsteller", style_heading))
    story.append(table_zahlendes_mitglied)
    story.append(Spacer(1, 0.2*inch))

    # Tabelle für Sportarten ------------------------------------------
    story.append(Paragraph("Gewählte Sportarten", style_heading))
    
    header_row = [
    Paragraph("Allgemein:", style_bold),
    Paragraph("Leistungssport:", style_bold),
    Paragraph("Kinder-/Seniorensport:", style_bold)
]

    table_sport1 = [header_row]

    # Finde die maximale Länge der Werte in den Kategorien, um die Anzahl der Zeilen zu bestimmen
    max_length = max(
        len(sport_person1.get('Allgemein', [])),
        len(sport_person1.get('Leistungssport', [])),
        len(sport_person1.get('Kinder-/Seniorensport', []))
    )

    # Erhöhe die Indizes, um neue Werte hinzuzufügen, ohne vorhandene zu überschreiben
    for i in range(max_length):
        row = ["", "", ""]  # Leere Zeile für die Sportarten

        # Füge die Werte der Allgemein-Kategorie in die Tabelle ein
        
        if i < len(sport_person1.get('Allgemein', [])):
            row[0] = sport_person1['Allgemein'][i]

        # Füge die Werte der Leistungssport-Kategorie in die Tabelle ein
        if i < len(sport_person1.get('Leistungssport', [])):
            row[1] = sport_person1['Leistungssport'][i]

        # Füge die Werte der Kinder-/Seniorensport-Kategorie in die Tabelle ein
        if i < len(sport_person1.get('Kinder-/Seniorensport', [])):
            row[2] = sport_person1['Kinder-/Seniorensport'][i]

        table_sport1.append(row)

    sport_table = Table(table_sport1, colWidths=col_widths_sports, rowHeights=20)  # Breite der Spalten angepasst
    sport_table.setStyle(global_table_style)
    sport_table.hAlign = 'LEFT'

    story.append(sport_table)

    # Tabelle für Antrag bestätigt ------------------------------------------
    confirm_heading = "Antrag bestätigt"

    confirm_table_data = [
        ["Zustimmung:", "Zustimmung zu AGB, Datenschutz, Lastschrifteinzug erteilt."],
        ["Unterschrift:", None],
        ["Antrag gesendet:", datetime.datetime.now().strftime("%d.%m.%Y %H:%M")]
    ]

    # Signatur-Bild zu base64 string konvertieren
    buffered = BytesIO()
    signature_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    confirm_table_data[1][1] = PlatypusImage(BytesIO(base64.b64decode(img_str)), width=100, height=30)
    
    confirm_table = Table(confirm_table_data, colWidths=col_widths, rowHeights=0.5*inch)
    confirm_table.setStyle(global_table_style)
    confirm_table.hAlign = 'LEFT'

    story.append(Paragraph(confirm_heading, style_heading))
    story.append(confirm_table)

    doc.build(story)


@app.route('/mitgliedsantrag', methods=["GET", "POST"])
def download_pdf():
    
    #Zwischenablage
    file_path = os.path.join('static', 'fileAblage', 'Mitgliedsantrag.pdf')

    # Variablen aus Form Requesten

    # Persönliche Daten für max 5 Personen abfragen (1. Person = Zahlendes Mitglied, anderen Personen optional )
    persons = {
        'Person1': {'gender': None, 'vn': None, 'nn': None, 'date': None, 'email': None, 'mobile': None},
        'Person2': {'gender': None, 'vn': None, 'nn': None, 'date': None, 'email': None, 'mobile': None},
        'Person3': {'gender': None, 'vn': None, 'nn': None, 'date': None, 'email': None, 'mobile': None},
        'Person4': {'gender': None, 'vn': None, 'nn': None, 'date': None, 'email': None, 'mobile': None},
        'Person5': {'gender': None, 'vn': None, 'nn': None, 'date': None, 'email': None, 'mobile': None}
    }

    for i in range(1, 6):  # 5 Personen von 1 bis 5
        if f'vn{i}' in request.form:            
            if f'male{i}' in request.form:
                persons[f'Person{i}']['gender'] = 'Männlich'
            else:
                persons[f'Person{i}']['gender'] = 'Weiblich'
        if f'vn{i}' in request.form:
            persons[f'Person{i}']['vn'] = request.form[f'vn{i}']
        if f'nn{i}' in request.form:
            persons[f'Person{i}']['nn'] = request.form[f'nn{i}']
        if f'date{i}' in request.form:
            persons[f'Person{i}']['date'] = request.form[f'date{i}']
        if f'email{i}' in request.form:
            persons[f'Person{i}']['email'] = request.form[f'email{i}']
        if f'mobile{i}' in request.form:                                    # Überprüfe, ob Daten vorhanden sind, bevor sie dem Dictionary hinzugefügt werden
            persons[f'Person{i}']['mobile'] = request.form[f'mobile{i}']    # Zugriffbeispiel: persons['Person3']['vn']
    
    # Restlichen Daten Zahlendes Mitglied
    membership_type = request.form['membership-type']
    
    adresse = request.form['adresse']
    ort = request.form['ort']

    kontoinhaber = request.form['kontoinhaber']
    iban = request.form['iban']
    bic = request.form['bic']

    signature_data = request.form['signature']

    # Angemeldete Sportarten abfragen

    sportarten = {
    'Person1': {
        'Allgemein': [],
        'Leistungssport': [],
        'Kinder-/Seniorensport': []
    },
    'Person2': {
        'Allgemein': [],
        'Leistungssport': [],
        'Kinder-/Seniorensport': []
    },
    'Person3': {
        'Allgemein': [],
        'Leistungssport': [],
        'Kinder-/Seniorensport': []
    },
    'Person4': {
        'Allgemein': [],
        'Leistungssport': [],
        'Kinder-/Seniorensport': []
    },
    'Person5': {
        'Allgemein': [],
        'Leistungssport': [],
        'Kinder-/Seniorensport': []
    }
}

    for i in range(1, 5):  # Abrage für die 5 Personen
        if f'klettern{i}' in request.form:
            sportarten[f'Person{i}']['Allgemein'].append("Klettern")
        if f'volleyball{i}' in request.form:
            sportarten[f'Person{i}']['Allgemein'].append("Volleyball")
        if f'indiaca{i}' in request.form:
            sportarten[f'Person{i}']['Allgemein'].append("Indiaca")
        if f'faustball{i}' in request.form:
            sportarten[f'Person{i}']['Allgemein'].append("Faustball")
        if f'basketball{i}' in request.form:
            sportarten[f'Person{i}']['Allgemein'].append("Basketball")
        if f'boule{i}' in request.form:
            sportarten[f'Person{i}']['Allgemein'].append("Boule")
        if f'tae_bo{i}' in request.form:
            sportarten[f'Person{i}']['Allgemein'].append("Tae Bo")
        if f'pilates{i}' in request.form:
            sportarten[f'Person{i}']['Allgemein'].append("Pilates")
        if f'fitness{i}' in request.form:
            sportarten[f'Person{i}']['Allgemein'].append("Fitness")
        if f'power_workout{i}' in request.form:
            sportarten[f'Person{i}']['Allgemein'].append("Power Workout")
        if f'passives_mitglied{i}' in request.form:
            sportarten[f'Person{i}']['Allgemein'].append("Passives Mitglied")

        if f'handball{i}' in request.form:
            sportarten[f'Person{i}']['Leistungssport'].append("Handball")
        if f'fussball{i}' in request.form:
            sportarten[f'Person{i}']['Leistungssport'].append("Fußball")
        if f'turnen{i}' in request.form:
            sportarten[f'Person{i}']['Leistungssport'].append("Turnen")
        if f'judo{i}' in request.form:
            sportarten[f'Person{i}']['Leistungssport'].append("Sportarten")
        if f'badminton{i}' in request.form:
            sportarten[f'Person{i}']['Leistungssport'].append("Badminton")
        if f'tischtennis{i}' in request.form:
            sportarten[f'Person{i}']['Leistungssport'].append("Tischtennis")

        if f'kinderturnen{i}' in request.form:
            sportarten[f'Person{i}']['Kinder-/Seniorensport'].append("Kinderturnen")
        if f'mutter_kind{i}' in request.form:
            sportarten[f'Person{i}']['Kinder-/Seniorensport'].append("Mutter-/Kind")
        if f'ballschule{i}' in request.form:
            sportarten[f'Person{i}']['Kinder-/Seniorensport'].append("Ballschule")
        if f'seniorensport{i}' in request.form:
            sportarten[f'Person{i}']['Kinder-/Seniorensport'].append("Seniorensport")

    # PDF Struktur mit Werten befüllen
    generate_pdf(file_path, persons['Person1'], persons['Person2'], persons['Person3'], persons['Person4'], persons['Person5'], sportarten['Person1'], sportarten['Person2'], sportarten['Person3'], sportarten['Person4'], sportarten['Person5'], membership_type, adresse, ort, kontoinhaber, iban, bic, signature_data)

    return send_file(
        file_path,
        as_attachment=True,
        mimetype='application/pdf',
        download_name='Mitgliedsantrag.pdf'
    )

if __name__ == "__main__":
    app.run(debug=True)
