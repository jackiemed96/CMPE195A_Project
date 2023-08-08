from os import path

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "hjshjhdjah kjshkjdhjs"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
db.init_app(app)

from .views import views

app.register_blueprint(views, url_prefix="/")

from .models import Plant, User, WaterLevelData, WeatherData

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = "views.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# def create_app():
#     app = Flask(__name__)
#     app.config["SECRET_KEY"] = "hjshjhdjah kjshkjdhjs"
#     app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
#     db.init_app(app)

#     from .views import views

#     app.register_blueprint(views, url_prefix="/")

#     from .models import Plant, User, WaterLevelData, WeatherData

#     with app.app_context():
#         db.create_all()

#     login_manager = LoginManager()
#     login_manager.login_view = "views.login"
#     login_manager.init_app(app)

#     @login_manager.user_loader
#     def load_user(id):
#         return User.query.get(int(id))

#     return app


def create_database(app):
    if not path.exists("smart_planter/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")

from planter import models, views