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

def generate_pdf(file_path, persons1, persons2, persons3, persons4, persons5, sport_person1, sport_person2, sport_person3, sport_person4, sport_person5, membership_type, adresse, ort, kontoinhaber, iban, bic, signature_data1, signature_data2):
    signature_image1 = PILImage.open(BytesIO(base64.b64decode(signature_data1.split(',')[1])))
    
    if signature_data2 is not None:
        signature_image2 = PILImage.open(BytesIO(base64.b64decode(signature_data2.split(',')[1])))

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
        [Paragraph("Art des Antrags", style_bold), membership_type]
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

    # Sportarten ------------------------------------------
    story.append(Paragraph("Gewählte Sportarten", style_heading))
    sport_person1 = [item.replace("Tae Bo", "Tae-Bo").replace("Power Workout", "Power-Workout").replace("Passives Mitglied", "Passives-Mitglied") for item in sport_person1]
    sport_person1_string = ', '.join(sport_person1).replace(' ', ', ').lstrip(', ').rstrip(', ')
    story.append(Paragraph(sport_person1_string))
    
    # Start 2. Person ------------------------------------------------
    if f'vn2' in request.form:
        mitglied2 = [
            ["Geschlecht:", persons2['gender']],
            ["Vorname:", persons2['vn']],
            ["Name:", persons2['nn']],
            ["Geburtsdatum:", persons2['date']],
            ["E-Mail:", persons2['email']],
            ["Telefon/Mobil:", persons2['mobile']],
            ["Ehrenamtliche Tätigkeit:", "Ja"]
        ]

        data_mitlgied2 = [
            [item if isinstance(item, PlatypusImage) else item for item in row] for row in mitglied2
        ]

        
        # Identifiziere die Indizes der ersten und vierten Spalte
        first_column_indices = [0, 2]
        fourth_column_indices = [3, 5]

        # Erstelle die aktualisierte Datenstruktur für das zahlende Mitglied
        data_mitlgied2 = [
            [
                Paragraph(row[i], style_bold) if idx in first_column_indices else row[i]
                for idx, i in enumerate(range(len(row)))
            ] for row in mitglied2
        ]

        table_mitglied2 = Table(data_mitlgied2, colWidths=col_widths_application, rowHeights=0.25*inch)
        table_mitglied2.setStyle(global_table_style)
        table_mitglied2.hAlign = 'LEFT'
        story.append(Paragraph("______________________________________________________________________________", style_heading))
        story.append(Paragraph("Persönliche Informationen zweite Person", style_heading))
        story.append(table_mitglied2)
        story.append(Spacer(1, 0.2*inch))

        # Sportarten ------------------------------------------
        story.append(Paragraph("Gewählte Sportarten", style_heading))
        sport_person2 = [item.replace("Tae Bo", "Tae-Bo").replace("Power Workout", "Power-Workout").replace("Passives Mitglied", "Passives-Mitglied") for item in sport_person2]
        sport_person2_string = ', '.join(sport_person2).replace(' ', ', ').lstrip(', ').rstrip(', ')
        story.append(Paragraph(sport_person2_string))

    # Start 3. Person ------------------------------------------------
    if f'vn3' in request.form:
        mitglied3 = [
            ["Geschlecht:", persons3['gender']],
            ["Vorname:", persons3['vn']],
            ["Name:", persons3['nn']],
            ["Geburtsdatum:", persons3['date']],
            ["E-Mail:", persons3['email']],
            ["Telefon/Mobil:", persons3['mobile']],
            ["Ehrenamtliche Tätigkeit:", "Ja"]
        ]

        data_mitlgied3 = [
            [item if isinstance(item, PlatypusImage) else item for item in row] for row in mitglied3
        ]

        
        # Identifiziere die Indizes der ersten und vierten Spalte
        first_column_indices = [0, 2]
        fourth_column_indices = [3, 5]

        # Erstelle die aktualisierte Datenstruktur für das zahlende Mitglied
        data_mitlgied3 = [
            [
                Paragraph(row[i], style_bold) if idx in first_column_indices else row[i]
                for idx, i in enumerate(range(len(row)))
            ] for row in mitglied3
        ]

        table_mitglied3 = Table(data_mitlgied3, colWidths=col_widths_application, rowHeights=0.25*inch)
        table_mitglied3.setStyle(global_table_style)
        table_mitglied3.hAlign = 'LEFT'
        story.append(Paragraph("______________________________________________________________________________", style_heading))
        story.append(Paragraph("Persönliche Informationen dritte Person", style_heading))
        story.append(table_mitglied3)
        story.append(Spacer(1, 0.2*inch))


        # Sportarten ------------------------------------------
        story.append(Paragraph("Gewählte Sportarten", style_heading))
        sport_person3 = [item.replace("Tae Bo", "Tae-Bo").replace("Power Workout", "Power-Workout").replace("Passives Mitglied", "Passives-Mitglied") for item in sport_person3]
        sport_person3_string = ', '.join(sport_person3).replace(' ', ', ').lstrip(', ').rstrip(', ')
        story.append(Paragraph(sport_person3_string))

    # Start 4. Person ------------------------------------------------
    if f'vn4' in request.form:
        mitglied4 = [
            ["Geschlecht:", persons4['gender']],
            ["Vorname:", persons4['vn']],
            ["Name:", persons4['nn']],
            ["Geburtsdatum:", persons4['date']],
            ["E-Mail:", persons4['email']],
            ["Telefon/Mobil:", persons4['mobile']],
            ["Ehrenamtliche Tätigkeit:", "Ja"]
        ]

        data_mitlgied4 = [
            [item if isinstance(item, PlatypusImage) else item for item in row] for row in mitglied4
        ]

        
        # Identifiziere die Indizes der ersten und vierten Spalte
        first_column_indices = [0, 2]
        fourth_column_indices = [3, 5]

        # Erstelle die aktualisierte Datenstruktur für das zahlende Mitglied
        data_mitlgied4 = [
            [
                Paragraph(row[i], style_bold) if idx in first_column_indices else row[i]
                for idx, i in enumerate(range(len(row)))
            ] for row in mitglied4
        ]

        table_mitglied4 = Table(data_mitlgied4, colWidths=col_widths_application, rowHeights=0.25*inch)
        table_mitglied4.setStyle(global_table_style)
        table_mitglied4.hAlign = 'LEFT'
        story.append(Paragraph("______________________________________________________________________________", style_heading))
        story.append(Paragraph("Persönliche Informationen vierte Person", style_heading))
        story.append(table_mitglied4)
        story.append(Spacer(1, 0.2*inch))


        # Sportarten ------------------------------------------
        story.append(Paragraph("Gewählte Sportarten", style_heading))
        sport_person4 = [item.replace("Tae Bo", "Tae-Bo").replace("Power Workout", "Power-Workout").replace("Passives Mitglied", "Passives-Mitglied") for item in sport_person4]
        sport_person4_string = ', '.join(sport_person4).replace(' ', ', ').lstrip(', ').rstrip(', ')
        story.append(Paragraph(sport_person4_string))

    # Start 5. Person ------------------------------------------------
    if f'vn5' in request.form:
        mitglied5 = [
            ["Geschlecht:", persons5['gender']],
            ["Vorname:", persons5['vn']],
            ["Name:", persons5['nn']],
            ["Geburtsdatum:", persons5['date']],
            ["E-Mail:", persons5['email']],
            ["Telefon/Mobil:", persons5['mobile']],
            ["Ehrenamtliche Tätigkeit:", "Ja"]
        ]

        data_mitlgied5 = [
            [item if isinstance(item, PlatypusImage) else item for item in row] for row in mitglied5
        ]

        
        # Identifiziere die Indizes der ersten und vierten Spalte
        first_column_indices = [0, 2]
        fourth_column_indices = [3, 5]

        # Erstelle die aktualisierte Datenstruktur für das zahlende Mitglied
        data_mitlgied5 = [
            [
                Paragraph(row[i], style_bold) if idx in first_column_indices else row[i]
                for idx, i in enumerate(range(len(row)))
            ] for row in mitglied5
        ]

        table_mitglied5 = Table(data_mitlgied5, colWidths=col_widths_application, rowHeights=0.25*inch)
        table_mitglied5.setStyle(global_table_style)
        table_mitglied5.hAlign = 'LEFT'
        story.append(Paragraph("______________________________________________________________________________", style_heading))
        story.append(Paragraph("Persönliche Informationen fünfte Person", style_heading))
        story.append(table_mitglied5)
        story.append(Spacer(1, 0.2*inch))


        #Sportarten 5. Person ------------

        # Sportarten ------------------------------------------
        story.append(Paragraph("Gewählte Sportarten", style_heading))
        sport_person5 = [item.replace("Tae Bo", "Tae-Bo").replace("Power Workout", "Power-Workout").replace("Passives Mitglied", "Passives-Mitglied") for item in sport_person5]
        sport_person5_string = ', '.join(sport_person5).replace(' ', ', ').lstrip(', ').rstrip(', ')
        story.append(Paragraph(sport_person5_string))

    # Tabelle für Antrag bestätigt ------------------------------------------
    confirm_heading = "Antrag bestätigt"

    if 'signature-2' in request.form and request.form['signature-2']:
        confirm_table_data = [
        [Paragraph("Zustimmung:", style_bold), "Zustimmung zu AGB, Datenschutz, Lastschrifteinzug erteilt."],
        [Paragraph("Unterschrift:", style_bold), None, None],
        [None, None, None],
        [Paragraph("Antrag gesendet:", style_bold), datetime.datetime.now().strftime("%d.%m.%Y %H:%M")]
    ]

    else:
        confirm_table_data = [
        [Paragraph("Zustimmung:", style_bold), "Zustimmung zu AGB, Datenschutz, Lastschrifteinzug erteilt."],
        [Paragraph("Unterschrift:", style_bold), None, None],
        [Paragraph("Antrag gesendet:", style_bold), datetime.datetime.now().strftime("%d.%m.%Y %H:%M")]
    ]

    # Signatur-Bild zu base64 string konvertieren
    buffered1 = BytesIO()
    signature_image1.save(buffered1, format="PNG")
    img_str1 = base64.b64encode(buffered1.getvalue()).decode('utf-8')

    if signature_data2 is not None:
        buffered2 = BytesIO()
        signature_image2.save(buffered2, format="PNG")
        img_str2 = base64.b64encode(buffered2.getvalue()).decode('utf-8')

    # Signaturen zu den entsprechenden Tabellenzeilen hinzufügen
    if signature_data2 is not None:
        confirm_table_data[1][1] = PlatypusImage(BytesIO(base64.b64decode(img_str2)), width=100, height=30)
        confirm_table_data[1][2] = Paragraph(f"{persons1['vn']} {persons1['nn']}")
        
        confirm_table_data[2][1] = PlatypusImage(BytesIO(base64.b64decode(img_str1)), width=100, height=30)
        confirm_table_data[2][2] = Paragraph(f"{persons2['vn']} {persons2['nn']}")
    
    else:
        confirm_table_data[1][1] = PlatypusImage(BytesIO(base64.b64decode(img_str1)), width=100, height=30)
        confirm_table_data[1][2] = Paragraph(f"{persons1['vn']} {persons1['nn']}")



    confirm_table = Table(confirm_table_data, colWidths=col_widths, rowHeights=0.5*inch)
    confirm_table.setStyle(global_table_style)
    confirm_table.hAlign = 'LEFT'

    story.append(Paragraph("______________________________________________________________________________", style_heading))
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
            if request.form[f'gender{i}'] == "M":
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

    leereSignatur = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAogAAACCCAYAAADFTTn1AAAHf0lEQVR4Xu3ZIQ7EMBAEwfj/nw51QKTmU4eXbK1BK3cePwIECBAgQIAAAQKXwKFBgAABAgQIECBA4BYQiN4DAQIECBAgQIDAR0AgehAECBAgQIAAAQIC0RsgQIAAAQIECBD4F/AF0esgQIAAAQIECBDwBdEbIECAAAECBAgQ8AXRGyBAgAABAgQIEIgC/mKOUMYIECBAgAABAisCAnHl0vYkQIAAAQIECEQBgRihjBEgQIAAAQIEVgQE4sql7UmAAAECBAgQiAICMUIZI0CAAAECBAisCAjElUvbkwABAgQIECAQBQRihDJGgAABAgQIEFgREIgrl7YnAQIECBAgQCAKCMQIZYwAAQIECBAgsCIgEFcubU8CBAgQIECAQBQQiBHKGAECBAgQIEBgRUAgrlzangQIECBAgACBKCAQI5QxAgQIECBAgMCKgEBcubQ9CRAgQIAAAQJRQCBGKGMECBAgQIAAgRUBgbhyaXsSIECAAAECBKKAQIxQxggQIECAAAECKwICceXS9iRAgAABAgQIRAGBGKGMESBAgAABAgRWBATiyqXtSYAAAQIECBCIAgIxQhkjQIAAAQIECKwICMSVS9uTAAECBAgQIBAFBGKEMkaAAAECBAgQWBEQiCuXticBAgQIECBAIAoIxAhljAABAgQIECCwIiAQVy5tTwIECBAgQIBAFBCIEcoYAQIECBAgQGBFQCCuXNqeBAgQIECAAIEoIBAjlDECBAgQIECAwIqAQFy5tD0JECBAgAABAlFAIEYoYwQIECBAgACBFQGBuHJpexIgQIAAAQIEooBAjFDGCBAgQIAAAQIrAgJx5dL2JECAAAECBAhEAYEYoYwRIECAAAECBFYEBOLKpe1JgAABAgQIEIgCAjFCGSNAgAABAgQIrAgIxJVL25MAAQIECBAgEAUEYoQyRoAAAQIECBBYERCIK5e2JwECBAgQIEAgCgjECGWMAAECBAgQILAiIBBXLm1PAgQIECBAgEAUEIgRyhgBAgQIECBAYEVAIK5c2p4ECBAgQIAAgSggECOUMQIECBAgQIDAioBAXLm0PQkQIECAAAECUUAgRihjBAgQIECAAIEVAYG4cml7EiBAgAABAgSigECMUMYIECBAgAABAisCAnHl0vYkQIAAAQIECEQBgRihjBEgQIAAAQIEVgQE4sql7UmAAAECBAgQiAICMUIZI0CAAAECBAisCAjElUvbkwABAgQIECAQBQRihDJGgAABAgQIEFgREIgrl7YnAQIECBAgQCAKCMQIZYwAAQIECBAgsCIgEFcubU8CBAgQIECAQBQQiBHKGAECBAgQIEBgRUAgrlzangQIECBAgACBKCAQI5QxAgQIECBAgMCKgEBcubQ9CRAgQIAAAQJRQCBGKGMECBAgQIAAgRUBgbhyaXsSIECAAAECBKKAQIxQxggQIECAAAECKwICceXS9iRAgAABAgQIRAGBGKGMESBAgAABAgRWBATiyqXtSYAAAQIECBCIAgIxQhkjQIAAAQIECKwICMSVS9uTAAECBAgQIBAFBGKEMkaAAAECBAgQWBEQiCuXticBAgQIECBAIAoIxAhljAABAgQIECCwIiAQVy5tTwIECBAgQIBAFBCIEcoYAQIECBAgQGBFQCCuXNqeBAgQIECAAIEoIBAjlDECBAgQIECAwIqAQFy5tD0JECBAgAABAlFAIEYoYwQIECBAgACBFQGBuHJpexIgQIAAAQIEooBAjFDGCBAgQIAAAQIrAgJx5dL2JECAAAECBAhEAYEYoYwRIECAAAECBFYEBOLKpe1JgAABAgQIEIgCAjFCGSNAgAABAgQIrAgIxJVL25MAAQIECBAgEAUEYoQyRoAAAQIECBBYERCIK5e2JwECBAgQIEAgCgjECGWMAAECBAgQILAiIBBXLm1PAgQIECBAgEAUEIgRyhgBAgQIECBAYEVAIK5c2p4ECBAgQIAAgSggECOUMQIECBAgQIDAioBAXLm0PQkQIECAAAECUUAgRihjBAgQIECAAIEVAYG4cml7EiBAgAABAgSigECMUMYIECBAgAABAisCAnHl0vYkQIAAAQIECEQBgRihjBEgQIAAAQIEVgQE4sql7UmAAAECBAgQiAICMUIZI0CAAAECBAisCAjElUvbkwABAgQIECAQBQRihDJGgAABAgQIEFgREIgrl7YnAQIECBAgQCAKCMQIZYwAAQIECBAgsCIgEFcubU8CBAgQIECAQBQQiBHKGAECBAgQIEBgRUAgrlzangQIECBAgACBKCAQI5QxAgQIECBAgMCKgEBcubQ9CRAgQIAAAQJRQCBGKGMECBAgQIAAgRUBgbhyaXsSIECAAAECBKKAQIxQxggQIECAAAECKwICceXS9iRAgAABAgQIRAGBGKGMESBAgAABAgRWBATiyqXtSYAAAQIECBCIAgIxQhkjQIAAAQIECKwICMSVS9uTAAECBAgQIBAFBGKEMkaAAAECBAgQWBEQiCuXticBAgQIECBAIAoIxAhljAABAgQIECCwIiAQVy5tTwIECBAgQIBAFHgBIG8AgzZprpcAAAAASUVORK5CYII='

    signature_data1 = request.form['signature-1']

    if 'signature-2' in request.form and not request.form['signature-2'] == leereSignatur:
        signature_data2 = request.form['signature-2']

    else:
    # Andernfalls ist 'signature-2' nicht vorhanden oder hat die Klasse 'hidden-opacity'
       signature_data2 = None

    # Angemeldete Sportarten abfragen

    sportarten = {
    'Person1': [],
    'Person2': [],
    'Person3': [],
    'Person4': [],
    'Person5': [],
}

    for i in range(1, 5):  # Abrage für die 5 Personen
        if f'sportarten_member{i}' in request.form:
            sportarten[f'Person{i}'].append(request.form[f'sportarten_member{i}'])

    # PDF Struktur mit Werten befüllen
    generate_pdf(file_path, persons['Person1'], persons['Person2'], persons['Person3'], persons['Person4'], persons['Person5'], sportarten['Person1'], sportarten['Person2'], sportarten['Person3'], sportarten['Person4'], sportarten['Person5'], membership_type, adresse, ort, kontoinhaber, iban, bic, signature_data1, signature_data2)

    return send_file(
        file_path,
        as_attachment=True,
        mimetype='application/pdf',
        download_name='Mitgliedsantrag.pdf'
    )

if __name__ == "__main__":
    app.run(debug=True)