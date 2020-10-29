import os
from flask import Flask,render_template,url_for,request,session,flash,redirect	
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
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

@app.route('/home')
@app.route('/')
def home():
   return render_template("index.html.jinja")

@app.route('/admin')
@app.route('/admin/home')
def admin():
   return render_template("admin.html.jinja")   

@app.errorhandler(404)
def error(e):
  return render_template("404.html.jinja"), 200

if "__name__" == "__main__":
    #db.create_all()
    app.run(debug=True)
