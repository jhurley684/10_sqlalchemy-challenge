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
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/active_station<br/>"
        
    )



###############   PRECIPITATION  ##########################
@app.route("/api/v1.0/precip")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)
   
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



#############  STATIONS #########################
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


# ##########  TOBS BY MOST ACTIVE STATION  ##########################

@app.route("/api/v1.0/active_station")
def active_station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for station activity.  Take the most active station.
    results = session.query(Measurement.station, func.count(Measurement.prcp)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.prcp).desc()).first()

# # Query for all tobs measurements at each station. Filter for only the most active station (above)
    session.query(Measurement.station, Measurement.data, Measurement.tobs ).\
        filter( Measurement.station == results).\
        filter(year_ago = dt.date.today() - dt.timedelta(days=365))


    session.close()

 # Convert list of tuples into normal list
    most_active = list(np.ravel(results))

    return jsonify(most_active)





########## MIN, MAX, AVG TOBS  ########################
# @app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/justice-league/real_name/<start>")
def tobs_search_start_date(start):
    """Fetch the date that matches the date supplied by user or a 404 if not."""

    canonicalized = start.replace(" ", "").lower()
    for date in tobs_search_start_date:
        search_term = date["start"].replace(" ", "").lower()

        if search_term == canonicalized:
            return jsonify(date)

    return jsonify({"error": f"Character with real_name {real_name} not found."}), 404



############## Run in terminal  ######################################

if __name__ == '__main__':
    app.run(debug=True)
