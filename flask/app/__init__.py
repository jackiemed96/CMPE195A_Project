import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

baseDir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY = "you-will-never-guess",
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(baseDir, 'app.db')
)

db = SQLAlchemy(app)

from app import models, routes