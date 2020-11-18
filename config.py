#!/env/bin/python3
# coding: utf-8

import os
from datetime import timedelta
from flask import Flask, flash, redirect, render_template, request, session, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from  sqlalchemy.sql.expression import func
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()

app = Flask(__name__)

# configuring file uploads
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# configuring session storage
app.config['SECRET_KEY'] = os.getenv('ECOM_SECRET_KEY')
app.permanent_session_lifetime = timedelta(days=30)


# configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_PATH')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)      #initialize db
bcrypt = Bcrypt(app)      #initialize bcrypt
