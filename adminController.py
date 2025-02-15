#!/env/bin/python3
# coding: utf-8

from config import *
from models import Admin
from models import Product
from models import User
from models import Order

# creating an object for admin-controller
adminController = Blueprint('adminController', __name__, template_folder="templates", static_folder="static")


@adminController.route('/admin')
@adminController.route('/admin/home')
@adminController.route('/admin/products')
@adminController.route('/admin/')
def admin():
    if "admin" in session:
        Products = Product.query.all()
        return render_template('admin.jinja', products=Products)
    else:
        flash('Please Login')
        return redirect(url_for('adminController.adminLogin'))


@adminController.route('/admin/products/edit', methods=['POST', 'GET'])
def editProduct():

    if request.method == 'POST':
        if 'admin' in session:
            # Requesting form data
            productname = request.form['productname']
            productprice = request.form['productprice']
            productbrand = request.form['productbrand']
            stockstatus = request.form['stockstatus']
            productdescription = request.form['productdescription']
            productimage = request.files['productimage']

            # Querying the database for the product to be updated
            found_product = Product.query.filter_by(product_name=productname).first()
           
            # checking if the filename is null
            if productimage.filename != '':
                # Securing the filename 
                secured_filename = secure_filename(productimage.filename)
                filename = found_product.product_image

                # Deleting old product image and saving the new image
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                productimage.save(os.path.join(app.config['UPLOAD_FOLDER'], secured_filename))
                
                # Updating the sql database to new values
                found_product.product_name = productname
                found_product.product_price = productprice
                found_product.product_brand = productbrand
                found_product.stock_status = stockstatus
                found_product.product_description = productdescription
                found_product.product_image = secured_filename
                
                # Commit database session
                db.session.commit()

                flash('Product updated successfully')
                return redirect(url_for('adminController.admin'))
            else:
                flash('No file selected')
                return redirect(url_for('adminController.editproduct'))
        else:
            # Throw a 403 html status code
            abort(403)
    else:
        return redirect(url_for('adminController.admin'))


@adminController.route('/admin/products/edit/<productName>', methods=['GET', 'POST'])
def editproduct(productName):
    
    if 'admin' in session:
        # Query database for product and render the edit page
        found_product = Product.query.filter_by(product_name=productName).first()
        return render_template('edit-products.jinja', product=found_product)
    else:
        # Throw a 403 html status code
        abort(403)


@adminController.route('/admin/login', methods=['POST', 'GET'])
def adminLogin():

  if request.method == "POST":
        # Check if the admin is already logged in
         if 'admin' in session:
             flash('Already Logged in')
             return redirect(url_for('adminController.admin'))
         
         elif request.method == "POST":
             
             # Setting session to permanent
             session.permanent = True

             # Query form and database for data
             username = request.form['Name']
             password = request.form['Password']
             found_admin = Admin.query.filter_by(admin_name=username).first()
             
             # Checking credentials
             if found_admin is not None and found_admin.admin_name == username:
                if bcrypt.check_password_hash(found_admin.admin_password, password):
                    session['admin'] = found_admin.admin_name
                    flash('Login Successful')
                    return redirect(url_for('adminController.admin'))
                else:
                   flash('Incorrect username or password')
                   return redirect(url_for('adminController.adminLogin'))
             else:
                 flash('Incorrect username or password')
                 return redirect(url_for('adminController.adminLogin'))
  else:
      return render_template('admin-login.jinja')


@adminController.route('/admin/logout')
def adminLogout():

    # Delete session data
    session.pop('admin', '')
    return redirect(url_for('adminController.adminLogin'))



@adminController.route('/admin/products/create', methods=['POST', 'GET'])
def create():

    if 'admin' in session:
        if request.method == "POST":

            # Query form data
            productname = request.form['productname']
            productprice = request.form['productprice']
            productbrand = request.form['productbrand']
            stockstatus = request.form['stockstatus']
            productdescription = request.form['productDescription']
            file = request.files['filename']
        
            try:
                if file.filename != '':

                    # Secure filename
                    secured_filename = secure_filename(file.filename)
                    
                    # Save file
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], secured_filename))
                    
                    # Declare database model data and commit it to database 
                    product = Product(product_name=productname, product_price=productprice, product_brand=productbrand,
                                      product_image=secured_filename, product_description=productdescription, stock_status=stockstatus)
                    db.session.add(product)
                    db.session.commit()

                    flash("Product created successfully")
                    return redirect(url_for('adminController.admin'))
                else:
                    flash('No file selected')
                    return redirect(url_for('adminController.create'))
            
            except:
                  flash("Error creating product")
                  return redirect(url_for('adminController.create'))
        else:
            return render_template('add-products.jinja')

    else:
        return render_template("add-products.jinja")


@adminController.route('/admin/products/delete/<productname>', methods=['POST', 'GET'])
def deleteProduct(productname):

    if request.method == 'POST' or productname:
        if 'admin' in session:
            productName = productname

            # Query database for product 
            found_product = Product.query.filter_by(product_name=productName).first()
            filename = found_product.product_image

            if found_product is not None:

                # Delete product data from database
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db.session.delete(found_product)
                db.session.commit()
                flash('Product Deleted successfully')
                return redirect(url_for('adminController.admin'))
            else:
                flash('The product does not exist')
                return redirect(url_for('adminController.admin'))
        else:
            flash('Please Login First')
            return redirect(url_for('adminController.adminlogin'))
            

@adminController.route('/admin/orders/all')
def orders():

    if 'admin' in session:

        # Query database for order data
        Orders = Order.query.all()
        return render_template('admin-orders.jinja', orders=Orders)
    else:
        flash('Please Login First')
        return redirect(url_for('adminController.adminlogin'))


@adminController.route('/admin/users/all')
def viewusers():

    if 'admin' in session:

        # Query database for users
        Users = User.query.all()
        return render_template('users.jinja', users=Users)


@adminController.route('/admin/new', methods=['POST', 'GET'])
def addAdmin():

    if request.method == 'POST':
        if 'admin' in session:

            # Request form data
            adminName = request.form['Name']
            adminPassword = request.form['Password']

            # Query database for data
            found_admin = Admin.query.filter_by(admin_name=adminName).first()
            
            if found_admin != '':
                flash('Admin already exists')
                return redirect(url_for('adminController.addAdmin'))
            else:
                # Add data to database
                admin = Admin(admin_name=adminName, admin_password=adminPassword)
                db.session.add(admin)
                db.session.commit()

                flash('New admin created successfully')
                return redirect(url_for('adminController.admin'))
        else:
            flash('Please Login')
            return redirect(url_for('adminController.adminLogin'))
    else:
        if 'admin' in session:
            return render_template('add-admin.jinja')
        else:
            abort(403)


@adminController.route('/admin/orders/view/all')
def allOrders():

    if 'admin' in session:
        # Query database for orders
        Orders = Order.query.all()
        return render_template('admin-orders.jinja', orders=Orders)
    else:
        abort(403)


@adminController.route('/admin/orders/view/<order_id>')
def viewOrder(order_id):
    if 'admin' in session:
        # Get data from database
        order = Order.query.filter_by(order_id=order_id).first()
        products = OrderProduct.query.filter_by(order_id=order_id).all()
        return render_template('admin-view-order.jinja', order=order, products=products)
    else:
        abort(403)
