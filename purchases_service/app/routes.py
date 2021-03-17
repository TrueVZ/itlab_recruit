from app.models import User, Check, Purchase
from app.schemas import (
    user_schema,
    users_schema,
    purchase_schema,
    check_schema,
    checks_schema,
)
from app.validation import CreateCheckSchema
from app import db
from flask import Blueprint, jsonify
from webargs import fields
from webargs.flaskparser import use_args
from sqlalchemy.exc import IntegrityError
import requests

bp = Blueprint("purchases", __name__)


@bp.route("/user/create", methods=["POST"])
@use_args({"username": fields.String(required=True)}, location="json")
def add_user(args):
    """
    Create user
    ---
    post:
      description: Create user
      requestBody:
          content:
              application/json:
                  schema:
                    type: object
                    properties:
                        username:
                          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserSchema
        '400':
          description: Bad request
        '404':
          description: User not found
        default:
          description: Unexpected error
    """
    try:
        user = User(username=args["username"])
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user)
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Username blocked"}), 400


@bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    """
    Get user by ID
    ---
    get:
      description: Get user by ID
      parameters:
      - name: user_id
        required: true
        in: path
        schema:
          type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserSchema
        '400':
          description: Bad request
        '404':
          description: User not found
        default:
          description: Unexpected error

    """
    user = User.query.get(user_id)
    if user is not None:
        return user_schema.dump(user)
    else:
        return jsonify({"message": "User not found"}), 404


@bp.route("/user/all", methods=["GET"])
def get_all_user():
    """
    Get all users
    ---
    get:
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'

    """
    users = User.query.all()
    return jsonify(users=users_schema.dump(users)), 200


@bp.route("/user/<int:user_id>/check/buy", methods=["POST"])
@use_args(CreateCheckSchema)
def add_check(args, user_id):
    """
    Buy product from shop and create check
    ---
    post:
      description: Create check
      parameters:
      - name: userID
        required: true
        in: path
        schema:
          type: integer
      requestBody:
          content:
              application/json:
                  schema: CreateCheckSchema
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserSchema
        '400':
          description: Bad request
        '404':
          description: User not found
        default:
          description: Unexpected error

    """
    user = User.query.get(user_id)
    if user is None:
        db.session.rollback()
        return jsonify(message="User not found"), 404
    args["user"] = user_id
    print(args)
    req = requests.put(f"http://shop-service:5001/api/shop/buy", json=args)
    if req.status_code != 200:
        return req.json(), req.status_code
    req_data = req.json()
    check = check_schema.load(req_data)
    check.customer = user
    db.session.add(check)
    db.session.commit()
    return check_schema.dump(check)


@bp.route("/user/<int:user_id>/purchases/<int:purchase_id>", methods=["PUT"])
@use_args({"category": fields.Str(required=True)})
def change_category(args, user_id, purchase_id):
    """
    Change category purchase
    ---
    put:
      description: Change category purchase
      parameters:
      - name: user_id
        required: true
        in: path
        schema:
          type: integer
      - name: purchase_id
        required: true
        in: path
        schema:
          type: integer
      requestBody:
          content:
              application/json:
                  schema:
                    type: object
                    properties:
                        category:
                          type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: Purchase
        '400':
          description: Bad request
        '404':
          description: User or Purchase not found
        default:
          description: Unexpected error
    """
    purchase = Purchase.query.get(purchase_id)
    user = User.query.get(user_id)
    if purchase is None or User is not None:
        return jsonify(message="Purchase or User not found"), 404
    purchase.category = args["category"]
    db.session.commit()
    return purchase_schema.dump(purchase)
