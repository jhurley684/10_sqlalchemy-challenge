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

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"Enter start date as 01-01-21"
        f"/api/v1.0/start<br/>"
        
    )

###############   PRECIPITATION  ##########################
@app.route("/api/v1.0/precip")
def precip():
    # Create our session (link) from Python to the DB
    # session = Session(engine)
   
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["precip"] = prcp
        all_precip.append(precip_dict)

    return jsonify(precipitation = all_precip)



#############  LIST OF STATIONS STATIONS #########################
@app.route("/api/v1.0/stations")
def station():
    # # Create our session (link) from Python to the DB
    # session = Session(engine)

    """Return a list of stations  from data set"""
    # Query all station measurements in Staton measurements
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_station = list(np.ravel(results))

    return jsonify(all_station)



# ########## MOST ACTIVE STATION   ######################

@app.route("/api/v1.0/active_station")
def active_station():
    # # Create session (link) from Python to the DB
    session = Session(engine)

    # Query for station activity.  Take the most active station.
    results = session.query(Measurement.station,func.count(Measurement.tobs)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.tobs).desc()).first()

    session.close()

     # Convert list of tuples into normal list
    station1 = list(np.ravel(results))

    return jsonify(station1)


# ########## TOBS AT THE MOST ACTIVE STATION   ######################
# # # # Query for all tobs measurements at each station. Filter for only the most active station (above)
@app.route("/api/v1.0/tobs_data")
def tobs_data():

    # # Create session (link) from Python to the DB
    session = Session(engine)

    most_active = session.query(Measurement.station, func.count(Measurement.tobs)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.tobs).desc()).first()

    most_active_station = most_active[0]
    # print(most_active)
    tobs_station = session.query( Measurement.tobs).\
        filter(Measurement.station == most_active_station).all()
       

    session.close()

     # Convert list of tuples into normal list
    tobs_station = list(np.ravel(tobs_station))

    return jsonify(temperature = tobs_station)



# ########## TOBS FOR PREVIOUS YEAR   ######################
# @app.route("/api/v1.0/tobs_data")
# def tobs_data():

#     # # Create session (link) from Python to the DB
#     session = Session(engine)

# # Find the most recent date in the data set.
#     recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

# # Starting from the most recent data point in the database. 
#     past_year = session.query(Measurement.date, Measurement.prcp).filter(func.strftime("%x", Measurement.date) > (recent_date - 1 year))
    
 
#     session.close()

#      # Convert list of tuples into normal list
#     past_year = list(np.ravel(past_year))

#     return jsonify(temperature = past_year)




######## MIN, MAX, AVG TOBS - START DATE ONLY  #############
# for all stock in the month of May
# Sort the result by stock name


########## MIN, MAX, AVG TOBS - START & END DATE ###########





############# Run in terminal  ##############################

if __name__ == '__main__':
    app.run(debug=True)
