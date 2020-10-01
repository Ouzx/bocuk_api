from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bocuk.db'

db = SQLAlchemy(app)

"""================================================================="""
class JobsQueue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    level = db.Column(db.String)

    # def __repr__(self):
    #     return f"Queue(link = {link}, level = {level})"

# JobsQueue
jobsQueue_put_args = reparse.RequestParser()
jobsQueue_put_args.add_argument("link", type=str, required=True)
jobsQueue_put_args.add_argument("level", type=str, required=True)

jobsQueue_fields = {
    'id': fields.Integer,
    'link': fields.String,
    'level': fields.String
}

class Queue(Resource):
    @marshal_with(jobsQueue_fields)
    def get (self):
        # id ya da tokeni parametre al
        # eğer sistemde kayıtlı değilse 404 döndür
        # ilk ya da sondaki satırdaki veriyi döndür
        # sonra bu satırı kesip  taken jobsa gönder
        pass

    @marshal_with(jobsQueue_fields)
    def put(self):
        # id ya da tokeni al
        # eğer sistemde yoksa 403 döndür
        # tablonun sonuna veriyi ekle
        # başarılı kod döndür
        pass

"""================================================================="""
class CrawledJobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    level = db.Column(db.String)
    crawler = db.Column(db.Integer)

    # def __repr__(self):
    #     return f"Queue(link = {link}, level = {level})"

# CrawledJobs
crawledJobs_put_args = reparse.RequestParser()
crawledJobs_put_args.add_argument("link", type=str, required=True)
crawledJobs_put_args.add_argument("level", type=str, required=True)
crawledJobs_put_args.add_argument("crawler", type=int, required=True)

crawledJobs_fields = {
    'id': fields.Integer,
    'link': fields.String,
    'level': fields.String,
    'crawler': fields.id
}
# burada api üzerinden erişim olmayacak 
"""================================================================="""
class TakenJobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    level = db.Column(db.String)
    crawler = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now())

    # def __repr__(self):
    #     return f"Queue(link = {link}, level = {level}, crawler = {crawler}, time = {time})"

# TakenJobs
takenJobs_put_args = reparse.RequestParser()
takenJobs_put_args.add_argument("link", type=str, required=True)
takenJobs_put_args.add_argument("level", type=str, required=True)
takenJobs_put_args.add_argument("crawler", type=int, required=True)

takenJobs_fields = {
    'id': fields.Integer,
    'link': fields.String,
    'level': fields.String,
    'crawler': fields.id,
    'time': fields.DateTime
}

"""================================================================="""
class Crawlers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String)
    counter = db.Column(db.Integer)

# Crawler
crawler_put_args = reparse.RequestParser()
crawler_put_args.add_argument("token", type=str, required=True)
crawler_put_args.add_argument("counter", type=int, required=True)

crawler_fields = {
    'id': fields.Integer,
    'token': fields.String,
    'counter': fields.Integer
}

"""================================================================="""
class ActiveCrawlers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    crawler = db.Column(db.Integer)
    until = db.Column(db.DateTime)

# ActiveCrawler
activeCrawler_put_args = reparse.RequestParser()
activeCrawler_put_args.add_argument("link", type=str, required=True)
activeCrawler_put_args.add_argument("crawler", type=int, required=True)
activeCrawler_put_args.add_argument("until", type=datetime, required=True)

takenJobs_fields = {
    'id': fields.Integer,
    'link': fields.String,
    'crawler': fields.id,
    'until': fields.DateTime
}





