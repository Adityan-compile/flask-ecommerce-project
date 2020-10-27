from flask import Flask, render_template, url_for, redirect, request, session, flash
from datetime import timedelta
import sqlalchemy

app = Flask(__name__)
app.secret_key = "awwep932089rjdnc+_{EFWVWDVDASC+};:}WE{V}]D_WS_O!_+0id-0wkWS+"


@app.route("/home")
def home():
    return render_template("index.html.jinja", title="Home", content="Home"), 200

@app.route("/redirect")
def redirection():
    print("Redirected successfully")
    return redirect(url_for("home")), 307

if "__name__" == "__main__":
    app.run(debug=True)
