# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  November 05, 2024 15:17:29
# Database: sqlite:////tmp/tmp.oZI5xxW7G9/TEST_1/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Category(SAFRSBaseX, Base):
    """
    description: Categorizes products into different types.
    """
    __tablename__ = 'categories'
    _s_collection_name = 'Category'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    ProductCategoryList : Mapped[List["ProductCategory"]] = relationship(back_populates="category")



class Customer(SAFRSBaseX, Base):
    """
    description: Represents the customers in the system, storing personal and contact information.
    """
    __tablename__ = 'customers'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    balance = Column(Float)
    credit_limit = Column(Float)

    # parent relationships (access parent)

    # child relationships (access children)
    AddressList : Mapped[List["Address"]] = relationship(back_populates="customer")
    OrderList : Mapped[List["Order"]] = relationship(back_populates="customer")
    ReviewList : Mapped[List["Review"]] = relationship(back_populates="customer")



class Product(SAFRSBaseX, Base):
    """
    description: Stores product information available for sale.
    """
    __tablename__ = 'products'
    _s_collection_name = 'Product'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    unit_price = Column(Float)

    # parent relationships (access parent)

    # child relationships (access children)
    InventoryList : Mapped[List["Inventory"]] = relationship(back_populates="product")
    ProductCategoryList : Mapped[List["ProductCategory"]] = relationship(back_populates="product")
    ReviewList : Mapped[List["Review"]] = relationship(back_populates="product")
    ItemList : Mapped[List["Item"]] = relationship(back_populates="product")



class Supplier(SAFRSBaseX, Base):
    """
    description: Contains supplier information for products.
    """
    __tablename__ = 'suppliers'
    _s_collection_name = 'Supplier'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact_info = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)



class Address(SAFRSBaseX, Base):
    """
    description: Stores addresses for customers.
    """
    __tablename__ = 'addresses'
    _s_collection_name = 'Address'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customers.id'))
    street = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("AddressList"))

    # child relationships (access children)



class Inventory(SAFRSBaseX, Base):
    """
    description: Manages inventory stock levels.
    """
    __tablename__ = 'inventory'
    _s_collection_name = 'Inventory'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('products.id'))
    quantity_in_stock = Column(Integer)

    # parent relationships (access parent)
    product : Mapped["Product"] = relationship(back_populates=("InventoryList"))

    # child relationships (access children)



class Order(SAFRSBaseX, Base):
    """
    description: Holds information about customer orders.
    """
    __tablename__ = 'orders'
    _s_collection_name = 'Order'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customers.id'))
    order_date = Column(DateTime)
    amount_total = Column(Float)
    date_shipped = Column(DateTime)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("OrderList"))

    # child relationships (access children)
    ItemList : Mapped[List["Item"]] = relationship(back_populates="order")
    PaymentList : Mapped[List["Payment"]] = relationship(back_populates="order")
    ShipmentList : Mapped[List["Shipment"]] = relationship(back_populates="order")



class ProductCategory(SAFRSBaseX, Base):
    """
    description: Links products to their categories.
    """
    __tablename__ = 'product_categories'
    _s_collection_name = 'ProductCategory'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('products.id'))
    category_id = Column(ForeignKey('categories.id'))

    # parent relationships (access parent)
    category : Mapped["Category"] = relationship(back_populates=("ProductCategoryList"))
    product : Mapped["Product"] = relationship(back_populates=("ProductCategoryList"))

    # child relationships (access children)



class Review(SAFRSBaseX, Base):
    """
    description: Stores customer reviews for products.
    """
    __tablename__ = 'reviews'
    _s_collection_name = 'Review'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('products.id'))
    customer_id = Column(ForeignKey('customers.id'))
    rating = Column(Integer)
    comment = Column(String)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("ReviewList"))
    product : Mapped["Product"] = relationship(back_populates=("ReviewList"))

    # child relationships (access children)



class Item(SAFRSBaseX, Base):
    """
    description: Represents individual items in an order.
    """
    __tablename__ = 'items'
    _s_collection_name = 'Item'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('orders.id'))
    product_id = Column(ForeignKey('products.id'))
    quantity = Column(Integer)
    unit_price = Column(Float)
    amount = Column(Float)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("ItemList"))
    product : Mapped["Product"] = relationship(back_populates=("ItemList"))

    # child relationships (access children)



class Payment(SAFRSBaseX, Base):
    """
    description: Records customer payments against orders.
    """
    __tablename__ = 'payments'
    _s_collection_name = 'Payment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('orders.id'))
    date = Column(DateTime)
    amount = Column(Float, nullable=False)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("PaymentList"))

    # child relationships (access children)



class Shipment(SAFRSBaseX, Base):
    """
    description: Details shipments related to customer orders.
    """
    __tablename__ = 'shipments'
    _s_collection_name = 'Shipment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('orders.id'))
    shipment_date = Column(DateTime)
    tracking_number = Column(String)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("ShipmentList"))

    # child relationships (access children)
