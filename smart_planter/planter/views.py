import json

from flask import Blueprint, flash, jsonify, render_template, request, url_for, redirect
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import Plant, User

views = Blueprint("views", __name__)

@views.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email does not exist.", category="error")

    return render_template("login.html", user=current_user)


@views.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.login"))

@views.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("User with email already exists.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif len(first_name) < 2:
            flash("First name must be greater than 1 character.", category="error")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category="error")
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("sign-up.html", user=current_user)

@views.route("/", methods=["GET"])
@login_required
def home():
    plants = Plant.query.all()
    return render_template("home.html", user=current_user, plants=plants)


@views.route("/delete-plant", methods=["POST"])
def delete_plant():
    plant = json.loads(
        request.data
    )  # this function expects a JSON from the INDEX.js file
    plantId = Plant["plantId"]
    plant = plant.query.get(plantId)
    if plant:
        if plant.user_id == current_user.id:
            db.session.delete(plant)
            db.session.commit()

    return jsonify({})


@views.route("/search", methods=["GET", "POST"])
@login_required
def search_plant():
    if request.method == "POST":
        if request.form:
            plant_name = request.form.get("plant_name")
            print(f"Plant name: {plant_name}")
            plant = Plant.query.filter_by(plant_name=plant_name).first()
            print(f"Plant name: {plant}")

            if plant:
                flash(f"Plant '{plant.plant_name}' found!", category="success")
            else:
                flash("Plant not found!", category="error")

    return render_template("search-plant.html", user=current_user)


@views.route("/add-plants", methods=["GET", "POST"])
@login_required
def add_plants():
    if request.method == "POST":
        if request.form:
            plant_name = request.form.get("plant_name")
            previous_temp = request.form.get("previous_temp")
            current_temp = request.form.get("current_temp")
            humidity = request.form.get("humidity")
            water_level = request.form.get("water_level")

            # add the plant information
            plant = Plant(
                plant_name=plant_name,
                previous_temp=previous_temp,
                current_temp=current_temp,
                humidity=humidity,
                water_level=water_level,
            )

            db.session.add(plant)
            db.session.commit()
            flash("Plant added", category="success")

    return render_template("add-plant.html", user=current_user)


@views.route("/view-plants", methods=["GET"])
@login_required
def view_plants():
    plants = Plant.query.all()
    return render_template("view-plants.html", user=current_user, plants=plants)
