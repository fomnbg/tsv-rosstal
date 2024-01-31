from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from sqlalchemy.orm import relationship
from werkzeug.datastructures import ImmutableMultiDict

db = SQLAlchemy()

class Zahlendesmitglied(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(10))
    vorname = db.Column(db.String(50))
    nachname = db.Column(db.String(50))
    geburtsdatum = db.Column(db.DateTime)
    email = db.Column(db.String(60))
    telefonnr = db.Column(db.String(30))
    sportart = db.Column(db.String(30))
    adresse = db.Column(db.String(100))

    familienmitglied = relationship("Familienmitglied", backref="zahlendesmitglied")

class Familienmitglied(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    family_id = db.Column(db.Integer, db.ForeignKey('zahlendesmitglied.id'))
    gender = db.Column(db.String(10))
    vorname = db.Column(db.String(50))
    nachname = db.Column(db.String(50))
    geburtsdatum = db.Column(db.DateTime)
    email = db.Column(db.String(60))
    telefonnr = db.Column(db.String(30))
    sportart = db.Column(db.String(30))
    adresse = db.Column(db.String(100))

def write_to_database(form)-> bool: 
    data = ImmutableMultiDict(form)
    print(data)

    # TODO sportart

    if 'female1' in data:
        female_value = data.get('female1')
        if female_value == 'on':
            gender1 = 'female'
        else:
            gender1 = 'male'
    vorname1 = data.get('vn1')
    nachname1 = data.get('nn1')
    geburtsdatum1 = data.get('date1')
    email1 = data.get('email1')
    phonenumber1 = data.get('mobile1')
    # sportart hier

    if 'female2' in data:
        female_value2 = data.get('female2')
        if female_value2 == 'on':
            gender2 = 'female'
        else:
            gender2 = 'male'
    vorname2 = data.get('vn2')
    nachname2 = data.get('nn2')
    geburtsdatum2 = data.get('date2')
    email2 = data.get('email2')
    phonenumber2 = data.get('mobile2')
    #sportart hier

    if 'female3' in data:
        female_value3 = data.get('female3')
        if female_value3 == 'on':
            gender3 = 'female'
        else:
            gender3 = 'male'
    vorname3 = data.get('vorname3')
    nachname3 = data.get('nachname3')
    geburtsdatum3 = data.get('geburtsdatum3')
    email3 = data.get('email3')
    phonenumber3 = data.get('phonenumber3')
    #sportart hier

    if 'female4' in data:
        female_value4 = data.get('female4')
        if female_value4 == 'on':
            gender4 = 'female'
        else:
            gender4 = 'male'
    vorname4 = data.get('vorname4')
    nachname4 = data.get('nachname4')
    geburtsdatum4 = data.get('geburtsdatum4')
    email4 = data.get('email4')
    phonenumber4 = data.get('phonenumber4')
    #sportart hier

    if 'female5' in data:
        female_value = data.get('female5')
    if female_value == 'on':
        gender5 = 'female'
    else:
        gender5 = 'male'
    vorname5 = data.get('vorname5')
    nachname5 = data.get('nachname5')
    geburtsdatum5 = data.get('geburtsdatum5')
    email5 = data.get('email5')
    phonenumber5 = data.get('phonenumber5')
    #sportart hier

    try:
        zahlendesmitglied = Zahlendesmitglied(
            gender = gender1,
            vorname = vorname1,
            nachname = nachname1,
            geburtsdatum = geburtsdatum1,
            email = email1,
            telefonnr = phonenumber1
            # TODO adresse und sportart fehlen
        )

        db.session.add(zahlendesmitglied)
        db.session.commit()

        familienmitglied1 = Familienmitglied(
            gender = gender2,
            vorname = vorname2,
            nachname = nachname2,
            geburtsdatum = geburtsdatum2,
            email = email2,
            telefonnr = phonenumber2
            # TODO adresse und sportart
        )

        familienmitglied2 = Familienmitglied(
            gender = gender3,
            vorname = vorname3,
            nachname = nachname3,
            geburtsdatum = geburtsdatum3,
            email = email3,
            telefonnr = phonenumber3
            # TODO adresse und sportart
        )

        familienmitglied3 = Familienmitglied(
            gender = gender4,
            vorname = vorname4,
            nachname = nachname4,
            geburtsdatum = geburtsdatum4,
            email = email4,
            telefonnr = phonenumber4
            # TODO adresse und sportart
        )

        familienmitglied4 = Familienmitglied(
            gender = gender5,
            vorname = vorname5,
            nachname = nachname5,
            geburtsdatum = geburtsdatum5,
            email = email5,
            telefonnr = phonenumber5
            # TODO adresse und sportart
        )

        db.session.add(familienmitglied1, family_id=zahlendesmitglied.id)
        db.session.add(familienmitglied2, family_id=zahlendesmitglied.id)
        db.session.add(familienmitglied3, family_id=zahlendesmitglied.id)
        db.session.add(familienmitglied4, family_id=zahlendesmitglied.id)
        db.session.commit()

    except:
        pass
        # ? error handling? raise error oder extra nachricht?

    return True
