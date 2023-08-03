

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model.dbmodel import db

class N11Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255))
    brand_name = db.Column(db.String(50))
    price = db.Column(db.String(50))  # Use a numeric data type for the price (assuming it contains decimal values)
    review_rating = db.Column(db.String(50))  # Use a numeric data type for the review rating
    review_count = db.Column(db.String(50))  # Use an integer data type for the review count
    product_link = db.Column(db.String(255))
    image_link = db.Column(db.String(255))
    fromWhere = db.Column(db.String(50), default="n11")
    saved_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, product_name, brand_name, price, review_rating, review_count, product_link, image_link):
        self.product_name = product_name
        self.brand_name = brand_name
        self.price = price
        self.review_rating = review_rating
        self.review_count = review_count
        self.product_link = product_link
        self.image_link = image_link

# Define the N11DataReadOnly model for the read-only copy
class N11DataReadOnly(db.Model):
    __tablename__ = 'n11_data'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255))
    brand_name = db.Column(db.String(50))
    price = db.Column(db.String(50))  # Use a numeric data type for the price (assuming it contains decimal values)
    review_rating = db.Column(db.String(50))  # Use a numeric data type for the review rating
    review_count = db.Column(db.String(50))  # Use an integer data type for the review count
    product_link = db.Column(db.String(255))
    image_link = db.Column(db.String(255))
    fromWhere = db.Column(db.String(50), default="n11")
    saved_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, product_name, brand_name, price, review_rating, review_count, product_link, image_link):
        self.product_name = product_name
        self.brand_name = brand_name
        self.price = price
        self.review_rating = review_rating
        self.review_count = review_count
        self.product_link = product_link
        self.image_link = image_link