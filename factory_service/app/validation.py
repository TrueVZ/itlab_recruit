from marshmallow import fields, Schema


class CreateFactorySchema(Schema):
    name = fields.String()
    kpd = fields.Integer()


class CreateProductsSchema(Schema):
    shop_id = fields.Integer()
    products = fields.List(fields.String)
