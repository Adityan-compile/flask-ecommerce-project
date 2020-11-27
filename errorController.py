#!/env/bin/python3
# coding: utf-8

from config import *

# Creating an object for error controller
errorController = Blueprint('errorController', __name__, template_folder="templates", static_folder="static")


# Error handler for errors caused when the user tries to visit a nonexistant page or url
@app.errorhandler(404)
def error404(e):
    message = "OOPS look's like you are lost"
    return render_template("error.html.jinja", err="404 Not Found!!", msg=message)


# Error handler for errors caused when a user tries to access a forbidden page
@app.errorhandler(403)
def error403(e):
    message = "Looks like you are trying to look into our little secret"
    return render_template('error.html.jinja', err='403 Forbidden', msg=message)


# Error handler for errors caused by errors in application code
@app.errorhandler(500)
def error500(e):
    message = "our servers encountered an error"
    return render_template('error.html.jinja', err="500 Internal Server Error", msg=message)


# Error handler for errors caused by request payload size
@app.errorhandler(413)
def error413(e):
    message = "look's like you are carrying way too much stuff"
    return render_template('error.html.jinja', err='413 Payload too large', msg=message)


# Error handler for conflict errors during requests
@app.errorhandler(409)
def error409(e):
     message = "we are unable to handle your request, hang tight"
     return render_template('error.html.jinja', err="409 Conflict", msg=message)


# Error handler for http 400 error status 
@app.errorhandler(400)
def error400(e):
    message = "look's like our servers can't understand you"
    return render_template('error.html.jinja', err='400 Bad Request', msg=message)