from app import db
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length, DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Integer)
    humidity = db.Column(db.Integer)

    def __repr__(self):
        return f'''Temp: {self.temp}F Humidity: {self.humidity}'''

class DistanceData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Integer)

    def __repr__(self):
        return f'''Distance: {self.distance}inches'''
