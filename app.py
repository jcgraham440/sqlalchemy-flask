from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import and_
from datetime import date
from copy import deepcopy
import time


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/date/<date><br>"
        f"/api/v1.0/dates/<start-date>/<end-date>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """List all precipitation, ever. Return as a dict"""
    
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    
    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(engine, reflect=True)
    
    Measurement = Base.classes.measurement 
    
    session = Session(engine)
    
    rs = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date)
    
    """ Convert sqlalchemy results into a dict where date is a key, prcp is a value. """
    d = {}
    for row in rs:
        d[row.date] = row.prcp
    
    return jsonify(d)

@app.route("/api/v1.0/stations")
def stations():
    """List all of the stations"""
    
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(engine, reflect=True)
    
    Measurement = Base.classes.measurement
    Station = Base.classes.station
    
    session = Session(engine)
    
    rs = session.query(Station.station).order_by(Station.station)
    
    return jsonify(rs.all()) 


@app.route("/api/v1.0/tobs")
def tobs():
    """ Return all temperature observations for the last year"""
    
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(engine, reflect=True)
    
    Measurement = Base.classes.measurement
    
    session = Session(engine)
    
    year = 2016
    month = 8
    day = 23
    
    start_date = date(year, month, day)
    end_date = date(start_date.year + 1, start_date.month, start_date.day)
    rs = session.query(Measurement.tobs).filter(and_(Measurement.date >= start_date, Measurement.date <= end_date))
    
    return jsonify(rs.all())
    
@app.route("/api/v1.0/date/<date>")
def start(date):
    """ Get all readings for a particular date """
    
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(engine, reflect=True)
    
    Measurement = Base.classes.measurement
    
    session = Session(engine)
    
    rs = session.query(Measurement).filter(Measurement.date == date)
    q = rs.first()
    if (q == None):
         return jsonify({"error": f"Measurement with date of {date} not found."}), 404
    lst = []
    for r in rs:
        # remove extraneous dict elements and append to list of dicts
        d = deepcopy(r.__dict__)
        del d["_sa_instance_state"]
        del d["id"]
        lst.append(d)
    
    return jsonify(lst)
    
@app.route("/api/v1.0/dates/<startdate>/<enddate>")
def startend(startdate, enddate): 
    """ Return all readings between certain dates """
    
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(engine, reflect=True)
    
    Measurement = Base.classes.measurement
    
    session = Session(engine)
    
    rs = session.query(Measurement).filter(and_(Measurement.date >= startdate, Measurement.date <= enddate))\
    
    q = rs.first()
    if (q == None):
         return jsonify({"error": f"Measurement with dates of {startdate} or {enddate} not found."}), 404
    
    lst = []
    for r in rs:
        # remove extraneous dict elements and append to list of dicts
        d = deepcopy(r.__dict__)
        del d["_sa_instance_state"]
        del d["id"]
        lst.append(d)
    
    return jsonify(lst)

if __name__ == "__main__":
    app.run(debug=True)