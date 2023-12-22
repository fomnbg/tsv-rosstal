from collections.abc import Mapping, Sequence
from typing import Any
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, DateField, RadioField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError
import re

class LoginForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(min=6, max=150)], render_kw={"placeholder": "E-Mail"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    first_name = StringField(render_kw={"placeholder": "Vorname"})
    last_name = StringField(render_kw={"placeholder": "Nachname"})
    email = EmailField(render_kw={"placeholder": "E-Mail"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_email(self, email: EmailField):
        # Valid: ["leonard@kruppa.de", max.mustermann@muter-firma.com]
        # Invalid: ["mäx@muster_firma.d"]
        email_pattern = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email.data):
            raise ValidationError("Email is out of expected range.")
        
class LoginForm(FlaskForm):
    title         = RadioField()
    sex           = RadioField()
    birthday      = DateField()
    phone_number  = StringField()
    street        = StringField()
    house_number  = StringField()
    plz           = IntegerField
    city          = StringField()
    accountholder = StringField()
    iban          = StringField()

    submit = SubmitField('Save')

    def validate_streete(self, street: StringField):
        # Valid: ["Im Espan", "Georg-Ohm-Straße", "Reifenberg"]
        # Invalid: ["Im Espan 7"]
        german_street_name_pattern = re.compile(r'^[a-zA-ZäöüÄÖÜß\s-]+$')

        if not german_street_name_pattern.match(street.data):
            raise ValidationError("Street name is out of expected range.")
        
    def validate_house_number(self, house_number):
        # Valid: ["123a", "12", "7", "16b"]
        # Invalid: ["c27", "56hallo", "23a6"]
        german_street_name_pattern = re.compile(r'^\d{1,}[a-zA-Z]?$')

        if not german_street_name_pattern.match(house_number.data):
            raise ValidationError("House number is out of expected range.")
       
    def validate_plz(self, plz):
        # Valid: ["91365"]
        # Invalid: ["D91365", "ABC", "123456"]
        german_postal_code_pattern = re.compile(r'^\d{5}$')

        if not german_postal_code_pattern.match(plz.data):
            raise ValidationError("PLZ number is out of expected range.")
    
    def validate_city(self, city):
        # Valid: ["Baden-Baden", "Frankfurt am Main", "Nürnberg"]
        # Invalid: ["91365 Weilersbach", "3rlangen"]
        german_postal_code_pattern = re.compile(r'[a-zA-ZäöüÄÖÜß\s-]+')

        if not german_postal_code_pattern.match(city.data):
            raise ValidationError("PLZ number is out of expected range.")
