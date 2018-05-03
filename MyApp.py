# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 14:31:23 2018

@author: sceac10
"""

from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import ElexonAPI
from functions import get_request, xml_to_pd, time_details
import config as conf

app = Flask(__name__)
app.config['DEBUG'] = True

api = ElexonAPI.ElexonAPI(conf.APIKEY)
#data = pd.read_csv("dataset.csv")
#data["Hour"]= ((data["settlementperiod"]-1)*30//60%24).map('{:02.0f}'.format)
#data["Minute"]= ((data["settlementperiod"]-1)*30%60).map('{:02.0f}'.format)
#data["settlementdate"]=data["settlementdate"].map(str)
#data["full date"] = pd.to_datetime(data["settlementdate"]+" "+data["Hour"]+":"+data["Minute"], format="%Y-%m-%d %H:%M")
#data["full date"]=pd.to_datetime(data["full date"], unit='ms')

@app.route('/')
def index():

    generation_data = []

#    technology = data["powersystemresourcetype"].unique()
#
#    for i in range(1, 3, 1):
#        for tech in technology:
#            #print(i, tech)
#            generation = {
#                    'source': tech,
#                    'date': data.loc[(data["settlementperiod"] == i) & (data["powersystemresourcetype"] == tech), "settlementdate"].values[0],
#                    'period': i,
#                    'value': data.loc[(data["settlementperiod"] == i) & (data["powersystemresourcetype"] == tech), "quantity"].values[0],
#            }      
#            generation_data.append(generation)
    return render_template('home.html', generation_data = generation_data)


@app.route('/about')
def about():

    return render_template('about.html')


@app.route('/live-data')
def live_data():
    series = []
    if api.get_data():
        for tech in api.data.index:
            generation = {
                    'name': tech,
                    'data': api.data.loc[api.data.index == tech, :].values[0][-1],
            }
            series.append(generation)
            print(series)
    return jsonify(series)

@app.route('/dashboard')
def dashboard(chartID='chart_ID', chart_type='area', chart_height=450):
    
    historical = 30 #number of historical periods to display
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height}
    title = {"text": 'Actual Aggregated Generation Per Type'}
    yAxis = {"title": {"text": 'Quantity (MW)'}}

    startDate = datetime.now() - timedelta(hours=historical/2)
    api.get_full_historical_data(startDate)

    series = []
    for tech in api.data.index:
        generation = {
                'name': tech,
                'data': api.data.loc[api.data.index == tech, :].values.tolist()[0],
        }
        series.append(generation)

    year = startDate.year
    month = startDate.month-1
    day = startDate.day
    hour = startDate.hour
    minutes = startDate.minute//30*30
    starttime = [year, month, day, hour, minutes]    
    return render_template('dashboard.html', chartID=chartID, chart=chart, series=series, title=title, starttime=starttime, yAxis=yAxis)

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run()
