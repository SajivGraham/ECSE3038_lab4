from marshmallow import Schema, fields, ValidationError
from flask import Flask, request, jsonify
from flask_cors import CORS
from json import loads
import pandas as pd
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate, migrate

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://bszqmhzn:HEch-D3ALjJbWVY1liS4Rah5ca61kExB@ziggy.db.elephantsql.com:5432/bszqmhzn"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

Profile = {
     "success": True,
     "data": {
        "last_updated": "2/3/2021, 8:48:51 PM",
        "username": "coolname",
        "role": "Engineer",
        "color": "#3478ff"
     }
}

class Tanks(db.Model):
    __tablename__ = "Tanks"

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(50), unique=True, nullable=False)
    lat = db.Column(db.String(50), nullable=False)
    long = db.Column(db.String(50), nullable=False)
    percentage_full = db.Column(db.Integer, nullable=False)
    
class TankSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tanks
        fields = ("id", "location", "lat", "long", "percentage_full")

db.init_app(app)
migrate = Migrate(app, db)





@app.route("/")
def home():
    return "ECSE3038 Lab 4"

@app.route("/profile", methods=["GET", "POST", "PATCH"])
def getting_profile():
    if request.method == "GET":
        return jsonify(Profile)

    elif request.method == "POST":
        now = datetime.now()
        datetimee = now.strftime("%d/%m/%Y %H:%M:%S")

        Profile["data"]["last_updated"] = (datetimee)
        Profile["data"]["username"] = (request.json["username"])
        Profile["data"]["role"] = (request.json["role"])
        Profile["data"]["color"] = (request.json["color"])

        return jsonify(Profile)

    elif request.method == "PATCH":
        now = datetime.now()
        datetimee = now.strftime("%d/%m/%Y %H:%M:%S")
    
        data = Profile["data"]

        r = request.json
        r["last_updated"] = datetimee
        attributes = r.keys()
        for attribute in attributes:
            data[attribute] = r[attribute]

        return jsonify(Profile)      

@app.route("/data", methods=["GET", "POST"])
def tank_data():
    if request.method == "GET":
        Tank_ = Tanks.query.all()
        TankList = TankSchema(many=True).dump(Tank_)

        return jsonify(TankList)

    elif request.method == "POST":
        NewTank = Tanks(
            location = request.json["location"],
            lat = request.json["lat"],
            long = request.json["long"],
            percentage_full =  request.json["percentage_full"]
        )

        db.session.add(NewTank)
        db.session.commit()
        return TankSchema().dump(NewTank)


@app.route('/data/<int:id>', methods=["PATCH", "DELETE"])
def ChangeTankData(id):
    if request.method == "PATCH":

        Tank_ = Tanks.query.get(id)
        update = request.json

        if "location" in update:
                tank.location = update["location"]
        elif "lat" in update:
            tank.lat = update["lat"]
        elif "long" in update:
            tank.long = update["long"]
        elif "percentage_full" in update:
            tank.percentage_full = update["percentage_full"] 

        db.session.commit()
        return TankSchema().dump(Tank_)

    if request.method == "DELETE":
        Tank_ = Tanks.query.get(id)
        db.session.delete(Tank_)
        db.session.commit()

        return {
            "success": True
        }

if __name__ == "__main__":
    app.run( debug=True)