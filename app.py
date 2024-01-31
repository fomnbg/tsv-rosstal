from flask import Flask, render_template, redirect, url_for, request, abort, flash
from urllib import response
import requests
import secrets
from forms import Antrag
from flask import Flask, render_template, request
from pdf_generator import download_pdf
import csv
from database import write_to_database

app = Flask(__name__)

#app setup
foo = secrets.token_urlsafe(16)
app.secret_key = foo
app.static_folder = 'static'

#db_setup global
#app.config['SQLALCHEMY_DATABASE_URL'] = ''
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#DB = SQLAlchemy(app)

#für site key und secret key frag entweder Philipp oder hol dir deine eigenen auf https://www.google.com/recaptcha/admin/create?hl=de
#!!! V3 RECAPTCHA !!!#
SITE_KEY = '6Lf7LxkpAAAAAKZT2zaDVLVPMYP1PQqBj5usMKWz'
SECRET_KEY = '6Lf7LxkpAAAAAKfrwOGJRp_AKPKQMCLeemLN5bxf'
VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'


#views
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

@app.route('/mitgliedsantrag', methods=["GET", "POST"])
def mitgliedsantrag():
    if request.method == 'POST':
        print(request.form)

        ###
        # recaptcha handling
        ###
        secret_response = request.form['g-recaptcha-response']
        verify_response = requests.post(url=f'{VERIFY_URL}?secret={SECRET_KEY}&response={secret_response}').json()
        #print("secret-response:", secret_response)
        if verify_response['success'] == False or verify_response['score'] < 0.7:
            abort(401)#if bot detected or recaptcha request failed
        else:
            ###
            # write to database
            ###
            write_to_database(request.form)
            return render_template('daten-uebermittelt.html')
        
        


    else:
        sportarten_a = []
        sportarten_k = []
        sportarten_l = []
        
        with open('static/fileAblage/sportarten-allgemein.txt', 'r', encoding='utf-8-sig') as file:
            lines = file.readlines()
        sportarten_a = [line.strip() for line in lines]

        with open('static/fileAblage/sportarten-kinder_seniorensport.txt', 'r', encoding='utf-8-sig') as file:
            lines = file.readlines()
        sportarten_k = [line.strip() for line in lines]

        with open('static/fileAblage/sportarten-leistungssport.txt', 'r', encoding='utf-8-sig') as file:
            lines = file.readlines()
        sportarten_l = [line.strip() for line in lines]
        del lines

        print(sportarten_a)
        print(sportarten_k)
        print(sportarten_l)

        return render_template('mitgliedsantrag.html', site_key=SITE_KEY, sportarten_a = sportarten_a, sportarten_k = sportarten_k, sportarten_l = sportarten_l)

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
