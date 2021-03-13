from app.extensions import db
from sqlalchemy import event


class Factory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    kpd = db.Column(db.Integer, default=0)  # Create products in 5 seconds
    products = db.relationship("Product", backref="factory", lazy="dynamic")


@event.listens_for(Factory.__table__, "after_create")
def create_factory(*args, **kwargs):
    db.session.add(Factory(name="FactorySmartphone", kpd=20))
    db.session.add(Factory(name="FactoryClothes", kpd=40))
    db.session.commit()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    factory_id = db.Column(db.Integer, db.ForeignKey("factory.id"))
    name = db.Column(db.String(50))
    count = db.Column(db.Integer, default=0)
    shop_id = db.Column(db.Integer)


@event.listens_for(Product.__table__, "after_create")
def create_product(*args, **kwargs):
    db.session.add(Product(name="macbook", factory_id=1, shop_id=1))
    db.session.add(Product(name="iphone", factory_id=1, shop_id=1))
    db.session.add(
        Product(
            name="hoodie",
            factory_id=2,
            shop_id=2,
        )
    )
    db.session.add(Product(name="t-shirt", factory_id=2, shop_id=2))
    db.session.commit()
