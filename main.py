from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import encrypt as enc
import aborty
import os
from threading import Thread
from time import sleep

"""
Yapılacaklar:
    1-) Kuyruğa link eklerken bocuk listesinde olup olmadığını kontrol et.
"""


# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init
ma = Marshmallow(app)


####################################### Bocuk Model #######################################
class Bocuk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, unique=True)
    counter = db.Column(db.Integer, default=0)

    def __init__(self, token):
        self.token = token
        self.counter = 0

# Bocuk Schema
class BocukSchema(ma.Schema):
    class Meta:
        fields = ('id', 'token', 'counter')


# Init Schema
bocuk_schema = BocukSchema()
bocuks_schema = BocukSchema(many=True)

# Create a Bocuk
@app.route('/bocuk', methods=['POST'])
def add_product():
    text = request.json['text']
    token = enc.encrypt(text)
    result = Bocuk.query.filter_by(token=token).first()
    if result:
        return aborty.abort(409, "Token is already taken...")
    else:
        new_bocuk = Bocuk(token)
        db.session.add(new_bocuk)
        db.session.commit()
        return bocuk_schema.jsonify(new_bocuk)

# Get All Bocuks
@app.route('/bocuk', methods=['GET'])
def get_bocuks():
    all_bocuks = Bocuk.query.all()
    result = bocuks_schema.dump(all_bocuks)
    return jsonify(result)

# Get Bocuk by Token
@app.route('/bocuk/<token>', methods=['GET'])
def get_bocuk(token):
    bocuk = Bocuk.query.filter_by(token=token).first()

    return bocuk_schema.jsonify(bocuk)


####################################### Query Model #######################################
class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    level = db.Column(db.String)

    def __init__(self, link, level):
        self.link = link
        self.level = level

# Query Schema
class QuerySchema(ma.Schema):
    class Meta:
        fields = ('id', 'link', 'level')


# Init Schema
query_schema = QuerySchema()
queries_schema = QuerySchema(many=True)

# Add link to Query
@app.route('/query', methods=['POST'])
def append_link():
    token = request.json['token']
    if not Bocuk.query.filter_by(token=token).first():
        return aborty.abort(403, "You are not BOCUK!")
    else:
        link = request.json['link']
        level = request.json['level']
        new_link = Query(link, level)
        db.session.add(new_link)
        db.session.commit()
        taken = TakenQuery.query.filter_by(bocuk=token).first()
        if taken:   
            db.session.delete(taken)

            append_to_crawled(taken)
            
            active_bocuk = ActiveBocuk.query.filter_by(bocuk=token).first()
            db.session.delete(active_bocuk)

            bocuk = Bocuk.query.filter_by(token=token).first()
            bocuk.counter += 1
            db.session.commit()            
        return query_schema.jsonify(new_link)
       
            

# Get All Links
@app.route('/query', methods=['GET'])
def get_links():
    query = Query.query.all()
    result = queries_schema.dump(query)
    return jsonify(result)

# Get last link by Token
@app.route('/query/<token>', methods=['GET'])
def get_link(token):
    bocuk = Bocuk.query.filter_by(token=token).first()
    if not bocuk:
        return aborty.abort(403, "You are not BOCUK!")
    else:
        query = Query.query.order_by(Query.id.desc()).first()
        if query:
            append_to_takens(query, token)
            db.session.delete(query)
            db.session.commit()
            append_to_active(query.link, token)
            return query_schema.jsonify(query)
        else:
            return aborty.abort(404, "There is no link left!")

####################################### TakenQuery Model #######################################
class TakenQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    level = db.Column(db.String)
    bocuk = db.Column(db.String)
    
    def __init__(self, link, level, bocuk):
        self.link = link
        self.level = level
        self.bocuk = bocuk

# Taken Schema
class TakenSchema(ma.Schema):
    class Meta:
        fields = ('id', 'link', 'level', 'bocuk')

# Schema Init
taken_queries_schema = TakenSchema(many=True)

# Get All Links
@app.route('/takens', methods=['GET'])
def get_takens():
    takens = TakenQuery.query.all()
    result = taken_queries_schema.dump(takens)
    return jsonify(result)

# Append to Takens
def append_to_takens(query, token):
    taken = TakenQuery(query.link, query.level, bocuk=token)
    db.session.add(taken)
    db.session.commit()

