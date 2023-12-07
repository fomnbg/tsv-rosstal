import os
from flask import Flask, request, send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer, Image as PlatypusImage
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image as PILImage
from io import BytesIO
from base64 import b64decode
from reportlab.lib.units import inch
import datetime

app = Flask(__name__)

def generate_pdf(signature_data, file_path):
    signature_image = PILImage.open(BytesIO(b64decode(signature_data.split(',')[1])))

    doc = SimpleDocTemplate(file_path, pagesize=letter, leftMargin=30, rightMargin=30)
    story = []

    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    style_heading = styles["Heading2"]

    # Überschrift Mitgliedsantrag hinzufügen
    story.append(Paragraph("Mitgliedsantrag", styles["Heading1"]))  # Überschrift hinzufügen
    story.append(Spacer(1, 12))  # Leerraum nach der Überschrift

    # Membership type section...
    membership_types = [
        "Mitgliedschaft", "Neumitgliedschaft", "Umstellung Familienmitgliedschaft", "Antrag auf Beitragsbefreiung"
    ]

    membership_table_data = [[f"[ ] {membership}", ""] for membership in membership_types]
    membership_table = Table(membership_table_data, colWidths=[2*inch, 2*inch], rowHeights=20)
    membership_table.setStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Linksbündig ausrichten
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),  # Linker Seitenabstand für die Tabelle
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),  # Rechter Seitenabstand für die Tabelle
    ])

    story.append(Paragraph("Mitgliedschaft", style_heading))
    story.append(membership_table)
    story.append(Spacer(1, 0.2*inch))

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
    personal_table.setStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Linksbündig ausrichten
                             ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')])

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
    story.append(sport_table)

    # Address table
    story.append(Paragraph("Adresse", style_heading))
    address_info = [
        ["Straße Hausnr.:", ""],
        ["Stadt, Postleitzahl:", ""]
    ]
    address_table = Table(address_info, colWidths=[2*inch, 2*inch], rowHeights=0.25*inch)
    story.append(address_table)

    # Bank data table
    story.append(Paragraph("Bankdaten", style_heading))
    bank_info = [
        ["IBAN:", ""],
        ["BIC:", ""]
    ]
    bank_table = Table(bank_info, colWidths=[2*inch, 2*inch], rowHeights=0.25*inch)
    story.append(bank_table)

     # Antrag bestätigt Abschnitt
    confirm_heading = "Antrag bestätigt"

  # Bild verkleinern und als BytesIO speichern
    max_width = 800  # Maximal erlaubte Breite
    max_height = 400  # Maximal erlaubte Höhe

    # Verkleinere das Bild unter Beibehaltung der Qualität
    signature_image.thumbnail((max_width, max_height), resample=PILImage.BICUBIC)

    signature_buffer = BytesIO()
    signature_image.save(signature_buffer, format="PNG")
    signature_buffer.seek(0)

    # Füge das temporäre Bild zur Tabelle hinzu
    confirm_table_data = [
        ["Unterschrift:", PlatypusImage(signature_buffer, width=100, height=50)],
        ["Antrag gesendet:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    ]
    
    confirm_table = Table(confirm_table_data, colWidths=[2*inch, 2*inch], rowHeights=0.5*inch)
    confirm_table.setStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Linksbündig ausrichten
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),  # Linker Seitenabstand für die Tabelle
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),  # Rechter Seitenabstand für die Tabelle
    ])

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