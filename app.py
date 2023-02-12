
import datetime 
import json
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import pandas as pd

from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)

@app.route('/')
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def percipitation():
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).all()
    session.close()

    rain_measurement = []
    format_data = "%Y-%m-%d"

    for date, prcp in results:
        rain_info = {}
        rain_info["date"] = datetime.datetime.strptime(date, format_data)
        rain_info["prcp"] = prcp
        rain_measurement.append(rain_info)
    return jsonify(rain_measurement)

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    results = session.query(station.station, station.name)
    session.close()

     names = list(np.ravel(results))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(measurement.date, measurement.tobs).all
          
    session.close()

    tobs = []
    popular = 'USC00519281'
    for day, temp in results:
        temp_info = {}
        temp_info["station"] = popular
        temp_info["date"] = day
        temp_info["temp"] = temp
        tobs.append(temp_info)     
    return jsonify(tobs)

@app.route("/api/v1.0/2016-08-23")
# Start date: 2016-08-23 to End date: 2017-08-23
def start():
    session = Session(engine)
    mn = func.min(measurement.tobs)
    mx = func.max(measurement.tobs)
    ag = func.avg(measurement.tobs)
    results = session.query(mn, mx, ag).\
        filter(measurement.date >= '2016-08-23').all()
    session.close()

    stats = []

    for a, b, c in results:
        info = {"Date Range": "2016-08-23 to End"}
        info["min"] = a
        info["max"] = b
        info["avg"] = c
        stats.append(info)
    return jsonify(stats)
#@app.route("/api/v1.0/<start>/<end>")

if __name__ == '__main__':
    app.run(debug=True)