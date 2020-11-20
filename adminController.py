#!/env/bin/python3
# coding: utf-8

from config import *
from models import Admin
from models import Product
from models import User
from models import Order

# creating an object for admin-controller
adminController = Blueprint('adminController', __name__,
                            template_folder="templates", static_folder="static")


@adminController.route('/admin')
@adminController.route('/admin/home')
@adminController.route('/admin/products')
@adminController.route('/admin/')
def admin():
    if "admin" in session:
        Products = Product.query.all()
        return render_template('admin.html.jinja', products=Products)
    else:
        return redirect(url_for('adminController.adminLogin'))


@adminController.route('/admin/edit')
def editProduct():
    return render_template('admin.html.jinja')


@adminController.route('/admin/login', methods=['POST', 'GET'])
def adminLogin():
  if request.method == "POST":
         if 'admin' in session:
             flash('Already Logged in')
             return redirect(url_for('adminController.admin'))
         elif request.method == "POST":
             session.permanent = True
             username = request.form['Name']
             password = request.form['Password']
             found_admin = Admin.query.filter_by(admin_name=username).first()

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
      return render_template('admin-login.html.jinja')


@adminController.route('/admin/logout')
def adminLogout():
    session.pop('admin', '')
    return redirect(url_for('adminController.adminLogin'))



@adminController.route('/admin/products/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        productname = request.form['productname']
        productprice = request.form['productprice']
        productbrand = request.form['productbrand']
        stockstatus = request.form['stockstatus']
        productdescription = request.form['productDescription']
        file = request.files['filename']
        
        try:
            if file.filename != '':
                    secured_filename = secure_filename(file.filename)

                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], secured_filename))

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
        return render_template("add-products.html.jinja")


@adminController.route('/admin/products/delete/<productname>', methods=['POST', 'GET'])
def deleteProduct(productname):
    if request.method == 'POST' or productname: 
        productName = productname
        found_product = Product.query.filter_by(product_name=productName).first()
        filename = found_product.product_image

        if found_product is not None:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db.session.delete(found_product)
            db.session.commit()
            flash('Product Deleted successfully')
            return redirect(url_for('adminController.admin'))
        else:
            flash('The product does not exist')
            return redirect(url_for('adminController.admin'))
            
