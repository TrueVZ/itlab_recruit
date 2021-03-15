from app.models import Product, Factory
from app.schemas import products_schema, factory_schema
from app.validation import *
from app import db
from flask import Blueprint, jsonify
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs
from sqlalchemy.exc import IntegrityError
import requests

bp = Blueprint("shop", __name__)


@bp.route("/factory/create/", methods=["POST"])
@use_args(CreateFactorySchema)
def add_factory(args):
    """
    Create factory
    ---
    post:
      description: Create factory
      parameters:
      - name: factory
        in: body
        required: true
        schema: CreateFactorySchema
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: FactorySchema
        '400':
          description: Bad request
        '404':
          description: Factory already exist
        '5xx':
          description: Unexpected error
    """
    try:
        factory = Factory(name=args['name'], kpd=args['kpd'])
        db.session.add(factory)
        db.session.commit()
        return factory_schema.dump(factory)
    except IntegrityError:
        db.session.rollback()
        return jsonify(message="Factory already exist"), 400


@bp.route("/factory/<int:factory_id>/order", methods=["POST"])
@use_args(CreateProductsSchema)
def add_product(args, factory_id):
    """
    Add product to factory
    ---
    post:
      description: Add products to factory
      parameters:
      - name: order
        in: body
        required: true
        schema: CreateProductsSchema
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: FactorySchema
        '400':
          description: Bad request
        '404':
          description: Factory not found
        '5xx':
          description: Unexpected error
    """
    factory = Factory.query.get(factory_id)
    if factory is None:
        return jsonify(message="Factory not found")
    for p in args['products']:
        product = Product(name=p, factory_id=factory_id, shop_id=args['shop_id'])
        db.session.add(product)
        db.session.commit()
    return factory_schema.dump(factory)


@bp.route("/factory/<int:factory_id>/product", methods=['GET'])
def get_product(factory_id):
    """
    Get products list
    ---
    post:
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Product'
        '400':
          description: Bad request
        '404':
          description: Factory not found
        '5xx':
          description: Unexpected error
    """
    factory = Factory.query.get(factory_id)
    if factory is None:
        return jsonify(message="Factory not found")
    products = Product.query.filter_by(factory_id=factory_id).all()
    return jsonify(products=products_schema.dump(products))


@bp.route("/factory/<int:factory_id>", methods=['GET'])
def get_factory(factory_id):
    """
    Get foctory by id
    ---
    post:
      description: Get factory by id
      parameters:
      - name: factoryID
        in: path
        required: true
        schema:
          type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: FactorySchema
        '400':
          description: Bad request
        '404':
          description: Factory already exist
        '5xx':
          description: Unexpected error
    """
    factory = Factory.query.get(factory_id)
    if factory is None:
        return jsonify(message="Factory not found")
    return factory_schema.dump(factory)
