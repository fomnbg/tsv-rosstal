import os
from flask import Flask, request, send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer, Image as PlatypusImage
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import HexColor
from PIL import Image as PILImage
from io import BytesIO
import base64
import datetime
from reportlab.lib.units import inch


app = Flask(__name__)

def generate_pdf(signature_data, file_path):
    signature_image = PILImage.open(BytesIO(base64.b64decode(signature_data.split(',')[1])))

    doc = SimpleDocTemplate(file_path, pagesize=letter, leftMargin=30, rightMargin=30)
    story = []

    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    style_heading = styles["Heading2"]

    # Global table styles
    global_table_style = [
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Left-align content
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),  # Left padding for the table
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),  # Right padding for the table
        ('LEFTINDENT', (0, 0), (-1, -1), 0),
        ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#333333')),  # Text color
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#CCCCCC'))  # Table grid color
    ]

    # Überschrift Mitgliedsantrag hinzufügen (mittig)
    story.append(Paragraph("Mitgliedsantrag", style_heading))  # Überschrift hinzufügen
    story.append(Spacer(1, 12))  # Leerraum nach der Überschrift

    # Table for application type
    application_type = [
        ["Art des Antrags", ""]
    ]
    application_table = Table(application_type, colWidths=[2*inch, 2*inch], rowHeights=0.25*inch)
    application_table.setStyle(global_table_style)

    # Add the table to the story
    story.append(application_table)

    # Tabelle für persönliche Informationen...
    personal_info = [
        ["Geschlecht:", ""],
        ["Vorname:", ""],
        ["Name:", ""],
        ["Geburtsdatum:", ""],
        ["E-Mail:", ""],
        ["Telefon/Mobil:", ""],
        ["Ich bin bereit ehrenamtliche Tätigkeiten zu übernehmen", ""]
    ]

    data = [
        [Paragraph(item[0], style_normal), Paragraph(item[1], style_normal)] for item in personal_info
    ]

    personal_table = Table(data, colWidths=[2*inch, 2*inch], rowHeights=0.25*inch)
    personal_table.setStyle(global_table_style)

    story.append(Paragraph("Persönliche Informationen", style_heading))
    story.append(personal_table)
    story.append(Spacer(1, 0.2*inch))

    # Sport selection table
    story.append(Paragraph("Sportarten", style_heading))
    sports = [
        "Handball", "Mutter-/Kind", "Basketball", "Fußball", "Ballschule", "Boule",
        "Turnen", "Seniorensport", "Tae Bo", "Judo", "Klettern", "Pilates", "Badminton",
        "Volleyball", "Fitness", "Tischtennis", "Indica", "Power Workout", "Kinderturnen",
        "Faustball", "Passives Mitglied"
    ]
    sport_table = Table([[f"[ ] {sport}"] for sport in sports], colWidths=300, rowHeights=20)
    sport_table.setStyle(global_table_style)
    story.append(sport_table)

    # Address table
    story.append(Paragraph("Adresse", style_heading))
    address_info = [
        ["Straße:", ""],
        ["Hausnummer:", ""],
        ["Postleitzahl:", ""],
        ["Stadt:",""]
    ]
    address_table = Table(address_info, colWidths=[2*inch, 2*inch], rowHeights=0.25*inch)
    address_table.setStyle(global_table_style)
    story.append(address_table)

    # Bank data table
    story.append(Paragraph("Bankdaten", style_heading))
    bank_info = [
        ["IBAN:", ""],
        ["BIC:", ""]
    ]
    bank_table = Table(bank_info, colWidths=[2*inch, 2*inch], rowHeights=0.25*inch)
    bank_table.setStyle(global_table_style)
    story.append(bank_table)

     # Antrag bestätigt Abschnitt
    confirm_heading = "Antrag bestätigt"

    confirm_table_data = [
        ["Unterschrift:", None],
        ["Antrag gesendet:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    ]

    # Convert signature image to base64 string
    buffered = BytesIO()
    signature_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    confirm_table_data[0][1] = PlatypusImage(BytesIO(base64.b64decode(img_str)), width=100, height=50)
    
    confirm_table = Table(confirm_table_data, colWidths=[2*inch, 2*inch], rowHeights=0.5*inch)
    confirm_table.setStyle(global_table_style)

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
