# Import the dependencies.
import os
import pandas as pd

from sqlalchemy import create_engine, text, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from flask import Flask, jsonify


#################################################
# Database Setup
dirname = os.path.dirname(__file__)
database_path = os.path.join(dirname, 'Resources/hawaii.sqlite')
engine = create_engine(f"sqlite:///{database_path}")

# #Test query to make sure the the databse is connected
# query = text("SELECT * FROM station")
# data = engine.execute(query)

# for record in data:
#     print(record)
#################################################


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#Helper function to query easily
def query_db(query_text, column_list):
    '''Helper function to quickly query the database into a pandas DF
    must pass the query text followed by a list of column names'''
    
    return pd.DataFrame(engine.execute(query_text), columns=column_list).to_json(orient='index', indent=2)


@app.route("/")
def homepage():
    """List all of the routes"""
    return(
        f"Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def percipitation():
    """Returns a table of Date and Percipitation values for the last 12 months"""
    
    query = "select date, prcp from measurement where julianday(date) >= (select julianday(max(date))-365 from measurement)"
    column_list = ['Date', 'Percipitation']
    return query_db(query,column_list)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    
    query = "select distinct station from station"
    column_list = ['Station']
    return query_db(query,column_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the dates and temperature for the most active station,
    including only the last year of data"""
    
    query = """select date, tobs from measurement where 
         station = (select station from measurement group by station order by count(station) desc limit 1) -- most active WS filter
         and (julianday(date) >= (select julianday(max(date))-365 from measurement)) -- most recent year filter"""
    column_list = ['Date', 'Observed Temp']
    return query_db(query,column_list)

@app.route("/api/v1.0/start=<start>")
def start_(start):
    """min, max, and avg temp for the time range (all dates greater than and including start date)"""

    query = f"select min(tobs), max(tobs), avg(tobs) from measurement where date >= {start}"
    column_list = ['Min Temp', 'Max Temp', 'Avg Temp']
    return query_db(query,column_list)

@app.route("/api/v1.0/start=<start>/end=<end>")
def start_end(start, end):
    """min, max, and avg temp for the time range (all dates within and including the bounds)"""
    
    query = f"select min(tobs), max(tobs), avg(tobs) from measurement where date >= {start} and date <= {end}"
    column_list = ['Min Temp', 'Max Temp', 'Avg Temp']
    return query_db(query,column_list)

if __name__ == '__main__':
    app.run(debug=True)