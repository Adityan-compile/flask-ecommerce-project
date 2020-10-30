from flask import Flask, render_template
from flask import redirect, url_for
from flask import request, session
from flask import Blueprint, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'products.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

class products(db.Model):
    _id = db.coloumn(db.integer, primary_key=True)
    _product_name = db.coloumn( db.String(100))
    _product_price = db.coloumn(db.String(8))
    _product_brand = db.coloumn(db.String(100))
    _product_img = db.coloumn(db.String(100))
    _product_description = db.coloumn(db.String(2000))
    def __init__(self):
        self._id = _id
        self._product_name = _product_name
        self._product_price = _product_price
        self._product_brand = _product_brand
        self._product_img = _product_img
        self._product_description = _product_description



class cart(db.Model):
	serial_no=db.Column(db.Integer,primary_key=True)
	product_id=db.Column(db.Integer)
	customer_id=db.Column(db.Integer)
	product_name=db.Column(db.String(100))
	product_image=db.Column(db.String(50))
	def __init__(self,product_id,customer_id,product_name,product_image):
		self.product_id=product_id
		self.customer_id=customer_id
		self.product_name=product_name
		self.product_image=product_image