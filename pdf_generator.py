import os
from flask import Flask, request, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from base64 import b64decode
from PIL import Image
from io import BytesIO
import datetime

app = Flask(__name__)

def generate_pdf(signature_data, file_path):
    signature_image_data = b64decode(signature_data.split(',')[1])

    pdf = canvas.Canvas(file_path, pagesize=letter)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, "Mitgliedsantrag TSV Roßtal")

    pdf.setFont("Helvetica", 12)
    table_data = [
        ["Name:", ""],
        ["Vorname:", ""],
        ["Adresse:", ""],
        ["PLZ:", ""],
        ["Ort:", ""],
        ["Datum:", ""],
        ["Unterschrift:", ""]
    ]

    current_timestamp = datetime.datetime.now().strftime("%d.%m.%Y")
    table_data[5][1] = current_timestamp

    for row_index, row in enumerate(table_data):
        pdf.drawString(100, 700 - 50 * row_index, row[0])
        if row_index == 5:
            pdf.drawString(300, 700 - 50 * row_index, row[1])
            pdf.setStrokeColor(colors.lightgrey)  # Hellgraue Rahmenfarbe
            pdf.rect(300, 685 - 50 * row_index, 200, 50, stroke=1, fill=0)  # Anpassung der Höhe für die Unterschrift auf 50
        else:
            pdf.drawString(300, 700 - 50 * row_index, row[1])
            pdf.setStrokeColor(colors.lightgrey)  # Hellgraue Rahmenfarbe
            pdf.rect(300, 685 - 50 * row_index, 200, 50, stroke=1, fill=0)  # Beibehaltung der Höhe für andere Zellen auf 50

        if row_index == 6:
            signature_image = Image.open(BytesIO(signature_image_data))
            image_width, image_height = signature_image.size
            scale_factor = 190 / image_width if image_width > 0 else 1
            scaled_width = image_width * scale_factor
            scaled_height = image_height * scale_factor

            table_data[6][1] = pdf.drawInlineImage(signature_image, 305, 730 - 50 * row_index - scaled_height, width=scaled_width, height=scaled_height)

    pdf.save()

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    print("Route '/download_pdf' wurde aufgerufen.")
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
