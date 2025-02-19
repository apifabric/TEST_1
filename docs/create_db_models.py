# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Base class for SQLAlchemy models
Base = declarative_base()

class Customer(Base):
    """description: Represents the customers in the system, storing personal and contact information."""
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    balance = Column(Float, default=0.0)
    credit_limit = Column(Float, default=0.0)

class Product(Base):
    """description: Stores product information available for sale."""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    unit_price = Column(Float, nullable=True)

class Order(Base):
    """description: Holds information about customer orders."""
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=True)
    order_date = Column(DateTime, default=datetime.datetime.now)
    amount_total = Column(Float, default=0.0)
    date_shipped = Column(DateTime, nullable=True)

class Item(Base):
    """description: Represents individual items in an order."""
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True)
    quantity = Column(Integer, nullable=True)
    unit_price = Column(Float, nullable=True)
    amount = Column(Float, default=0.0)

class Supplier(Base):
    """description: Contains supplier information for products."""
    __tablename__ = 'suppliers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    contact_info = Column(String, nullable=True)

class Inventory(Base):
    """description: Manages inventory stock levels."""
    __tablename__ = 'inventory'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True)
    quantity_in_stock = Column(Integer, nullable=True)

class Shipment(Base):
    """description: Details shipments related to customer orders."""
    __tablename__ = 'shipments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=True)
    shipment_date = Column(DateTime, nullable=True)
    tracking_number = Column(String, nullable=True)

class Payment(Base):
    """description: Records customer payments against orders."""
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=True)
    date = Column(DateTime, default=datetime.datetime.now)
    amount = Column(Float, nullable=False)

class Category(Base):
    """description: Categorizes products into different types."""
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)

class ProductCategory(Base):
    """description: Links products to their categories."""
    __tablename__ = 'product_categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)

class Review(Base):
    """description: Stores customer reviews for products."""
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=True)
    rating = Column(Integer, nullable=True)
    comment = Column(String, nullable=True)

class Address(Base):
    """description: Stores addresses for customers."""
    __tablename__ = 'addresses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=True)
    street = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)

# Create an SQLite database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite', echo=False)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Insert sample data into each table
# Customers
customer1 = Customer(name="Alice Smith", email="alice@example.com", balance=300.0, credit_limit=500.0)
customer2 = Customer(name="Bob Jones", email="bob@example.com", balance=150.0, credit_limit=200.0)
session.add(customer1)
session.add(customer2)

# Products
product1 = Product(name="Widget", unit_price=25.0)
product2 = Product(name="Gadget", unit_price=45.0)
session.add(product1)
session.add(product2)

# Orders
order1 = Order(customer_id=1, amount_total=50.0, date_shipped=None)
order2 = Order(customer_id=2, amount_total=90.0, date_shipped=datetime.datetime.now())
session.add(order1)
session.add(order2)

# Items
item1 = Item(order_id=1, product_id=1, quantity=2, unit_price=25.0, amount=50.0)
item2 = Item(order_id=2, product_id=2, quantity=2, unit_price=45.0, amount=90.0)
session.add(item1)
session.add(item2)

# Suppliers
supplier1 = Supplier(name="Supplier A", contact_info="contactA@example.com")
supplier2 = Supplier(name="Supplier B", contact_info="contactB@example.com")
session.add(supplier1)
session.add(supplier2)

# Inventory
inventory1 = Inventory(product_id=1, quantity_in_stock=100)
inventory2 = Inventory(product_id=2, quantity_in_stock=200)
session.add(inventory1)
session.add(inventory2)

# Shipments
shipment1 = Shipment(order_id=1, shipment_date=None, tracking_number="TRACK123")
shipment2 = Shipment(order_id=2, shipment_date=datetime.datetime.now(), tracking_number="TRACK456")
session.add(shipment1)
session.add(shipment2)

# Payments
payment1 = Payment(order_id=1, date=datetime.datetime.now(), amount=50.0)
payment2 = Payment(order_id=2, date=datetime.datetime.now(), amount=90.0)
session.add(payment1)
session.add(payment2)

# Categories
category1 = Category(name="Electronics")
category2 = Category(name="Home Goods")
session.add(category1)
session.add(category2)

# Product Categories
product_category1 = ProductCategory(product_id=1, category_id=1)
product_category2 = ProductCategory(product_id=2, category_id=2)
session.add(product_category1)
session.add(product_category2)

# Reviews
review1 = Review(product_id=1, customer_id=1, rating=5, comment="Excellent product!")
review2 = Review(product_id=2, customer_id=2, rating=4, comment="Very good, prompt delivery.")
session.add(review1)
session.add(review2)

# Addresses
address1 = Address(customer_id=1, street="123 Elm St", city="Somewhere", state="NY", zip_code="12345")
address2 = Address(customer_id=2, street="456 Oak St", city="Anywhere", state="CA", zip_code="67890")
session.add(address1)
session.add(address2)

# Commit the session to write the data to the database
session.commit()
session.close()
