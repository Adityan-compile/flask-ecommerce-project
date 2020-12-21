# coding: utf-8
from sqlalchemy import Column, Integer, Table, Text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from config import db

Base = declarative_base()
metadata = Base.metadata


class Admin(db.Model):
    __tablename__ = 'Admins'
    __table_args__ = {'extend_existing': True}


    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.Text, nullable=False)
    admin_password = db.Column(db.Text, nullable=False)


class Cart(db.Model):
    __tablename__ = 'Cart'

    serial_number = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.Text, nullable=False)
    customer_name = db.Column(db.Text, nullable=False)
    customer_email = db.Column(db.Text, nullable=False)
    product_image = db.Column(db.Text, nullable=False)
    product_price = db.Column(db.Text, nullable=False)


# t_Orders = Table(
#     'Orders', metadata,
#     Column('order_id', Text, nullable=False),
#     Column('payment_id', Text, nullable=False),
#     Column('razorpay_signature', Text, nullable=False),
#     Column('order_date', Text, nullable=False),
#     Column('customer_name', Text, nullable=False),
#     Column('customer_email', Text, nullable=False),
#     Column('customer_address', Text, nullable=False),
#     Column('customer_zip', Text, nullable=False),
#     Column('customer_phone', Text, nullable=False),
#     Column('payment_status', Text, nullable=False),
#     Column('product_name', Text, nullable=False),
#     Column('total_order_price', Text, nullable=False)
# )

class Order(db.Model):
    __tablename__ = 'Orders'

    serial_number = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Text, nullable=False)
    payment_id = db.Column(db.Text, nullable=False)
    razorpay_signature = db.Column(db.Text, nullable=False)
    order_date = db.Column(db.Text, nullable=False)
    customer_name = db.Column(db.Text, nullable=False)
    customer_email = db.Column(db.Text, nullable=False)
    customer_address = db.Column(db.Text, nullable=False)
    customer_zip = db.Column(db.Text, nullable=False)
    customer_phone = db.Column(db.Text, nullable=False)
    payment_status = db.Column(db.Text, nullable=False)
    product_name = db.Column(db.Text, nullable=False)
    total_order_price = db.Column(db.Text, nullable=False)

class Product(db.Model):
    __tablename__ = 'Products'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.Text, nullable=False)
    product_price = db.Column(db.Text, nullable=False)
    product_brand = db.Column(db.Text, nullable=False)
    product_image = db.Column(db.Text, nullable=False)
    product_description = db.Column(db.Text, nullable=False)
    stock_status = db.Column(db.Text, nullable=False)


class User(db.Model):
    __tablename__ = 'Users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Text, nullable=False)
    user_email = db.Column(db.Text, nullable=False)
    user_address = db.Column(db.Text, nullable=False)
    user_password = db.Column(db.Text, nullable=False)
    user_phonenumber = db.Column(db.Text, nullable=False)
    user_city = db.Column(db.Text, nullable=False)
    user_state = db.Column(db.Text, nullable=False)
    user_zip = db.Column(db.Text, nullable=False)


class OrderProduct(db.Model):
    __tablename__ = 'OrderProducts'

    serial_number = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Text, nullable=False)
    product_name = db.Column(db.Text, nullable=False)
    product_price = db.Column(db.Text, nullable=False)
    product_brand = db.Column(db.Text, nullable=False)
    product_image = db.Column(db.Text, nullable=False)
    

t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)
