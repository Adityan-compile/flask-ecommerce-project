#!/env/bin/python3
# coding: utf-8

import os
from datetime import timedelta
from flask import Flask, flash, redirect, render_template, request, session, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from  sqlalchemy.sql.expression import func

app = Flask(__name__)

# configuring file uploads
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# configuring session storage
app.secret_key = "fc1dj4ad6s47dep932089rjdnc+_{EF37W998VW798DeqVDrewASewC+};:}WE{V}]D_WS_O!_+"
app.permanent_session_lifetime = timedelta(days=30)


# configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)      #initialize db
bcrypt = Bcrypt(app)      #initialize bcrypt