####################################### CrawledQuery Model #######################################
class CrawledQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    level = db.Column(db.String)
    bocuk = db.Column(db.String)

    def __init__(self, link, level, bocuk):
        self.link = link
        self.level = level
        self.bocuk = bocuk

# Crawled Schema
class CrawledSchema(ma.Schema):
    class Meta:
        fields = ('id', 'link', 'level', 'bocuk')

# Schema Init
crawled_queries_schema = CrawledSchema(many=True)

# Get All Links
@app.route('/crawleds', methods=['GET'])
def get_crawleds():
    crawleds = CrawledQuery.query.all()
    result = crawled_queries_schema.dump(crawleds)
    return jsonify(result)

# Add data to crawled table
def append_to_crawled(taken):
    crawled = CrawledQuery(taken.link, taken.level, taken.bocuk)
    db.session.add(crawled)
    db.session.commit()

####################################### CrawledQuery Model #######################################
class ActiveBocuk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    bocuk = db.Column(db.String)
    time_by_second = db.Column(db.Integer)

    def __init__(self, link, bocuk):
        self.link = link
        self.bocuk = bocuk
        self.time_by_second = time_in_seconds

# Active Schema
class ActiveSchema(ma.Schema):
    class Meta:
        fields = ('id', 'link', 'bocuk', 'time_by_second')

# Schema Init
actives_schema = ActiveSchema(many=True)

# Get All Links
@app.route('/bocuk/actives', methods=['GET'])
def get_actives():
    actives = ActiveBocuk.query.all()
    result = actives_schema.dump(actives)
    return jsonify(result)

# Add bocuk to active table
def append_to_active(link, token):
    active_bocuk = ActiveBocuk(link, token)
    db.session.add(active_bocuk)
    db.session.commit()

####################################### Time #######################################
until = 480
# Second by second counter
time_in_seconds = 0
def timer():
    global time_in_seconds
    while True:
        sleep(1)
        time_in_seconds += 1

def supervision():
    global time_in_seconds
    global until
    while True:
        for bocuk in ActiveBocuk.query.all():
            if bocuk:
                if time_in_seconds - bocuk.time_by_second >= until:
                    db.session.delete(bocuk)
                    
                    taken = TakenQuery.query.filter_by(bocuk=bocuk.bocuk).first()
                    db.session.delete(taken)

                    query_link = Query(taken.link, taken.level)
                    db.session.add(query_link)
                    db.session.commit()
        sleep(1)

# Get current API time in seconds
@app.route('/time', methods=["GET"])
def get_time():
    return {"time_in_seconds": str(time_in_seconds)}

####################################### Brief #######################################
@app.route('/brief', methods=["GET"])
def brief():
    global time_in_seconds
    bocuk = Bocuk.query.order_by(Bocuk.id.desc()).first()
    if not bocuk:
        bocuk = 0
    else:
        bocuk = bocuk.id
        
    active_bocuk = ActiveBocuk.query.order_by(ActiveBocuk.id.desc()).first()
    if not active_bocuk:
        active_bocuk = 0
    else:
        active_bocuk = active_bocuk.id
         
    query = Query.query.order_by(Query.id.desc()).first()
    if not query:
        query = 0
    else:
        query = query.id
     
    takens = TakenQuery.query.order_by(TakenQuery.id.desc()).first()
    if not takens:
        takens = 0
    else:
        takens = takens.id
        
    crawleds = CrawledQuery.query.order_by(CrawledQuery.id.desc()).first()
    if not crawleds:
        crawleds = 0
    else:
        crawleds = crawleds.id
    
    percentage = 0
    if crawleds > 0 and query > 0:
        percentage = (crawleds * 100) / (crawleds + query)
     
    return {
        "brief":{
            "bocuks": bocuk,
            "active_bocuks": active_bocuk,
            "query": query,
            "takens": takens,
            "crawleds": crawleds,
            "time": str(time_in_seconds)
            },
        "Completed": "%" + str(percentage)
        }


# Run Server
if __name__ == '__main__':
    t1 = Thread(target=timer)
    t1.start() # Start timer thread

    t2 = Thread(target=supervision)
    t2.start()
    app.run(debug=True, host="188.166.163.91", port=5000)