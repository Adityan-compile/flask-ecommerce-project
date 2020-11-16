#!/env/bin/python3
# coding: utf-8

from config import *
from adminController import adminController
from userController import userController
from errorController import errorController


# registering blueprints for admin and user controllers
app.register_blueprint(userController)
app.register_blueprint(adminController)
app.register_blueprint(errorController)


if '__name__' == '__main__':
    app.run(debug=True)
