from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from sqlalchemy.orm import relationship
from app import db
from werkzeug.datastructures import ImmutableMultiDict


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

    # TODO sportart

    #Getting values of Response Form Mode
    if 'female' in data:
        female_value = data.get('female')
        if female_value == 'on':
            gender1 = 'female'
        else:
            gender1 = 'male'
    vorname1 = data.get('vorname1')
    nachname1 = data.get('nachname1')
    geburtsdatum1 = data.get('geburtsdatum')
    email1 = data.get('email1')
    phonenumber1 = data.get('phonenumber1')
    # sportart hier

    if 'familyFemale' in data:
        female_value = data.get('familyFemale')
        if female_value == 'on':
            gender2 = 'female'
        else:
            gender2 = 'male'
    vorname2 = data.get('vorname2')
    nachname2 = data.get('nachname2')
    geburtsdatum2 = data.get('geburtsdatum2')
    email2 = data.get('email2')
    phonenumber2 = data.get('phonenumber2')
    #sportart hier

    if 'recommendationFemale' in data:
        female_value = data.get('recommendationFemale')
        if female_value == 'on':
            gender3 = 'female'
        else:
            gender3 = 'male'
    vorname3 = data.get('vorname3')
    nachname3 = data.get('nachname3')
    geburtsdatum3 = data.get('geburtsdatum3')
    email3 = data.get('email3')
    phonenumber3 = data.get('phonenumber3')
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

        db.session.add(familienmitglied1, family_id=zahlendesmitglied.id)
        db.session.commit()

    except:
        pass

    return True
