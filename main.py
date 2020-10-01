from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bocuk.db'

db = SQLAlchemy(app)

class JobsQueue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    level = db.Column(db.String)

    # def __repr__(self):
    #     return f"Queue(link = {link}, level = {level})"

class CrawledJobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    level = db.Column(db.String)
    user_id = db.Column(db.Integer)

    # def __repr__(self):
    #     return f"Queue(link = {link}, level = {level})"

class TakenJobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    level = db.Column(db.String)
    crawler = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now())

    # def __repr__(self):
    #     return f"Queue(link = {link}, level = {level}, crawler = {crawler}, time = {time})"

class Crawlers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String)
    counter = db.Column(db.Integer)

class ActiveCrawlers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crawler_id = db.Column(db.Integer)
    job_id = db.Column(db.Integer)
    time = db.Column(db.DateTime)



