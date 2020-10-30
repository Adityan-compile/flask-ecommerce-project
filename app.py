import os
from flask import Flask,render_template,url_for,request,session,flash,redirect	
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import timedelta
#from werkzeug import secure_filename
#from flask.ext.uploads import UploadSet,configure_uploads,IMAGES
#from werkzeug.security import generate_password_hash, \
#     check_password_hash
#from flask_admin import Admin 
#from flask_admin import Admin, BaseView, expose
#from flask_admin.contrib.sqla import ModelView
#import re
#from models import *


#app.config['UPLOAD_FOLDER']=folder
#app.config['UPLOADED_PHOTOS_DEST']='static/images'

#configure_uploads(app,photos)

app = Flask(__name__)

app.secret_key = "fc1dj4ad6s47dep932089rjdnc+_{EF37W998VW798DeqVDrewASewC+};:}WE{V}]D_WS_O!_+"
app.permanent_session_lifetime = timedelta(days=30)

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

@app.errorhandler(404)
def error(e):
   return render_template("404.html.jinja")

if '__name__' == '__main__':
   #db.create_all()
   app.run(debug=True)
