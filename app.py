from flask import Flask, render_template, url_for, request, session, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import *


@app.route('/home')
@app.route('/')
def home():
    if "user" in session:
        return render_template("index.html.jinja")
    else:
        flash('You are not logged in')
        return redirect('login')


@app.route('/admin')
@app.route('/admin/home')
@app.route('/admin/products')
@app.route('/admin/')
def admin():
    return render_template("admin.html.jinja")


@app.route('/admin/delete')
@app.route('/admin/edit')
def admintasks():
    return render_template('admin.html.jinja')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        session.permanent = True
        username = request.form['Name']
        password = request.form['Password']
        found_user = Users.query.filter_by(name=username).first()
        if found_user.user_name == username:
           if bcrypt.check_password_hash(found_user.password, password):
               db.session.commit()
               session['user'] = found_user.user_name
               flash('Login Successful')
               return redirect('home')
           else:
               flash('Incorrect username or password')
               return redirect('login')
        else:
            if "user" in session:
                flash('Already Logged in') 
    else:
        return render_template("login.html.jinja")


@app.route('/logout')
def logout():
    session.pop('user','')


@app.route('/cart')
def addtocart():
    return render_template("cart.html.jinja")


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        user_name = request.form['Name']
        user_email = request.form['Email']
        password = request.form['Password']
        phonenumber = request.form['Phonenumber']
        address = request.form['Address']
        city = request.form['City']
        state = request.form['State']
        zip_code = request.form['Zip']

        username = Users(user_name, "")
        db.session.add(username)

        email = Users(user_email, "")
        db.session.add(email)
        
        Password = Users(password, "")
        pw_hash =  bcrypt.generate_password_hash(Password)
        db.session.add(pw_hash)

        Phonenumber = Users(phonenumber, "")
        db.session.add(Phonenumber)

        Address = Users(address, "")
        db.session.add(Address)

        City = Users(city, "")
        db.session.add(City)

        State = Users(city, "")
        db.session.add(State)

        Zip_code = Users(zip_code, "")
        db.session.add(Zip_code)

        db.session.commit()

        session['user'] = username

    else:
        return render_template("signup.html.jinja")


@app.route('/admin/create')
def create():
    if request.method == "POST":
        product_name = request.form['productname']
        product_price = request.form['productprice']
        product_brand = request.form['productbrand']
        stock_status = request.form['stockstatus']
        product_description = request.form['productdescription']
        product_image = request.file['filename']

        try:
            secured_filename = secure_filename(product_name.filename)
            product_image.save(secured_filename)
            
            name = Products(product_name, "")
            db.session.add(name)

            price = Products(product_price, "")
            db.session.add(price)

            brand = Products(product_brand, "")
            db.session.add(brand)
    
            db.session.add(secured_filename, "")

            status = Products(stock_status, "")
            db.session.add(status)

            description = Products(product_description, "")
            db.session.add(description)

            flash("Product created successfully")
            return redirect('admin')
        except:
            return redirect('admin')
            flash("Error creating prooduct")    

    else:
        return render_template("add-products.html.jinja")


@app.errorhandler(404)
def error(e):
    return render_template("404.html.jinja")


if '__name__' == '__main__':
    app.run(debug=True)
