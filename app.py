from flask import Flask, render_template, request
from pdf_generator import download_pdf

app = Flask(__name__)

app.static_folder = 'static'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download_pdf', methods=['GET', 'POST'])
def handle_pdf_download():
    if request.method == 'POST':
        # Hier rufen Sie Ihre modifizierte download_pdf-Funktion auf
        return download_pdf()
    else:
        # Wenn es sich um eine GET-Anfrage handelt, leiten Sie z.B. zurück zur Hauptseite
        return render_template('index.html')
    
@app.route('/mitglied-werden')
def mitglied_werden():
    return render_template('mitglied-werden.html')

@app.route('/mitgliedsantrag')
def mitgliedsantrag():
    return render_template('mitgliedsantrag.html')

@app.route('/pricelist')
def pricelist():
    return render_template('pricelist.html')


if __name__ == '__main__':
    app.run(debug=True)
