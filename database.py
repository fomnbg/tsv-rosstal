from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from sqlalchemy.orm import relationship
from .app import db

class Zahlendesmitglied(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(50))
    nachname = db.Column(db.String(50))
    geburtsdatum = db.Column(db.DateTime)
    e_mail = db.Column(db.String(60))
    telefonnr = db.Column(db.String(30))
    sportart = db.Column(db.String(30))
    adresse = db.Column(db.String(100))

    familienmitglied = relationship("Familienmitglied", backref="zahlendesmitglied") #-> 

class Familienmitglied(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    family_id = db.Column(db.Integer, db.ForeignKey('zahlendesmitglied.id'))
    vorname = db.Column(db.String(50))
    nachname = db.Column(db.String(50))
    geburtsdatum = db.Column(db.DateTime)
    e_mail = db.Column(db.String(60))
    telefonnr = db.Column(db.String(30))
    sportart = db.Column(db.String(30))
    adresse = db.Column(db.String(100))

def write_to_database(form)-> bool: 
    pass