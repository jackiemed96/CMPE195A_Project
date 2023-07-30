import json

from flask import Blueprint, flash, jsonify, render_template, request
from flask_login import current_user, login_required

from . import db
from .models import Plant

views = Blueprint("views", __name__)


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
