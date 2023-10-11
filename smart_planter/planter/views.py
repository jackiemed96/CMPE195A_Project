import json

from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, session, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from planter.models import Plant, User, UserPlants, WeatherData, WaterLevelData, db
from datetime import datetime


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
    user_plants = UserPlants.query.filter_by(user=current_user.id).all()
    current_plant = UserPlants.query.filter_by(user=current_user.id, current=True).first()

    # Get the latest water level data
    latest_water_level = WaterLevelData.query.order_by(WaterLevelData.id.desc()).first()
    latest_distance = latest_water_level.distance if latest_water_level else None

    # Get the latest temperature and humidity values
    latest_weather_data = WeatherData.query.order_by(WeatherData.id.desc()).first()
    latest_temp = latest_weather_data.temp if latest_weather_data else None
    latest_humidity = latest_weather_data.humidity if latest_weather_data else None

    return render_template(
        "home.html", 
        user=current_user, 
        plants=user_plants, 
        current_plant=current_plant, 
        latest_temp=latest_temp,
        latest_humidity=latest_humidity,
        latest_distance=latest_distance  # Pass the latest distance
    )


# @views.route("/delete-plant", methods=["POST"])
# def delete_plant():
#    plant = json.loads(
#        request.data
#    )  # this function expects a JSON from the INDEX.js file
#    plantId = Plant["plantId"]
#    plant = plant.query.get(plantId)
#    if plant:
#        if plant.user_id == current_user.id:
#            db.session.delete(plant)
#            db.session.commit()

#    return jsonify({})


@views.route("/search", methods=["GET", "POST"])
@login_required
def search_plant():
    plants = Plant.query.all()

    if request.method == "POST":
        if request.form:
            plant_name = request.form.get("plant_name")
            plant = Plant.query.filter(Plant.name.ilike(f"%{plant_name}%")).first()

            if plant:
                flash(f"Plant '{plant.name}' found!", category="success")
                return render_template('view-plant.html', user=current_user, plant=plant)

            else:
                flash("Plant not found!", category="error")

    return render_template("search-plant.html", user=current_user, plants=plants)



@views.route("/search-history", methods=["GET"])
@login_required
def searched_plants_user_history():
    history = UserPlants.query.filter_by(user=session.get("_user_id")).all()
    return render_template('search-history.html', user=current_user, history=history)


@views.route("/view-plants", methods=["GET"])
@login_required
def view_plants():
    plants = Plant.query.all()
    return render_template("view-plants.html", user=current_user, plants=plants)

@views.route("/add-to-user-plants", methods=["POST"])
@login_required
def add_to_collection():
    if request.method == "POST":
        plant_name = request.form.get("plant_name")

        # Check if the user already has this plant in their collection
        existing_user_plant = UserPlants.query.filter_by(
            user=current_user.id, plant=plant_name).first()

        if not existing_user_plant:
            # Save the plant to the user's collection with added date
            user_plant = UserPlants(
                user=current_user.id, plant=plant_name, date_added=datetime.now())
            db.session.add(user_plant)
            db.session.commit()

            flash(f"Plant '{plant_name}' added to collection!", category="success")
        else:
            flash(f"Plant '{plant_name}' is already in your collection", category="warning")
        # Redirect back to the search page or wherever you want to go
        return redirect(url_for("views.search_plant"))

@views.route("/delete-plant", methods=["POST"])
def delete_plant():
    plant_id = request.form.get("plant_id")
    user_plant = UserPlants.query.get(plant_id)

    if user_plant and user_plant.user == current_user.id:
        db.session.delete(user_plant)
        db.session.commit()
        flash("Plant deleted successfully!", category="success")
    else:
        flash("Unable to delete plant.", category="error")

    return redirect(url_for("views.home"))


@views.route("/set-current-plant", methods=["POST"])
def set_current_plant():
    plant_name = request.form.get("current_plant")
    print(f"Received plant name: {plant_name}")
    user_plant = UserPlants.query.filter_by(user=current_user.id, plant=plant_name).first()
    
    # Unset the current plant for this user
    UserPlants.query.filter_by(user=current_user.id).update({"current": False})
    
    # Set the new current plant
    if user_plant:
        user_plant.current = 1
        db.session.commit()

        flash(f"Current plant set to '{plant_name}'!", category="success")
    else:
        flash(f"Plant '{plant_name}' not found in your collection.", category="error")

    return redirect(url_for("views.home", current_plant=plant_name))

@views.route("/update-temperature", methods=["GET"])
@login_required
def update_temperature():
    print("Executing update_temperature route")
    # Step 1: Retrieve the latest temperature reading
    latest_weather_data = WeatherData.query.order_by(WeatherData.id.desc()).first()

    # Step 2: Identify the current user and their associated current plant
    current_user_id = current_user.id
    current_plant = UserPlants.query.filter_by(user=current_user_id, current=True).first()

    # Step 3: Update the UserPlants table
    if current_plant and latest_weather_data:
        current_plant.temperature = latest_weather_data.temp
        db.session.commit()
        flash(f"Temperature updated for {current_plant.plant}", category="success")
    else:
        flash("Unable to update temperature.", category="error")

    return redirect(url_for("views.home"))

