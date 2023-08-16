from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model.dbmodel import db
from datetime import datetime, timezone


class HepsiburadaData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255))
    brand_name = db.Column(db.String(50))
    price = db.Column(db.Integer)
    review_rating = db.Column(db.Float,default=0.0)
    review_count = db.Column(db.Integer,default=0)
    product_link = db.Column(db.String(255))
    image_link = db.Column(db.String(255))
    fromWhere = db.Column(db.String(50), default="hepsiburada")  
    saved_time = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).replace(second=0, microsecond=0))

    def __init__(self, product_name, brand_name, price, review_rating, review_count, product_link, image_link):
        self.product_name = product_name
        self.brand_name = brand_name
        self.price = price
        self.review_rating = review_rating
        self.review_count = review_count
        self.product_link = product_link
        self.image_link = image_link

class HepsiburadaDataReadOnly(db.Model):
    __tablename__ = 'hepsiburada_data'  # Same table name as the original HepsiburadaData table
    __table_args__ = {'extend_existing': True}  # to extend the existing table
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255))
    brand_name = db.Column(db.String(50))
    price = db.Column(db.Integer)
    review_rating = db.Column(db.Float)
    review_count = db.Column(db.Integer)
    product_link = db.Column(db.String(255))
    image_link = db.Column(db.String(255))
    fromWhere = db.Column(db.String(50), default="hepsiburada")  # Add the new column with the default value "hepsiburada"
    saved_time = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).replace(second=0, microsecond=0))

    def __init__(self, product_name, brand_name, price, review_rating, review_count, product_link, image_link):
        self.product_name = product_name
        self.brand_name = brand_name
        self.price = price
        self.review_rating = review_rating
        self.review_count = review_count
        self.product_link = product_link
        self.image_link = image_link
