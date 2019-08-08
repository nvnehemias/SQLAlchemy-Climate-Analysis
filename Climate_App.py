import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite",echo = True)

Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/station<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start><end><br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation"""
    # Query all passengers
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/station")
def station():
     """Return a list of the stations"""
    # Query all stations
     session = Session(engine)
     results = session.query(Station.station).all()

     # Create a dictionary from the row data and append to a list of stations
     all_stations = []
     for station in results:
         all_stations.append(station[0])

     return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
     """query for the dates and temperature observations from a year from the last data point"""
     # Query all passengers
     session = Session(engine)
     #twelve_months = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
     one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
     results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > one_year).all()

     # Create a dictionary from the row data and append to a list of all_passengers
     all_tobs = []
     for tobs in results:
         all_tobs.append(tobs[1])

     return jsonify(all_tobs)

@app.route("/api/v1.0/start_date")
def start(start_date):
     """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
     # Query all passengers
     session = Session(engine)
     results = session.query(Station.station, func.min(Measurement.tobs),func.avg(Measurement.tobs),
                        func.max(Measurement.max)).\
                        filter(Measurement.station == Station.station).\
                        filter(Measurement.date >= start_date).all()

     # Create a dictionary from the row data and append to a list of all_passengers
     for temps in results:
         print(temps)

     return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def end(start_date,end_date):
     """Return a list of passenger data including the name, age, and sex of each passenger"""
     # Query all passengers
     session = Session(engine)
     results = session.query(Station.station, func.min(Measurement.tobs),func.avg(Measurement.tobs),
                        func.max(Measurement.max)).\
                        filter(Measurement.station == Station.station).\
                        filter(Measurement.date <= end_date).\
                        filter(Measurement.date >= start_date).all()

     # Create a dictionary from the row data and append to a list of all_passengers
     all_passengers = []
     for answer in results:
         print(answer)

     return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
