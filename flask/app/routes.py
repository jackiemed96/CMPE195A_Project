from app import app, db
from flask import render_template, Flask, request, redirect, url_for
from app.models import SensorData, DistanceData

@app.route('/', methods=["GET", "POST"])
def hello():
    if (request.method == "POST"):
        sensorData = SensorData.query.order_by(SensorData.id.desc()).limit(5).all()
        distance = DistanceData.query.order_by(DistanceData.id.desc()).limit(5).all()
        return render_template("home.html", data=sensorData, distance=distance)
        
    distance = DistanceData.query.order_by(DistanceData.id.desc()).limit(5).all()
    return render_template("home.html", distance=distance)
