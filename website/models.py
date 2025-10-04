from . import db
from flask import Flask, render_template, url_for
from datetime import datetime
from flask_login import UserMixin

app = Flask(__name__)

class User(db.Model, UserMixin):

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    venue = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    image = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(20), default="Open")

@app.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

class Comment(db.Model):

class Order(db.Model):