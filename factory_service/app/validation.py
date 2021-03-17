from marshmallow import fields, Schema, validate


class CreateFactorySchema(Schema):
    name = fields.String()
    kpd = fields.Integer(validate=validate.Range(min=1))


class CreateProductsSchema(Schema):
    shop_id = fields.Integer()
    products = fields.List(fields.String)
