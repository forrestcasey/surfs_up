#This will be the file we use to create our Flask application.

#dependencies and their aliases
import datetime as dt
import numpy as np
import pandas as pd

#dependencies for SQL Alchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#import the dependencies that we need for Flask
from flask import Flask, jsonify

#access the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into our classes
Base = automap_base()
Base.prepare(engine,reflect = True)

#function to reflect the tables into SQLAlchemy
Base.prepare(engine, reflect=True)

# create a variable for each of the classes so that we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station

#create a session link from Python to our database
session = Session(engine)

#all routes should go after this code
#create a Flask application called "app."
app = Flask(__name__)

# define the welcome route 
@app.route("/")

#create function welcome()
#add the precipitation, stations, tobs, 
#and temp routes that we'll need for this module into our return statement.
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

#The next route will return the precipitation data for the last year.
@app.route("/api/v1.0/precipitation")

#create precipitation function
# code that calculates the date one year ago from the most recent date
#add a query to get the date and precipitation for the previous year
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

#create stations route

@app.route("/api/v1.0/stations")

#create a query that will allow us to get all of the stations in our database
#
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
#add remainder to route http://127.0.0.1:5000/ with "v1.0/stations" or other route variable

#--create temperature observation route

@app.route("/api/v1.0/tobs")

#1)create a function called temp_monthly()
#2)calculate the date one year ago from the last date in the database
#3)query the primary station for all the temperature observations from the previous year
#4)unravel the results into a one-dimensional array and convert that array into a list
#5)jsonify our temps list, and then return it
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#---create route for statistics analysis
#create route for minimum, maximum, and average temperatures
#provide both a starting and ending date

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#create a function called stats()
#add parameters to our stats()function: 
    # a start parameter and an end parameter. For now, set them both to None
#create a query to select the minimum, average, and maximum temperatures from our SQLite database
#start by creating list called "sel"
#need to determine the starting and ending date, add an if-not statement 
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

#enter url for proper date range: http://127.0.0.1:5000/api/v1.0/temp/2017-06-01/2017-06-30
