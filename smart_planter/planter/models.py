from flask_login import UserMixin
from sqlalchemy.sql import func

from . import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    plants = db.relationship("Plant")

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    previous_temp = db.Column(db.Float)
    current_temp = db.Column(db.Float)
    humidity = db.Column(db.Float)
    water_level = db.Column(db.Float)
    plant_name = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

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
