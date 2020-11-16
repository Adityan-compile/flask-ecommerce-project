#!/env/bin/python3
# coding: utf-8

from config import *

errorController = Blueprint('errorController', __name__)

@app.errorhandler(404)
def error404(e):
    message = "OOPS look's like you are lost"
    return render_template("error.html.jinja", err="404 Not Found!!", msg=message), 404


@errorController.errorhandler(403)
def error403(e):
    message = "Looks like you are trying to look into our little secret"
    return render_template('error.html.jinja', err='403 Forbidden', msg=message), 403