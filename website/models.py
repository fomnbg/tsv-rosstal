from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    data    = db.Column(db.String(10000))
    date    = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id                  = db.Column(db.Integer, primary_key=True)
    first_name          = db.Column(db.String(150))
    last_name           = db.Column(db.String(150))
    email               = db.Column(db.String(150), unique=True)
    password            = db.Column(db.String(150))
    notes               = db.relationship('Note')
    profile             = db.relationship('Profile')
    courseregistrations = db.relationship('Courseregistration')

class Profile(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('user.id'))
    title         = db.Column(db.String(150))
    sex           = db.Column(db.String(150))
    birthday      = db.Column(db.String(150))
    phone_number  = db.Column(db.String(150))
    street        = db.Column(db.String(150))
    house_number  = db.Column(db.String(150))
    plz           = db.Column(db.String(150))
    city          = db.Column(db.String(150))
    accountholder = db.Column(db.String(150))
    iban          = db.Column(db.String(150))

class Sporttype(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(150))
    sportcourses = db.relationship('Sportcourse')

class Sportcourse(db.Model):
    id                  = db.Column(db.Integer, primary_key=True)
    sporttype           = db.Column(db.Integer, db.ForeignKey('sporttype.id'))
    instructor          = db.Column(db.Integer, db.ForeignKey('user.id'))
    min_participants    = db.Column(db.String(150))
    max_participants    = db.Column(db.String(150))
    courseregistrations = db.relationship('Courseregistration')

class Courseregistration(db.Model):
    id             = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey('user.id'))
    sportcourse_id = db.Column(db.Integer, db.ForeignKey('sportcourse.id'))
