from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt
import pandas as pd 
import numpy as np
# 
# #################################################
# # Database Setup
# #################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# 
# # reflect an existing database into a new model
Base = automap_base()
# # reflect the tables
Base.prepare(engine, reflect=True)
# 
# # Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# # Create our session (link) from Python to the DB
session = Session(engine)  #allows the session.query

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route('/')
def welcome():
#     """List all available api routes."""
        
    return  (
    		f"Available Routes</br>"
    		f"/api/v1.0/precipitation</br>"
    		f"/api/v1.0/stations</br>"
    		f"/api/v1.0/tobs</br>"
    		f"/api/v1.0/<start_date></br> * change to the exact date you like"
    		f"/api/v1.0/start_date/end_date</br>"

    )

@app.route('/api/v1.0/precipitation')
def precipitation_func():

# Query for the dates and temperature observations from the last year.
	prev_year=dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Convert the query results to a Dictionary using date as the key and tobs as the value.
	precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > prev_year).all()
	precip = {date: prcp for date, prcp in precipitation}
# Return the JSON representation of your dictionary.
	return jsonify(precip)


@app.route('/api/v1.0/stations')
def stations_func():
# Return a JSON list of stations from the dataset.
	stations_list = session.query(Measurement.station).all()

	return jsonify(stations_list)


@app.route('/api/v1.0/tobs')
def temperature_func():
# Return a JSON list of Temperature Observations (tobs) for the previous year.
	prev_year=dt.date(2017, 8, 23) - dt.timedelta(days=365)
	
	temperatures = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > prev_year).all()
	temps = {date: tobs for date, tobs in temperatures}

	return jsonify(temps)
	
@app.route('/api/v1.0/<start>')	
@app.route('/api/v1.0/<start>/<end>')
# def min_max_avg_func():
def calc_temps(start, end=None):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    if end != None:
    	return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        	filter(Measurement.date >= start).filter(Measurement.date <= end).all())
    else:
    	return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        	filter(Measurement.date >= start).all())
        
        
        
# and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# 	min_max_avg=session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))
#               .filter(Measurement.station == most_active_station_id).all()
# 	return jsonify(min_max_avg)

# 	temps_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
#                             .filter(Measurement.date >= start).all()
# 	
	
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.


# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.








# Hints
# You will need to join the station and measurement tables for some of the analysis queries.
# Use Flask jsonify to convert your API data into a valid JSON response object.



# C

if __name__ == "__main__":
 #This line starts the server. Not needed if the program is called from another program.
    app.run(debug=True)     


# all_min_avg_max = []
# 	for min_avg_max in temps_data:
# 		min_avg_max_dict = {}
# 		min_avg_max_dict["TMIN"] = min_avg_max[0]
# 		min_avg_max_dict["TAVG"] = min_avg_max[1]
# 		min_avg_max_dict["TMAX"] = min_avg_max[2]
# 		all_min_avg_max.append(min_avg_max_dict)
# 
# 	return jsonify(all_min_avg_max)
