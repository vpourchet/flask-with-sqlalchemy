# wsgi.py
import os
import logging
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restx import Namespace, Resource, fields

api =  Namespace('Products')

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema
logging.warn(os.environ["DUMMY"])

@api.route('/hello')
def hello():
    return "Hello World!"

@api.route('/products')
def products():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return products_schema.jsonify(products)

@api.route('/products/<int:id>')
@api.response(404, 'Product not found')
@api.param('id', 'The product unique identifier')
def get(self, id):
        product = db.session.query(Product).get(id)
        if product is None:
            api.abort(404, "Product {} doesn't exist".format(id))
        else:
            return product
