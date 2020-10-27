
from flask import Flask, render_template 
from flask import redirect, url_for
from flask import request, session
from flask import Blueprint, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "fc1dj4ad6s47dep932089rjdnc+_{EF37W998VW798DeqVDrewASewC+};:}WE{V}]D_WS_O!_+"
app.permanent_session_lifetime = timedelta(days=30)

#app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.sqlite3'
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#db = SQLAlchemy(app)

# class users(db.Model):
#    _id = db.coloumn("id", db.integer, primary_key = True)
#    name = db.coloumn("name", db.String(100))
#    email = db.coloumn("email", db.String(320))

#    def __init__(self,):
#        self.name = name
#        self.email = email
#        self.id = id

@app.route("/home")
def home():
    return render_template("index.html.jinja", title = "Home", content = "Home"), 200

@app.route("/redirect")
def redirection():
    print("Redirected successfully")
    return redirect(url_for("home")), 307

if "__name__" == "__main__":
  # db.create_all()
    app.run(debug=True)
