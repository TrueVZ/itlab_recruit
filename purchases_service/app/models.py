from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    checks = db.relationship(
        "Check", backref="customer", lazy="dynamic", cascade="all,delete"
    )


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check_id = db.Column(db.Integer, db.ForeignKey("check.id"))
    name = db.Column(db.String(200))
    price = db.Column(db.Integer)
    count = db.Column(db.Integer)
    category = db.Column(db.String(200))


class Check(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    shop = db.Column(db.String(100))
    payment = db.Column(db.String(100))
    purchases = db.relationship(
        "Purchase", backref="check", lazy="dynamic", cascade="all, delete"
    )
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    total = db.Column(db.Integer)
