from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model.dbmodel import db



class VatanData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255))
    brand_name = db.Column(db.String(50))
    price = db.Column(db.Float)
    review_rating = db.Column(db.Integer)
    review_count = db.Column(db.Integer)
    product_link = db.Column(db.String(255))
    image_link = db.Column(db.String(255))
    fromWhere = db.Column(db.String(50), default="vatan")  # Add the new column with the default value "vatan"
    saved_time = db.Column(db.DateTime, default=datetime.utcnow)  # Add the new column for timestamp

    def __init__(self, product_name, brand_name, price, review_rating, review_count, product_link, image_link):
        self.product_name = product_name
        self.brand_name = brand_name
        self.price = price
        self.review_rating = review_rating
        self.review_count = review_count
        self.product_link = product_link
        self.image_link = image_link

# Define the ProductDataReadOnly model for the read-only copy
class VatanDataReadOnly(db.Model):
    __tablename__ = 'vatan_data'  # Same table name as the original ProductData table
    __table_args__ = {'extend_existing': True}  # Use this option to extend the existing table
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255))
    brand_name = db.Column(db.String(50))
    price = db.Column(db.Float)
    review_rating = db.Column(db.Integer)
    review_count = db.Column(db.Integer)
    product_link = db.Column(db.String(255))
    image_link = db.Column(db.String(255))
    fromWhere = db.Column(db.String(50), default="vatan")  # Add the new column with the default value "vatan"
    saved_time = db.Column(db.DateTime, default=datetime.utcnow)  # Add the new column for timestamp

    def __init__(self, product_name, brand_name, price, review_rating, review_count, product_link, image_link):
        self.product_name = product_name
        self.brand_name = brand_name
        self.price = price
        self.review_rating = review_rating
        self.review_count = review_count
        self.product_link = product_link
        self.image_link = image_link