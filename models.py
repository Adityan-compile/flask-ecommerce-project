#!/env/bin/python3
# coding: utf-8

from sqlalchemy import Column, Integer, Table, Text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from config import db

Base = declarative_base()
metadata = Base.metadata


class Admin(db.Model):
    __tablename__ = 'Admins'

    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.Text, nullable=False)
    admin_password = db.Column(db.Text(100), nullable=False)


class Cart(db.Model):
    __tablename__ = 'Cart'

    serial_number = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.Text, nullable=False)
    customer_name =db.Column(db.Text, nullable=False)
    product_image = db.Column(db.Text, nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    product_price = db.Column(db.Text, nullable=False)


class Order(db.Model):
    __tablename__ = 'Orders'

    order_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.Text, nullable=False)
    customer_email = db.Column(db.Text, nullable=False)
    customer_address = db.Column(db.Text, nullable=False)
    customer_city = db.Column(db.Text, nullable=False)
    customer_state = db.Column(db.Text, nullable=False)
    customer_zip = db.Column(db.Text, nullable=False)
    customer_phone = db.Column(db.Text, nullable=False)
    payment_status = db.Column(db.Text, nullable=False)
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
    user_city = Column(db.Text, nullable=False)
    user_state = db.Column(db.Text, nullable=False)
    user_zip = db.Column(db.Text, nullable=False)


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)