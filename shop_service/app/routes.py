from app.models import Purchase, Shop, Product
from app.schemas import (
    purchases_schema,
    shop_schema,
    product_schema,
    products_schema,
    purchase_out_schema,
)
from app.validation import (
    CreatePurchaseSchema,
    CreateShopSchema,
    CreateProductSchema,
    DeliveryProductSchema,
    BuyInputSchema,
)
from app import db
from flask import Blueprint, jsonify
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs
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
    """
    Get shop by id
    ---
      parameters:
        - name: shopID
          in: path
          type: integer
          required: true
      responses:
        '200':
          description: OK
          schema:
            $ref: '#/definitions/Shop'
        '400':
          description: Bad request
        '404':
          description: Shop not found
        '5xx':
          description: Unexpected error

    """
    shop = Shop.query.get(shop_id)
    if shop is not None:
        return shop_schema.dump(shop)
    return jsonify(message="Shop not found"), 404


@bp.route("/shop/<int:shop_id>/product/", methods=["POST"])
@use_args({"products": fields.Nested(CreateProductSchema, many=True)}, location="json")
def add_product(args, shop_id):
    shop = Shop.query.get(shop_id)
    try:
        for p in args["products"]:
            product = product_schema.load(p)
            product.shop = shop
            db.session.add(product)
    except IntegrityError:
        db.session.rollback()
        return jsonify(message="Name product already exists")
    db.session.commit()
    return shop_schema.dump(shop)


@bp.route("/shop/<int:shop_id>/history/", methods=["GET"])
def get_history(shop_id):
    """
    History of purchases
    ---
      parameters:
        - name: shopID
          in: path
          type: integer
          required: true
      responses:
        '200':
          description: OK
          schema:
            type: array
            items:
              $ref: '#/definitions/Purchase'
        '400':
          description: Bad request
        '404':
          description: Shop not found
        '5xx':
          description: Unexpected error

    """
    purchases = Purchase.query.filter_by(shop_id=shop_id).all()
    return jsonify(purchases=purchases_schema.dump(purchases))


@bp.route("/shop/<int:shop_id>/product/", methods=["GET"])
@use_kwargs({"category": fields.Str(required=False)}, location="query")
def get_product_category(shop_id, category=None):
    """
    Get products from shop
    ---
      parameters:
        - name: shopID
          in: path
          type: integer
          required: true
        - name: category
          in: body
          type: object
          properties:
            categoryName:
              type: string
          required: true
      responses:
        '200':
          description: OK
          schema:
            type: array
            items:
              $ref: '#/definitions/Product'
        '400':
          description: Bad request
        '404':
          description: Shop not found
        '5xx':
          description: Unexpected error

    """
    if category is not None:
        products = Product.query.filter_by(shop_id=shop_id, category=category).all()
    else:
        products = Product.query.filter_by(shop_id=shop_id).all()

    return jsonify(products=products_schema.dump(products))


@bp.route("/shop/<int:shop_id>/delivery/", methods=["PUT"])
@use_args({"products": fields.Nested(DeliveryProductSchema(many=True))})
def delivery(args, shop_id):
    for p in args["products"]:
        product = Product.query.filter_by(name=p["name"], shop_id=shop_id).first()
        if product is None:
            db.session.rollback()
            return "Product not found", 404
        product.count += p["count"]
    db.session.commit()
    return "Ok", 200


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
    req = requests.post(
        f"http://purchase-service:5000/user/{args['user']}/check/buy", json=data
    )
    if req.status_code != 200:
        db.session.rollback()
        return "Error from CheckService", 400
    db.session.commit()
    return jsonify(data), 200
