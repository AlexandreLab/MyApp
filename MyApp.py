# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 14:31:23 2018

@author: sceac10
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://tmp/bmrs.db'
db= SQLAlchemy(app)


class Bmrs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(20), unique=False, nullable=False)
    value = db.Column(db.String(20), unique=False, nullable=False)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run()
