from app import make_celery, db
from app.models import Factory, Product
from app.schemas import products_schema
import requests

celery = make_celery()


@celery.task(name="task.create_products")
def create_products():
    factory = Factory.query.all()
    for f in factory:
        products = Product.query.filter_by(factory_id=f.id)
        for p in products:
            if p.count > 500:
                continue
            p.count += f.kpd
    db.session.commit()


@celery.task(name="task.delivery")
def delivery():
    shop_ids = Product.query.distinct(Product.shop_id).all()
    for p in shop_ids:
        products = Product.query.filter_by(shop_id=p.shop_id)
        products_json = products_schema.dump(products)
        req = requests.put(
            f"http://shop-service:5001/shop/{p.shop_id}/delivery", json=products_json
        )
        if req.status_code != 200:
            continue
        for prod in products:
            prod.count = 0
    db.session.commit()
