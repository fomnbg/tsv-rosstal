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

def generate_pdf(signature_data, file_path):
    signature_image = PILImage.open(BytesIO(base64.b64decode(signature_data.split(',')[1])))

    # PDF Styling ------------------------------------------

    doc = SimpleDocTemplate(file_path, pagesize=letter, leftMargin=30, rightMargin=30)
    story = []

    #Überschriften
    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    style_heading = styles["Heading3"]
    style_heading0 = styles["Heading2"]

    #Tabellen
    global_table_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        #('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')), 
        #('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ])

    header_image_path = 'static/fileAblage/pdf_header.png'  # Header PNG öffnen
    header_image = PlatypusImage(header_image_path, width=letter[0], height=0.75*inch)  # PNG auf bolle Breite
    story.insert(0, header_image)  # Bild als erstes Element einfügen

    doc = SimpleDocTemplate(file_path, pagesize=letter, leftMargin=30, rightMargin=30, topMargin=0)  # TopMargin auf 0

    # Überschrift Mitgliedsantrag hinzufügen
    story.append(Spacer(1, 12))

    # Tabelle für Antragsart ------------------------------------------
    application_type = [
        ["Art des Antrags", ""]
    ]
    application_table = Table(application_type, colWidths=[2*inch, 2*inch], rowHeights=0.25*inch)
    application_table.setStyle(global_table_style)
    application_table.hAlign = 'LEFT'

    # Add the table to the story
    story.append(application_table)

    # Tabelle für Persönliche Informationen ------------------------------------------
    personal_info = [
        ["Geschlecht:", ""],
        ["Vorname:", ""],
        ["Name:", ""],
        ["Geburtsdatum:", ""],
        ["E-Mail:", ""],
        ["Telefon/Mobil:", ""],
        ["Ehrenamtliche Tätigkeit:", ""]
    ]

    data = [
        [Paragraph(item[0], style_normal), Paragraph(item[1], style_normal)] for item in personal_info
    ]

    personal_table = Table(data, colWidths=[2*inch, 2*inch], rowHeights=0.25*inch)
    personal_table.setStyle(global_table_style)
    personal_table.hAlign = 'LEFT'

    story.append(Paragraph("Persönliche Informationen", style_heading))
    story.append(personal_table)
    story.append(Spacer(1, 0.2*inch))

    # Tabelle für Sportarten ------------------------------------------
    story.append(Paragraph("Gewählte Sportarten", style_heading))
    sports = [
        "Handball", "Mutter-/Kind", "Basketball", "Fußball", "Ballschule", "Boule",
        "Turnen", "Seniorensport", "Tae Bo", "Judo", "Klettern", "Pilates", "Badminton",
        "Volleyball", "Fitness", "Tischtennis", "Indica", "Power Workout", "Kinderturnen",
        "Faustball", "Passives Mitglied"
    ]

    # Modifizierte Sports-Liste mit schmaler Spalte vorne
    sports_with_column = [[f" ", f"  {sport}"] for sport in sports]
    sport_table = Table(sports_with_column, colWidths=[20, 280], rowHeights=20)  # Breite der Spalten angepasst
    sport_table.setStyle(global_table_style)
    sport_table.hAlign = 'LEFT'
    story.append(sport_table)

    # Tabelle für Adresse ------------------------------------------
    story.append(Paragraph("Adresse", style_heading))
    address_info = [
        ["Straße:", ""],
        ["Hausnummer:", ""],
        ["Postleitzahl:", ""],
        ["Stadt:",""]
    ]
    address_table = Table(address_info, colWidths=[2*inch, 2*inch], rowHeights=0.25*inch)
    address_table.setStyle(global_table_style)
    address_table.hAlign = 'LEFT'
    story.append(address_table)

    # Tabelle für Bankdaten ------------------------------------------
    story.append(Paragraph("Bankdaten", style_heading))
    bank_info = [
        ["IBAN:", ""],
        ["BIC:", ""]
    ]
    bank_table = Table(bank_info, colWidths=[2*inch, 2*inch], rowHeights=0.25*inch)
    bank_table.setStyle(global_table_style)
    bank_table.hAlign = 'LEFT'
    story.append(bank_table)

     # Tabelle für Antrag bestätigt ------------------------------------------
    confirm_heading = "Antrag bestätigt"

    confirm_table_data = [
        ["Unterschrift:", None],
        ["Antrag gesendet:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    ]

    # Signatur-Bild zu base64 string konvertieren
    buffered = BytesIO()
    signature_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    confirm_table_data[0][1] = PlatypusImage(BytesIO(base64.b64decode(img_str)), width=100, height=30)
    
    confirm_table = Table(confirm_table_data, colWidths=[2*inch, 2*inch], rowHeights=0.5*inch)
    confirm_table.setStyle(global_table_style)
    confirm_table.hAlign = 'LEFT'

    story.append(Paragraph(confirm_heading, style_heading))
    story.append(confirm_table)

    doc.build(story)


@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    signature_data = request.form['signature']
    file_path = os.path.join('static', 'fileAblage', 'unterschrift.pdf')

    generate_pdf(signature_data, file_path)

    return send_file(
        file_path,
        as_attachment=True,
        mimetype='application/pdf',
        download_name='unterschrift.pdf'
    )

if __name__ == "__main__":
    app.run(debug=True)
