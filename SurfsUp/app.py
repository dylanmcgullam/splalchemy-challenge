import pandas as pd
import numpy as np
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.measurement

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome ():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_year_query = session.query(measurement.date, measurement.prcp).filter(measurement.date > last_year).all()


    session.close()


    last_year_2 = []
    for date,prcp in last_year_query:
        last_year_2_dict = {}
        last_year_2_dict['date'] = 'date'
        last_year_2_dict['precipitation'] = prcp
        last_year_2.append(last_year_2_dict)

    return jsonify(last_year_2)


@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)


    stations = session.query(station.station).distinct().count()


    session.close()

    listed_stations = list(np.ravel(stations))
    
    return jsonify(listed_stations)


@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    most_temp = session.query(measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= last_year).all()
    
    session.close()

    most_temps_2 = []
    for date, tobs in most_temp:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        most_temps_2.append(tobs_dict)
    return jsonify(most_temps_2)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    session = Session(engine)

    select = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]

    if not end:

        select_results = session.query(*select).filter(measurement.date >= start).all()
        
        session.close()
        
        temperatures = list(np.ravel(select_results))
        return jsonify(temperatures)
    
    select = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    
    select_results = session.query(*select).filter(measurement.date >= start).filter(measurement.date <= end).all()

    session.close()

    temperatures = list(np.ravel(select_results))
    return jsonify(temperatures)

if __name__ == '__main__':
    app.run(debug=True)


