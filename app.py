#!/env/bin/python3
# coding: utf-8

from config import *
from models import Admin
from models import User
from models import Cart
from models import Order
from models import Product


@app.route('/home')
@app.route('/')
def home():
    if "user" in session:
        return render_template("index.html.jinja", products=Product.query.order_by(func.random).all())
    else:
        flash('You are not logged in')
        return redirect(url_for('login'))


@app.route('/admin')
@app.route('/admin/home')
@app.route('/admin/products')
@app.route('/admin/')
def admin():
    if "admin" in session:
        Products = Product.query.all()
        return render_template("admin.html.jinja", products=Products, image="images/"+Products.product_image)
    else:
        return redirect(url_for('adminLogin'))


@app.route('/admin/delete')
@app.route('/admin/edit')
def admintasks():
    return render_template('admin.html.jinja')


@app.route('/profile')
def profile():
    if 'user' in session:
        username = session.get('user')
        user = User.query.filter_by(user_name=username).first()
        return render_template('profile.html.jinja', info=user)
    else:
        flash('Please Login')
        return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
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
                return redirect(url_for('home'))
            else:
                flash('Incorrect username or password')
                return redirect(url_for('login'))
        else:
            flash('Incorrect username or password')
            return redirect(url_for('login'))
   else:
        return redirect(url_for('home'))


@app.route('/admin/login', methods=['POST', 'GET'])
def adminLogin():
    if 'admin' in session:
        flash('Already logged in')
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        session.permanent = True
        username = request.form['Name']
        password = request.form['Password']
        found_admin = Admin.query.filter_by(admin_name=username).first()
        if found_admin is not None and found_admin.admin_name == username:
            if found_admin.admin_password == password:
                session['admin'] = username
                flash('Login Successful')
                return redirect(url_for('admin'))
            else:
                flash('Incorrect username or password')
                return redirect(url_for('adminLogin'))
        else:
            flash('Incorrect username or password')
            return redirect(url_for('Incorrect username or password'))


@app.route('/logout')
def logout():
    session.pop('user', '')
    return redirect(url_for('login'))


@app.route('/admin/logout')
def adminLogout():
    session.pop('admin', '')
    return redirect(url_for('adminLogin'))


@app.route('/cart')
def cart():
    if 'user' in session:
        username = session.get('user')
        cart = Cart.query.filter_by(customer_name=username).all()
        return render_template("cart.html.jinja", serialnumber=cart.serial_number, productname=cart.product_name, productquantity=cart.product_quantity, productprice=cart.product_price)
    else:
        flash('Please Login')
        return redirect(url_for('login'))


@app.route('/checkout', methods=['POST', 'GET'])
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
        return redirect(url_for('login'))


@app.route('/signup', methods=['POST', 'GET'])
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

        pw_hash = bcrypt.generate_password_hash(password)

        user = User(user_name=username, user_email=useremail, user_address=address, user_password=pw_hash,
                    user_phonenumber=phonenumber, user_city=city, user_state=state, user_zip=zip_code)
        db.session.add(user)
        db.session.commit()

        session['user'] = username
        return redirect(url_for('home'))

    else:
        return render_template("signup.html.jinja")


@app.route('/admin/create')
def create():
    if request.method == "POST":
        productname = request.form['productname']
        productprice = request.form['productprice']
        productbrand = request.form['productbrand']
        stockstatus = request.form['stockstatus']
        productdescription = request.form['productdescription']
        product_image = request.file['filename']

        try:
            secured_filename = secure_filename(product_image.filename)
            product_image.save(secured_filename)

            product = Product(product_name=productname, product_price=productprice, product_brand=productbrand,
                              product_image=secure_filename, product_description=productdescription, stock_status=stockstatus)
            db.session.add(product)
            db.session.commit()

            flash("Product created successfully")
            return redirect(url_for('admin'))
        except:
            flash("Error creating product")
            return redirect(url_for('admin'))

    else:
        return render_template("add-products.html.jinja")


@app.errorhandler(404)
def error(e):
    return render_template("404.html.jinja")


if '__name__' == '__main__':
    app.run(debug=True)
