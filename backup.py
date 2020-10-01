from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import encrypt as enc

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
jobsQueue_put_args = reqparse.RequestParser()
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
        # eğer veri varsa: 
        # ilk ya da sondaki satırdaki veriyi döndür
        # sonra bu satırı kesip  taken jobsa gönder
        # yoksa wait adında bir string döndür.
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

"""================================================================="""
class TakenJobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    level = db.Column(db.String)
    crawler = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now())

"""================================================================="""
class Crawlers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String)
    counter = db.Column(db.Integer, default=0)

# Crawler
crawler_put_args = reqparse.RequestParser()
crawler_put_args.add_argument("token", type=str, required=True)
crawler_put_args.add_argument("counter", type=int)

crawler_fields = {
    'id': fields.Integer,
    'token': fields.String,
    'counter': fields.Integer
}

class SignUp(Resource):
    @marshal_with(crawler_fields)
    def put(self, seal):
        token = enc.encrypt(seal)
        # args = crawler_put_args.parse_args()
        result = Crawlers.query.filter_by(token=token)
        if result['token'] != None:
            return result
            abort(409, message="Token is already taken")
        db.session(token)
        db.session.commit()
        return token, 201
        
        

"""================================================================="""
class ActiveCrawlers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    crawler = db.Column(db.Integer)
    until = db.Column(db.DateTime)

api.add_resource(SignUp,"/signup/<string:seal>")

if __name__ == "__main__":
    app.run(debug=True)