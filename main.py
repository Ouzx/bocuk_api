from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import encrypt as enc
import aborty
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init
ma = Marshmallow(app)

# Bocuk Model
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

    text =  request.json['text']
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
    


# Run Server
if __name__ == '__main__':
  app.run(debug=True)

