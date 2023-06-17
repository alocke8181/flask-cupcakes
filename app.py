"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

@app.route('/')
def show_home():
    return render_template('home.html')


@app.route('/api/cupcakes', methods=['GET'])
def get_all_cupcakes():
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:cc_id>', methods=['GET'])
def get_cupcake(cc_id):
    cupcake = Cupcake.query.get(cc_id)
    return jsonify(cupcake=cupcake.serialize()),200

@app.route('/api/cupcakes', methods=['POST'])
def create_new_cupcake():
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']
    new_cupcake = Cupcake(flavor=flavor,size=size,rating=rating,image=image)
    with app.app_context():
        db.session.add(new_cupcake)
        db.session.commit()
    cupcake = Cupcake.query.order_by(Cupcake.id.desc()).first()
    return (jsonify(cupcake=cupcake.serialize()),201)

@app.route('/api/cupcakes/<int:cc_id>',methods=['PATCH'])
def update_cupcake(cc_id):
    cupcake = Cupcake.query.get_or_404(cc_id)
    cupcake.flavor = request.json.get('flavor',cupcake.flavor)
    cupcake.size = request.json.get('size',cupcake.size)
    cupcake.rating = request.json.get('rating',cupcake.rating)
    cupcake.image = request.json.get('image',cupcake.image)
    db.session.add(cupcake)
    db.session.commit()
    updated_cc = Cupcake.query.order_by(Cupcake.id.desc()).first()
    return jsonify(cupcake=updated_cc.serialize()),200

@app.route('/api/cupcakes/<int:cc_id>',methods=['DELETE'])
def delete_cupcake(cc_id):
    cc = Cupcake.query.get_or_404(cc_id)
    db.session.delete(cc)
    db.session.commit()
    return jsonify(message='Deleted'),200
