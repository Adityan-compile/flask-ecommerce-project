from flask import Flask, render_template
from flask import redirect, url_for
from flask import request, session
from flask import Blueprint, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# configuring file uploads
UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#configuring session storage
app.secret_key = "fc1dj4ad6s47dep932089rjdnc+_{EF37W998VW798DeqVDrewASewC+};:}WE{V}]D_WS_O!_+"
app.permanent_session_lifetime = timedelta(days=30)

basedir = os.path.abspath(os.path.dirname(__file__))

#configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

class products(db.Model):
    _id = db.column(db.integer, primary_key=True)
    _product_name = db.column( db.String(100))
    _product_price = db.column(db.String(8))
    _product_brand = db.column(db.String(100))
    _product_img = db.column(db.String(100))
    _product_description = db.column(db.String(2000))
    _product_stock = db.column(db.String(10))
    def __init__(self,_id, _product_name,  _product_price,  _product_brand, _product_img, _product_description, _product_stock):
        self._id = _id
        self._product_name = _product_name
        self._product_price = _product_price
        self._product_brand = _product_brand
        self._product_img = _product_img
        self._product_description = _product_description
        self._product_stock = _product_stock



class cart(db.Model):
	serial_no=db.Column(db.Integer,primary_key=True)
	product_id=db.Column(db.Integer)
	customer_id=db.Column(db.Integer)
	product_name=db.Column(db.String(100))
	product_image=db.Column(db.String(50))
	def __init__(self, product_id, customer_id, product_name, product_image):
		self.product_id=product_id
		self.customer_id=customer_id
		self.product_name=product_name
		self.product_image=product_image


class users(db.Model):
    user_id=db.column(db.integer,primary_key=True)
    user_name=db.column(db.String(500))
    user_email=db.column(db.string(500))
    user_password=db.column(db.String(500))
    user_address=db.column(db.String(1000))
    user_city=db.column(db.String(500))
    user_state=db.column(db.String(500))
    user_zip=db.column(db.String(50))
    def __init__(self, user_id, user_name, user_email, user_password, user_address,  user_city, user_state, user_zip):
        self.user_id=user_id
        self.user_name=user_name
        self.user_email=user_email
        self.user_password=user_password
        self.user_address=user_address
        self.user_city=user_city
        self.user_state=user_state
        self.user_zip=user_zip