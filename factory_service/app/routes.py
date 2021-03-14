from app.models import Product, Factory
from app.schemas import products_schema, factory_schema
from app import db
from flask import Blueprint, jsonify
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs
from sqlalchemy.exc import IntegrityError
import requests

bp = Blueprint("shop", __name__)


@bp.route("/factory/create/", methods=["POST"])
@use_args({"name": fields.String(), "kpd": fields.Integer()})
def add_factory(args):
    try:
        factory = Factory(name=args['name'], kpd=args['kpd'])
        db.session.add(factory)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(message="Factory already exist"), 400


@bp.route("/factory/<int:factory_id>/order", methods=["POST"])
@use_args({"products": fields.List(fields.String), "shop_id": fields.Integer()})
def add_product(args, factory_id):
    factory = Factory.query.get(factory_id)
    if factory is None:
        return jsonify(message="Factory not found")
    for p in args['products']:
        product = Product(name=p, factory_id=factory_id, shop_id=args['shop_id'])
        db.session.add(product)
        db.session.commit()
    return factory_schema.dumo(factory)


@bp.route("/factory/<int:factory_id>/product", methods=['GET'])
def get_product(factory_id):
    products = Product.query.fliter_by(factory_id=factory_id).all()
    return products_schema.dump(products)