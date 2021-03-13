from app.models import Purchase, Shop, Product
from app.schemas import purchases_schema, shop_schema, product_schema, purchase_out_schema
from app.validation import *
from app import db
from flask import Blueprint, jsonify
from webargs import fields
from webargs.flaskparser import use_args
from sqlalchemy.exc import IntegrityError
import requests


bp = Blueprint("shop", __name__)


@bp.route("/shop/create/", methods=["POST"])
@use_args(CreateShopSchema, location="json")
def add_shop(args):
    try:
        shop = shop_schema.load(args)
        db.session.add(shop)
        db.session.commit()
        return shop_schema.dump(shop), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify(message="Shop already create"), 404


@bp.route("/shop/<int:shop_id>/", methods=["GET"])
def get_shop(shop_id):
    shop = Shop.query.get(shop_id)
    if shop is not None:
        return shop_schema.load(shop)
    return jsonify(message="Shop not found"), 404


@bp.route("/shop/<int:shop_id>/product/", methods=["POST"])
@use_args({"products": fields.Nested(CreateProductSchema, many=True)}, location="json")
def add_product(args, shop_id):
    shop = Shop.query.get(shop_id)
    for p in args["products"]:
        product = product_schema.load(p)
        product.shop = shop
        db.session.add(product)
        db.session.commit()

    return shop_schema.dump(shop)


@bp.route("/shop/<int:shop_id>/history/", methods=["GET"])
def get_history(shop_id):
    purchases = Purchase.query.filter_by(shop_id=shop_id).all()
    return jsonify(purchases=purchases_schema.dump(purchases))


@bp.route("/buy/", methods=["PUT"])
@use_args(BuyInputSchema, location="json")
def buy(args):
    shop = Shop.query.filter_by(name=args["shop"]).first()
    if shop is None:
        return jsonify(message="Shop not found"), 404
    purchases = []
    for p in args["purchases"]:
        product = Product.query.filter_by(name=p["name"], shop=shop).first()
        if product.count < p["count"]:
            db.session.rollback()
            return jsonify(message=f"Not enough product {product.name}"), 404
        product.count -= p["count"]
        purchase = Purchase(
            shop_id=shop.id,
            product_id=product.id,
            name=product.name,
            user_id=args["user"],
            count=p["count"],
            price=product.price * p["count"],
        )
        db.session.add(purchase)
        purchase_json = purchase_out_schema.dump(purchase)
        purchase_json["category"] = product.category
        purchases.append(purchase_json)

    data = {
        "purchases": purchases,
        "total": sum([p["price"] for p in purchases]),
        "shop": shop.name,
        "payment": args["payment"],
    }
    return jsonify(data), 200
