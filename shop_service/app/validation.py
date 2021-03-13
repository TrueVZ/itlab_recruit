from marshmallow import Schema, fields


class CreateProductSchema(Schema):
    name = fields.String()
    price = fields.Integer()
    count = fields.Integer()
    description = fields.String(default=None)
    category = fields.String()


class CreatePurchaseSchema(Schema):
    name = fields.String()
    count = fields.Integer()


class CreateShopSchema(Schema):
    name = fields.String()
    address = fields.String()
    phone = fields.String()


class DeliveryProductSchema(Schema):
    name = fields.String()
    count = fields.Integer()


class BuyInputSchema(Schema):
    shop = fields.String()
    user = fields.Integer()
    payment = fields.String()
    purchases = fields.Nested(CreatePurchaseSchema(many=True))
