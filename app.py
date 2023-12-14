from flask import Flask, render_template, redirect, url_for, request, abort, flash
from urllib import response
import requests
import secrets
from forms import Antrag
from database import write_to_database

#app.py Flask Konstruktor aufrufen
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

@app.route('/mitglied-werden')
def mitglied_werden():
    return render_template('mitglied-werden.html')

@app.route('/mitgliedsantrag', methods=["GET", "POST"])
def mitgliedsantrag():
    if request.method == 'POST': 
        print(request.form)       
        secret_response = request.form['g-recaptcha-response']
        verify_response = requests.post(url=f'{VERIFY_URL}?secret={SECRET_KEY}&response={secret_response}').json()
        #print("secret-response:", secret_response)
        if verify_response['success'] == False or verify_response['score'] < 0.7:
            abort(401)#if bot detected or recaptcha request failed
        else: 
            write_to_database(request.form)
            return render_template('daten-uebermittelt.html')

    else:
        return render_template('mitgliedsantrag.html', site_key=SITE_KEY)


#mainloop
if __name__ == '__main__':
    app.run(debug=True)