
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from datetime import datetime, timezone
from model.dbmodel import db
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

# Create an instance of SQLAlchemy

class From_different_sources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    brand_name = db.Column(db.String(50))
    review_rating = db.Column(db.Float)
    review_count = db.Column(db.Integer)
    product_name = db.Column(db.String(255))
    product_link = db.Column(db.String(255))
    image_link = db.Column(db.String(255))
    fromWhere = db.Column(db.String(50))
    saved_time = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).replace(second=0, microsecond=0))
    cpu = db.Column(db.String(255), default=None)
    ram = db.Column(db.String(255), default=None)
    screen = db.Column(db.String(255), default=None)
    gpu = db.Column(db.String(255), default=None)
    os = db.Column(db.String(255), default=None)
    ssd = db.Column(db.String(255), default=None)
    hdd = db.Column(db.String(255), default=None)

    def __init__(self, product_name,price, product_link,review_rating,review_count, saved_time,image_link,fromWhere,brand_name, cpu=None, ram=None, screen=None, gpu=None, os=None, ssd=None, hdd=None):
        self.product_name = product_name
        self.price=price
        self.saved_time = saved_time
        self.review_rating = review_rating
        self.review_count = review_count
        self.brand_name=brand_name
        self.product_link = product_link
        self.image_link=image_link
        self.cpu = cpu
        self.ram = ram
        self.screen = screen
        self.gpu = gpu
        self.os = os
        self.ssd = ssd
        self.hdd = hdd
        self.fromWhere=fromWhere

# Define the From_different_sourcesReadOnly model for the read-only copy
class From_different_sourcesReadOnly(db.Model):
    __tablename__ = 'from_different_sources'
    __table_args__ = (
        {'extend_existing': True},
    )
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    brand_name = db.Column(db.String(50))
    product_name = db.Column(db.String(255))
    product_link = db.Column(db.String(255))
    image_link = db.Column(db.String(255))
    fromWhere = db.Column(db.String(50))
    saved_time = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).replace(second=0, microsecond=0))
    cpu = db.Column(db.String(255), default=None)
    ram = db.Column(db.String(255), default=None)
    screen = db.Column(db.String(255), default=None)
    gpu = db.Column(db.String(255), default=None)
    os = db.Column(db.String(255), default=None)
    ssd = db.Column(db.String(255), default=None)
    hdd = db.Column(db.String(255), default=None)

    def __init__(self, product_name, product_link,price,review_rating,review_count, saved_time,image_link,fromWhere,brand_name, cpu=None, ram=None, screen=None, gpu=None, os=None, ssd=None, hdd=None):
        self.product_name = product_name
        self.price=price
        self.brand_name=brand_name
        self.review_rating = review_rating
        self.review_count = review_count
        self.saved_time = saved_time
        self.product_link = product_link
        self.image_link=image_link
        self.cpu = cpu
        self.ram = ram
        self.screen = screen
        self.gpu = gpu
        self.os = os
        self.ssd = ssd
        self.hdd = hdd
        self.fromWhere=fromWhere