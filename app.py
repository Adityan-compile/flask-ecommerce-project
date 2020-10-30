
from flask import Flask,render_template,url_for,request,session,flash,redirect	
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

#from models import *


@app.route('/home')
@app.route('/')
def home():
   return render_template("index.html.jinja")

@app.route('/admin')
@app.route('/admin/home')
@app.route('/admin/products')
@app.route('/admin/')
def admin():
   return render_template("admin.html.jinja")

@app.route('/admin/delete')
@app.route('/admin/edit')
def admintasks():
   return render_template('admin.html.jinja') 

@app.route('/login')  
def login():
   return render_template("login.html.jinja")

@app.route('/cart')
def addtocart():
   return render_template("cart.html.jinja")

@app.route('/signup')
def signup():
   return render_template("signup.html.jinja")

@app.route('/admin/create')
def create():
   return render_template("add-products.html.jinja")

@app.errorhandler(404)
def error(e):
   return render_template("404.html.jinja")

if '__name__' == '__main__':
   db.create_all()
   app.run(debug=True)
