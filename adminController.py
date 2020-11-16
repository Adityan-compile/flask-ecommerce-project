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
        return render_template("admin.html.jinja", products=Products, image="images/"+Products.product_image)
    else:
        return redirect('adminLogin')


@adminController.route('/admin/delete')
@adminController.route('/admin/edit')
def admintasks():
    return render_template('admin.html.jinja')


@adminController.route('/admin/login', methods=['POST', 'GET'])
def adminLogin():
    if 'admin' in session:
        flash('Already logged in')
        return redirect('admin')
    
    if request.method == 'POST':
        session.permanent = True
        username = request.form['Name']
        password = request.form['Password']
        found_admin = Admin.query.filter_by(admin_name=username).first()
        if found_admin is not None and found_admin.admin_name == username:
            if found_admin.admin_password == password:
                session['admin'] = username
                flash('Login Successful')
                return redirect('admin')
            else:
                flash('Incorrect username or password')
                return redirect('adminLogin')
        else:
            flash('Incorrect username or password')
            return redirect('adminLogin')
    else:
        return render_template('admin-login.html.jinja')


@adminController.route('/admin/logout')
def adminLogout():
    session.pop('admin', '')
    return redirect('adminLogin')



@adminController.route('/admin/create')
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
            return redirect('admin')
        except:
            flash("Error creating product")
            return redirect('admin')

    else:
        return render_template("add-products.html.jinja")