# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 14:31:23 2018


in console:
    workon myapp
    python myapp.py


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

api5min = ElexonAPI.FUELINST(conf.APIKEY)
api30min = ElexonAPI.B1620(conf.APIKEY)

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
    if api5min.get_data():
        df = api5min.data
        for col in df.columns[2:]:
            generation = {
                    'name': col,
                    'data': df[col].iloc[-1],
                    }
            series.append(generation)
            
        print("new serie to be added:", series)
    return jsonify(series)


@app.route('/dashboard')
def dashboard(chartID='chart_ID', chart_type='area', chart_height=500):

    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height}
    title = {"text": 'Actual Aggregated Generation Per Type'}
    yAxis = {"title": {"text": 'Quantity (MW)'}}

    historical = 60  # number of hours to go back in time
    startDate = datetime.now() - timedelta(hours=historical)
    api5min.get_full_historical_data(startDate)
#    api.get_historical_data(startDate, startDate + timedelta(hours=10))

    df = api5min.data
    series = []
    if df.shape[0] > historical*60/5:
        length = int(historical)
    else:
        length = int(df.shape[0])

    # the format of data for Highcharts is:
    # [{'name': 'CCGT', 'data': [1, 2, 3, 4 , 5]}]
    for col in df.columns[2:]:
        generation = {
                    'name': col,
                    'data': df[col].values.tolist()[-length:],
                    }
        series.append(generation)

    startDate = df['publishingPeriodCommencingTime'].iloc[-length]
    print("StartDate: ", startDate)
    start = [startDate.year, startDate.month, startDate.day, startDate.hour, startDate.minute]    
    return render_template('dashboard.html', chartID=chartID, chart=chart, series=series, title=title, starttime=start, yAxis=yAxis)


# To build another dashboard for the 30min resolution and storing data into cookies/cache
@app.route('/dashboard2')
def dashboard2(chartID='chart_ID', chart_type='area', chart_height=500):

    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height}
    title = {"text": 'Actual Aggregated Generation Per Type'}
    yAxis = {"title": {"text": 'Quantity (MW)'}}

    historical = 5*120/60 # number of historical periods to display
    startDate = datetime.now() - timedelta(hours=historical)
    api30min.get_full_historical_data(startDate)
#    api.get_historical_data(startDate, startDate + timedelta(hours=10))
    
    df = api30min.data
    series = []
    if df.shape[1]>historical:
        length = int(historical)
    else:
        length = int(df.shape[1])
    
    #the format of data for Highcharts is: [{'name': 'CCGT', 'data': [1, 2, 3, 4 , 5]}]
    
    for col in df.columns[2:]:
        generation = {
                    'name': col,
                    'data': df[col].values.tolist()[-length:],
                    }
        series.append(generation)
        
    startDate= df['publishingPeriodCommencingTime'].iloc[-length]
    print(startDate)
    start = [startDate.year, startDate.month, startDate.day, startDate.hour, startDate.minute]    
    return render_template('dashboard.html', chartID=chartID, chart=chart, series=series, title=title, starttime=start, yAxis=yAxis)


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run()
