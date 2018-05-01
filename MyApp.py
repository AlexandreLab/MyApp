# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 14:31:23 2018

@author: sceac10
"""

from flask import Flask, render_template, jsonify
#from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import random
import numpy as np

import config


app = Flask(__name__)
app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'


#db = SQLAlchemy(app)
data = pd.read_csv("dataset.csv")
data["Hour"]= ((data["settlementperiod"]-1)*30//60%24).map('{:02.0f}'.format)
data["Minute"]= ((data["settlementperiod"]-1)*30%60).map('{:02.0f}'.format)
data["settlementdate"]=data["settlementdate"].map(str)
data["full date"] = pd.to_datetime(data["settlementdate"]+" "+data["Hour"]+":"+data["Minute"], format="%Y-%m-%d %H:%M")
data["full date"]=pd.to_datetime(data["full date"], unit='ms')

#class Bmrs(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    source = db.Column(db.String(20), unique=False, nullable=False)

@app.route('/')
def index():

    generation_data = []

    technology = data["powersystemresourcetype"].unique()

    for i in range(1, 3, 1):
        for tech in technology:
            #print(i, tech)
            generation = {
                    'source': tech,
                    'date': data.loc[(data["settlementperiod"] == i) & (data["powersystemresourcetype"] == tech), "settlementdate"].values[0],
                    'period': i,
                    'value': data.loc[(data["settlementperiod"] == i) & (data["powersystemresourcetype"] == tech), "quantity"].values[0],
            }      
            generation_data.append(generation)
    return render_template('home.html', generation_data = generation_data)


@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/live-data')
def live_data():
    
    
    index = random.randint(1,9)
    
    series= []
    technology = data["powersystemresourcetype"].unique()
    for tech in technology:
        generation = {
                'name': tech,
                'data': data.loc[(data["powersystemresourcetype"]==tech) & (data["settlementperiod"]==index), "quantity"].values[0],
        }
        series.append(generation)  
    
    
    return jsonify(series)

@app.route('/dashboard')
def dashboard(chartID = 'chart_ID', chart_type = 'area', chart_height = 350):
    
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    title = {"text": 'My Title'}

    #dt = data["full date"].values[0].astype(np.int64)// 10**9
    year=2018
    months = 3
    day=15
    hour=5
    minutes=30
    
    starttime=[year, months, day, hour, minutes]
    yAxis = {"title": {"text": 'yAxis Label'}}
    
    series= []
    technology = data["powersystemresourcetype"].unique()
    for tech in technology:
        generation = {
                'name': tech,
                'data': data.loc[data["powersystemresourcetype"]==tech, "quantity"].values.tolist()[:2],
        }
        series.append(generation)  
        
        
    return render_template('dashboard.html', chartID=chartID, chart=chart, series=series, title=title, starttime=starttime, yAxis=yAxis)

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run()
