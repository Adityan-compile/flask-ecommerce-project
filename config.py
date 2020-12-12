#!/env/bin/python3
# coding: utf-8

import os
from datetime import timedelta, date
from flask import Flask, flash, redirect, render_template, request, session, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from  sqlalchemy.sql.expression import func
from dotenv import load_dotenv
from dotenv import find_dotenv
import razorpay
import json


# Loading environment variables
load_dotenv(find_dotenv())


# Initialising flask app.
app = Flask(__name__)


# Configuring Payment Gateway
APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
razorpay_client = razorpay.Client(auth=(APP_ID, APP_SECRET))


# configuring file uploads
ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg']
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')

# configuring session storage
app.config['SECRET_KEY'] = os.getenv('ECOM_SECRET_KEY')
app.permanent_session_lifetime = timedelta(days=30)


# configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_PATH')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


db = SQLAlchemy(app)      #initialize db
bcrypt = Bcrypt(app)      #initialize bcrypt
