import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precip<br/>"
        f"/api/v1.0/stations<br>"
    )

# ############  STATIONS  #####################
@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations  from data set"""
    # Query all station measurements in Staton measurements
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_station = list(np.ravel(results))

    return jsonify(all_station)

############  PRECIPITITATION  ################################
@app.route("/api/v1.0/precip")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["precip"] = prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)



##########  MOST ACTIVE STATIONS  ##########################
@app.route("/api/v1.0/active_stations")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query to find station that took most measurements (prcp)
    results = session.query(Measurement.station, func.count(Measurement.prcp)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.prcp).desc()).all()

    session.close()

    # Create a dictionary from the row data and append to a list of station_activity
    station_activity = []
    for date, prcp in results:
        activity_dict = {}
        activity_dict["station"] = station
        activity_dict["measurements"] = prcp
        station_activity.append(activity_dict)

    return jsonify(station_activity)










if __name__ == '__main__':
    app.run(debug=True)
