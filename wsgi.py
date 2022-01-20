# wsgi.py
# pylint: disable=missing-docstring
import requests

BASE_URL = '/api/v1'

from flask import Flask
from flask import request, redirect, url_for, jsonify
from config import Config



app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow  # NEW LINE (L'ordre est important ici !)
db = SQLAlchemy(app)
ma = Marshmallow(app)  # NEW LINE

from models import Product
from flask_migrate import Migrate
migrate = Migrate(app, db)

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello World!", 200

from schemas import many_product_schema
from schemas import one_product_schema

# ['hello' route definition]

@app.route(f'{BASE_URL}/products', methods=['GET'])
def get_many_product():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return many_product_schema.jsonify(products), 200

@app.route(f'{BASE_URL}/products/<int:id>')
def get_one_product(id):
    products = db.session.query(Product).get(id)
    return one_product_schema.jsonify(products), 200

@app.route(f'{BASE_URL}/products', methods = ['POST'])
def insert_one_product():
    product = request.get_json()
    print(product)
    myproduct = Product()
    myproduct.name = product.name
    myproduct.description = product.description
    products = db.session.add(myproduct)
    return one_product_schema.jsonify(products), 200

@app.route(f'{BASE_URL}/products/add', methods = ['GET'])
def post_one_product():
    arguments = request.args
    #product = {"name":name, "description": description}
    
    #print(description)
    return redirect(f'{BASE_URL}/products', data = jsonify(arguments))
    #return jsonify(arguments)