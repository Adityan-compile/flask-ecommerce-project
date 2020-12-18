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
        return render_template('index.jinja', products=found_products)
    else:
        return render_template("index.jinja", products=Product.query.order_by(func.random()).all())


@userController.route('/user/profile')
def profile():

    if 'user' in session:

        # Using session data to authenticate the user
        email = session.get('user')
        user = User.query.filter_by(user_email=email).first()
        return render_template('profile.jinja', info=user)
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
    if 'user' in session:
        flash('Already Logged in')
        return redirect(url_for('userController.home'))
    else:
        return render_template('login.jinja')


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
        products = Cart.query.filter_by(customer_email=email).all()
        # cartTotal = Cart.query.with_entities(func.sum(Cart.product_price)).filter(Cart.customer_email==email).all()
        # cartTotal = str(cartTotal)
        # chars = ['[' , ']' , '(' , ')' , ',']

        # for i in chars:
        #     cartTotal = cartTotal.replace(i, '')
      
        cartTotal = 0

        for  product in products:
            cartTotal += product.product_price
         
        session['total'] = cartTotal

        return render_template("cart.jinja", carttotal=str(cartTotal), products=cart)
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

            # Get data from session and database
            email = session.get('user')
            Total = session.get('total')
            user = User.query.filter_by(user_email=email).first()
                                  
            current_date = date.today()

            # Get data from database
            products = Cart.query.filter(customer_email=email).all()

            # Send data to payment gateway for checkout
            order_amount = Total * 100
            order_currency = 'INR'
            order_receipt = 'order_rcptid_11'
            order = razorpay_client.order.create({ 'amount' : int(order_amount), 'currency' : order_currency, 'receipt' : order_receipt, 'payment_capture' : '1'})                      
            
            order = Order(order_id=order['order_id'],order_date=current_date, customer_name=user.user_name, customer_address=user.user_address, customer_city=user.user_city,
                          customer_state=user.user_state, customer_phone=user.user_phonenumber, customer_zip=user.user_zip, payment_status ='Pending', product_name=products.product_name, total_order_price=Total )
            
            db.session.add(order)
            db.session.commit()
            # Get api key from environment variables
            API_KEY = os.getenv('API_KEY')

            return render_template('checkout.jinja', total=Total, user=user, order=order, API_KEY=API_KEY)
        else:

            # Get json request data 
            data = request.get_json()

            payment_id = data['razorpay_payment_id']
            razorpay_signature = data['razorpay_signature']
            order_id = data['order_id']
            
            # Query database and update values
            Order = Order.query.filter_by(order_id=order_id).first()
            Order.payment_id = payment_id
            order.razorpay_signature = razorpay_signature
            order.payment_status = 'Successful'
            db.session.commit()
            
            # Delete cart data from database 
            cart = Cart.query.filter_by(customer_email=email).all()
            db.session.delete(cart)
            db.session.commit()

            flash('Order Placed Successfully')
            return redirect(url_for('userController.paymentSuccess', order_id=order_id))

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
        
        if validate_email(useremail, verify=True):
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
            flash('Entered email does not exist')
            return redirect(url_for('userController.signup'))
    else:
        return render_template('signup.jinja')


@userController.route('/user/changepassword', methods=['GET', 'POST'])
def changePassword():

    if 'user' in session:
        
        if request.method == 'GET':
            return render_template('changePassword.jinja')
        else:
            # Get form data 
            oldPassword = request.form['oldPassword']
            newPassword = request.form['newPassword']
            confirmPassword = request.form['confirmPassword']

            # Get data from session and database
            email = session.get('user')
            user = User.query.filter_by(user_email=email).first()
            
            # Check passwords and update if the passwords match
            if oldPassword == user.user_password:
                if newPassword == confirmPassword:
                    user.user_password = bcrypt.generate_password_hash(newPassword)
                    db.session.commit()

                    flash('Password changed successfully')
                    return redirect(url_for('userController.profile'))
                else:
                    flash('Entered passwords does not match')
                    return redirect(url_for('userController.changePassword'))
            else:
                flash('Password is incorrect')
                return redirect(url_for('userController.changePassword'))
    else:
        flash('Please login')
        return redirect(url_for('userController.login'))


@userController.route('/user/checkout/payment/success/<order_id>')
def paymentSuccess(order_id):
    if 'user' in session:
        return render_template('payment-Success.jinja', order_id=order_id)
    else:
        flash('Please Login')
        return redirect(url_for('userController.login'))


@userController.route('/user/checkout/payment/fail/<_order_id>')
def paymentFailed(_order_id):
    if 'user' in session:
        
        # Delete failed order from database   
        order = razorpay_client.query.filter_by(order_id=_order_id).first()
        db.session.delete(order)
        db.session.commit()

        return render_template('payment-Failed.jinja')
    else:
        flash('Please Login')
        return redirect(url_for('userController.login'))


@userController.route('/user/account/delete', methods=['POST', 'GET'])
def deleteAccount():
    if 'user' in session:
        # Get session data and query database 
        email = session.get('user')
        user = User.query.filter_by(user_email=email).first()

        # Delete user account
        db.session.delete(user)
        db.session.commit()

        session.pop('user')

        flash('Account Deleted Successfully')
        return redirect(url_for('userController.signup'))


@userController.route('/user/order/receipt/<order_id>')
def orderRecipt(order_id):
    
    if 'user' in session:
        order = Order.query.filter_by(order_id=order_id).first()
        return render_template('receipt.jinja', order=order)
    else:
        flash('Please Login')
        return redirect(url_for('userController.login'))


# @userController.route('/test')
# def test():
#     return render_template('checkout.jinja')