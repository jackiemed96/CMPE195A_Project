from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    def __repr__(self):
        return f'User: {self.first_name} with email: {self.email}'


class UserPlants(db.Model):
    '''Stores the searched plants by the user.'''
    __tablename__ = 'user_plants'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    plant = db.Column(db.String(200), db.ForeignKey('plants.name'))
    date_added = db.Column(db.DateTime, default=datetime.now)
    current = db.Column(db.Boolean, default=0)
    


class Plant(db.Model):
    __tablename__ = 'plants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    scientific_name = db.Column(db.String(200), unique=True)
    description = db.Column(db.String(600))
    soil = db.Column(db.String(600))
    water = db.Column(db.String(600))
    sunlight_requirements = db.Column(db.String(200))
    minimum_cold_hardiness = db.Column(db.String)

    def __repr__(self):
        return f'Plant name: {self.name} Scientific name: {self.scientific_name}'


class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Integer)
    humidity = db.Column(db.Integer)

    def __repr__(self):
        return f'''Temp: {self.temp}F Humidity: {self.humidity}'''


class WaterLevelData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Integer)

    def __repr__(self):
        return f'''Distance: {self.distance}inches'''
