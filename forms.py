from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, FormField

class Mitglied(FlaskForm): 
    vorname = StringField()
    nachname = StringField()
    geburtsdatum = DateField()
    e-Mail = StringField()
    telefon = StringField()
    sportart = StringField()
    straße_hausnummer = StringField()
    ort_plz = StringField()

class Kontoverbindung(FlaskForm): 
    iban = StringField()
    bic = StringField()

class Unterschrift(FlaskForm): 
    image = FileField(u'Image File', [validators.regexp(u'^[^/\\]\.jpg$')])

class Antrag(FlaskForm): 
    zahlendes_Mitglied = FormField(Mitglied)
    familien_Mitglied_1 = FormField(Mitglied)
    familien_Mitglied_2 = FormField(Mitglied)
    familien_Mitglied_3 = FormField(Mitglied)
    familien_Mitglied_4 = FormField(Mitglied)
    konto = FormField(Kontoverbindung)
    g-recaptcha-response = StringField()



