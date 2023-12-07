import os
from flask import Flask, request, send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer, Image as PlatypusImage
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image as PILImage
import datetime
from io import BytesIO
from base64 import b64decode
from reportlab.lib.units import inch

app = Flask(__name__)

def generate_pdf(signature_data, file_path):
    signature_image = PILImage.open(BytesIO(b64decode(signature_data.split(',')[1])))

    doc = SimpleDocTemplate(file_path, pagesize=letter, leftMargin=30, rightMargin=30)
    story = []

    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    style_heading = styles["Heading2"]

    # Membership type section...
    membership_type_text = "Mitgliedschaft   Neumitgliedschaft   Umstellung Familienmitgliedschaft   Antrag auf Beitragsbefreiung"
    story.append(Paragraph(f"O {membership_type_text}", style_normal))

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
    personal_table.setStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE')])

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

    # Konvertieren des PIL-Bildes in ein ReportLab-Bildobjekt
    image_buffer = BytesIO()
    signature_image.save(image_buffer, format="PNG")
    img = PlatypusImage(image_buffer)
    story.append(img)  # Das Bild wird der Geschichte hinzugefügt

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
