
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from datetime import datetime, timezone
from model.dbmodel import db



class From_different_sources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255))
    product_link = db.Column(db.String(255))
    saved_time = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).replace(second=0, microsecond=0))
 #   product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

   
    def __init__(self, product_name, product_link, saved_time):
        self.product_name = product_name
        self.saved_time=saved_time
        self.product_link = product_link

# Define the N11DataReadOnly model for the read-only copy
class From_different_sourcesReadOnly(db.Model):
    __tablename__ = 'from_different_sources'
    __table_args__ = (
        {'extend_existing': True},
    )
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255))
    product_link = db.Column(db.String(255))
    saved_time = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).replace(second=0, microsecond=0))
  #  product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __init__(self, product_name, product_link, saved_time):
        self.product_name = product_name
        self.saved_time = saved_time
        self.product_link = product_link
