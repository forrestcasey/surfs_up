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




