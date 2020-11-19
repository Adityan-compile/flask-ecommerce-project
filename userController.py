#!/env/bin/python3
# coding: utf-8

from config import *
from models import Product
from models import User
from models import Order
from models import Cart

# creating an object for user-controller
userController = Blueprint('userController', __name__, template_folder="templates", static_folder="static")

@userController.route('/home')
@userController.route('/')
def home():
    if "user" in session:
        return render_template("index.html.jinja", products=Product.query.order_by(func.random()).all())
    else:
        flash('You are not logged in')
        return redirect(url_for('userController.login'))


@userController.route('/profile')
def profile():
    if 'user' in session:
        username = session.get('user')
        user = User.query.filter_by(user_name=username).first()
        return render_template('profile.html.jinja', info=user)
    else:
        flash('Please Login')
        return redirect(url_for('userController.login'))


@userController.route('/login', methods=['POST', 'GET'])
def login():
  if request.method == "POST":
     if 'user'in session:
         flash('Already logged in')
         return redirect(url_for('home'))
     elif request.method == "POST":
          session.permanent = True
          username = request.form['Name']
          password = request.form['Password']
          found_user = User.query.filter_by(user_name=username).first()
          if found_user is not None and found_user.user_name == username:
             if bcrypt.check_password_hash(found_user.user_password, password):
                  session['user'] = found_user.user_name
                  flash('Login Successful')
                  return redirect(url_for('userController.home'))
             else:
                 flash('Incorrect username or password')
                 return redirect(url_for('userController.login'))
          else:
              flash('Incorrect username or password')
              return redirect(url_for('userController.login'))
  else:
      return render_template('login.html.jinja')


@userController.route('/logout')
def logout():
    session.pop('user', '')
    flash('Logged out successfully')
    return redirect(url_for('userController.login'))



@userController.route('/cart')
def cart():
    if 'user' in session:
        username = session.get('user')
        cart = Cart.query.filter_by(customer_name=username).all()
        return render_template("cart.html.jinja", serialnumber=cart.serial_number, productname=cart.product_name, productquantity=cart.product_quantity, productprice=cart.product_price)
    else:
        flash('Please Login')
        return redirect(url_for('userController.login'))


@userController.route('/checkout', methods=['POST', 'GET'])
def checkout():
    if 'user' in session:
        if request.method == 'GET':
            return render_template('checkout.html.jinja')
        else:
            username = session.get('user')
            user = User.query.filter_by(user_name=username).first()
            order = Order(customer_name=user.user_name, customer_address=user.user_address, customer_city=user.user_city,
                          customer_state=user.user_state, customer_phone=user.user_phonenumber, customer_zip=user.user_zip)
    else:
        return redirect(url_for('userController.login'))


@userController.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['Name']
        useremail = request.form['Email']
        password = request.form['Password']
        phonenumber = request.form['Phonenumber']
        address = request.form['Address']
        city = request.form['City']
        state = request.form['State']
        zip_code = request.form['Zip']

        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(user_name=username, user_email=useremail, user_address=address, user_password=pw_hash,
                    user_phonenumber=phonenumber, user_city=city, user_state=state, user_zip=zip_code)
        db.session.add(user)
        db.session.commit()

        session['user'] = username
        return redirect(url_for('userController.home'))

    else:
        return render_template('signup.html.jinja')


