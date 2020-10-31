import os
from datetime import timedelta

from flask import (Blueprint, Flask, flash, redirect, render_template, request,
                   session, url_for)
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

# configuring file uploads
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

#configuring session storage
app.secret_key = "fc1dj4ad6s47dep932089rjdnc+_{EF37W998VW798DeqVDrewASewC+};:}WE{V}]D_WS_O!_+"
app.permanent_session_lifetime = timedelta(days=30)


#configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Products(db.Model):
    _id = db.Column((db.Integer), primary_key=True)
    _product_name = db.Column( db.String(100), nullable=False)
    _product_price = db.Column(db.String(8), nullable=False)
    _product_brand = db.Column(db.String(100), nullable=False)
    _product_img = db.Column(db.String(100), nullable=False)
    _product_description = db.Column(db.String(2000), nullable=False)
    _product_stock = db.Column(db.String(10))
    def __init__(self,_id, _product_name,  _product_price,  _product_brand, _product_img, _product_description, _product_stock):
        self._id = _id
        self._product_name = _product_name
        self._product_price = _product_price
        self._product_brand = _product_brand
        self._product_img = _product_img
        self._product_description = _product_description
        self._product_stock = _product_stock



class Cart(db.Model):
	serial_no=db.Column((db.Integer), primary_key=True)
	product_id=db.Column(db.Integer, unique=True)
	customer_id=db.Column(db.Integer)
	product_name=db.Column(db.String(100))
	product_image=db.Column(db.String(50))
	def __init__(self, product_id, customer_id, product_name, product_image):
		self.product_id=product_id
		self.customer_id=customer_id
		self.product_name=product_name
		self.product_image=product_image


class Users(db.Model):
    user_id=db.Column((db.Integer), primary_key=True)
    user_name=db.Column(db.String(500), unique=True, nullable=False)
    user_email=db.Column(db.String(500), unique=True, nullable=False)
    user_password=db.Column(db.String(500), nullable=False)
    user_address=db.Column(db.String(1000), nullable=False)
    user_city=db.Column(db.String(500), nullable=False)
    user_state=db.Column(db.String(500), nullable=False)
    user_zip=db.Column(db.String(50), nullable=False)
    def __init__(self, user_id, user_name, user_email, user_password, user_address,  user_city, user_state, user_zip):
        self.user_id=user_id
        self.user_name=user_name
        self.user_email=user_email
        self.user_password=user_password
        self.user_address=user_address
        self.user_city=user_city
        self.user_state=user_state
        self.user_zip=user_zip


class Orders(db.Model):
    customer_name=db.Column(db.String(500), nullable=False)
    customer_email=db.Column(db.String(500), unique=True, nullable=False)
    customer_address=db.Column(db.String(1000), nullable=False)
    customer_city=db.Column(db.String(500), nullable=False)
    customer_state=db.Column(db.String(500), nullable=False)
    customer_zip=db.Column(db.String(50), nullable=False)
    product_quantity=db.Column(db.Integer, nullable=False)
    def __init__(self, customer_name, customer_email, customer_address, customer_city, customer_state, customer_zip, product_quantity):
        self.customer_name=customer_name
        self.customer_email=customer_email
        self.customer_address=customer_address
        self.customer_city=customer_city
        self.customer_state=customer_state
        self.customer_zip=customer_zip
        self.product_quantity=product_quantity
