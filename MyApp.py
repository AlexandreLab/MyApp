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


@app.route('/')
def index():

    generation_data = []

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
#            print(series)
    return jsonify(series)

@app.route('/dashboard')
def dashboard(chartID='chart_ID', chart_type='area', chart_height=500):
    

    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height}
    title = {"text": 'Actual Aggregated Generation Per Type'}
    yAxis = {"title": {"text": 'Quantity (MW)'}}

    historical = 30 #number of historical periods to display
    startDate = datetime.now() - timedelta(hours=historical)
    api.get_full_historical_data(startDate)
#    api.get_historical_data(startDate, startDate + timedelta(hours=10))
    
    series = []
    if api.data.shape[1]>historical:
        length = int(historical)
    else:
        length = int(api.data.shape[1])
    
    for tech in api.data.index:
        generation = {
                    'name': tech,
                    'data': api.data.loc[api.data.index == tech, :].values.tolist()[0][-length:],
                    }
        series.append(generation)
    
    tempDate= api.data.columns[-length]
    period= int(tempDate.split(" ")[1])
    startDate = datetime.strptime(tempDate.split(" ")[0], "%Y-%m-%d")
    year = startDate.year
    month = startDate.month-1
    day = startDate.day
    hour = period//2
    minutes = period%2*30
    start = [year, month, day, hour, minutes]    
    return render_template('dashboard.html', chartID=chartID, chart=chart, series=series, title=title, starttime=start, yAxis=yAxis)

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run()
