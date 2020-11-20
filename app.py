import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
import datetime as dt
from flask import Flask, jsonify
import pandas as pd


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare Base using automap_base
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# print(Base.classes.keys())

# Save reference to the measurement table as "Measurement"
Measurement = Base.classes.measurement
# save reference to the station table as "Station"
Station = Base.classes.station
connection = engine.connect()
cursor = connection.execute("Select * from sqlite_master where type = 'table'")
# for c in cursor:
#     print(c)
# data = pd.read_sql('select * from measurement', connection)
# print (data)

# Create our session from python to the DB
session = Session(engine)

#######################################################
# flask set up
######################################################
app = Flask (__name__)

#########################################################
# Flask Routes
############################################################


@app.route("/")
def home():
    return(
    "/api/v1.0/precipitation<br/>"
    "/api/v1.0/stations<br/>"
    "/api/v1.0/tobs<br/>"
    "/api/v1.0/yyyy-mm-dd<br/>"
    "/api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

###############################################################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    

#query for last 12 months of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()

# Create a dictionary fof precipitation and append 
    precip_details = []
    for prcp_info in results:
        prcp_dict = {}
        prcp_dict["Date"] = prcp_info[0]
        prcp_dict["Precipitation"] = prcp_info[1]
        precip_details.append(prcp_dict)
        
    return jsonify(precip_details)

##############################################################################################
@app.route("/api/v1.0/stations")
def stations():
    """Return a json list of stations from the dataset."""
    # Query all the stations
    results = session.query(Station.name,Station.station).all()
#create dictionary of all stations and append 


    stations_report = []
    for stations in results:
        stations_info = {}
        stations_info["Station"] = stations[0]
        stations_info["Station Name"] = stations[1]
        # stations_info["Latitude"] = stations.latitude
        # stations_info["Longitude"] = stations.longitude
        # stations_info["Elevation"] = stations.elevation
        stations_report.append(stations_info)
    
    return jsonify(stations_report)
# ##############################################################################################
@app.route("/api/v1.0/tobs")
def tobs():

    """Return a json list of Temperature Observations (tobs) for the previous year"""
    # Query all the stations and for the previous date. 
    results =  session.query(Measurement.station,Measurement.date,Measurement.tobs).\
                    group_by(Measurement.date).\
                    filter(Measurement.date > '2016-08-23').all()


#convert query to dictionary and append  list
    temp_data = []
    for tobs_info in results:
        tobs_dict = {}
        tobs_dict["Station"] = tobs_info.station
        tobs_dict["Date"] = tobs_info.date
        tobs_dict["Temperature"] = tobs_info.tobs
        temp_data.append(tobs_dict)
    
    return jsonify(temp_data)

################################################################################################

@app.route("/api/v1.0/<start>")
def start_date(start):
                        
#Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start date
    # Query all the stations and for the given date. 
    results = session.query(Measurement.date,func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).group_by(Measurement.date).all()

# convert query to dictionary

    temp_nums = {}
#looping through the results to get min,max,avg temperature for each date
    for data in results:
        temp_nums [data [0]] = {'min temp': data[1],'max temp':data[2], 'avg temp':data[3]}

    return jsonify(temp_nums)
# ###############################################################################################
@app.route("/api/v1.0/<start>/<end>")
def end_date(start,end):

    """Return a json list of the minimum temperature, the average temperature, 
    and the max temperature for a given start-end date range."""
    

    # Query all the stations and for the given range of dates. 
    results = session.query(Measurement.date,func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
#convert query to distcionary
    temp_nums2 = {}
#looping through the results to get min,max,avg temperature for a given year
    for data in results:
        temp_nums2 [data [0]] = {'min temp': data[1],'max temp':data[2], 'avg temp':data[3]}

    return jsonify(temp_nums2)

if __name__ == '__main__':
    app.run(debug=True)



