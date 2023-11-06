from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(50))
    user_name = db.Column(db.String(50))
    time = db.Column(db.String(50))
    result = db.Column(db.String(50))
    date = db.Column(db.String(50))