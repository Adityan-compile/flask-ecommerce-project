#!/env/bin/python3
# coding: utf-8

from config import *
from models import Product
from models import User
from models import Order
from models import Cart

# creating an object for user-controller
userController = Blueprint('userController', __name__, template_folder="templates", static_folder="static")

@userController.route('/home', methods=['GET', 'POST'])
@userController.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        # Query form and database to search for the product
        search = request.form['search']
        found_products = Product.query.filter_by(Product.product_name.like('%'+search+'%')).all()
        return render_template('index.html.jinja', products=found_products)
    else:
        return render_template("index.html.jinja", products=Product.query.order_by(func.random()).all())


@userController.route('/profile')
def profile():

    if 'user' in session:

        # Using session data to authenticate the user
        email = session.get('user')
        user = User.query.filter_by(user_email=email).first()
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

         # Setting session to permanent
          session.permanent = True

          # Request form data
          # username = request.form['Name']
          password = request.form['Password']
          email = request.form['Email']
          
          # Query database for user
          found_user = User.query.filter_by(user_email=email).first()

          # Authenticate user
          if found_user is not None and found_user.user_email ==email:
             if bcrypt.check_password_hash(found_user.user_password, password):

                  # Set session data
                  session['user'] = found_user.user_email
                  flash('Login Successful')
                  return redirect(url_for('userController.home'))
             else:
                 flash('Incorrect Credentials')
                 return redirect(url_for('userController.login'))
          else:
              flash('Incorrect Credentials')
              return redirect(url_for('userController.login'))
  else:
      return render_template('login.html.jinja')


@userController.route('/logout')
def logout():

    # Delete session data
    session.pop('user', '')
    flash('Logged out successfully')
    return redirect(url_for('userController.login'))



@userController.route('/cart')
def cart():

    if 'user' in session:

        # Get data from session and database
        email = session.get('user')
        cart = Cart.query.filter_by(customer_email=email).all()
        cartTotal = Cart.query.with_entities(func.sum(Cart.product_price)).filter_by(customer_email=email).all()
        return render_template("cart.html.jinja", carttotal=cartTotal, products=cart)
    else:
        flash('Please Login')
        return redirect(url_for('userController.login'))


@userController.route('/cart/add/<productName>',methods=['POST', 'GET'])
def addtocart(productName):

    if request.method == 'POST' or productName:
        if 'user' in session:
            # Get data from session and database
            email = session.get('user')
            found_user = User.query.filter_by(user_email=email).first()
            found_product = Product.query.filter_by(product_name=productName).first()

            # Declare and commit database models and data
            cart = Cart(product_name=found_product.product_name, customer_name=found_user.user_name, customer_email=found_user.user_email, 
                        product_image=found_product.product_image, product_price=found_product.product_price)
            db.session.add(cart)
            db.session.commit()
            return redirect(url_for('userController.cart'))
        else:
            flash('Please Login')
            return redirect(url_for('userController.login'))
    else:
        abort(400)


@userController.route('/cart/delete/<productName>', methods=['POST','GET'])
def deletefromcart(productName):

    if request.method == 'POST' or productName:
        if 'user' in session:
            # Get data from session and database and delete the corresponding product
            email = session.get('user')
            cart = Cart.query.filter_by(customer_email=email, product_name=productName).first()
            db.session.delete(cart)
            db.session.commit()
            return redirect(url_for('userController.cart'))
        else:
            flash('Please Login')
            return redirect(url_for('userController.login'))
    else:
        abort(400)


@userController.route('/checkout', methods=['POST', 'GET'])
def checkout():

    if 'user' in session:
        if request.method == 'GET':
            return render_template('checkout.html.jinja')
        else:

            # Get data from session and database
            email = session.get('user')
            user = User.query.filter_by(user_email=email).first()
            order = Order(customer_name=user.user_name, customer_address=user.user_address, customer_city=user.user_city,
                          customer_state=user.user_state, customer_phone=user.user_phonenumber, customer_zip=user.user_zip)
            
            # Send data to payment gateway for checkout
            amount = 5100
            payment_id = request.form['razorpay_payment_id']
            razorpay_client.payment.capture(payment_id, amount)
            return json.dumps(razorpay_client.payment.fetch(payment_id))

    else:
        return redirect(url_for('userController.login'))


@userController.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':

         # Get data from session 
        username = request.form['Name']
        useremail = request.form['Email']
        password = request.form['Password']
        phonenumber = request.form['Phonenumber']
        address = request.form['Address']
        city = request.form['City']
        state = request.form['State']
        zip_code = request.form['Zip']

        # Generate hash of password for storage
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Declare database models and data and commit to database
        user = User(user_name=username, user_email=useremail, user_address=address, user_password=pw_hash,
                    user_phonenumber=phonenumber, user_city=city, user_state=state, user_zip=zip_code)
        db.session.add(user)
        db.session.commit()

        # Set session data
        session['user'] = useremail
        return redirect(url_for('userController.home'))

    else:
        return render_template('signup.html.jinja')


@userController.route('/test')
def test():
    return render_template('checkout.html.jinja')