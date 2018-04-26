# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 14:31:23 2018

@author: sceac10
"""

from flask import Flask, render_template
#from flask_sqlalchemy import SQLAlchemy
import pandas as pd


app = Flask(__name__)
app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'


#db = SQLAlchemy(app)
data = pd.read_csv("dataset.csv")


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


@app.route('/dashboard')
def dashboard(chartID = 'chart_ID', chart_type = 'bar', chart_height = 350):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
    title = {"text": 'My Title'}
    xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
    yAxis = {"title": {"text": 'yAxis Label'}}
    return render_template('dashboard.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run()
