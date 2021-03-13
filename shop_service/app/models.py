from app import db
import datetime


class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    products = db.relationship(
        "Product", backref="shop", lazy="dynamic", cascade="all, delete-orphan"
    )
    purchases = db.relationship("Purchase", backref="shop", lazy="dynamic")


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey("shop.id"))
    name = db.Column(db.String(200))
    description = db.Column(db.String(200))
    price = db.Column(db.Integer)
    category = db.Column(db.String(200))
    count = db.Column(db.Integer, default=0)


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey("shop.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    name = db.Column(db.String(200))
    user_id = db.Column(db.Integer)
    count = db.Column(db.Integer)
    price = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
