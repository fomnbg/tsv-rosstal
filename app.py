from flask import Flask, render_template, request
from pdf_generator import download_pdf
import csv

app = Flask(__name__)

app.static_folder = 'static'

@app.route('/')
def index():
    return render_template('index.html')

# Obsolete - wird nicht mehr benötigt, da die Funktion in price_list.html implementiert wurde
#
# @app.route('/download_pdf', methods=['GET', 'POST'])
# def handle_pdf_download():
#     if request.method == 'POST':
#         # Hier rufen Sie Ihre modifizierte download_pdf-Funktion auf
#         return download_pdf()
#     else:
#         # Wenn es sich um eine GET-Anfrage handelt, leiten Sie z.B. zurück zur Hauptseite
#         return render_template('index.html')
    
@app.route('/mitglied-werden')
def mitglied_werden():
    return render_template('mitglied-werden.html')

@app.route('/mitgliedsantrag')
def mitgliedsantrag():
    return render_template('mitgliedsantrag.html')

@app.route('/pricelist')
def pricelist():
    data = []
    with open('static/fileAblage/data.csv', 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.reader(file, delimiter=';')
        for row in csv_reader:
            data.append(row)
    return render_template('pricelist.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
