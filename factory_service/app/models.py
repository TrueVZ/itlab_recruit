from app.extensions import db
from sqlalchemy import event


class Factory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    kpd = db.Column(db.Integer, default=0)  # Create products in 5 seconds
    products = db.relationship("Product", backref="factory", lazy="dynamic")


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    factory_id = db.Column(db.Integer, db.ForeignKey("factory.id"))
    name = db.Column(db.String(50))
    count = db.Column(db.Integer, default=0)
    shop_id = db.Column(db.Integer)
    db.UniqueConstraint('factory_id', 'name', name='unique_product')
