#!/env/bin/python3
# coding: utf-8

from config import *

errorController = Blueprint('errorController', __name__, template_folder="templates", static_folder="static")


@app.errorhandler(404)
def error404(e):
    message = "OOPS look's like you are lost"
    return render_template("error.html.jinja", err="404 Not Found!!", msg=message)


@app.errorhandler(403)
def error403(e):
    message = "Looks like you are trying to look into our little secret"
    return render_template('error.html.jinja', err='403 Forbidden', msg=message)


@app.errorhandler(500)
def error500(e):
    message = "Uh,Oh our servers encountered an error"
    return render_template('error.html.jinja', err="500 Internal Server Error", msg=message)


@app.errorhandler(413)
def error413(e):
    message = "Whoop's look's like you are way too heavy"
    return render_template('error.html.jinja', err='413 Payload too large', msg=message)


@app.errorhandler(409)
def error409(e):
    message = "Uh,Oh We are unable to handle your request, hang tight"
    return render_template('error.html.jinja', err="409 Conflict", msg=message)